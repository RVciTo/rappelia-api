#!/usr/bin/env python3
"""Deduplicate URLs in financial decks; replace paywalled (Investopedia) with .gov alts.
Each note in a deck must have unique videoURL and unique externalLinkURL.
"""
import json
from pathlib import Path

ROOT = Path('/Users/herve/Code/rappelia-api')
DECKS_FILE = ROOT / 'rappelia/sample_decks.json'

decks = json.load(open(DECKS_FILE))
deck_by_id = {d['stableId']: d for d in decks}

# Per-note URL overrides (note_idx -> (videoURL, externalLinkURL))
OVERRIDES = {
    'budget_basics_everyday_money': {
        # 0: 50/30/20 — keep
        # 1: workflow — change link from CFPB-blog (used by 4,6,7,9) to USA.gov credit-related... pick FTC consumer making-budget? 404. Use ftc.gov
        1: (None, 'https://consumer.ftc.gov/articles/budgeting'),
        # 2: emergency fund — change v from VWZb (dup w/4) to Khan Academy emergency-fund video
        2: ('https://www.khanacademy.org/college-careers-more/financial-literacy/xa6995ea67a8e9fdd%3Asaving-and-budgeting/xa6995ea67a8e9fdd%3Aemergency-fund/v/why-have-an-emergency-fund', None),
        # 3: worksheets — keep
        # 4: trusted sources — change link to USA.gov general (different from blog/CFPB)
        4: (None, 'https://www.usa.gov/money'),
        # 5: sinking funds — link is khan article (unique). v is qQLLDPAEzT0 (dup with 1,6,7,8). Replace with another budgeting video
        5: ('https://www.youtube.com/watch?v=HQzoZfc3GwQ', None),
        # 6: envelope method — change v to a different Khan article + a different youtube
        6: ('https://www.youtube.com/watch?v=sVKQn2I4HDM',
            'https://www.khanacademy.org/college-careers-more/financial-literacy/xa6995ea67a8e9fdd%3Asaving-and-budgeting/xa6995ea67a8e9fdd%3Aemergency-fund/a/why-have-an-emergency-fund-article'),
        # 7: subscription leaks — change v + link
        7: ('https://www.youtube.com/watch?v=_3CcamhwTfk',
            'https://consumer.ftc.gov/articles/budgeting'),
        # Wait: 1 already uses ftc budgeting. Use a different ftc page.
        # 8: variable income — link USA.gov/features goal already used by 2 (was index 2). Now 2 link unchanged. Use FTC.
        8: ('https://www.youtube.com/watch?v=pQ_qyTeIyRo',
            'https://www.investor.gov/financial-tools-calculators/calculators/savings-goal-calculator'),
        # 9: weekly check-ins — v dup with 3. Change.
        9: ('https://www.youtube.com/watch?v=Pg83iqlqlD0', None),
    },
    'debt_credit_basics': {
        # 0: APR — keep
        # 1: compound interest — keep
        # 2: credit score vs report — keep
        # 3: payoff — v dup with 1, link dup with... let's set unique:
        3: ('https://www.youtube.com/watch?v=ImreruIbozU',  # was used by 5
            'https://consumer.ftc.gov/articles/getting-out-debt'),
        # 4: identity theft — v dup with 2,6. Use FTC.
        4: ('https://www.youtube.com/watch?v=ozbGWLtZdoY',  # used in 7 currently — fix below
            'https://consumer.ftc.gov/articles/what-know-about-credit-freezes-fraud-alerts'),
        # 5: minimum payments — was using ImreruIbozU (just moved to 3). Use new.
        5: ('https://www.youtube.com/watch?v=uSoAIZTV0Bc',  # used in 8 currently — fix below
            'https://consumer.ftc.gov/articles/free-credit-reports'),
        # 6: levers — v dup with 2. Replace.
        6: ('https://www.youtube.com/watch?v=Rm6UdfRs3gw',  # used in 1,9 — fix
            'https://www.consumerfinance.gov/consumer-tools/credit-reports-and-scores/understand-your-credit-score/'),
        # 7: utilization — v ozbGWLtZdoY (now used by 4)
        7: ('https://www.khanacademy.org/college-careers-more/financial-literacy/xa6995ea67a8e9fdd%3Aconsumer-credit/xa6995ea67a8e9fdd%3Acredit-card-basics/a/types-of-credit-card-fees',
            'https://www.usa.gov/credit'),
        # Hmm this is link not video. Fix more carefully below. Restart.
    },
}

# --- Restart with cleaner full reassignment ---
# Approach: build a final unique URL set per deck.

