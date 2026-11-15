#!/usr/bin/env python3
"""Surgical edits for financial_literacy_en collection.
- Wire linkedCardIndices on every note.
- Strip URLs from card front/back/hint, move into note externalLinkURL if missing.
- Update tile description (verb-led).
"""
import json, re, sys
from pathlib import Path

ROOT = Path('/Users/herve/Code/rappelia-api')
DECKS_FILE = ROOT / 'rappelia/sample_decks.json'
COLS_FILE = ROOT / 'rappelia/collections.json'

decks = json.load(open(DECKS_FILE))
cols = json.load(open(COLS_FILE))

deck_by_id = {d['stableId']: d for d in decks}

# ---- linkedCardIndices map (note_index -> [card indices]) ----
LINKS = {
    'budget_basics_everyday_money': {
        # 0 50/30/20 rule
        0: [5, 4, 34, 6, 0, 26],
        # 1 fixed-first + sinking funds
        1: [2, 3, 8, 9, 10, 22, 36, 30],
        # 2 emergency fund
        2: [7, 22, 32, 17, 26, 27],
        # 3 worksheets / tracking
        3: [15, 30, 31, 12, 13, 38],
        # 4 trusted sources
        4: [12, 13, 14, 25],
        # 5 sinking funds
        5: [8, 10, 29, 36, 22],
        # 6 envelope method
        6: [11, 3, 4, 24, 35, 19],
        # 7 subscription leaks
        7: [16, 38, 24, 17, 19],
        # 8 variable income
        8: [18, 20, 1, 27, 28, 21],
        # 9 weekly check-ins
        9: [15, 30, 31, 35, 9, 38],
    },
    'debt_credit_basics': {
        # 0 APR
        0: [0, 1, 2, 16, 28, 13, 22, 25],
        # 1 compound interest
        1: [3, 4, 5, 6, 24, 29],
        # 2 credit score vs report
        2: [7, 8, 14, 15, 20, 23],
        # 3 payoff strategies
        3: [10, 11, 26, 21, 17, 27],
        # 4 identity theft
        4: [12, 18, 19, 20, 8],
        # 5 minimum payments
        5: [6, 1, 3, 26, 17, 28],
        # 6 credit score levers
        6: [7, 9, 14, 15, 23, 20],
        # 7 credit utilization
        7: [9, 7, 8, 23, 21],
        # 8 credit cards
        8: [0, 1, 6, 9, 28, 17, 27],
        # 9 avalanche/snowball
        9: [10, 11, 26, 17, 21, 27],
    },
    'investing_basics_wealth_building': {
        # 0 compound interest
        0: [0, 1, 17, 21, 22, 26],
        # 1 stock ownership
        1: [2, 3, 4, 19, 23, 28],
        # 2 bonds
        2: [5, 6, 14, 22, 24],
        # 3 index funds vs active
        3: [7, 8, 13, 18, 19, 26],
        # 4 dollar-cost averaging
        4: [10, 15, 16, 23, 28],
        # 5 tax-advantaged accounts
        5: [11, 12, 18, 25, 27],
        # 6 inflation
        6: [17, 4, 14, 22, 18, 28],
    },
}

# ---- URL strips on cards (sid -> {card_idx: new_back}) ----
# We strip the URL out of `back` (and `hint`/`front` if present). The note's externalLinkURL
# already covers the resource for budget cards 12,13,14,25 and debt cards 13,14,15,22,23,24,25.
URL_STRIPS = {
    'budget_basics_everyday_money': {
        12: ('Where can you get a budgeting worksheet PDF?',
             'Consumer.gov publishes a free Make-a-Budget worksheet you can fill in by hand.',
             'Federal consumer site.'),
        13: ('Where can you learn about budgeting from CFPB?',
             'The Consumer Financial Protection Bureau has a plain-language guide for creating and sticking to a budget.',
             'CFPB consumer guide.'),
        14: ('Where can you watch a 50/30/20 lesson?',
             'Khan Academy has a free video lesson on the 50/30/20 budget rule inside its financial-literacy course.',
             'Free non-profit lesson.'),
        25: ('Where can you find U.S. government budgeting tips?',
             'USA.gov publishes a budgeting and financial-goals page with checklists and links to other federal tools.',
             'Official .gov resource.'),
    },
    'debt_credit_basics': {
        13: ('Where can you learn APR basics from a federal regulator?',
             'The Consumer Financial Protection Bureau (CFPB) explains what a credit card interest rate and APR mean in plain language.',
             'Federal consumer agency.'),
        14: ('Where can you learn credit report and score basics?',
             'CFPB publishes a hub of plain-language answers to credit-report and credit-score questions.',
             'Federal consumer agency.'),
        15: ('Where can you watch a free explainer on credit scores?',
             'Khan Academy has a short, free video that explains what a credit score is.',
             'Free non-profit lesson.'),
        22: ('Where can you learn the difference between APR and interest rate?',
             'CFPB has a short Q&A explaining how loan interest rate and APR differ.',
             'Federal consumer agency.'),
        23: ('Where can you learn how to read a credit score?',
             'CFPB explains what credit-score ranges mean and how lenders use them.',
             'Federal consumer agency.'),
        24: ('Where can you watch a free explainer on compound interest?',
             'Khan Academy has a free video introducing compound interest and how it accumulates.',
             'Free non-profit lesson.'),
        25: ('Where can you watch a free explainer on APR?',
             'Khan Academy has a free video explaining APR and how it differs from a stated rate.',
             'Free non-profit lesson.'),
    },
}

URL_RE = re.compile(r'https?://\S+')

def strip_urls_in_card(card):
    for f in ('front', 'back', 'hint'):
        v = card.get(f)
        if v and URL_RE.search(v):
            card[f] = URL_RE.sub('', v).rstrip(' .:').rstrip()

# Apply linkedCardIndices
for sid, mapping in LINKS.items():
    d = deck_by_id[sid]
    n_cards = len(d['cards'])
    for j, idxs in mapping.items():
        for k in idxs:
            assert 0 <= k < n_cards, f'{sid} note[{j}] index {k} out of range (n={n_cards})'
        d['sampleIdeas'][j]['linkedCardIndices'] = list(idxs)

# Apply URL strips (full replacement of front/back/hint)
for sid, mapping in URL_STRIPS.items():
    d = deck_by_id[sid]
    for ci, (front, back, hint) in mapping.items():
        c = d['cards'][ci]
        c['front'] = front
        c['back'] = back
        c['hint'] = hint

# Belt-and-suspenders: strip any residual URL from any card in these decks
for sid in LINKS:
    for c in deck_by_id[sid]['cards']:
        strip_urls_in_card(c)

# Update collection tile description (verb-led)
for c in cols:
    if c['id'] == 'financial_literacy_en':
        c['description'] = 'Master budgeting, credit, and investing for everyday money decisions.'

# Save
with open(DECKS_FILE, 'w') as f:
    json.dump(decks, f, indent=2, ensure_ascii=False)

with open(COLS_FILE, 'w') as f:
    json.dump(cols, f, indent=2, ensure_ascii=False)

print('OK financial_literacy_en')
