"""
Génère deux graphiques PNG statiques à partir des CSV produits par analyze.py,
pour intégration directe dans le README (impact visuel immédiat sur GitHub,
sans la complexité d'un dashboard interactif).
"""

import matplotlib
matplotlib.use("Agg")  # pas d'affichage interactif, juste des fichiers PNG
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

REPORT_DIR = Path("report")

# Ordre fixe des marques pour que les deux graphiques restent cohérents
BRAND_ORDER = [
    "Semrush", "Ahrefs", "Moz", "Screaming Frog", "SE Ranking",
    "Surfer SEO", "AnswerThePublic", "BrightLocal", "Conductor",
]


def chart_brand_ranking():
    df = pd.read_csv(REPORT_DIR / "frequency_by_language_excl_self.csv")

    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(BRAND_ORDER))
    width = 0.35

    for i, lang in enumerate(["en", "fr"]):
        sub = df[df["language"] == lang].set_index("brand")
        freqs = [sub.loc[b, "frequency"] * 100 if b in sub.index else 0 for b in BRAND_ORDER]
        errs_low = [
            (sub.loc[b, "frequency"] - sub.loc[b, "ci_low"]) * 100 if b in sub.index else 0
            for b in BRAND_ORDER
        ]
        errs_high = [
            (sub.loc[b, "ci_high"] - sub.loc[b, "frequency"]) * 100 if b in sub.index else 0
            for b in BRAND_ORDER
        ]
        offset = -width / 2 if lang == "en" else width / 2
        label = "English" if lang == "en" else "French"
        ax.bar(
            [xi + offset for xi in x], freqs, width,
            yerr=[errs_low, errs_high], capsize=3,
            label=label,
        )

    ax.set_xticks(list(x))
    ax.set_xticklabels(BRAND_ORDER, rotation=35, ha="right")
    ax.set_ylabel("Citation frequency (%, Wilson 95% CI)")
    ax.set_title("Generative share of voice by brand — SEO tools panel (n=490 per language)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORT_DIR / "chart_brand_ranking.png", dpi=150)
    plt.close(fig)
    print("Écrit : report/chart_brand_ranking.png")


def chart_se_ranking_divergence():
    df = pd.read_csv(REPORT_DIR / "frequency_by_language_provider_excl_self.csv")
    sub = df[df["brand"] == "SE Ranking"]

    fig, ax = plt.subplots(figsize=(6, 5))
    languages = ["en", "fr"]
    providers = ["anthropic", "openai"]
    x = range(len(languages))
    width = 0.35

    for i, provider in enumerate(providers):
        freqs, errs_low, errs_high = [], [], []
        for lang in languages:
            row = sub[(sub["language"] == lang) & (sub["provider"] == provider)]
            if len(row):
                r = row.iloc[0]
                freqs.append(r["frequency"] * 100)
                errs_low.append((r["frequency"] - r["ci_low"]) * 100)
                errs_high.append((r["ci_high"] - r["frequency"]) * 100)
            else:
                freqs.append(0)
                errs_low.append(0)
                errs_high.append(0)
        offset = -width / 2 if provider == "anthropic" else width / 2
        label = "Anthropic (Claude)" if provider == "anthropic" else "OpenAI (GPT)"
        ax.bar(
            [xi + offset for xi in x], freqs, width,
            yerr=[errs_low, errs_high], capsize=4,
            label=label,
        )

    ax.set_xticks(list(x))
    ax.set_xticklabels(["English", "French"])
    ax.set_ylabel("Citation frequency (%, Wilson 95% CI)")
    ax.set_title("SE Ranking: citation frequency by provider")
    ax.set_ylim(0, 65)
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORT_DIR / "chart_se_ranking_divergence.png", dpi=150)
    plt.close(fig)
    print("Écrit : report/chart_se_ranking_divergence.png")


def main():
    chart_brand_ranking()
    chart_se_ranking_divergence()


if __name__ == "__main__":
    main()
