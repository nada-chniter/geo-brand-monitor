"""
Interroge OpenAI et Anthropic sur le panier de questions GEO/AEO.

Design volontaire :
- IDEMPOTENT : si data/raw_responses/{id}.json existe déjà, on saute l'appel.
  Indispensable sur ~980 appels : si le script plante à l'appel 600,
  tu le relances et il ne refait QUE ce qui manque.
- Chaque appel est sauvegardé individuellement, immédiatement.
  Jamais tout en mémoire jusqu'à la fin : un crash ne fait perdre
  qu'un appel, pas le run entier.
- Chaque appel est tenté isolément (try/except par appel).
  Un timeout sur une question ne doit jamais interrompre les autres.
"""

import csv
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic

load_dotenv()

# --- Config -------------------------------------------------------------
N_REPETITIONS = 7
QUESTIONS_FILE = Path("data/questions_panel.csv")
OUTPUT_DIR = Path("data/raw_responses")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# NOTE: vérifie ces noms de modèles sur la doc officielle avant de lancer —
# les fournisseurs renomment/déprécient leurs modèles régulièrement.
# On utilise volontairement des modèles "mini" : moins chers, ET plus
# représentatifs de ce que la majorité des utilisateurs consultent en
# usage gratuit/standard.
OPENAI_MODEL = "gpt-4o-mini"
ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"

openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
anthropic_client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 5


def call_openai(question_text: str) -> str:
    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": question_text}],
        temperature=0.7,  # variabilité naturelle : on VEUT la non-déterminisme ici
        max_tokens=500,
    )
    return response.choices[0].message.content


def call_anthropic(question_text: str) -> str:
    response = anthropic_client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=500,
        temperature=0.7,
        messages=[{"role": "user", "content": question_text}],
    )
    return response.content[0].text


PROVIDER_FUNCTIONS = {
    "openai": call_openai,
    "anthropic": call_anthropic,
}


def call_with_retry(provider: str, question_text: str) -> str | None:
    fn = PROVIDER_FUNCTIONS[provider]
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return fn(question_text)
        except Exception as e:
            print(f"  [!] {provider} tentative {attempt}/{MAX_RETRIES} échouée : {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)
    print(f"  [X] {provider} abandonné après {MAX_RETRIES} tentatives.")
    return None


def load_questions() -> list[dict]:
    with open(QUESTIONS_FILE, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    questions = load_questions()
    total_calls = len(questions) * len(PROVIDER_FUNCTIONS) * N_REPETITIONS
    print(f"Panier : {len(questions)} questions x {len(PROVIDER_FUNCTIONS)} "
          f"fournisseurs x {N_REPETITIONS} répétitions = {total_calls} appels prévus.")

    done, skipped, failed = 0, 0, 0

    for q in questions:
        for provider in PROVIDER_FUNCTIONS:
            for rep in range(1, N_REPETITIONS + 1):
                call_id = f"{q['question_id']}_{provider}_rep{rep}"
                out_path = OUTPUT_DIR / f"{call_id}.json"

                if out_path.exists():
                    skipped += 1
                    continue

                print(f"-> {call_id}")
                raw_text = call_with_retry(provider, q["question_text"])

                if raw_text is None:
                    failed += 1
                    continue

                record = {
                    "call_id": call_id,
                    "question_id": q["question_id"],
                    "pair_id": q["pair_id"],
                    "language": q["language"],
                    "category": q["category"],
                    "question_text": q["question_text"],
                    "target_brand": q["target_brand"],
                    "provider": provider,
                    "model": OPENAI_MODEL if provider == "openai" else ANTHROPIC_MODEL,
                    "repetition": rep,
                    "raw_response": raw_text,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                }
                out_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
                done += 1

    print(f"\nTerminé. Nouveaux : {done} | Déjà présents (sautés) : {skipped} | Échecs : {failed}")
    if failed:
        print("Relance simplement le script : les échecs seront retentés, "
              "les succès déjà sauvegardés seront sautés.")


if __name__ == "__main__":
    main()