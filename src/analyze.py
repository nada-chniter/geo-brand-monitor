"""
Agrège les extractions en fréquences de citation par marque, avec
intervalle de confiance de Wilson (pas d'approximation normale : on
travaille sur des échantillons trop petits pour ça, 7 répétitions
par question).

Unité de calcul : pour une marque donnée, dans une langue et un
fournisseur donnés, on compte sur COMBIEN de trials (question x
répétition) elle a été citée, sur le nombre total de trials
disponibles dans ce sous-ensemble. C'est ça, la "part de voix
générative".
"""

import json
from pathlib import Path

import pandas as pd
from statsmodels.stats.proportion import proportion_confint

EXTRACTED_DIR = Path("data/extracted")
REPORT_DIR = Path("report")
REPORT_DIR.mkdir(exist_ok=True)

# --- Normalisation des marques -------------------------------------------
# L'extracteur (LLM) ne respecte pas toujours parfaitement la consigne de
# recopier le nom EXACT de la liste fermée : on a observé "SEMrush" au lieu
# de "Semrush", "Moz Pro" au lieu de "Moz", "SERanking" au lieu de
# "SE Ranking", et même une marque totalement hors liste ("BrightEdge").
# On ne refait PAS les appels d'extraction (coûteux, déjà payés) : on
# normalise ici, côté code, en dernière ligne de défense.
BRAND_CANONICAL = {
    "semrush": "Semrush",
    "sem rush": "Semrush",
    "semrush local": "Semrush",
    "moz": "Moz",
    "moz pro": "Moz",
    "se ranking": "SE Ranking",
    "seranking": "SE Ranking",
    "brightlocal": "BrightLocal",
    "bright local": "BrightLocal",
    "ahrefs": "Ahrefs",
    "screaming frog": "Screaming Frog",
    "surfer seo": "Surfer SEO",
    "surfer": "Surfer SEO",
    "nightwatch": "Nightwatch",
    "search atlas": "Search Atlas",
    "conductor": "Conductor",
    "answerthepublic": "AnswerThePublic",
    "answer the public": "AnswerThePublic",
}


def normalize_brand(raw_name: str) -> str | None:
    """
    Renvoie le nom canonique (l'un des 11 de la liste fermée), ou None si
    la marque ne correspond à aucune variante connue -- dans ce cas elle
    est hors périmètre (ex: BrightEdge) et doit être écartée du comptage.
    """
    return BRAND_CANONICAL.get(raw_name.strip().lower())


def load_all_extracted() -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in EXTRACTED_DIR.glob("*.json")]


def build_long_dataframe(records: list[dict]) -> pd.DataFrame:
    """Une ligne par (trial, marque citée dans ce trial)."""
    rows = []
    dropped = []
    for r in records:
        for brand in r.get("brands_cited", []):
            canonical = normalize_brand(brand["name"])
            if canonical is None:
                dropped.append(brand["name"])
                continue
            rows.append({
                "call_id": r["call_id"],
                "question_id": r["question_id"],
                "language": r["language"],
                "category": r["category"],
                "provider": r["provider"],
                "brand": canonical,
                "rank_position": brand["rank_position"],
                "sentiment": brand["sentiment"],
            })

    if dropped:
        from collections import Counter
        print(f"\n[Normalisation] {len(dropped)} mentions écartées (marque hors liste fermée) :")
        for name, count in Counter(dropped).most_common():
            print(f"  - '{name}' : {count} fois")

    return pd.DataFrame(rows)


def compute_frequencies(records: list[dict], mentions_df: pd.DataFrame,
                         group_cols: list[str]) -> pd.DataFrame:
    """
    Fréquence de citation par marque, groupée par group_cols
    (ex: ['language'] ou ['language', 'provider']).
    """
    trials_df = pd.DataFrame(records)

    # nombre total de trials disponibles par groupe (dénominateur)
    n_trials = trials_df.groupby(group_cols).size().rename("n_trials")

    # nombre de trials où chaque marque a été citée (numérateur)
    citations = (
        mentions_df
        .drop_duplicates(subset=group_cols + ["call_id", "brand"])
        .groupby(group_cols + ["brand"])
        .size()
        .rename("n_citations")
    )

    result = citations.reset_index().merge(n_trials.reset_index(), on=group_cols)

    result["frequency"] = result["n_citations"] / result["n_trials"]
    ci_low, ci_high = proportion_confint(
        result["n_citations"], result["n_trials"], method="wilson"
    )
    result["ci_low"] = ci_low
    result["ci_high"] = ci_high

    return result.sort_values(group_cols + ["frequency"], ascending=[True] * len(group_cols) + [False])


