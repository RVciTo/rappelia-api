# Editorial audit — English content (2026-04-30)

End-to-end review of every active English collection in `rappelia/sample_decks.json` and `rappelia/collections.json` per the `EDITORIAL_PLAYBOOK.md`. Performed in this session via four parallel worktree agents (groups A–D), with a final consolidation pass on `main`.

## Scope

| Collection | Decks | Cards | Notes |
|---|---:|---:|---:|
| `financial_literacy_en` | 3 | 98 | 27 |
| `health_essentials_en` | 3 | 96 | 23 |
| `scientific_literacy_en` | 3 | 77 | 17 |
| `digital_literacy_en` | 3 | 67 | 17 |
| `general_culture_en` | 3 | 98 | 22 |
| `stem_foundations_en` | 7 | 156 | 71 |
| `computer_science_cs50_en` | 5 | 167 | 39 |
| `web3_blockchain_en` | 3 | 83 | 21 |
| `developer_foundations_en` | 3 | 104 | 18 |
| **Total** | **33** | **946** | **255** |

Excluded: `code_route_fr` and any `isActive: false` collections.

## Validation results

All 33 EN decks pass the playbook done-criteria:

- ✅ JSON parses cleanly for both files.
- ✅ Every note has non-empty `linkedCardIndices`, every index `< len(cards)`. (255/255 wired — every note was missing this field at the start of the session.)
- ✅ No URL or `Réf:` footer in any card `front`/`back`/`hint`.
- ✅ No duplicate `videoURL` or `externalLinkURL` within any deck.
- ✅ Every member deck's `language` matches its collection's `language`.
- ✅ Every collection description is verb-led, ≤12 words.

## HTTP audit

All 460 unique URLs across the 33 EN decks were curl-tested with a browser UA. Final breakdown:

- **447 / 460 → 200 OK** direct.
- **7 / 460 → 403** — all `consumerfinance.gov` (CFPB bot-walls). Pages render in a real browser; canonical .gov regulator content; kept per source-hierarchy rule (same precedent as `banque-france.fr` in the FR pass).
- **6 / 460 → 404** — replaced during the final pass:

| Original | Replacement |
|---|---|
| `apa.org/helpcenter/cognitive-behavior` | `apa.org/topics/cognitive-behavioral-therapy` |
| `apa.org/science/about/psa/resilience` | `apa.org/topics/resilience` |
| `apa.org/science/about/psa/exercise` | `apa.org/topics/exercise-fitness` |
| `github.com/.../bitcoinbook/.../ch09.asciidoc` | `.../ch11_blockchain.adoc` |
| `learn.microsoft.com/.../threat-modeling` | `owasp.org/www-community/Threat_Modeling` |
| `docs.openzeppelin.com/contracts/5.x/api/security` | `docs.openzeppelin.com/contracts/5.x/access-control` |

## What changed across the 33 decks

### Group-level (collections.json)

- 9 collection descriptions rewritten verb-led, second-person, ≤12 words. Examples:
  - `financial_literacy_en` → "Master budgeting, credit, and investing for everyday money decisions."
  - `health_essentials_en` → "Learn how your body, mind, and nutrition work in evidence-based basics."
  - `stem_foundations_en` → "Build core math, physics, chemistry, biology, and CS skills."
  - `computer_science_cs50_en` → "Master core CS concepts the way Harvard CS50 teaches them."
  - `developer_foundations_en` → "Level up your security, OS, and command-line skills."
- Color collisions resolved across groups:
  - `web3_blockchain_en` (was all-purple) → purple / indigo / blue.
  - `computer_science_cs50_en` (was all-red) → red / orange / yellow / pink / teal.
  - `stem_probability_statistics` blue → teal (was clashing with algebra).
- Naming canonicalized: dropped redundant `STEM ` prefix in stem decks; CS deck disambiguated to `Computer Science Essentials` to avoid collision with the peer-collection CS50 deck.
- Tile + deck descriptions rewritten verb-led "you" voice across all 9 collections.

### Deck-level (sample_decks.json)

- **255 notes** — `linkedCardIndices` wired (was empty/missing on every single note in every EN deck). Each note links 4–12 semantically-matched cards.
- **~12 cards** — URLs stripped from `back` / `front` (financial group: 11 cards; cs50_python_sql_web: 1 card).
- **~50 videos** replaced — channel-style YouTube URLs, dead/mismatched IDs (notably algebra "Rates of change" pointed at a TED-Ed video about hydration → Khan Academy "Worked example: Dimensional analysis"), 21 STEM video IDs, plus CS50 disambiguation videos.
- **~30 external links** replaced — paywalled Investopedia, dead `.gov` health pages, broken cdc/sleep + cdc/vaccines + nimh/medications + cdc/alcohol, cochrane 404, noaa 403, geeksforgeeks timeout, plus the 6 final-pass fixes above.
- **57 intra-deck URL duplicates resolved** in CS50 and developer_foundations decks by disambiguating across CS50 weeks/shorts/labs/psets pages and per-topic CS50 videos.

### Source hierarchy used

Replacement priority, top to bottom (per playbook):