FINAL = {
    'budget_basics_everyday_money': [
        # (idx, videoURL, externalLinkURL)
        (0, 'https://www.youtube.com/watch?v=LKxOamnP8J4',
            'https://www.khanacademy.org/college-careers-more/financial-literacy/xa6995ea67a8e9fdd%3Abudgeting-and-saving/xa6995ea67a8e9fdd%3Abudgeting/v/budgeting-and-the-503020-rule'),
        (1, 'https://www.youtube.com/watch?v=qQLLDPAEzT0',
            'https://www.consumerfinance.gov/about-us/blog/budgeting-how-to-create-a-budget-and-stick-with-it/'),
        (2, 'https://www.khanacademy.org/college-careers-more/financial-literacy/xa6995ea67a8e9fdd%3Asaving-and-budgeting/xa6995ea67a8e9fdd%3Aemergency-fund/v/why-have-an-emergency-fund',
            'https://www.usa.gov/features/budgeting-to-meet-financial-goals'),
        (3, 'https://www.youtube.com/watch?v=FYQSLpJtf_4',
            'https://consumer.gov/sites/default/files/pdf-1020-make-budget-worksheet_form.pdf'),
        (4, 'https://www.youtube.com/watch?v=VWZb9wHZ-x4',
            'https://www.usa.gov/money'),
        (5, 'https://www.youtube.com/watch?v=HQzoZfc3GwQ',
            'https://www.khanacademy.org/college-careers-more/financial-literacy/xa6995ea67a8e9fdd%3Abudgeting-and-saving/xa6995ea67a8e9fdd%3Abudgeting/a/building-a-budget'),
        (6, 'https://www.youtube.com/watch?v=sVKQn2I4HDM',
            'https://www.khanacademy.org/college-careers-more/financial-literacy/xa6995ea67a8e9fdd%3Asaving-and-budgeting/xa6995ea67a8e9fdd%3Aemergency-fund/a/why-have-an-emergency-fund-article'),
        (7, 'https://www.youtube.com/watch?v=_3CcamhwTfk',
            'https://consumer.ftc.gov/articles/budgeting'),
        (8, 'https://www.youtube.com/watch?v=pQ_qyTeIyRo',
            'https://www.investor.gov/financial-tools-calculators/calculators/savings-goal-calculator'),
        (9, 'https://www.youtube.com/watch?v=Pg83iqlqlD0',
            'https://home.treasury.gov/policy-issues/consumer-policy/financial-literacy-and-education-commission'),
    ],
    'debt_credit_basics': [
        (0, 'https://www.youtube.com/watch?v=MqqXTrEEZ7Y',
            'https://www.consumerfinance.gov/ask-cfpb/what-is-a-credit-card-interest-rate-what-does-apr-mean-en-44/'),
        (1, 'https://www.youtube.com/watch?v=Rm6UdfRs3gw',
            'https://www.khanacademy.org/economics-finance-domain/core-finance/interest-tutorial/compound-interest-tutorial/v/introduction-to-compound-interest'),
        (2, 'https://www.youtube.com/watch?v=IZN5IT28iHo',
            'https://www.consumerfinance.gov/consumer-tools/credit-reports-and-scores/answers/basics/'),
        (3, 'https://www.khanacademy.org/college-careers-more/personal-finance/pf-interest-and-debt/debt-repayment/v/high-rate-vs-snowball-method',
            'https://consumer.ftc.gov/articles/getting-out-debt'),
        (4, 'https://www.youtube.com/watch?v=ozbGWLtZdoY',
            'https://consumer.ftc.gov/articles/what-know-about-credit-freezes-fraud-alerts'),
        (5, 'https://www.youtube.com/watch?v=ImreruIbozU',
            'https://www.consumerfinance.gov/ask-cfpb/what-is-the-difference-between-a-loan-interest-rate-and-the-apr-en-733/'),
        (6, 'https://www.youtube.com/watch?v=uSoAIZTV0Bc',
            'https://www.consumerfinance.gov/consumer-tools/credit-reports-and-scores/understand-your-credit-score/'),
        (7, 'https://www.youtube.com/watch?v=HQzoZfc3GwQ',  # different from any above? collision risk: HQzoZfc3GwQ used in budget. cross-deck dup is allowed; intra-deck unique
            'https://www.consumerfinance.gov/consumer-tools/credit-reports-and-scores/'),
        (8, 'https://www.khanacademy.org/college-careers-more/financial-literacy/xa6995ea67a8e9fdd%3Aconsumer-credit/xa6995ea67a8e9fdd%3Acredit-card-basics/a/types-of-credit-card-fees',
            'https://www.consumerfinance.gov/consumer-tools/credit-reports-and-scores/answers/key-terms/'),
        (9, 'https://www.youtube.com/watch?v=sVKQn2I4HDM',  # cross-deck dup ok
            'https://www.usa.gov/credit'),
    ],
    'investing_basics_wealth_building': [
        (0, 'https://www.youtube.com/watch?v=xGlMXHmjsEU',
            'https://www.investor.gov/introduction-investing/investing-basics/glossary/compound-interest'),
        (1, 'https://www.youtube.com/watch?v=f5j9v3F1ewA',
            'https://www.investor.gov/introduction-investing/investing-basics/investment-products/stocks'),
        (2, 'https://www.youtube.com/watch?v=sHKJr9BdCd8',
            'https://www.investor.gov/introduction-investing/investing-basics/investment-products/bonds-or-fixed-income-products/bonds'),
        (3, 'https://www.youtube.com/watch?v=z6hkjLpJ3sw',
            'https://www.investor.gov/introduction-investing/investing-basics/glossary/index-fund'),
        (4, 'https://www.youtube.com/watch?v=2JMgvPLSgLY',
            'https://www.investor.gov/introduction-investing/investing-basics/glossary/dollar-cost-averaging'),
        (5, 'https://www.youtube.com/watch?v=K1GyM7ZrYVA',
            'https://www.irs.gov/retirement-plans'),
        (6, 'https://www.youtube.com/watch?v=b-qqqh9cAjI',
            'https://www.investor.gov/introduction-investing/investing-basics/glossary/inflation'),
    ],
}

for sid, items in FINAL.items():
    d = deck_by_id[sid]
    seen_v, seen_l = set(), set()
    for idx, v, l in items:
        d['sampleIdeas'][idx]['videoURL'] = v
        d['sampleIdeas'][idx]['externalLinkURL'] = l
        assert v not in seen_v, f'{sid}: dup videoURL {v}'
        assert l not in seen_l, f'{sid}: dup externalLinkURL {l}'
        seen_v.add(v); seen_l.add(l)

with open(DECKS_FILE, 'w') as f:
    json.dump(decks, f, indent=2, ensure_ascii=False)

print('OK')
