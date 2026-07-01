# Custom note types — field reference

All three types are created automatically by `python anki.py ensure-models` (idempotent). The `Source` field renders small and gray at the bottom of every card; appearing on both front and back is intentional — it acts as a context cue while recalling the answer (per Wozniak Rule 16), not as a hint.

## `Basic (Source)`

Fields: `Front`, `Back`, `Source`

## `Cloze (Source)`

Fields: `Text`, `Back Extra`, `Source`

Set `"isCloze": true`. Note the `{{#Back Extra}}...{{/Back Extra}}` conditional so the back stays clean when `Back Extra` is empty.

## `Cloze (Source + Resource)`

Fields: `Text`, `Back Extra`, `Source`, `Resource Label` (display text), `Resource` (URL)

The `Resource Label` and `Resource` fields render as a clickable link (`🎥 label`) below Source on the card back. The link is gated on `{{#Resource Label}}`, so leaving both fields empty keeps the card identical to `Cloze (Source)`.

---

## `add-notes` payload format

Write a JSON array of note objects to `/tmp/anki_notes.json`, then run `python anki.py add-notes /tmp/anki_notes.json`.

**Cloze (Source):**

```json
[
  {
    "deckName": "Mathematics",
    "modelName": "Cloze (Source)",
    "fields": {
      "Text": "A proposition is a statement that is {{c1::true or false}}, but not both.",
      "Back Extra": "",
      "Source": "TW1-11 · Proof Techniques, Lecture 1 · Propositional Logic"
    },
    "tags": ["TW1-11::L1", "definitions"]
  }
]
```

**Cloze (Source + Resource):**

```json
[
  {
    "deckName": "Mathematics",
    "modelName": "Cloze (Source + Resource)",
    "fields": {
      "Text": "The implication p → q is false if and only if p is {{c1::true}} and q is {{c2::false}}.",
      "Back Extra": "",
      "Source": "TW1-11 · Proof Techniques, Lecture 1 · Propositional Logic",
      "Resource Label": "CrashCourse: Logic & Reasoning #5",
      "Resource": "https://www.youtube.com/watch?v=abc123"
    },
    "tags": ["TW1-11::L1", "implication"]
  }
]
```

`add-notes` returns a non-zero exit code and reports which notes were skipped if any were duplicates or invalid.
