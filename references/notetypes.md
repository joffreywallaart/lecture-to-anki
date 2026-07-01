# Custom note types for AnkiConnect

Both note types carry a dedicated `Source` field that renders small and grey at the bottom of every card. Create them with the `createModel` action only if `modelNames` shows they're missing on the active profile.

Shared CSS (use the same string for both `css` parameters):

```css
.card { font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white; }
.source { font-size: 12px; color: #999; margin-top: 14px; }
hr { margin-top: 14px; }
```

## `Basic (Source)`

`createModel` payload:

```json
{
  "modelName": "Basic (Source)",
  "inOrderFields": ["Front", "Back", "Source"],
  "isCloze": false,
  "css": "<shared CSS above>",
  "cardTemplates": [
    {
      "Name": "Card 1",
      "Front": "{{Front}}\n<div class=\"source\">{{Source}}</div>",
      "Back": "{{FrontSide}}\n<hr id=answer>\n{{Back}}"
    }
  ]
}
```

## `Cloze (Source)`

Set `isCloze: true`. Note the `{{#Back Extra}}...{{/Back Extra}}` conditional so the back stays clean when `Back Extra` is empty.

```json
{
  "modelName": "Cloze (Source)",
  "inOrderFields": ["Text", "Back Extra", "Source"],
  "isCloze": true,
  "css": "<shared CSS above>",
  "cardTemplates": [
    {
      "Name": "Cloze",
      "Front": "{{cloze:Text}}\n<div class=\"source\">{{Source}}</div>",
      "Back": "{{cloze:Text}}\n<div class=\"source\">{{Source}}</div>\n{{#Back Extra}}<hr id=answer>{{Back Extra}}{{/Back Extra}}"
    }
  ]
}
```

## `Cloze (Source + Resource)`

Use for cards where a supplementary video resource was found. Adds a clickable link below the Source field on the card back, with a descriptive label instead of raw URL.

Shared CSS (extend with this addition):

```css
.card { font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white; }
.source { font-size: 12px; color: #999; margin-top: 14px; }
.resource { font-size: 14px; color: #06c; margin-top: 8px; word-break: break-all; }
hr { margin-top: 14px; }
```

`createModel` payload (use the extended CSS above):

```json
{
  "modelName": "Cloze (Source + Resource)",
  "inOrderFields": ["Text", "Back Extra", "Source", "Resource Label", "Resource"],
  "isCloze": true,
  "css": "<extended CSS above>",
  "cardTemplates": [
    {
      "Name": "Cloze",
      "Front": "{{cloze:Text}}\n<div class=\"source\">{{Source}}</div>",
      "Back": "{{cloze:Text}}\n<div class=\"source\">{{Source}}</div>\n{{#Resource Label}}<div class=\"resource\"><a href=\"{{Resource}}\">🎥 {{Resource Label}}</a></div>{{/Resource Label}}\n{{#Back Extra}}<hr id=answer>{{Back Extra}}{{/Back Extra}}"
    }
  ]
}
```

`addNotes` example with resource:

```json
{
  "action": "addNotes",
  "version": 6,
  "params": {
    "notes": [
      {
        "deckName": "Mathematics",
        "modelName": "Cloze (Source + Resource)",
        "fields": {
          "Text": "The implication p → q is false if and only if p is {{c1::true}} and q is {{c2::false}}.",
          "Back Extra": "",
          "Source": "TW1-11 · Proof Techniques, Les 1 · Propositional Logic",
          "Resource Label": "CrashCourse: Logic & Reasoning #5",
          "Resource": "https://www.youtube.com/watch?v=abc123"
        },
        "tags": ["TW1-11::L1", "implication"]
      }
    ]
  }
}
```

## Example `addNotes` call

```json
{
  "action": "addNotes",
  "version": 6,
  "params": {
    "notes": [
      {
        "deckName": "Mathematics",
        "modelName": "Cloze (Source)",
        "fields": {
          "Text": "A proposition is a statement that is {{c1::true or false}}, but not both.",
          "Back Extra": "",
          "Source": "TW1-11 · Proof Techniques, Les 1 · Propositional Logic"
        },
        "tags": ["TW1-11::L1", "definitions"]
      }
    ]
  }
}
```

`addNotes` returns a list of note IDs; a `null` entry means Anki rejected that note (usually a duplicate). Check for nulls and report which card failed rather than assuming success.