def build_target_brand_map(records: list[dict]) -> dict[str, set[str]]:
    """
    question_id -> ensemble des marques nommées DANS la question elle-même
    (target_brand, séparées par ';' pour les comparaisons à deux marques).
    Vide pour les catégories qui ne nomment aucune marque (recommandation,
    cas d'usage, question ouverte) : le filtre n'a alors aucun effet.
    """
    mapping = {}
    for r in records:
        tb = r.get("target_brand", "") or ""
        mapping[r["question_id"]] = {b.strip() for b in tb.split(";") if b.strip()}
    return mapping


def exclude_self_citations(mentions_df: pd.DataFrame, target_map: dict[str, set[str]]) -> pd.DataFrame:
    """
    Retire les lignes où la marque citée est celle-là même nommée dans la
    question (ex: "alternative à Semrush" -> Semrush cité mécaniquement).
    Ce n'est PAS un signal de préférence du modèle, juste un écho de la
    question -- on ne veut pas le compter comme une "citation" au même
    titre qu'une marque suggérée spontanément.
    """
    def is_self_citation(row):
        return row["brand"] in target_map.get(row["question_id"], set())

    mask = mentions_df.apply(is_self_citation, axis=1)
    return mentions_df[~mask]


def main():
    records = load_all_extracted()
    print(f"{len(records)} trials chargés.")

    mentions_df = build_long_dataframe(records)

    # 1. Part de voix par marque et par langue (le résultat central)
    by_language = compute_frequencies(records, mentions_df, ["language"])
    by_language.to_csv(REPORT_DIR / "frequency_by_language.csv", index=False)

    # 2. Par marque, langue ET fournisseur (pour voir si OpenAI et Anthropic divergent)
    by_language_provider = compute_frequencies(records, mentions_df, ["language", "provider"])
    by_language_provider.to_csv(REPORT_DIR / "frequency_by_language_provider.csv", index=False)

    # 3. Par marque, langue ET catégorie de question (quel type de requête favorise qui)
    by_language_category = compute_frequencies(records, mentions_df, ["language", "category"])
    by_language_category.to_csv(REPORT_DIR / "frequency_by_language_category.csv", index=False)

    # --- Versions "signal propre" : on retire les auto-citations -------
    # (marque nommée dans la question elle-même, catégories
    # alternative/comparaison uniquement -- sans effet sur les autres
    # catégories, où target_brand est vide)
    target_map = build_target_brand_map(records)
    mentions_clean = exclude_self_citations(mentions_df, target_map)

    by_language_clean = compute_frequencies(records, mentions_clean, ["language"])
    by_language_clean.to_csv(REPORT_DIR / "frequency_by_language_excl_self.csv", index=False)

    by_language_provider_clean = compute_frequencies(records, mentions_clean, ["language", "provider"])
    by_language_provider_clean.to_csv(REPORT_DIR / "frequency_by_language_provider_excl_self.csv", index=False)

    by_language_category_clean = compute_frequencies(records, mentions_clean, ["language", "category"])
    by_language_category_clean.to_csv(REPORT_DIR / "frequency_by_language_category_excl_self.csv", index=False)

    print("Rapports écrits dans report/ :")
    print(" - frequency_by_language.csv                       (brut)")
    print(" - frequency_by_language_provider.csv               (brut)")
    print(" - frequency_by_language_category.csv               (brut)")
    print(" - frequency_by_language_excl_self.csv              (sans auto-citation)")
    print(" - frequency_by_language_provider_excl_self.csv     (sans auto-citation)")
    print(" - frequency_by_language_category_excl_self.csv     (sans auto-citation, LA VUE À UTILISER")
    print("   pour comparer alternative/comparaison aux autres catégories)")

    print("\nAperçu — top marques par langue :")
    for lang in by_language["language"].unique():
        print(f"\n[{lang.upper()}]")
        top5 = by_language[by_language["language"] == lang].head(5)
        for _, row in top5.iterrows():
            print(f"  {row['brand']:<20} freq={row['frequency']:.0%}  "
                  f"IC=[{row['ci_low']:.0%}, {row['ci_high']:.0%}]  "
                  f"({row['n_citations']}/{row['n_trials']})")


if __name__ == "__main__":
    main()