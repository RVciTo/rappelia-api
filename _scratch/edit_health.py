#!/usr/bin/env python3
"""Surgical edits for health_essentials_en collection."""
import json
from pathlib import Path

ROOT = Path('/Users/herve/Code/rappelia-api/.claude/worktrees/agent-af39c8a7b47156961')
DECKS_FILE = ROOT / 'rappelia/sample_decks.json'
COLS_FILE = ROOT / 'rappelia/collections.json'

decks = json.load(open(DECKS_FILE))
cols = json.load(open(COLS_FILE))
deck_by_id = {d['stableId']: d for d in decks}

LINKS = {
    'human_body_energy_basics': {
        # 0 Energy balance
        0: [0, 1, 2, 3, 4, 15, 16],
        # 1 Muscle growth
        1: [5, 6, 7, 8, 38],
        # 2 Sleep quality
        2: [10, 11, 36, 37, 38],
        # 3 Stress physiology
        3: [12, 13, 36, 37],
        # 4 Physical activity dose
        4: [9, 14, 18, 19, 32, 33, 38],
        # 5 Innate vs adaptive immunity
        5: [20, 21, 22],
        # 6 Cardiovascular system
        6: [9, 23, 24, 25, 30],
        # 7 Hormones and metabolism
        7: [17, 26, 27, 28, 29, 34, 35],
    },
    'mental_health_wellbeing_basics': {
        # 0 Anxiety vs normal worry
        0: [2, 3, 5, 20, 23, 24, 27],
        # 1 Sleep deprivation
        1: [7, 8, 9],
        # 2 Cognitive distortions
        2: [5, 6, 17, 23, 27],
        # 3 Exercise as intervention
        3: [10, 11, 27],
        # 4 Seek professional help
        4: [4, 16, 17, 19, 21, 22, 25],
        # 5 Resilience
        5: [12, 13, 14, 15, 24, 26],
        # 6 Antidepressants
        6: [18, 4, 16, 17, 19, 25],
    },
    'nutrition_science_basics': {
        # 0 Macronutrients without myths
        0: [0, 1, 2, 3, 4, 13, 25],
        # 1 Fiber
        1: [5, 15, 26, 17],
        # 2 Glycemic index
        2: [6, 14, 19, 24, 26, 9],
        # 3 Supplements
        3: [4, 11, 28, 7],
        # 4 Food safety
        4: [22, 23, 25],
        # 5 Omega fatty acids
        5: [3, 16, 17, 28],
        # 6 Alcohol
        6: [20, 21, 27],
        # 7 Protein and muscle
        7: [2, 8, 18, 24],
    },
}

# URL fixes (404 replacements). Keep the same intent, point to live .gov pages.
URL_FIXES = {
    # (sid, idea_idx, key) -> new url
    ('human_body_energy_basics', 2, 'externalLinkURL'): 'https://www.cdc.gov/sleep/about/index.html',
    ('human_body_energy_basics', 5, 'externalLinkURL'): 'https://www.cdc.gov/vaccines/index.html',
    ('mental_health_wellbeing_basics', 6, 'externalLinkURL'): 'https://www.nimh.nih.gov/health/topics/mental-health-medications',
    ('nutrition_science_basics', 6, 'externalLinkURL'): 'https://www.cdc.gov/alcohol/about-alcohol-use/index.html',
}

# Apply linkedCardIndices
for sid, mapping in LINKS.items():
    d = deck_by_id[sid]
    n_cards = len(d['cards'])
    for j, idxs in mapping.items():
        for k in idxs:
            assert 0 <= k < n_cards, f'{sid} note[{j}] {k} OOR'
        d['sampleIdeas'][j]['linkedCardIndices'] = list(idxs)

# Apply URL fixes
for (sid, idx, key), url in URL_FIXES.items():
    deck_by_id[sid]['sampleIdeas'][idx][key] = url

# Tile description (verb-led, ≤12 words, second-person)
for c in cols:
    if c['id'] == 'health_essentials_en':
        c['description'] = 'Learn how your body, mind, and nutrition work in evidence-based basics.'

with open(DECKS_FILE, 'w') as f:
    json.dump(decks, f, indent=2, ensure_ascii=False)
with open(COLS_FILE, 'w') as f:
    json.dump(cols, f, indent=2, ensure_ascii=False)
print('OK')