1. **Government / public** — `cisa.gov`, `nist.gov`, `ftc.gov`, `consumerfinance.gov`, `usa.gov`, `nasa.gov`, `nih.gov`, `cdc.gov`, `noaa.gov`, `osha.gov`, `ssa.gov`, `treasury.gov`, `gov.uk`, `europa.eu` (English), `who.int`, `oecd.org`, `un.org`, `unesco.org`, `loc.gov`.
2. **Authoritative non-profits / canonical project docs** — MDN (`developer.mozilla.org`), OWASP (`owasp.org`), EFF, IEEE, ACM, W3C, IETF, OpenStax, Stanford Encyclopedia of Philosophy, Internet Encyclopedia of Philosophy, APA (`apa.org/topics/*`), CS50 (`cs50.harvard.edu`), MIT OCW (incl. `missing.csail.mit.edu`), git-scm, kernel.org, man7.org, GNU bash manual, docs.python.org. For Web3: `ethereum.org/en`, `docs.uniswap.org`, `aave.com/docs`, `compound.finance`, `makerdao.com/en`, `solidity-by-example.org`, `chain.link`, OpenZeppelin docs, `bitcoinbook` (canonical Mastering Bitcoin source).
3. **University OCW + free education** — Khan Academy, 3Blue1Brown (Essence of Calculus), Crash Course (Hank Green: Physics, Chemistry, Statistics, Biology, CS, World History, Philosophy), PBS Space Time, Whiteboard Crypto, Finematics.
4. **Wikipedia EN** — last resort for concept articles when no specific authoritative page exists.

Avoided: paywalled freemium consumer-finance sites (Investopedia paid, NerdWallet pro, paywalled WSJ/FT), promotional crypto-trader content, channel-style YouTube URLs (`youtube.com/c/<channel>`), root-domain links, English news links that 403 to bots, tutorialspoint / geeksforgeeks / w3schools (often outdated/inaccurate), generic learning-platform pages.

## Residual notes (out of scope for this pass)

Per the user's earlier direction (no new content, polish only), these were identified but **not addressed**:

- **Card length.** Many backs in `investing_basics_wealth_building`, `mental_health_wellbeing_basics`, `ai_literacy_essentials`, `web3_*`, `general_culture_history_civics`, `general_culture_philosophy_thinking`, and the STEM decks (algebra, calculus, probability) exceed the playbook's ≤2-sentence / ≤30-word recipe. STEM decks consistently include a "Why does this matter?" framing paragraph that pushes backs to 60–100 words. Substantive content; rewriting would change pedagogy. Flagged for a future content polish pass.
- **Note title casing in technical decks.** Web3, AI, and CS50 decks use Title-Case headings (`"Understanding EVM Gas Mechanics and Why Storage is Expensive"`, `"How Machine Learning Works: From Data to Predictions"`) that breach the lowercase preference in the recipe. Same residual as the FR audit. Per playbook's "out of scope" rule for technical decks, not auto-rewritten.
- **Title canonical-pattern drift across decks.** Each group has 2–3 different naming styles (`"X Basics"` / `"X & Y Basics"` / `"X: subtitle"`). Renaming risks breaking external references (user state); flagged for product call.
- **Cross-deck duplicate YouTube IDs** (e.g., `5MuIMqhT8DM`, `lXfEGSYqB9I` shared between body and nutrition decks). Allowed by playbook (intra-deck uniqueness only).
- **A few legacy YouTube IDs** in `practical_cybersecurity_foundations` remain 200-but-marginal (e.g., `oVA0fNwGqB0`, `eFwtPujBbKM`, `QZ7a1Qy6Qn0`). They returned 200 to oEmbed verification and were left in non-duplicate positions.
- **Some canonical project English docs retained** in `web3_*` decks (`ethereum.org`, `uniswap.org`, `aave.com/docs`, `compound.finance`, `makerdao.com`, `chain.link`, OpenZeppelin) — they are the authoritative project documentation; these are the right authority for their subject.

## Reproducibility

The validation script in `EDITORIAL_PLAYBOOK.md` "Validation gate" reproduces these results. The HTTP audit is reproducible via:

```bash
python3 -c "
import json
decks=json.load(open('rappelia/sample_decks.json'))
cols=json.load(open('rappelia/collections.json'))
en={c['id'] for c in cols if c.get('language')=='en' and c.get('isActive',True)}
en_decks={s for c in cols for s in c['stableDeckIds'] if c['id'] in en}
seen=set()
for d in decks:
    if d['stableId'] not in en_decks: continue
    for i in d['sampleIdeas']:
        for k in ('videoURL','externalLinkURL'):
            v=i.get(k)
            if v and v not in seen:
                seen.add(v); print(v)
" | xargs -I{} curl -sIL -o /dev/null -w "%{http_code} {}\n" -m 8 -A "Mozilla/5.0" "{}"
```

A non-200 result (excluding the 7 known `consumerfinance.gov` bot-walls) triggers the playbook's "Link audit gate" replacement workflow.

## Commits on `main`

```
425d497 Editorial review (EN): cs50 + developer_foundations (8 decks) + final fixes
cb86dea Editorial review (EN): stem_foundations (7 decks)
3e9b82b Editorial review (EN): web3_blockchain (3 decks)
e90959d Editorial review (EN): general_culture (3 decks)
5773f84 Editorial review (EN): digital_literacy (3 decks)
c138889 Editorial review (EN): scientific_literacy (3 decks)
1182869 Editorial review (EN): health_essentials (3 decks)
6103d75 Editorial review (EN): financial_literacy (3 decks)
```

Not yet pushed — awaiting explicit user `push to main`.
