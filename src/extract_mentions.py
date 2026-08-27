"""
Transforme chaque réponse brute (texte libre) en données structurées.

Pourquoi un second appel LLM plutôt que du regex :
une réponse type "Je te recommande Semrush, qui est excellent pour les PME,
ou sinon Ahrefs si le budget le permet" n'est pas fiablement parsable par
règles. On délègue l'extraction à un modèle, en mode JSON strict, avec
la liste fermée des marques connues pour éviter les hallucinations
(le modèle ne doit PAS inventer une marque absente du panier).
Température à 0 : ici on veut un extracteur déterministe, pas créatif.
"""

import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

RAW_DIR = Path("data/raw_responses")
OUTPUT_DIR = Path("data/extracted")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

EXTRACTOR_MODEL = "gpt-4o-mini"  # vérifie le nom du modèle courant avant de lancer

KNOWN_BRANDS = [
    "Semrush", "Ahrefs", "Moz", "Screaming Frog", "Surfer SEO",
    "SE Ranking", "Nightwatch", "Search Atlas", "Conductor",
    "BrightLocal", "AnswerThePublic",
]

client = OpenAI()

EXTRACTION_SYSTEM_PROMPT = f"""Tu es un extracteur de données strict, pas un assistant conversationnel.

Voici la liste FERMÉE des marques à repérer : {", ".join(KNOWN_BRANDS)}.

Analyse le texte fourni et renvoie UNIQUEMENT un JSON avec cette structure :
{{
  "brands_cited": [
    {{"name": "<nom exact de la liste>", "rank_position": <entier, ordre d'apparition dans le texte, 1 = premier cité>, "sentiment": "<positive|neutral|negative>"}}
  ],
  "sources_cited": ["<domaine ou nom de source mentionné explicitement, ex: g2.com>"]
}}

Règles strictes :
- N'inclus QUE des marques présentes dans la liste fermée ci-dessus. Ignore toute autre marque mentionnée.
- Si une marque de la liste n'est pas citée dans le texte, ne l'inclus pas.
- rank_position = position d'apparition dans le texte (1er mentionné = 1, 2e = 2, etc.), jamais un jugement de qualité.
- sentiment = ton du texte envers CETTE marque précisément, pas le ton général de la réponse.
- sources_cited = liste vide si aucune source explicite n'est citée. N'invente rien.
- Réponds uniquement avec le JSON, sans texte autour, sans balises markdown.
"""


def extract_one(raw_response: str) -> dict:
    response = client.chat.completions.create(
        model=EXTRACTOR_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": raw_response},
        ],
    )
    return json.loads(response.choices[0].message.content)


def main():
    raw_files = sorted(RAW_DIR.glob("*.json"))
    print(f"{len(raw_files)} réponses brutes à traiter.")

    done, skipped, failed = 0, 0, 0

    for raw_path in raw_files:
        out_path = OUTPUT_DIR / raw_path.name

        if out_path.exists():
            skipped += 1
            continue

        record = json.loads(raw_path.read_text(encoding="utf-8"))

        try:
            extraction = extract_one(record["raw_response"])
        except Exception as e:
            print(f"  [!] Échec extraction sur {raw_path.name} : {e}")
            failed += 1
            continue

        record["brands_cited"] = extraction.get("brands_cited", [])
        record["sources_cited"] = extraction.get("sources_cited", [])
        out_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        done += 1

        if done % 50 == 0:
            print(f"  ... {done} traitées")

    print(f"\nTerminé. Extraits : {done} | Déjà présents (sautés) : {skipped} | Échecs : {failed}")


if __name__ == "__main__":
    main()