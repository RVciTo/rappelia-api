# Editorial Playbook — Rappelia content review

How to review and polish a collection (group) and its decks. Run this for every group, every deck. The README owns the **schema** contract; this file owns the **editorial** contract.

> **Working unit.** One group at a time. Inside a group: one deck at a time. Inside a deck: surgical edits, validated before moving on. Never batch across decks — diffs become unreviewable.

---

## Phase 0 — Pick the group

```bash
python3 -c "
import json
cols = json.load(open('rappelia/collections.json'))
for i,c in enumerate(cols):
    print(i, '|', c.get('language','-'), '|', c['id'], '|', c['name'], '|', len(c['stableDeckIds']),'decks','|', 'active' if c.get('isActive',True) else 'INACTIVE')
"
```

Pick by language (FR or EN) and intent. Inactive collections are skipped.

---

## Phase 1 — Group-level review (collection tile)

Dump the collection + every deck's header in display order:

```bash
python3 - <<'PY'
import json
cols = json.load(open('rappelia/collections.json'))
decks = {d['stableId']: d for d in json.load(open('rappelia/sample_decks.json'))}
c = next(x for x in cols if x['id']=='<COLLECTION_ID>')
print('=== COLLECTION ===')
for k in ('id','name','description','iconName','colorName','language','isActive'):
    print(f'{k}: {c.get(k)}')
print('\n=== DECKS IN ORDER ===')
for sid in c['stableDeckIds']:
    d = decks.get(sid)
    if not d: print(f'!!! MISSING: {sid}'); continue
    print(f'- {sid}')
    print(f'  name: {d["name"]}')
    print(f'  desc: {d["description"]}')
    print(f'  cat/diff/lang/color: {d["category"]} / {d["difficulty"]} / {d["language"]} / {d["color"]}')
    print(f'  cards: {len(d["cards"])} | ideas: {len(d["sampleIdeas"])} | tags: {d["tags"]}')
    print(f'  active: {d.get("isActive", True)}\n')
PY
```

### Checklist (group)

- **Tile name** — ≤4 words, names a destination (not a topic).
- **Tile description** — ≤12 words, **starts with a verb**, sells the outcome (not "this is a collection of…"). Voice: plain language, second person, present tense.
- **`iconName`** — SF Symbol that exists on iOS 17+.
- **`colorName`** — from the 12-color allowed list (lowercase).
- **Language consistency** — every deck's `language` must match the collection's `language` (or a documented cross-language exception). **High-priority bug if mismatched** — French users won't see EN-tagged decks in an FR collection (the Explore tab filters by user locale).
- **Deck order** — first deck = the one a new user should tap. Pattern: foundational/method → topic decks → final/capstone deck. Never alphabetical.
- **Naming pattern** — every deck title should follow one canonical formula (e.g. `Bac <Matière>: <angle> (Terminale)`). Drift across decks is the most common issue.
- **Card-count outliers** — flag decks far below the group's median (peer median ± 30%); usually means thin content or notes that should have been cards.
- **≥3 decks** before publishing a collection.
- **Tag consistency** across decks (audience + topic + use-case taxonomy).
- **Color collisions** — at most one deck per color when possible (helps Explore visual scanning).

### Output (group)

A tight written review with: tile-copy verdict, language bugs, naming inconsistencies, order proposal, outliers, then a **surgical-edit queue** (one bullet per change, smallest first). Apply group edits before zooming into decks; revalidate after each.

---

## Phase 2 — Deck-by-deck review

Pull the full deck:

```bash
python3 - <<'PY'
import json
d = next(x for x in json.load(open('rappelia/sample_decks.json')) if x['stableId']=='<STABLE_ID>')
print('NAME:', d['name'])
print('DESC:', d['description'])
print('CAT/DIFF/LANG/COLOR:', d['category'],'/',d['difficulty'],'/',d['language'],'/',d['color'])
print('TAGS:', d['tags'])
print('CARDS:', len(d['cards']),'| IDEAS:', len(d['sampleIdeas']))
print('\n=== CARDS ===')
for i,c in enumerate(d['cards']):
    print(f'[{i}] Q: {c["front"]}')
    print(f'    A: {c["back"]}')
    print(f'    H: {c["hint"]}')
print('\n=== IDEAS ===')
for i,idea in enumerate(d['sampleIdeas']):
    print(f'[{i}] {idea["name"]}')
    print(f'    linked: {idea.get("linkedCardIndices","MISSING!")}')
    print(f'    video:  {idea.get("videoURL")}')
    print(f'    link:   {idea.get("externalLinkURL")}')
    print(f'    text:   {idea.get("textDescription","")[:300]}...\n')
PY
```

