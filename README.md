# rappelia-api

Static JSON content repo for the **Rappelia** iOS app's public deck library.
This repo is **not a server**: there is no backend, no auth, no build step.
The app fetches two raw JSON files over HTTPS and caches them for 7 days.

## Status

| Owner | Stack | Version | Stage | Live | Last commit | Branch |
|---|---|---|---|---|---|---|
| Heva Pulse (Pitsana), backs the Rappelia iOS app | Static JSON, served via raw.githubusercontent.com | n/a (content repo) | Production | Yes, served live to the app via raw.githubusercontent.com | 2026-06-07 | main |

### Production readiness: 90%

Assessed 2026-09-14.

| Stage | Weight | Score | State |
|---|---|---|---|
| Spec and feasibility | 5 | 5 | Schema, editorial playbook and content rules are exhaustively documented. |
| Scaffold | 10 | 10 | Simple, complete structure: two JSON files, a validation script. |
| Working prototype | 15 | 15 | Files parse and serve correctly to the live app today. |
| First real use | 10 | 10 | Actively fetched by the published Rappelia iOS app. |
| MVP complete | 15 | 15 | Content pipeline (add deck, add collection, soft-delete) is complete and in daily use. |
| Validated by users | 10 | 10 | Real app users pull this data on every 7-day refresh cycle. |
| Hardening | 20 | 10 | CI runs `scripts/validate.py` on push and pull request; no further automated tests. |
| Production | 15 | 15 | Live in production, serving the shipped app via raw.githubusercontent.com. |

### Left to finish

1. Make the `validate` check required on `main` (repo setting).
2. Resolve the `editorial/fr-content-review-2026-04` and `claude/add-premium-onboarding-tVSXq` remote branches (merge or drop).
3. Create the first `content-*` tag after merge (see section 1.1).

> If you change anything here, the JSON you commit **is** what users get on
> their next refresh. There is no review pipeline. Read this whole README
> before opening a PR.

---

## 1. What the app fetches

The Rappelia iOS app pulls these two URLs (overridable via Firebase Remote
Config keys `remote_decks_url` / `remote_collections_url`, defaults below):

| Purpose      | URL                                                                                                  |
| ------------ | ---------------------------------------------------------------------------------------------------- |
| Decks        | `https://raw.githubusercontent.com/RVciTo/rappelia-api/main/rappelia/sample_decks.json`              |
| Collections  | `https://raw.githubusercontent.com/RVciTo/rappelia-api/main/rappelia/collections.json`               |

This repo is content versioning only: there is no site and no custom domain.
**All live traffic goes through `raw.githubusercontent.com`**. Do not move files around without updating the
defaults in `Rappelia/Services/RemoteConfigService.swift`.

**Cache:** clients keep a 7-day local cache. Edits propagate within 7 days, or
immediately for users who tap "Force refresh" in the debug menu. Plan rollouts
accordingly — never depend on instant propagation.

### 1.1 Rollback to a tagged release

Content releases are tagged `content-YYYY-MM-DD` (for example
`content-2026-10-09`). The first tag to create after this change merges is
`content-2026-10-09`, on the merge commit.

To roll back, point the Firebase Remote Config key `remote_decks_url` (and
`remote_collections_url`) at the tag instead of `main`, by replacing `main` in
the path with the tag name:

```
https://raw.githubusercontent.com/RVciTo/rappelia-api/content-2026-10-09/rappelia/sample_decks.json
https://raw.githubusercontent.com/RVciTo/rappelia-api/content-2026-10-09/rappelia/collections.json
```

Publish the Remote Config change; clients pick it up on their next refresh
(up to 7 days, see the cache note above). Clear the two keys to return to the
`main` defaults.

---

## 2. Repository layout

```
rappelia-api/
├── scripts/validate.py          # deck validator (run by CI)
├── .github/workflows/validate.yml
├── README.md                    # this file
└── rappelia/
    ├── sample_decks.json        # array of decks (the catalog)
    └── collections.json         # array of collections (groupings)
```

