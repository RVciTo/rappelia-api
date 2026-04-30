# Editorial audit — French content (2026-04-30)

End-to-end review of every active French collection in `rappelia/sample_decks.json` and `rappelia/collections.json` per the `EDITORIAL_PLAYBOOK.md`. Performed in this session and a parallel set of background agents.

## Scope

| Collection | Decks | Cards | Notes |
|---|---:|---:|---:|
| `bac_terminale_fr` | 11 | 481 | 101 |
| `financial_literacy_fr` | 3 | 118 | 27 |
| `health_essentials_fr` | 3 | 98 | 23 |
| `scientific_literacy_fr` | 3 | 76 | 17 |
| `digital_literacy_fr` | 3 | 64 | 17 |
| `general_culture_fr` | 3 | 93 | 22 |
| `computer_science_cs50_fr` | 5 | 170 | 35 |
| `web3_blockchain_fr` | 3 | 83 | 21 |
| **Total** | **34** | **1 183** | **263** |

Excluded: `code_route_fr` (`isActive: false`).

## Validation results

All 34 decks pass the playbook done-criteria:

- ✅ JSON parses cleanly for both files.
- ✅ Every note has `linkedCardIndices` non-empty, every index `< len(cards)`.
- ✅ No URL or `Réf:` footer in any card `front`/`back`/`hint`.
- ✅ No duplicate `videoURL` or `externalLinkURL` within any deck.
- ✅ Every `videoURL` is a real YouTube `watch?v=` URL (no channel pages, no non-YouTube hosts).
- ✅ Every member deck's `language` matches its collection's `language`.
- ✅ Every collection description is verb-led, ≤14 words.

## HTTP audit

All 478 unique URLs across the 34 FR decks were curl-tested. After fixing the residuals identified, the breakdown is:

- 478 / 478 verified working (`200` direct, or eduscol equivalent for routes that bot-block at HEAD).

Six broken/blocked URLs were replaced during the final pass:

| Original | Replacement |
|---|---|
| `cybermalveillance.gouv.fr/.../bonnes-pratiques/hameconnage-phishing` (404, 2 occurrences) | `cybermalveillance.gouv.fr/.../fiches-reflexes/hameconnage-phishing` |
| `fr.wikipedia.org/wiki/Corrélation_et_causalité` (404, doesn't exist) | `fr.wikipedia.org/wiki/Corrélation_n'implique_pas_causalité` |
| `education.gouv.fr/sites/.../spe243_annexe1_1159172.pdf` (404) | `eduscol.education.fr/729/presentation-du-grand-oral` |
| `education.gouv.fr/bo/20/Special7/MENE2019312N.htm` (403) | `eduscol.education.fr/1726/programmes-et-ressources-en-langues-vivantes-voie-gt` |
| `education.gouv.fr/bo/2025/Hebdo30/MENE2518792N` (403) | `eduscol.education.fr/729/presentation-du-grand-oral` |

## What changed across the 34 decks

### Group-level (collections.json)

- 8 collection descriptions rewritten to verb-led `tu` voice, ≤12 words.
- Naming patterns canonicalized within each group (consistent `: bases` / `— <focus>` suffix).
- 8 sets of deck descriptions rewritten verb-led `tu`.
- Color collisions resolved (`investissement_epargne_bases` blue→purple, climate green→teal, CS50 deck red→teal, Web3 all-purple → purple/indigo/blue).
- `bac_anglais_bases.language` flipped `en`→`fr` (visibility bug — French users couldn't see the deck).
- `bac_terminale_fr.stableDeckIds` reordered (méthode → matières → Grand Oral).
- Tag taxonomy alignment.

### Deck-level (sample_decks.json)

- **263 notes** — `linkedCardIndices` wired (was missing from most). Each note links 4–12 semantically-matched cards.
- **~30 cards** — URLs stripped from `back`, rewritten as plain knowledge cards.
- **~80 videos** replaced — channel-style YouTube URLs (`youtube.com/c/<channel>`), non-YouTube URLs, English-language TED/BBC/Khan-EN.
- **~70 external links** replaced — generic root domains, English/US sources (CDC, NCBI, Harvard, hsph, britannica, worldhistory, climate.nasa, cia.gov), 404s, paywalled / auth-walled targets.
- **~30 typos** fixed — anglicisms (`loneliness`, `Inability`, `Energy`, `EFFET`), missing accents (`recepteurs`, `serieusement`), broken phrasing.

### Source hierarchy used

Replacement priority, top to bottom (per playbook):

1. **Government / Ministry** — `eduscol.education.fr`, `education.gouv.fr`, `service-public.gouv.fr`, `economie.gouv.fr`, `solidarites.gouv.fr`, `cnil.fr`, `cybermalveillance.gouv.fr`, `cyber.gouv.fr`, `francenum.gouv.fr`, `notre-environnement.gouv.fr`, `vie-publique.fr`, `diplomatie.gouv.fr`.
2. **Public-sector education / research** — `inserm.fr`, `presse.inserm.fr`, `ipubli.inserm.fr`, `pasteur.fr`, `cnrs.fr`, `anses.fr`, `ameli.fr`, `mesquestionsdargent.fr`, `banque-france.fr`, `amf-france.org/fr`, `lafinancepourtous.com`, `santepubliquefrance.fr`, `meteofrance.com`, `lumni.fr`, `geoconfluences.ens-lyon.fr`.
3. **Public school textbooks / free educational** — `lelivrescolaire.fr`, `assistancescolaire.com`, `aftcc.org`, `psycom.org`, Khan Academy FR, `developer.mozilla.org/fr`.
4. **Wikipédia FR** — last resort for concept articles when no specific institutional page exists.

Avoided: paywalled freemium services (`schoolmouv.fr`, `lesbonsprofs` premium, `kartable.fr` premium tiers), promotional crypto-trader content, English-only academic PDFs, TED talks (mostly English), BBC educational shorts, US `cdc.gov` / `ncbi.nlm.nih.gov` / `hsph.harvard.edu`.

## Residual notes (out of scope for this pass)

Per the user's earlier direction (no new content, polish only), these were identified but **not addressed**:

- **Card length**: many backs in `health_essentials_fr` and `web3_blockchain_fr` exceed the playbook's ≤2-sentence / ≤30-word recipe. Substantive content; rewriting would change pedagogy. Flagged for a future content polish pass.
- **Note titles in Web3**: ~21 use Title-Case headings (`"Comprendre la Mécanique du Gaz EVM…"`) that breach the lowercase preference in the recipe. Not auto-fixed.
- **Franglais in `litteratie_ia` / `climat`**: phrases like "stranded assets", "AGI", "engagement" persist. Not auto-rewritten.
- **A few canonical project English docs retained** in `web3_*` decks (`solidity-by-example.org`, `compound.finance`, `chain.link`, `uniswap.org`, `makerdao.com`) — they are the authoritative project documentation; no FR equivalent exists. Flagged for user judgment.
- **EN collections** (financial_literacy_en, health_essentials_en, scientific_literacy_en, digital_literacy_en, stem_foundations_en, general_culture_en, computer_science_cs50_en, web3_blockchain_en, developer_foundations_en) — explicitly deferred to a separate session.

## Reproducibility

The validation script in `EDITORIAL_PLAYBOOK.md` "Validation gate" section reproduces these results. The HTTP audit is reproducible via:

```bash
python3 -c "
import json
decks=json.load(open('rappelia/sample_decks.json'))
cols=json.load(open('rappelia/collections.json'))
fr={c['id'] for c in cols if c.get('language')=='fr' and c.get('isActive',True)}
fr_decks={s for c in cols for s in c['stableDeckIds'] if c['id'] in fr}
seen=set()
for d in decks:
    if d['stableId'] not in fr_decks: continue
    for i in d['sampleIdeas']:
        for k in ('videoURL','externalLinkURL'):
            v=i.get(k);
            if v and v not in seen:
                seen.add(v); print(v)
" | xargs -I{} curl -sIL -o /dev/null -w "%{http_code} {}\n" -m 8 -A "Mozilla/5.0" "{}"
```

A non-200 result triggers the playbook's "Link audit gate" replacement workflow.
