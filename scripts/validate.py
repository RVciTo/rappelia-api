#!/usr/bin/env python3
"""Validate the Rappelia deck and collection files (syntax, schema, references).

Usage: python3 scripts/validate.py [decks.json collections.json]
Defaults to rappelia/sample_decks.json and rappelia/collections.json, resolved
from the repo root. Exits 0 on success, 1 on any error.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_DECK = {'stableId', 'name', 'description', 'color', 'category', 'language',
                 'difficulty', 'tags', 'cards', 'sampleIdeas'}
# `hint` is optional: the app's SampleCard model treats it as optional.
REQUIRED_CARD = {'front', 'back'}
REQUIRED_IDEA = {'name', 'textDescription', 'linkedCardIndices'}
ALLOWED_LANG = {'en', 'fr'}
ALLOWED_DIFF = {'Beginner', 'Intermediate', 'Advanced', 'Débutant', 'Intermédiaire', 'Avancé'}
ALLOWED_COLOR = {'blue', 'green', 'orange', 'pink', 'purple', 'red', 'yellow', 'indigo',
                 'teal', 'mint', 'cyan', 'brown'}


def load(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        print(f'{path}: cannot load JSON: {e}')
        sys.exit(1)


def main(argv):
    decks_path = Path(argv[1]) if len(argv) > 2 else ROOT / 'rappelia' / 'sample_decks.json'
    cols_path = Path(argv[2]) if len(argv) > 2 else ROOT / 'rappelia' / 'collections.json'
    decks = load(decks_path)
    cols = load(cols_path)
    errors = []
    ids = set()
    for i, d in enumerate(decks):
        miss = REQUIRED_DECK - d.keys()
        if miss:
            errors.append(f'deck[{i}] {d.get("stableId", "?")}: missing {miss}')
        sid = d.get('stableId', '')
        if sid in ids:
            errors.append(f'duplicate stableId: {sid}')
        ids.add(sid)
        if d.get('language') not in ALLOWED_LANG:
            errors.append(f'{sid}: bad language {d.get("language")}')
        if d.get('difficulty') not in ALLOWED_DIFF:
            errors.append(f'{sid}: bad difficulty {d.get("difficulty")}')
        if d.get('color') not in ALLOWED_COLOR:
            errors.append(f'{sid}: bad color {d.get("color")}')
        n = len(d.get('cards', []))
        if n < 5:
            errors.append(f'{sid}: only {n} cards (min 5)')
        for j, c in enumerate(d.get('cards', [])):
            if REQUIRED_CARD - c.keys():
                errors.append(f'{sid} card[{j}]: missing {REQUIRED_CARD - c.keys()}')
            if 'hint' in c and not isinstance(c['hint'], str):
                errors.append(f'{sid} card[{j}]: hint must be a string')
        for j, s in enumerate(d.get('sampleIdeas', [])):
            if REQUIRED_IDEA - s.keys():
                errors.append(f'{sid} idea[{j}]: missing {REQUIRED_IDEA - s.keys()}')
            for k in s.get('linkedCardIndices', []):
                if not isinstance(k, int) or k < 0 or k >= n:
                    errors.append(f'{sid} idea[{j}]: linkedCardIndices {k} out of range (0..{n - 1})')

    all_deck_ids = {d.get('stableId') for d in decks}
    col_ids = set()
    for c in cols:
        if c['id'] in col_ids:
            errors.append(f'duplicate collection id: {c["id"]}')
        col_ids.add(c['id'])
        for sid in c.get('stableDeckIds', []):
            if sid not in all_deck_ids:
                errors.append(f'collection {c["id"]}: unknown stableDeckId {sid}')

    if errors:
        print('\n'.join(errors))
        return 1
    print(f'OK: {len(decks)} decks, {sum(len(d["cards"]) for d in decks)} cards, {len(cols)} collections')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