Both files are **single JSON arrays**, UTF-8, no BOM, no trailing commas, no
comments. The app uses Swift's `JSONDecoder` with strict parsing — any
malformed file breaks the Explore tab for every user until reverted.

---

## 3. `sample_decks.json` — deck schema

Top-level: `[Deck, Deck, ...]`. Each deck object:

| Field          | Type       | Required | Notes                                                                                                  |
| -------------- | ---------- | :------: | ------------------------------------------------------------------------------------------------------ |
| `stableId`     | `string`   |    ✅    | **Permanent identity.** snake_case, ASCII, unique across the entire file. Never rename — it's the join key with collections and the dedupe key on import. |
| `name`         | `string`   |    ✅    | User-facing title. Localize to the deck's `language`.                                                  |
| `description`  | `string`   |    ✅    | One or two sentences. User-facing.                                                                     |
| `color`        | `string`   |    ✅    | One of: `blue`, `green`, `orange`, `pink`, `purple`, `red`, `yellow` (also accepted client-side: `indigo`, `teal`, `mint`, `cyan`, `brown`). Lowercase. |
| `category`     | `string`   |    ✅    | Stable English key. Existing values: `Driving`, `Economics`, `General Culture`, `Geography`, `Health`, `History`, `Language`, `Mathematics`, `Philosophy`, `Science`, `Technology`. **Reuse an existing one** unless absolutely necessary. The app translates these at display time. |
| `language`     | `string`   |    ✅    | ISO-639-1: `en` or `fr` only.                                                                          |
| `difficulty`   | `string`   |    ✅    | One of: `Beginner`, `Intermediate`, `Advanced` for `en` decks; `Débutant`, `Intermédiaire`, `Avancé` for `fr` decks. Match the deck language. |
| `tags`         | `[string]` |    ✅    | 3–6 lowercase ASCII tags. Used for search/filter.                                                      |
| `cards`        | `[Card]`   |    ✅    | 15–55 cards is the working range. Hard floor: 5. Order matters — `linkedCardIndices` references it.    |
| `sampleIdeas`  | `[Idea]`   |    ✅    | 0–11 study notes. May be `[]` but **the field must exist**.                                            |
| `isActive`     | `bool`     |    ❌    | Optional, default `true`. Set `false` to **soft-delete** a deck without removing its data.             |

**Fields the schema does NOT define (do not add):** `id`, `version`, `affiliateURL`, anything else. The client generates `id` at decode time.

### 3.1 `Card` object

```json
{ "front": "…", "back": "…", "hint": "…" }
```

| Field   | Type     | Required | Notes                                                              |
| ------- | -------- | :------: | ------------------------------------------------------------------ |
| `front` | `string` |    ✅    | Question/prompt. One idea per card. Avoid lists — split them up.   |
| `back`  | `string` |    ✅    | Answer. Self-contained — readable without seeing the front.        |
| `hint`  | `string` |    optional    | Short nudge (≤ ~60 chars). May be omitted (the app treats it as optional), but prefer to write one. |

No HTML, no Markdown rendering — text is shown as-is. Use straight punctuation, but curly quotes (`'` `"`) are acceptable and preserved.

### 3.2 `Idea` object (study note)

```json
{
  "name": "…",
  "textDescription": "…",
  "videoURL": null,
  "externalLinkURL": null,
  "linkedCardIndices": [0, 3, 7]
}
```

| Field               | Type            | Required | Notes                                                                                           |
| ------------------- | --------------- | :------: | ----------------------------------------------------------------------------------------------- |
| `name`              | `string`        |    ✅    | Title of the note.                                                                              |
| `textDescription`   | `string`        |    ✅    | 2–4 paragraphs, separated by `\n\n`. The teaching context for the linked cards.                 |
| `videoURL`          | `string \| null`|    ❌    | Full `https://` URL or `null`. Omit the key or use `null` if absent.                            |
| `externalLinkURL`   | `string \| null`|    ❌    | Full `https://` URL or `null`.                                                                  |
| `linkedCardIndices` | `[int]`         |    ✅    | Zero-based indices into this deck's `cards` array. Every index **must be `< cards.count`**. May be `[]`. |

