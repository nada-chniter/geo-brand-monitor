# Rapport d'analyse — GEO Brand Monitor (Outils SEO, B2B)

🇬🇧 [Read in English](analysis_report.md) · Voir le [README](../README.fr.md) pour la méthodologie complète.

**Périmètre de ce document :** résultats détaillés, découpage par catégorie et par fournisseur, et recommandations formulées comme des hypothèses à tester — pas des conclusions prouvées. Échantillon : 980 appels bruts (70 questions × 2 fournisseurs × 7 répétitions), agrégés avec intervalles de confiance de Wilson partout. Toutes les fréquences ci-dessous utilisent le jeu de données `_excl_self` (auto-citations des questions "alternative"/"comparaison" retirées), sauf mention contraire — voir le README pour le pourquoi.

---

## 1. Résumé exécutif

- **Semrush, Ahrefs et Moz dominent** les réponses génératives dans les deux langues et chez les deux fournisseurs (60-73% de fréquence de citation), loin devant tout le reste du panier.
- **L'effet le plus important du dataset n'est pas un effet de marque — c'est un effet de fournisseur.** Claude (Anthropic) cite SE Ranking dans ~45% des réponses pertinentes ; GPT (OpenAI) la cite dans moins de 1%. Ça tient en anglais comme en français.
- **La visibilité en français est en retard sur l'anglais pour Moz et Surfer SEO**, avec des intervalles de confiance disjoints — un vrai écart, pas du bruit.
- **Sur les questions de comparaison, les modèles proposent rarement une troisième marque** — ils répondent presque exclusivement dans le cadre des deux marques nommées dans la question.

---

## 2. Classement global des marques (deux langues, hors auto-citation)

| Marque | Fréq. anglais | IC 95% anglais | Fréq. français | IC 95% français |
|---|---|---|---|---|
| Semrush | 71,4% | [67,3% ; 75,2%] | 72,7% | [68,5% ; 76,4%] |
| Ahrefs | 66,3% | [62,0% ; 70,4%] | 61,4% | [57,0% ; 65,6%] |
| Moz | 63,9% | [59,5% ; 68,0%] | 49,4% | [45,0% ; 53,8%] |
| Screaming Frog | 30,4% | [26,5% ; 34,6%] | 31,0% | [27,1% ; 35,3%] |
| SE Ranking | 24,1% | [20,5% ; 28,1%] | 22,2% | [18,8% ; 26,1%] |
| Surfer SEO | 18,4% | [15,2% ; 22,0%] | 11,6% | [9,1% ; 14,8%] |
| AnswerThePublic | 18,0% | [14,8% ; 21,6%] | 20,6% | [17,3% ; 24,4%] |
| BrightLocal | 6,9% | [5,0% ; 9,5%] | 4,9% | [3,3% ; 7,2%] |
| Conductor | 3,5% | [2,2% ; 5,5%] | 1,0% | [0,4% ; 2,4%] |
| Search Atlas | 0,2% | [0,04% ; 1,1%] | ~0% | — |
| Nightwatch | ~0% | — | ~0% | — |

**Note de lecture :** les seules apparitions de Search Atlas et Nightwatch dans les données brutes venaient de l'unique question de comparaison qui les nommait explicitement (auto-citations) — en dehors de ce prompt précis, aucune des deux n'a de visibilité spontanée mesurable dans ce panier.

---

## 3. Résultat n°1 — Divergence de fournisseur sur SE Ranking (le résultat phare)

| Fournisseur | Fréq. anglais (IC 95%) | Fréq. français (IC 95%) |
|---|---|---|
| Anthropic (Claude) | 47,3% [41,2% ; 53,6%] | 44,1% [38,0% ; 50,3%] |
| OpenAI (GPT) | 0,8% [0,2% ; 2,9%] | 0,4% [0,1% ; 2,3%] |

Les intervalles de confiance ne se chevauchent dans aucune des deux langues — un écart d'environ 46 points qui se répète sur deux langues indépendantes n'est pas du bruit d'échantillonnage. C'est le résultat le plus fort, le plus surprenant et le plus actionnable du dataset.

**Divergence de fournisseur secondaire, plus modeste mais notable — Moz en français :**

| Fournisseur | Fréq. français (IC 95%) |
|---|---|
| Anthropic (Claude) | 40,8% [34,5% ; 47,1%] |
| OpenAI (GPT) | 58,0% [51,7% ; 64,0%] |

