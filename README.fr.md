# GEO Brand Monitor - Optimisation pour moteurs génératifs sur le marché des outils SEO

*Mesurer quelles marques les IA génératives recommandent réellement, à quelle fréquence, et si la réponse dépend de la langue posée.*

🇬🇧 [Read in English](README.md)

---
![Provider divergence on SE Ranking](report/chart_se_ranking_divergence.png)
![Brand ranking by language](report/chart_brand_ranking.png)

## Pourquoi ce projet

La recherche change. De plus en plus de gens demandent à ChatGPT ou Claude "quel est le meilleur outil SEO pour une petite entreprise ?" plutôt que de taper la même requête sur Google. Pour une marque B2B, ce changement pose une question à laquelle le SEO classique ne répond pas : **à quelle fréquence un LLM cite-t-il votre marque, dans quel contexte, et peut-on seulement mesurer ça de façon fiable ?**

Ce projet construit un pipeline reproductible pour mesurer exactement ça, le **Generative Engine Optimization (GEO)** / **Answer Engine Optimization (AEO)**  appliqué à un marché réel et vérifiable : les **outils SEO & content** (Semrush, Ahrefs, Moz, et 8 autres acteurs B2B).

## Méthodologie

**Marché choisi :** les outils SEO, B2B ; un marché assez restreint pour avoir un périmètre fermé et lisible de marques connues (11), et sur lequel j'ai assez de contexte pour juger si une réponse de modèle est plausible ou n'importe quoi.

