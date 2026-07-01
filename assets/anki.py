#!/usr/bin/env python3
"""AnkiConnect CLI helper for the lecture-to-anki skill.

Usage:
  python anki.py version
  python anki.py deck-names
  python anki.py create-deck <name>
  python anki.py model-names
  python anki.py ensure-models
  python anki.py add-notes <notes.json>
  python anki.py find-notes <query>
"""

import json
import sys
import urllib.request
import urllib.error

ANKI_URL = "http://127.0.0.1:8765"

_BASE_CSS = (
    ".card { font-family: arial; font-size: 20px; text-align: center; "
    "color: black; background-color: white; } "
    ".source { font-size: 12px; color: #999; margin-top: 14px; } "
    "hr { margin-top: 14px; }"
)

_RESOURCE_CSS = (
    ".card { font-family: arial; font-size: 20px; text-align: center; "
    "color: black; background-color: white; } "
    ".source { font-size: 12px; color: #999; margin-top: 14px; } "
    ".resource { font-size: 14px; color: #06c; margin-top: 8px; word-break: break-all; } "
    "hr { margin-top: 14px; }"
)

_MODELS = [
    {
        "modelName": "Basic (Source)",
        "inOrderFields": ["Front", "Back", "Source"],
        "isCloze": False,
        "css": _BASE_CSS,
        "cardTemplates": [
            {
                "Name": "Card 1",
                "Front": '{{Front}}\n<div class="source">{{Source}}</div>',
                "Back": "{{FrontSide}}\n<hr id=answer>\n{{Back}}",
            }
        ],
    },
    {
        "modelName": "Cloze (Source)",
        "inOrderFields": ["Text", "Back Extra", "Source"],
        "isCloze": True,
        "css": _BASE_CSS,
        "cardTemplates": [
            {
                "Name": "Cloze",
                "Front": '{{cloze:Text}}\n<div class="source">{{Source}}</div>',
                "Back": (
                    '{{cloze:Text}}\n<div class="source">{{Source}}</div>\n'
                    "{{#Back Extra}}<hr id=answer>{{Back Extra}}{{/Back Extra}}"
                ),
            }
        ],
    },
    {
        "modelName": "Cloze (Source + Resource)",
        "inOrderFields": ["Text", "Back Extra", "Source", "Resource Label", "Resource"],
        "isCloze": True,
        "css": _RESOURCE_CSS,
        "cardTemplates": [
            {
                "Name": "Cloze",
                "Front": '{{cloze:Text}}\n<div class="source">{{Source}}</div>',
                "Back": (
                    '{{cloze:Text}}\n<div class="source">{{Source}}</div>\n'
                    '{{#Resource Label}}<div class="resource">'
                    '<a href="{{Resource}}">🎥 {{Resource Label}}</a>'
                    "</div>{{/Resource Label}}\n"
                    "{{#Back Extra}}<hr id=answer>{{Back Extra}}{{/Back Extra}}"
                ),
            }
        ],
    },
]


def _call(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    try:
        resp = json.loads(
            urllib.request.urlopen(
                urllib.request.Request(ANKI_URL, payload), timeout=10
            ).read()
        )
    except urllib.error.URLError as e:
        sys.exit(f"AnkiConnect unreachable ({e}). Is Anki running with the AnkiConnect add-on?")
    if resp.get("error"):
        sys.exit(f"AnkiConnect error: {resp['error']}")
    return resp["result"]


def cmd_version():
    v = _call("version")
    print(f"AnkiConnect {v} — OK")


def cmd_deck_names():
    for name in sorted(_call("deckNames")):
        print(name)


def cmd_create_deck(name):
    deck_id = _call("createDeck", deck=name)
    print(f"Deck ready: '{name}' (id {deck_id})")


def cmd_model_names():
    for name in sorted(_call("modelNames")):
        print(name)


def cmd_ensure_models():
    existing = set(_call("modelNames"))
    for model in _MODELS:
        name = model["modelName"]
        if name in existing:
            print(f"  exists:  {name}")
        else:
            _call("createModel", **model)
            print(f"  created: {name}")


def cmd_add_notes(path):
    with open(path, encoding="utf-8") as f:
        notes = json.load(f)

    # canAddNotes first: addNotes aborts the whole batch if any note is a duplicate
    can_add = _call("canAddNotes", notes=notes)
    valid = [n for n, ok in zip(notes, can_add) if ok]
    skipped = [n for n, ok in zip(notes, can_add) if not ok]

    if skipped:
        print(f"Skipping {len(skipped)} duplicate/invalid note(s):")
        for note in skipped:
            fields = note.get("fields") or {}
            label = fields.get("Front") or fields.get("Text") or "?"
            print(f"  - {str(label)[:100]}")

    if not valid:
        print("Nothing to add.")
        sys.exit(1)

    ids = _call("addNotes", notes=valid)
    added = sum(1 for nid in ids if nid is not None)
    print(f"Added {added}/{len(notes)} notes.")
    if skipped:
        sys.exit(1)


def cmd_find_notes(query):
    ids = _call("findNotes", query=query)
    if not ids:
        print("No notes found.")
        return
    infos = _call("notesInfo", notes=ids)
    print(f"Found {len(infos)} note(s):")
    for info in infos:
        fields = info.get("fields", {})
        src = (fields.get("Source") or {}).get("value", "")
        fallback = (fields.get("Front") or fields.get("Text") or {}).get("value", "")
        print(f"  [{info['noteId']}] {src or fallback[:80]}")


def _usage():
    print(__doc__.strip())
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if not args:
        _usage()

    cmd = args[0]

    if cmd == "version":
        cmd_version()
    elif cmd == "deck-names":
        cmd_deck_names()
    elif cmd == "create-deck":
        if len(args) < 2:
            sys.exit("create-deck requires a deck name")
        cmd_create_deck(args[1])
    elif cmd == "model-names":
        cmd_model_names()
    elif cmd == "ensure-models":
        cmd_ensure_models()
    elif cmd == "add-notes":
        if len(args) < 2:
            sys.exit("add-notes requires a JSON file path")
        cmd_add_notes(args[1])
    elif cmd == "find-notes":
        if len(args) < 2:
            sys.exit("find-notes requires a query string")
        cmd_find_notes(args[1])
    else:
        print(f"Unknown command: {cmd}")
        _usage()


if __name__ == "__main__":
    main()
