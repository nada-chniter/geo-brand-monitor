# Analysis Report — GEO Brand Monitor (SEO Tools, B2B)

🇫🇷 [Lire en français](analysis_report.fr.md) · See [README](../README.md) for the full methodology.

**Scope of this document:** detailed findings, category- and provider-level breakdowns, and recommendations framed as testable hypotheses — not proven conclusions. Sample: 980 raw calls (70 questions × 2 providers × 7 repetitions), aggregated with Wilson confidence intervals throughout. All frequencies below use the `_excl_self` dataset (self-citations from "alternative"/"comparison" questions removed) unless stated otherwise — see README for why.

---

## 1. Executive summary

- **Semrush, Ahrefs and Moz dominate** generative answers across both languages and both providers (60–73% citation frequency), far ahead of everything else in the panel.
- **The single largest effect in the dataset is not a brand effect — it's a provider effect.** Anthropic's Claude cites SE Ranking in ~45% of relevant answers; OpenAI's GPT cites it in under 1%. This holds in English and in French.
- **French-language visibility lags English for Moz and Surfer SEO**, with non-overlapping confidence intervals — a real gap, not noise.
- **On comparison-style questions, models rarely volunteer a third brand** — they answer almost exclusively within the two brands named in the question.

---

## 2. Overall brand ranking (both languages, self-citation excluded)

| Brand | English freq. | English 95% CI | French freq. | French 95% CI |
|---|---|---|---|---|
| Semrush | 71.4% | [67.3%, 75.2%] | 72.7% | [68.5%, 76.4%] |
| Ahrefs | 66.3% | [62.0%, 70.4%] | 61.4% | [57.0%, 65.6%] |
| Moz | 63.9% | [59.5%, 68.0%] | 49.4% | [45.0%, 53.8%] |
| Screaming Frog | 30.4% | [26.5%, 34.6%] | 31.0% | [27.1%, 35.3%] |
| SE Ranking | 24.1% | [20.5%, 28.1%] | 22.2% | [18.8%, 26.1%] |
| Surfer SEO | 18.4% | [15.2%, 22.0%] | 11.6% | [9.1%, 14.8%] |
| AnswerThePublic | 18.0% | [14.8%, 21.6%] | 20.6% | [17.3%, 24.4%] |
| BrightLocal | 6.9% | [5.0%, 9.5%] | 4.9% | [3.3%, 7.2%] |
| Conductor | 3.5% | [2.2%, 5.5%] | 1.0% | [0.4%, 2.4%] |
| Search Atlas | 0.2% | [0.04%, 1.1%] | ~0% | — |
| Nightwatch | ~0% | — | ~0% | — |

**Reading note:** Search Atlas and Nightwatch's only appearances in the raw dataset came from the one comparison question that named them explicitly (self-citations) — outside that single prompt, neither has any measurable unprompted visibility in this panel.

---

## 3. Finding #1 — Provider divergence on SE Ranking (the headline result)

| Provider | English freq. (95% CI) | French freq. (95% CI) |
|---|---|---|
| Anthropic (Claude) | 47.3% [41.2%, 53.6%] | 44.1% [38.0%, 50.3%] |
| OpenAI (GPT) | 0.8% [0.2%, 2.9%] | 0.4% [0.1%, 2.3%] |

The confidence intervals don't overlap in either language — a ~46-point gap that repeats across two independent languages is not sampling noise. This is the strongest, most surprising and most actionable result in the dataset.

**Secondary provider divergence, smaller but still notable — Moz in French:**

| Provider | French freq. (95% CI) |
|---|---|
| Anthropic (Claude) | 40.8% [34.5%, 47.1%] |
| OpenAI (GPT) | 58.0% [51.7%, 64.0%] |

Non-overlapping intervals here too (a ~17-point gap), but interestingly this gap **does not appear in English** (62.9% vs 64.9%, fully overlapping) — suggesting it's specific to how each provider's French-language training data represents Moz, not a general Anthropic-vs-OpenAI stance on the brand.

---

## 4. Finding #2 — Language gap: Moz and Surfer SEO underperform in French