`linkedCardIndices` is the most error-prone field. If you reorder, insert, or delete cards, **re-verify every `linkedCardIndices` array in that deck**. Out-of-range indices crash silently (the link just doesn't render) and waste the note.

---

## 4. `collections.json` — collection schema

Top-level: `[Collection, Collection, ...]`. A collection groups deck `stableId`s into a tile shown on the Explore tab.

| Field           | Type       | Required | Notes                                                                                |
| --------------- | ---------- | :------: | ------------------------------------------------------------------------------------ |
| `id`            | `string`   |    ✅    | snake_case, unique across `collections.json`. Suffix with `_en` / `_fr` if language-scoped. |
| `name`          | `string`   |    ✅    | User-facing tile title, in the collection's language.                                |
| `description`   | `string`   |    ✅    | One sentence shown on the tile.                                                      |
| `iconName`      | `string`   |    ✅    | SF Symbol name (e.g. `graduationcap.fill`, `flask.fill`, `globe`). Must exist on iOS 17+. |
| `colorName`     | `string`   |    ✅    | One of: `blue`, `green`, `orange`, `indigo`, `purple`, `red`, `pink`, `yellow`, `teal`, `mint`, `cyan`, `brown`. Lowercase. |
| `stableDeckIds` | `[string]` |    ✅    | List of deck `stableId`s. **Every entry must exist in `sample_decks.json`** or the deck is silently skipped. Order is preserved in the UI. |
| `language`      | `string`   |    ❌    | `en`, `fr`, or omit/null for cross-language. The Explore tab filters by user locale. |
| `isActive`      | `bool`     |    ❌    | Default `true`. Soft-delete: hides the tile but keeps the data for already-imported users. |

Collections with **zero active member decks** (after applying `isActive` on both sides) are dropped from the UI automatically — you don't need to deactivate them manually.

---

## 5. How to add a new deck

1. **Pick a `stableId`.** snake_case, ASCII, unique. Convention: `<topic>_<scope>` (e.g. `web3_blockchain_bases`, `cs50_python_sql_web_fr`). Once shipped, it is permanent.
2. **Pick `language`** (`en` or `fr`) and write all user-facing strings (`name`, `description`, every `front`/`back`/`hint`, `sampleIdeas[*]`) in that language.
3. **Reuse an existing `category`.** Only invent a new one if no existing category fits — new categories require a coordinated app update to add a localized display name.
4. **Match `difficulty` to `language`.** EN → `Beginner` / `Intermediate` / `Advanced`. FR → `Débutant` / `Intermédiaire` / `Avancé`.
5. **Write 15–55 cards.** One concept per card. Self-contained backs. Stable order — never reshuffle a published deck (it changes the meaning of every existing `linkedCardIndices` reference).
6. **Add 3–7 `sampleIdeas`.** Each note groups 4–12 related card indices. Verify every index is `< cards.count`.
7. **Append the deck object to the END of the `sample_decks.json` array.** Order doesn't matter functionally, but appending keeps diffs reviewable.
8. **If the deck belongs in a collection**, add its `stableId` to the corresponding collection's `stableDeckIds` in `collections.json`. To launch a new collection, see §6.
9. **Validate** (§7), commit, push.

### 5.1 Minimal valid deck (template)

```json
{
  "stableId": "example_topic_basics",
  "name": "Example Topic: Basics",
  "description": "Short user-facing description of what's inside.",
  "color": "blue",
  "category": "Science",
  "language": "en",
  "difficulty": "Beginner",
  "tags": ["example", "basics"],
  "cards": [
    { "front": "Question 1?", "back": "Answer 1.", "hint": "Short nudge." },
    { "front": "Question 2?", "back": "Answer 2.", "hint": "Short nudge." }
  ],
  "sampleIdeas": [
    {
      "name": "Why this matters",
      "textDescription": "Paragraph 1 explaining the framing.\n\nParagraph 2 with the practical takeaway.",
      "videoURL": null,
      "externalLinkURL": null,
      "linkedCardIndices": [0, 1]
    }
  ]
}
```

---

## 6. How to add a new collection (group of decks)

1. **All member decks must already exist** in `sample_decks.json`. Add the decks first, in a separate commit if helpful.
2. **Pick a unique `id`** in `collections.json`. snake_case. Suffix `_en` / `_fr` if the collection is language-scoped (most are).
3. **Pick an SF Symbol** for `iconName` that exists on iOS 17+. Test in Xcode's SF Symbols app if unsure.
4. **Pick `colorName`** from the allowed list (§4).
5. **List `stableDeckIds`** in display order. Every id must exist exactly as spelled in `sample_decks.json`.
6. **Set `language`** to match the member decks' language, or omit for cross-language collections.
7. Append to the end of the `collections.json` array. Validate, commit, push.

---

## 7. Validation before commit

CI runs the same check on every push and pull request. Run it locally first:

```bash
python3 scripts/validate.py
```

A passing run prints a single `OK:` line. Any other output blocks the commit.

---

## 8. Editing existing decks (the careful path)

| What you want to do                          | Allowed?                                                                                                  |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Fix typos in `front` / `back` / `hint`       | ✅ Safe.                                                                                                  |
| Add new cards at the **end**                 | ✅ Safe — existing `linkedCardIndices` stay valid.                                                        |
| Insert a card in the **middle**              | ⚠️ Re-verify and rewrite every `linkedCardIndices` array in that deck.                                    |
| Reorder cards                                | ⚠️ Same as above. Avoid unless you have a reason.                                                         |
| Delete a card                                | ⚠️ Re-verify every `linkedCardIndices` array; users who imported earlier keep the old card.               |
| Rename `stableId`                            | ❌ Never. It's the dedupe key. Use `isActive: false` + add a new deck instead.                            |
| Change `language` of an existing deck        | ❌ Never. Create a new deck with a `_<lang>` suffixed `stableId`.                                         |
| Change `category` to one not already in use  | ⚠️ Requires a coordinated app update. Don't do it without coordinating with the iOS team.                 |
| Soft-delete a deck                           | ✅ Set `isActive: false`. Existing imports are preserved; the deck disappears from Explore.               |
| Hard-delete a deck                           | ❌ Never. Soft-delete instead.                                                                            |

---

## 9. Style rules for content

- **One concept per card.** If you wrote "and", consider splitting.
- **Backs are self-contained.** A user reading only the back should understand the answer without re-reading the front.
- **Hints nudge, never give away.** ≤ ~60 characters.
- **No PII, no copyrighted excerpts, no scraped content.** Original or properly licensed only.
- **No URLs in `front`/`back`/`hint`.** URLs go in `sampleIdeas[*].externalLinkURL` / `videoURL`.
- **No emoji in `stableId`, `id`, `category`, `tags`.** Plain ASCII.
- **No trailing whitespace, no `\r\n`.** LF line endings.
- **UTF-8 only.** Curly quotes are fine.

---

## 10. Commit & push

```bash
git add rappelia/sample_decks.json rappelia/collections.json
git commit -m "Add <deck name> deck (<lang>) to <collection id>"
git push origin main
```

Commit messages: imperative, mention the affected `stableId`(s) and collection ids. One logical change per commit when feasible. The `main` branch is what users see — don't push speculative content.

---

## 11. Quick reference

- **Append-only is safest.** New decks at the end, new cards at the end, new collections at the end.
- **`stableId` is forever.** Choose carefully.
- **`linkedCardIndices` is fragile.** Re-verify on every card-list edit.
- **No review pipeline.** CI only validates structure; rollback is manual (section 1.1). What you push is what users get within 7 days.
- **In doubt, soft-delete (`isActive: false`)** rather than hard-delete.

If a rule here conflicts with reality (a field the app accepts that isn't documented, a category the app rejects, etc.), **fix the README first**, then make the JSON change. The README is the contract.