### Checklist (deck — structural, do first)

These are non-negotiable. Fix before any copy work.

- **`linkedCardIndices` present and non-empty on every note.** Empty arrays / missing fields = notes never surface contextually. Map each note to 4–12 cards.
- **No URLs in `front`/`back`/`hint`.** Move to a note's `externalLinkURL` or `videoURL`.
- **Every `linkedCardIndices` entry is `< len(cards)`.** Out-of-range = silent crash on render.
- **`difficulty` matches `language`.** EN → `Beginner`/`Intermediate`/`Advanced`. FR → `Débutant`/`Intermédiaire`/`Avancé`.
- **Title follows the group's canonical naming formula.**

### Checklist (deck — card recipe)

- **Front** — a question or imperative ("Conjugate…", "Cite trois…"). Ends in `?` or starts with a verb. Never a statement.
- **Back** — ≤2 sentences, ≤30 words, self-contained (readable without the front).
- **Hint** — a category or cue, ≤60 chars. Never a partial answer ("Lyrique/tragique/comique" leaks the answer; "Quatre tonalités fréquentes" nudges).
- **No meta in the question** — drop "(rappel utile)", "(grammaire)", "(important)", etc.
- **No trailing ellipsis ("…")** in backs unless genuinely truncating.
- **One concept per card.** If the front contains "et", consider splitting.

### Checklist (deck — note recipe)

- **Each note does one of three jobs**: framing (set up *why* a cluster matters), pattern (rule that several cards instantiate), or pitfall (common mistake / false-friend).
- **3–7 notes per deck** (schema allows 0–11; sweet spot is 5–8).
- **Each note links 4–12 cards.** <4 → it's a card. >12 → split.
- **Body structure**: takeaway in paragraph 1, example/application in paragraph 2, optional method/training step. Don't bury the lede.
- **Title** — no ALL-CAPS shouting, no `>` operators, no abbreviations. French typography: `:` with thin space, `« »` for inner quotes.
- **Body** — same. Use lowercase for emphasis; if you must emphasize, wrap in « ». Voice: `tu` consistently (not `vous` mixed in).
- **Inner double quotes inside JSON strings must be escaped (`\"…\"`).**

### Checklist (deck — link audit, FR groups)

Every note has `videoURL` and `externalLinkURL`. For FR decks, **all links must be in French, work (HTTP 200), and prefer official/educational sources**.