| Brand | English | French | Overlap? |
|---|---|---|---|
| Moz | 63.9% [59.5%, 68.0%] | 49.4% [45.0%, 53.8%] | No — real gap |
| Surfer SEO | 18.4% [15.2%, 22.0%] | 11.6% [9.1%, 14.8%] | No — real gap |
| Ahrefs | 66.3% [62.0%, 70.4%] | 61.4% [57.0%, 65.6%] | Yes — not significant |
| Screaming Frog | 30.4% [26.5%, 34.6%] | 31.0% [27.1%, 35.3%] | Yes — no gap |
| AnswerThePublic | 18.0% [14.8%, 21.6%] | 20.6% [17.3%, 24.4%] | Yes — no gap |

Only Moz and Surfer SEO show a statistically real English-vs-French gap; the rest of the panel is stable across languages. This rules out a blanket "English brands underperform in French" story — it's brand-specific, not systemic.

---

## 5. Finding #3 — Category-level patterns

**Ceiling effect on "specific use case" questions:** Semrush is cited in 100% (70/70) of responses in both languages for this category. A CI touching the 100% boundary can't distinguish "truly always" from "≥ ~95%, undetectable at this sample size" — treat as a methodological limit, not a hard fact.

**Comparison questions rarely introduce a third brand:**

| Language | Non-target brands cited (excl. self) | Out of |
|---|---|---|
| English | 0 | 112 trials |
| French | 6 total mentions (Semrush 3, Ahrefs 2, SE Ranking 1) | 112 trials |

In English, when a model is asked "Semrush or Ahrefs, which one?", it essentially never volunteers a third option. In French this happens slightly more often, but still rarely (~5% of trials at most). **Implication:** for this question type, the deciding factor for a brand isn't generative content optimization — it's already being one of the two brands a user thinks to name in the first place, which is a traditional brand-awareness outcome, not a GEO-specific lever.

**Open-ended questions ("best SEO tools in 2026?") favor Ahrefs and Screaming Frog more than other categories:**

| Brand | question_ouverte EN | question_ouverte FR |
|---|---|---|
| Ahrefs | 97.1% | 87.1% |
| Screaming Frog | 58.6% | 61.4% |

Screaming Frog barely registers in "recommend for a small business" or "cheaper alternative" style questions but performs comparatively much better on broad "best tools" list-style questions — consistent with it being positioned as a technical/power-user tool rather than a beginner recommendation.

---

## 6. Recommendations — framed as hypotheses to test, not conclusions

These are directional next steps a brand or a researcher could pursue, not proven causal claims. None of this data establishes causation on its own.

1. **Hypothesis — content breadth drives citation, not brand marketing spend.** Citation frequency for the top-tier brands (Semrush, Ahrefs, Moz) may correlate more with the volume of *third-party* comparison content (G2, Capterra, independent "X vs Y" articles) than with owned marketing content. **Test:** correlate citation frequency per brand against a count of third-party comparison/review articles indexed for that brand.

2. **Hypothesis — the SE Ranking/Anthropic gap reflects training-data composition, not product quality.** **Test:** re-run this panel after the next model release from each provider; if the gap persists or shifts predictably, that supports a training-data explanation over a transient artifact.

3. **Hypothesis — the French-language gap for Moz/Surfer SEO reflects a French-content gap, not lower product-market fit in French-speaking markets.** **Test:** audit each brand's French-language content volume (blog posts, localized docs, French backlinks) and check whether it's proportionally smaller than their English footprint, relative to competitors that don't show this gap (e.g. Ahrefs).

4. **Recommendation for GEO monitoring practice — never monitor a single provider.** The SE Ranking case alone shows that single-provider monitoring would produce a badly misleading picture: a brand relying only on ChatGPT-visibility tracking would conclude it has near-zero generative presence, while it's actually being recommended in nearly half of relevant Claude answers.

5. **Hypothesis — structured, factual content is more "extractable" than narrative marketing copy.** Feature comparison tables, pricing pages, and FAQ-style content may be easier for both the answering model and a downstream extraction step to cite confidently than long-form narrative content. **Test:** a controlled before/after study — publish structured comparison content for a brand, re-run the panel after a plausible re-indexing window, and check for a citation-frequency shift (with appropriate baseline controls, since LLM knowledge doesn't update instantly).

---

## 7. What this report does *not* claim

- It does not claim these 11 brands are the only ones users see in real LLM usage (see the closed-list limitation in the README).
- It does not claim causation between any content strategy and citation frequency — all "recommendations" above are hypotheses for further testing, not validated tactics.
- It does not generalize beyond the SEO tools category or beyond `gpt-4o-mini` / `claude-haiku-4-5` — flagship models or other categories may behave differently.
