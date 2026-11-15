#!/usr/bin/env python3
"""Surgical edits for scientific_literacy_en collection."""
import json
from pathlib import Path

ROOT = Path('/Users/herve/Code/rappelia-api/.claude/worktrees/agent-af39c8a7b47156961')
DECKS_FILE = ROOT / 'rappelia/sample_decks.json'
COLS_FILE = ROOT / 'rappelia/collections.json'

decks = json.load(open(DECKS_FILE))
cols = json.load(open(COLS_FILE))
deck_by_id = {d['stableId']: d for d in decks}

LINKS = {
    'scientific_method_evidence': {
        # 0 Correlation vs causation
        0: [12, 6, 5, 7, 26, 27],
        # 1 Study design ladder
        1: [5, 7, 8, 9, 11, 13, 14, 26],
        # 2 Replication and reproducibility
        2: [10, 17, 18, 19, 11],
        # 3 p-values, CIs, effect sizes
        3: [15, 16, 22, 23, 24, 25],
        # 4 How to read a science headline
        4: [11, 17, 20, 21, 26, 28, 29, 30],
    },
    'reasoning_with_data_science_lit': {
        # 0 Base rates and false positives
        0: [0, 1, 2, 3, 4, 5],
        # 1 Bias catalog
        1: [6, 7, 8, 9, 10],
        # 2 Effect sizes
        2: [15, 16, 17, 18, 19],
        # 3 Causal reasoning checklist
        3: [6, 11, 12, 13, 14],
        # 4 Reading risk numbers in news
        4: [4, 5, 16, 17, 18, 19, 15],
    },
    'climate_environment_science': {
        # 0 Greenhouse effect
        0: [0, 1, 5, 18, 23],
        # 1 Carbon cycle
        1: [2, 8, 9, 10, 16, 19, 22],
        # 2 Climate feedback loops
        2: [3, 14, 15, 17],
        # 3 Evidence for climate change
        3: [5, 11, 12, 18, 23, 25],
        # 4 Biodiversity loss
        4: [7, 8, 9, 21],
        # 5 Ocean acidification
        5: [4, 1, 6, 21],
        # 6 Evaluating climate claims
        6: [10, 11, 12, 23, 25, 13],
    },
}

# URL fixes: 404s, redirect loops, intra-deck duplicates
URL_FIXES = {
    # scientific_method_evidence
    # idea[3] dup video -> different stats explainer
    ('scientific_method_evidence', 3, 'videoURL'): 'https://www.youtube.com/watch?v=Z6gjY_YhnBo',
    # idea[4] dup video + dead nature.com -> different YT + NIH
    ('scientific_method_evidence', 4, 'videoURL'): 'https://www.youtube.com/watch?v=8B271L3NtAw',
    ('scientific_method_evidence', 4, 'externalLinkURL'): 'https://www.nih.gov/about-nih/what-we-do/science-health-public-trust',
    # idea[1] cochrane 404 -> /evidence
    ('scientific_method_evidence', 1, 'externalLinkURL'): 'https://www.cochrane.org/evidence',

    # reasoning_with_data_science_lit
    # idea[4] dup video + cdc 404 -> different YT + Wikipedia Relative_risk
    ('reasoning_with_data_science_lit', 4, 'videoURL'): 'https://www.youtube.com/watch?v=eVtCO84MDj8',
    ('reasoning_with_data_science_lit', 4, 'externalLinkURL'): 'https://en.wikipedia.org/wiki/Relative_risk',

    # climate_environment_science
    # idea[5] dup video (EqW used in idea[1]) + noaa 403 -> different YT + oceanservice
    ('climate_environment_science', 5, 'videoURL'): 'https://www.youtube.com/watch?v=dSLh6jc8YLI',
    ('climate_environment_science', 5, 'externalLinkURL'): 'https://oceanservice.noaa.gov/facts/acidification.html',
}

for sid, mapping in LINKS.items():
    d = deck_by_id[sid]
    n_cards = len(d['cards'])
    for j, idxs in mapping.items():
        for k in idxs:
            assert 0 <= k < n_cards, f'{sid} note[{j}] {k} OOR (n={n_cards})'
        d['sampleIdeas'][j]['linkedCardIndices'] = list(idxs)

for (sid, idx, key), url in URL_FIXES.items():
    deck_by_id[sid]['sampleIdeas'][idx][key] = url

for c in cols:
    if c['id'] == 'scientific_literacy_en':
        c['description'] = 'Reason like a scientist: evidence, data, and climate basics.'

with open(DECKS_FILE, 'w') as f:
    json.dump(decks, f, indent=2, ensure_ascii=False)
with open(COLS_FILE, 'w') as f:
    json.dump(cols, f, indent=2, ensure_ascii=False)
print('OK')