**Panier de questions :** 70 questions (35 en anglais, 35 en français — chaque paire est une traduction exacte de l'autre, pour que la comparaison de langue ne soit pas biaisée par des questions différentes). Réparties en 5 catégories d'intention :

| Catégorie | Nb/langue | Exemple |
|---|---|---|
| Recommandation directe | 10 | *"Quel outil SEO recommandes-tu pour une petite entreprise ?"* |
| Comparaison entre marques | 8 | *"Semrush ou Ahrefs, lequel choisir ?"* |
| Alternative à X | 7 | *"Quelle est une alternative moins chère à Semrush ?"* |
| Cas d'usage spécifique | 5 | *"Quel outil pour suivre mon positionnement local sur plusieurs villes ?"* |
| Question ouverte catégorielle | 5 | *"Quels sont les meilleurs outils SEO en 2026 ?"* |

**Non-déterminisme, traité rigoureusement :** les réponses d'un LLM varient d'un appel à l'autre. Chaque question a été répétée **7 fois** par fournisseur. Les résultats sont exprimés en **fréquence de citation avec intervalle de confiance de Wilson**, jamais en présence/absence binaire, l'intervalle classique par approximation normale devient incohérent (peut dépasser 100%) à cette taille d'échantillon, d'où l'usage systématique de `statsmodels.stats.proportion.proportion_confint(..., method='wilson')`.

**Modèles interrogés :** OpenAI (`gpt-4o-mini`) et Anthropic (`claude-haiku-4-5`) — deux fournisseurs différents, volontairement sur des modèles "mini" économiques, qui sont aussi ceux que la majorité des utilisateurs consultent en usage gratuit/standard.

**Extraction :** les réponses en texte libre sont transformées en données structurées (marques citées, ordre d'apparition, sentiment, sources citées) par un second appel LLM à température 0, contraint à une liste fermée des 11 marques connues — avec une couche de normalisation/validation côté code ajoutée après coup, car l'extracteur n'a pas toujours parfaitement respecté cette liste fermée en pratique (voir [Limites](#limites)).

## Pipeline

```
questions_panel.csv
      │
      ▼
query_models.py        → data/raw_responses/*.json   (980 appels : 70 questions × 2 fournisseurs × 7 répétitions)
      │
      ▼
extract_mentions.py    → data/extracted/*.json        (mentions de marques structurées)
      │
      ▼
analyze.py              → report/*.csv                (fréquence de citation + IC Wilson, à 3 niveaux de granularité)
```

Choix de conception à noter :
- **Idempotent par fichier** : chaque appel API/extraction écrit son propre fichier JSON et est sauté s'il existe déjà, donc un run interrompu reprend sans repayer le travail déjà fait.
- **Retry avec backoff, isolé par appel** : un appel raté ne fait jamais échouer tout le run.
- **Filtrage des auto-citations** : pour les questions "alternative" et "comparaison", la marque cible est nommée dans la question elle-même, donc elle apparaît dans la réponse presque par construction. C'est un artefact du prompt, pas un vrai signal. Tous les rapports sont générés en version **brute** et **sans auto-citation**, et c'est la version `_excl_self` qu'il faut privilégier pour comparer les catégories entre elles.

## Résultats clés

*(chiffres complets dans `report/*.csv`, ceci est la version courte)*

**1. Une hiérarchie à trois niveaux nette, stable dans les deux langues.** Semrush, Ahrefs et Moz forment un trio dominant (60-73% de fréquence de citation), avec un décrochage net vers Screaming Frog et SE Ranking (22-31%), puis une longue traîne de marques quasi invisibles sans sollicitation (Conductor, Search Atlas, Nightwatch sous les 5%).

**2. Le signal le plus fort du dataset : un écart massif entre fournisseurs sur SE Ranking, cohérent dans les deux langues.**

| | Anglais | Français |
|---|---|---|
| Anthropic (Claude) | 47,3% [41,2% ; 53,6%] | 44,1% [38,0% ; 50,3%] |
| OpenAI (GPT) | 0,8% [0,2% ; 2,9%] | 0,4% [0,1% ; 2,3%] |

Les intervalles de confiance ne se chevauchent pas, dans aucune des deux langues, c'est un vrai biais de fournisseur, répété, pas du bruit d'échantillonnage. Implication pratique : une stratégie GEO construite uniquement autour de "l'optimisation pour ChatGPT" manquerait complètement la visibilité générative réelle de cette marque sur Claude.

**3. Moz et Surfer SEO sont nettement moins visibles en français qu'en anglais**, avec des intervalles de confiance disjoints (Moz : 63,9% EN vs 49,4% FR). Hypothèse plausible  **non prouvée ici**  un manque de contenu/données d'entraînement en français pour ces marques, à creuser plus avant.

**4. Un effet plafond sur la catégorie "cas d'usage spécifique"** : Semrush est citée dans 100% des réponses (70/70) dans les deux langues. Un intervalle de confiance qui touche 100% ne permet pas de distinguer "vraiment toujours" de "≥ ~95%, échantillon trop petit pour le voir" signalé ici comme une limite méthodologique, pas comme un résultat absolu.

## Limites

- **Liste fermée de 11 marques.** Les modèles mentionnent fréquemment des outils gratuits/adjacents hors de cette liste (Google Search Console, Ubersuggest, Yoast SEO...) volontairement non comptabilisés, ce qui sous-estime probablement la part de voix réelle de la catégorie "outils gratuits". C'était un arbitrage de temps/périmètre assumé, pas un oubli.
- **L'extraction n'est pas parfaitement fiable.** Malgré une consigne explicite de liste fermée, le modèle d'extraction a occasionnellement introduit des marques hors périmètre ("BrightEdge", absente du panier) ou des orthographes incohérentes pour des marques du panier ("SEMrush" vs "Semrush"). Une couche de normalisation/validation côté code a été ajoutée en filet de sécurité — une bonne illustration du fait qu'on ne peut jamais faire une confiance aveugle à la sortie d'un LLM en aval, même sous consigne stricte.
- **Deux fournisseurs, modèles "mini" uniquement.** Les résultats pourraient différer avec des modèles phares ou des fournisseurs supplémentaires (Google Gemini, Perplexity).
- **Échantillon réduit par question (n=7).** Les intervalles de confiance sont larges au niveau d'une question isolée ; toute l'interprétation ici se fait aux niveaux agrégés (n=245 ou n=490), où les intervalles sont assez resserrés pour être significatifs.

## Reproduire ce projet

```bash
pip install -r requirements.txt
cp .env.example .env   # renseigner OPENAI_API_KEY et ANTHROPIC_API_KEY
python src/query_models.py
python src/extract_mentions.py
python src/analyze.py
```

Coût total du run complet (980 appels de requête + ~980 appels d'extraction, tous sur des modèles "mini") : largement sous les 5$.

## Structure du repo

```
├── data/
│   └── questions_panel.csv       # le panier de 70 questions (35 EN + 35 FR, paires miroir)
├── src/
│   ├── query_models.py           # étape 1 : interroge les deux fournisseurs
│   ├── extract_mentions.py       # étape 2 : structure les réponses brutes
│   └── analyze.py                # étape 3 : fréquences + IC Wilson
├── report/                       # CSV générés (brut + hors auto-citation, 3 granularités)
└── requirements.txt
```

## Pistes de prolongement

- Élargir la liste de marques pour capter les outils gratuits/adjacents, afin de tester directement l'hypothèse de sous-estimation.
- Ajouter un troisième fournisseur (Google Gemini) pour voir si l'écart sur SE Ranking est spécifique à Anthropic ou un schéma à deux camps.
- Suivre le même panier dans le temps pour voir si la visibilité de marque générative bouge aussi vite que le classement SEO classique.

---

**À propos de ce projet :** construit comme étude de cas concrète pendant une transition vers la gestion de projet IA, à l'interface entre produit, data et IA générative. Questions/retours bienvenus.

Nada Chniter — [Linkedin: https://www.linkedin.com/in/nada-chniter/ ] 