Intervalles disjoints ici aussi (écart d'environ 17 points), mais fait intéressant, cet écart **n'apparaît pas en anglais** (62,9% vs 64,9%, intervalles qui se chevauchent totalement) — ce qui suggère que c'est spécifique à la façon dont les données d'entraînement françaises de chaque fournisseur représentent Moz, pas une position générale d'Anthropic contre OpenAI sur la marque.

---

## 4. Résultat n°2 — Écart de langue : Moz et Surfer SEO sous-performent en français

| Marque | Anglais | Français | Chevauchement ? |
|---|---|---|---|
| Moz | 63,9% [59,5% ; 68,0%] | 49,4% [45,0% ; 53,8%] | Non — écart réel |
| Surfer SEO | 18,4% [15,2% ; 22,0%] | 11,6% [9,1% ; 14,8%] | Non — écart réel |
| Ahrefs | 66,3% [62,0% ; 70,4%] | 61,4% [57,0% ; 65,6%] | Oui — pas significatif |
| Screaming Frog | 30,4% [26,5% ; 34,6%] | 31,0% [27,1% ; 35,3%] | Oui — pas d'écart |
| AnswerThePublic | 18,0% [14,8% ; 21,6%] | 20,6% [17,3% ; 24,4%] | Oui — pas d'écart |

Seules Moz et Surfer SEO montrent un écart anglais/français statistiquement réel ; le reste du panier est stable entre les deux langues. Ça exclut un récit global du type "les marques anglophones sous-performent en français" — c'est spécifique à certaines marques, pas systémique.

---

## 5. Résultat n°3 — Dynamiques au niveau des catégories

**Effet plafond sur les questions "cas d'usage spécifique" :** Semrush est citée dans 100% (70/70) des réponses dans les deux langues sur cette catégorie. Un IC qui touche la borne des 100% ne permet pas de distinguer "vraiment toujours" de "≥ ~95%, indétectable à cette taille d'échantillon" — à traiter comme une limite méthodologique, pas comme un fait dur.

**Les questions de comparaison introduisent rarement une troisième marque :**

| Langue | Marques hors-cible citées (hors auto-citation) | Sur |
|---|---|---|
| Anglais | 0 | 112 essais |
| Français | 6 mentions au total (Semrush 3, Ahrefs 2, SE Ranking 1) | 112 essais |

En anglais, quand un modèle est interrogé "Semrush ou Ahrefs, lequel ?", il ne propose quasiment jamais une troisième option. En français, ça arrive un peu plus souvent, mais reste rare (~5% des essais au maximum). **Implication :** pour ce type de question, le facteur décisif pour une marque n'est pas l'optimisation de contenu générative — c'est déjà d'être l'une des deux marques qu'un utilisateur pense à nommer en premier lieu, ce qui relève de la notoriété de marque classique, pas d'un levier spécifique au GEO.

**Les questions ouvertes ("meilleurs outils SEO en 2026 ?") favorisent Ahrefs et Screaming Frog plus que les autres catégories :**

| Marque | question_ouverte EN | question_ouverte FR |
|---|---|---|
| Ahrefs | 97,1% | 87,1% |
| Screaming Frog | 58,6% | 61,4% |

Screaming Frog apparaît à peine sur les questions type "recommande pour une petite entreprise" ou "alternative moins chère", mais performe nettement mieux sur les questions larges type "meilleurs outils" — cohérent avec un positionnement d'outil technique/power-user plutôt que de recommandation pour débutant.

---

## 6. Recommandations — formulées comme hypothèses à tester, pas comme conclusions

Ce sont des pistes directionnelles qu'une marque ou un chercheur pourrait explorer, pas des affirmations causales prouvées. Aucune de ces données n'établit à elle seule une causalité.

1. **Hypothèse — l'ampleur du contenu tiers pousse la citation, pas le budget marketing de la marque.** La fréquence de citation des marques du trio de tête (Semrush, Ahrefs, Moz) pourrait corréler davantage avec le volume de contenu comparatif *tiers* (G2, Capterra, articles indépendants "X vs Y") qu'avec le contenu marketing propriétaire. **Test :** corréler la fréquence de citation par marque avec un décompte d'articles de comparaison/avis tiers indexés pour cette marque.

2. **Hypothèse — l'écart SE Ranking/Anthropic reflète la composition des données d'entraînement, pas la qualité produit.** **Test :** relancer ce panier après la prochaine sortie de modèle de chaque fournisseur ; si l'écart persiste ou évolue de façon prévisible, ça soutient une explication liée aux données d'entraînement plutôt qu'un artefact transitoire.

3. **Hypothèse — l'écart de langue pour Moz/Surfer SEO reflète un manque de contenu en français, pas une moindre adéquation produit-marché sur les marchés francophones.** **Test :** auditer le volume de contenu en français de chaque marque (articles de blog, documentation localisée, backlinks français) et vérifier s'il est proportionnellement plus faible que leur empreinte anglophone, par rapport à des concurrents qui ne montrent pas cet écart (ex. Ahrefs).

4. **Recommandation pour la pratique du monitoring GEO — ne jamais surveiller un seul fournisseur.** Le seul cas SE Ranking montre qu'un monitoring mono-fournisseur donnerait une image gravement trompeuse : une marque qui ne suivrait que sa visibilité sur ChatGPT conclurait à une présence générative quasi nulle, alors qu'elle est en réalité recommandée dans près de la moitié des réponses pertinentes de Claude.

5. **Hypothèse — le contenu structuré et factuel est plus "extractible" que le contenu marketing narratif.** Les tableaux comparatifs de fonctionnalités, les pages de tarification et le contenu type FAQ pourraient être plus faciles à citer avec confiance, pour le modèle répondant comme pour une étape d'extraction en aval, qu'un contenu narratif long format. **Test :** une étude contrôlée avant/après — publier du contenu comparatif structuré pour une marque, relancer le panier après une fenêtre de ré-indexation plausible, et vérifier un changement de fréquence de citation (avec des contrôles de référence appropriés, car la connaissance d'un LLM ne se met pas à jour instantanément).

---

## 7. Ce que ce rapport ne prétend pas

- Il ne prétend pas que ces 11 marques sont les seules que les utilisateurs voient en usage réel des LLM (voir la limite de liste fermée dans le README).
- Il ne prétend pas de causalité entre une stratégie de contenu quelconque et la fréquence de citation — toutes les "recommandations" ci-dessus sont des hypothèses à tester, pas des tactiques validées.
- Il ne généralise pas au-delà de la catégorie des outils SEO ni au-delà de `gpt-4o-mini` / `claude-haiku-4-5` — des modèles phares ou d'autres catégories pourraient se comporter différemment.