Source preference, top to bottom:
1. **Official government / Ministry**: `eduscol.education.fr`, `education.gouv.fr`
2. **Public broadcaster education**: `lumni.fr` (France Télévisions × Ministère de l'Éducation), `reseau-canope.fr` (only public pages, not the auth-walled `lesfondamentaux.*`)
3. **Public school textbooks**: `lelivrescolaire.fr`
4. **Free, no-login education**: `assistancescolaire.com`
5. **Wikipédia FR** as last resort
6. **Avoid**: paywalled / freemium services (`lesbonsprofs.com`, `schoolmouv.fr`, `kartable.fr` premium tiers), TikTok, blog posts, anything that redirects to a CAS/login page.

Rules:
- No two notes in the same deck share the same `externalLinkURL`. If two notes need the same resource, pick a more specific page for one of them.
- YouTube videos: verify FR + on-topic + level-appropriate (a Collège video for a Terminale deck is a level mismatch worth flagging).
- PDFs are acceptable from official `.education.fr` sources but prefer HTML when available.

### Output (deck)

Same structure as group: written review → surgical-edit queue, smallest first. Order matters:

1. **Structural** (links, URL-in-back, missing fields) — pure data, no debate.
2. **Card recipe nits** (hints leaking answers, meta parentheticals, phrasing).
3. **Note titles** (caps, typography).
4. **Note bodies** (caps, `vous`/`tu` consistency, typos, French typography).
5. **Link audit** (verify HTTP, language, source quality, replace paywalled / 404 / off-topic links).

Coverage gaps (missing topics) → flag but don't auto-add. Decide with the user.

---

## Phase 3 — Apply edits

- **Surgical edits only.** Use `Edit` with exact `old_string`/`new_string`. Never rewrite a whole note or card from scratch — diff stays reviewable.
- **One edit, then revalidate.** When in doubt, validate after each.
- **Inner quotes**: when adding text containing `"…"` inside a JSON string, escape as `\"…\"` or use French guillemets `« »`.
- **Don't reorder cards.** Reordering invalidates every `linkedCardIndices` array referencing that deck.
- **Don't rename `stableId`.** Ever. Soft-delete + add new instead.

### Validation gate (run after every batch)

```bash
python3 -m json.tool rappelia/sample_decks.json > /dev/null
python3 -m json.tool rappelia/collections.json > /dev/null
python3 - <<'PY'
import json
decks = json.load(open('rappelia/sample_decks.json'))
cols  = json.load(open('rappelia/collections.json'))
deck_by_id = {d['stableId']: d for d in decks}
errors = []
for d in decks:
    n = len(d['cards'])
    if n < 5: errors.append(f'{d["stableId"]}: only {n} cards')
    for j, idea in enumerate(d['sampleIdeas']):
        links = idea.get('linkedCardIndices')
        if links is None:
            errors.append(f'{d["stableId"]} idea[{j}]: missing linkedCardIndices')
            continue
        for k in links:
            if not isinstance(k,int) or k < 0 or k >= n:
                errors.append(f'{d["stableId"]} idea[{j}]: linked {k} out of range')
for c in cols:
    for sid in c['stableDeckIds']:
        if sid not in deck_by_id:
            errors.append(f'{c["id"]}: unknown stableDeckId {sid}')
        elif c.get('language') and deck_by_id[sid]['language'] != c['language'] and c.get('isActive', True):
            errors.append(f'{c["id"]}: deck {sid} language {deck_by_id[sid]["language"]} != collection {c["language"]}')
print('\n'.join(errors) if errors else 'OK')
PY
```

### Link audit gate (FR decks)

```bash
python3 -c "
import json
d = next(x for x in json.load(open('rappelia/sample_decks.json')) if x['stableId']=='<STABLE_ID>')
for i in d['sampleIdeas']:
    print(i['videoURL']); print(i['externalLinkURL'])
" | sort -u | while read u; do
  [ -z "$u" ] && continue
  code=$(curl -sIL -o /dev/null -w "%{http_code}" -A "Mozilla/5.0" "$u")
  echo "$code  $u"
done
```

Anything not `200` = broken. Anything redirecting to a login page = replace.

---

## Phase 4 — Commit

One coherent commit per logical batch (e.g. "fix language bug + reorder bac_terminale_fr deck order", "polish bac_francais_outils_reperes cards + notes", "audit links bac_francais_outils_reperes"). Imperative mood, mention the affected `stableId`(s) and collection id.

```bash
git add rappelia/sample_decks.json rappelia/collections.json
git commit -m "<scope>: <change>"
```

Do **not** push speculative content — `main` is what users see within 7 days.

---

## Anti-patterns (we have hit these)

- **`linkedCardIndices: []` on every note** — common bulk-import oversight. Always check first.
- **URL in card `back`** ("Réf : https://…"). Move to `externalLinkURL`.
- **ALL-CAPS-as-emphasis in note titles and bodies** — renders as shouting in the app since the client shows raw strings (no Markdown). Use lowercase or « ».
- **Mixing `tu` and `vous`** in the same note. Pick one (`tu` for Rappelia tone) and apply it consistently.
- **Cross-language deck inside a same-language collection** — invisible to users due to locale filter.
- **Two notes in the same deck pointing to the same `externalLinkURL`** — wasted resource slot.
- **Auth-walled / paywalled "educational" links** — verify with curl; a `302` to a login URL means replace.
- **PowerPoint or PPTX externalLinkURL** — bad UX on mobile, prefer HTML.
- **Unescaped inner `"..."` inside a JSON string** — breaks parse. Escape (`\"…\"`) or use guillemets.

---

## Done-criteria for a deck

- [ ] All notes have non-empty `linkedCardIndices`, every index `< cards.count`.
- [ ] No URLs in `front`/`back`/`hint`.
- [ ] Title follows the group's canonical naming formula.
- [ ] Cards pass the recipe checklist (no answer-leaking hints, no meta, ≤2-sentence backs).
- [ ] Notes pass the recipe checklist (no caps, consistent voice, French typography).
- [ ] Every link returns HTTP 200, is in the deck's language, and prefers official/educational sources.
- [ ] No duplicate `externalLinkURL` within the deck.
- [ ] `python3 -m json.tool` parses both files.
- [ ] Validation script prints `OK`.

## Done-criteria for a group

- [ ] Tile copy is verb-led, ≤12 words.
- [ ] Every member deck's `language` matches the collection's `language`.
- [ ] Deck order goes foundational → topic → capstone (not alphabetical).
- [ ] Naming formula is consistent across all member decks.
- [ ] Every member deck has individually passed its done-criteria above.
