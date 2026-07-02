---
name: lecture-to-anki
description: Turn lecture materials (slides, textbook chapter, answer key) into a gap-focused Anki deck via a self-quiz and AnkiConnect. Invoke explicitly with /lecture-to-anki when the user asks to create Anki cards or flashcards from course materials they have on hand.
---

# Lecture → quiz → reviewed Anki deck

Follow the steps below unless the user says otherwise.

The guiding principle: **the user's own brain is the filter.** They self-quiz, mark what they don't know, and only verified gaps become cards. You never push cards without an explicit go-ahead. Growth tracks knowledge, not slide count.

## The five stages

0. Preconditions + deck resolution + duplicate check
1. Build an interactive `quiz.html` (12–15 diagnostic questions)
2. Wait for quiz results, then draft gap-focused candidates
3. Present candidates as a table — push nothing yet
4. On approval, push via AnkiConnect into custom note types, then verify

Don't skip ahead. Each stage gates the next: no quiz before the deck is resolved, no cards before quiz results come back, no `addNotes` before approval.

## Setup — avoid repeat permission prompts

Install this skill into Claude Code's skills directory:

```bash
git clone https://github.com/joffreywallaart/lecture-to-anki.git ~/.claude/skills/lecture-to-anki
```

The skill talks to AnkiConnect via `assets/anki.py`. Add these entries to
`~/.claude/settings.json` under `permissions.allow`:

```json
{
  "permissions": {
    "allow": [
      "Read(~/.claude/skills/lecture-to-anki/**)",
      "Bash(python3 ~/.claude/skills/lecture-to-anki/assets/anki.py *)",
      "Write(/tmp/anki_notes.json)"
    ]
  }
}
```

> **Windows note:** `~` means your user home directory (`%USERPROFILE%`). Use PowerShell, Git Bash, or WSL, and verify the Bash permission matches the path the shell actually emits — if `~` is not expanded by the permission matcher, use the full absolute path instead.

**AnkiConnect pattern:** Write the notes array to `/tmp/anki_notes.json` (Linux/macOS) or `%TEMP%\anki_notes.json` (Windows), then call the module. The module handles all HTTP details, error-checking, and duplicate filtering — never write ad-hoc AnkiConnect scripts.

Available commands (all reference `~/.claude/skills/lecture-to-anki/assets/anki.py`):

```
python3 .../anki.py version           # verify AnkiConnect is live
python3 .../anki.py deck-names        # list available decks
python3 .../anki.py create-deck NAME  # create a new deck
python3 .../anki.py ensure-models     # idempotently create custom note types
python3 .../anki.py add-notes FILE    # add notes from a JSON array file
python3 .../anki.py find-notes QUERY  # find notes and show Source field
```

**Web search capability.** For Step 2 resource discovery, use `WebSearch` to find supplementary video explanations for concepts the user didn't know. Prioritize channels appropriate to the subject (e.g. 3Blue1Brown or Khan Academy for math, CrashCourse for humanities) and general high-quality content — language doesn't matter if it's better quality.

## Hard rules (from direct user feedback)

1. **Hold for approval.** Drafted cards stay pending until the user explicitly approves, edits, or cuts. The act of reviewing each card *is* part of the studying — never bypass it by pushing eagerly.
2. **One deck per subject area.** Consolidate into a single broad-subject deck. No `<course>::<lecture>` deck hierarchies — use tags for that instead (see Step 4). Per-lecture separation happens through tags and the `Source` field, never through deck splitting.
3. **Static sources only.** Extract from slides, textbook chapters, and official answer keys. Never use audio/video recordings (e.g. Collegerama). Cross-reference the textbook to resolve vague slide concepts, and trust official answer keys over your own worked solutions.
4. **Source goes in the Source field, never inline.** Keep the question text clean. Put full context in the dedicated `Source` field, formatted exactly: `<course code> · <course name>, Lecture <n> · <topic>` (e.g. `TW1-11 · Proof Techniques, Lecture 1 · Propositional Logic`). Use whatever word for "lecture" matches the source material's language (e.g. "Les" for Dutch) — the field is for the human reading the card, so it should read naturally in that language. The lecture *tag* (Step 0/4) stays language-neutral regardless.

## Step 0 — preconditions, deck, duplicate check

**Verify AnkiConnect is live.** Run this first, before anything else:

```bash
python3 ~/.claude/skills/lecture-to-anki/assets/anki.py version
```

Run it exactly as shown, as its own isolated Bash call — don't chain it with `&&`, `;`, `|`, or anything else (e.g. no appending `ls` to also peek at the working directory). Claude Code's permission rules match each subcommand in a chain independently, so chaining anything onto this call defeats the merged `permissions.json` and triggers an approval prompt even when the user set it up exactly as documented. Same goes for every other `anki.py` call in this skill.

A healthy response looks like `AnkiConnect 6 — OK`. If the call fails, **stop** and tell the user Anki desktop must be running with the AnkiConnect add-on installed. Do not generate a static `.apkg`/`.txt` import file as a fallback — that path was deprecated because it broke the review-and-approve loop this skill is built around.

**Resolve the target deck.** Per Hard Rule 2, find the one subject-area deck:
- Check local setup files (`CLAUDE.md`, `GEMINI.md`, project notes, etc.) for an
  already-designated deck. If found, reuse it silently.
- If none is recorded, run `python3 .../anki.py deck-names`, show the user the list, and have them pick an existing deck or name a new one (`python3 .../anki.py create-deck NAME`) — **before** drafting anything.
- Persist the choice to the project's notes file (`CLAUDE.md`, `GEMINI.md`,
  `AGENTS.md`, `.cursorrules`, etc.) so future lectures skip this prompt.

**Check for duplicates from this exact lecture.** Before generating, scan the deck so you don't silently re-add a lecture the user already studied. Prefer the **tag** — it's language-neutral and exact, unlike matching against the human-readable `Source` text:

```bash
python3 .../anki.py find-notes 'deck:"<deck>" tag:<CourseCode>::L<n>'
```

If matches turn up, report the **count** and the matched `Source` string, then ask whether to supplement, revise the existing cards, or skip this lecture. Never add silent duplicates and never skip without the user's say-so.

## Step 1 — interactive quiz (not a static markdown file)

Write `quiz.html` to the lecture-materials directory. If a `quiz.html` already exists there, ask before overwriting. Use the template in `assets/quiz_template.html` as your base scaffold — fill in `{{LECTURE_TITLE}}` (used in `<title>` and `<h1>`), `{{LANG}}` (BCP 47 language code, e.g. `en` or `nl`), and the `questions` array; keep everything else identical. Keeping the layout, CSS, and interactive behavior identical across lectures is deliberate: the user has built muscle memory around it. The template loads MathJax from a CDN, so `quiz.html` itself is no longer fully offline — a question with math needs an internet connection to render correctly in the browser (everything else in the quiz still works with no connection). This doesn't affect the Anki cards later: Anki bundles its own local MathJax and renders `\(...\)` fields offline regardless.

The questions array is a list of `[question, answer]` string pairs:

```js
const questions = [
  ["What is a proposition?", "A statement that is either true or false, but not both."],
  ["When is p → q false?", "Only when p is true and q is false."]
];
```

Answers may contain HTML (`<br>`, `<code>`, etc.) and render as-is. Match the **language of the source material** for both the questions and the on-screen labels — the template's built-in UI text (button labels, summary) is English by default; if the lecture material is in another language, translate those strings as well. Escape any literal `<`, `>`, `&` in math so it doesn't break the markup.

**Math notation.** The template loads MathJax, so use proper LaTeX for math, not Unicode — wrap inline math in `\(...\)` and standalone equations in `\[...\]` (same delimiters Anki's own reviewer recognizes, so this content can be reused verbatim in the cards later). This applies to any math notation, however small — a single connective like `\(A \lor B\)` or a lone Greek letter, not just multi-term formulas. Example: `\(f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}\)`.

**Cap it at 12–15 questions.** This is a diagnostic triage tool to surface current memory gaps, not an exhaustive review. Aim for one probe per core definition or law. For application skills (translations, conditional direction, validity checks), include only 1–2 representative items rather than mirroring every slide exercise.

After writing the file, give the user its path and tell them: answer each question in their head, reveal the answer, self-rate, then paste the summary back into the chat.

## Step 2 — wait for results, then draft gap-focused candidates

Wait for the user's pasted summary. **Don't draft cards before it arrives.**

Budget the cards by self-rating:
- `know` (knew it instantly) → **no card.** Don't reinforce what's already solid.
- `no` (didn't know) → the bulk of the budget. These are the real gaps.
- `shaky` (hesitated) → draft conservatively, typically one well-aimed card.

This is what ties deck growth to verified gaps rather than slide volume.

**Card design — distilled from Wozniak's 20 Rules and the cloze literature:**
- **Atomic.** One fact or mechanism per card. Split compound facts into separate notes or independent clozes rather than bundling.
- **Meaningful clozes / desirable difficulty.** Blank out the load-bearing concept, operator, or rule — not structural syntax or filler words that could be guessed from context.
- **Standalone context (no orphans).** The front must name the theorem/rule/boundary condition so it's unambiguous months later, with no reliance on lecture order.
- **Clean backs.** No conversational filler on the back.
- **Type selection.** Use **Cloze** for formulas, crisp definitions, and formal laws; use **Basic** for pattern-matching, judgment calls, and translations where cloze boundaries feel forced.
- **Independent clozes are encouraged.** `{{c1::...}}` and `{{c2::...}}` targeting *independent* facts in one note is good — Anki splits them into separate single-blank cards.
- **Math notation.** Same rule as the quiz: always LaTeX (`\(...\)` / `\[...\]`), never Unicode, for any math notation regardless of size. Anki's reviewer renders MathJax in every field natively — no note-type or template changes needed.

See `assets/card_examples.md` for worked good-vs-bad examples covering each principle.

**Discover supplementary resources.** For every question the user self-rated `no`, find **one** high-quality video that explains the same concept from a different angle:
- Extract the core concept from the question (e.g., "implication truth conditions", "contrapositive equivalence")
- Use `WebSearch` to find one video — prioritize established educational channels, then general quality content. Language doesn't matter if it's better quality.
- Extract or generate a descriptive label for the video (e.g., "CrashCourse: Logic & Reasoning #5" instead of raw YouTube URL)
- Present both label and link in Step 3

This turns the skill from pure memorization into a complete learning loop: quiz → identify gaps → alternative explanations → cards for retention.

**Self-review before presenting.** Before moving to Step 3, re-read every drafted card against the design rules above and `assets/card_examples.md` — atomic, meaningful cloze, standalone, clean back, right type for the content. Fix or redraft anything that fails a rule; cut it if it can't be fixed. This is a check on your own draft, not a rubber stamp — do it even when the cards look fine at a glance. The user's approval pass in Step 3 is for judgment calls (is this worth knowing, is the phrasing right), not for catching rule violations you could have caught yourself.

## Step 3 — present candidates with supplementary resources, push nothing

Present two sections: card candidates first, then supplementary resources for gaps.

**Cards table:** Show every candidate in a markdown table with these columns:

```
Type | Front / Text | Back / Blank | Tags
```

For cards that have a resource, note this in the presentation (e.g., append "🎥" to the Type column).

**Supplementary resources section:** Below the cards table, add a section for gaps:

```markdown
## Supplementary resources for gaps

| Concept | Video Label | URL |
|---------|-------------|-----|
| Implication truth conditions | CrashCourse: Logic & Reasoning #5 | https://youtube.com/watch?v=... |
| Contrapositive equivalence | 3Blue1Brown: Logical Equivalence | https://youtube.com/watch?v=... |
```

- One row per concept the user didn't know (from Step 2 resource discovery)
- **Video Label** is a descriptive title (not raw URL) — this becomes the display text on the card
- **URL** is the full link to the video
- User can approve, edit labels/links, or cut resources before pushing

The user sees readable titles in Step 3 and on the final card back — never raw URLs.

Then stop and wait for explicit feedback. Approve, edit, cut — the user decides before any Anki write happens. This review pass is itself part of the studying, so don't rush past it.

## Step 4 — push approved cards, then verify

**Use only the custom note types**, never plain `Basic`/`Cloze`:
- **`Basic (Source)`** — fields `Front`, `Back`, `Source`
- **`Cloze (Source)`** — fields `Text`, `Back Extra`, `Source`
- **`Cloze (Source + Resource)`** — fields `Text`, `Back Extra`, `Source`, `Resource Label` (display text), `Resource` (URL)

Resources are only supported on Cloze cards via `Cloze (Source + Resource)`. If a Basic card warrants a resource, convert it to a Cloze or add the link directly to its `Back` field.

**Ensure note types exist.** Run this once per Anki profile — it's idempotent:

```bash
python3 ~/.claude/skills/lecture-to-anki/assets/anki.py ensure-models
```

The `Source` field renders small and gray at the bottom of every card. The `Resource Label` and `Resource` fields render as a clickable link below Source when present. See `assets/notetypes.md` for the full field reference.

**Tags** combine the lecture locator with topic descriptors:
- Lecture: `<CourseCode>::L<n>` (e.g. `TW1-11::L1`)
- Topics: lowercase, specific (e.g. `implication`, `definitions`, `equivalences`, `translation`)

**Push and verify.** Write the approved notes as a JSON array to `/tmp/anki_notes.json` (field names and structure are in `assets/notetypes.md`), then:

```bash
python3 ~/.claude/skills/lecture-to-anki/assets/anki.py add-notes /tmp/anki_notes.json
```

The module pre-checks for duplicates, adds only valid notes, and reports any that were skipped. Confirm the result with:

```bash
python3 ~/.claude/skills/lecture-to-anki/assets/anki.py find-notes 'deck:"<deck>" tag:<CourseCode>::L<n>'
```

Report the outcome — e.g. "added 6 cards to `Mathematics`, all with Source `TW1-11 · Proof Techniques, Les 1 · Propositional Logic`."

## Files in this skill

- `assets/anki.py` — CLI module for all AnkiConnect calls (see Setup for commands).
- `assets/quiz_template.html` — the quiz scaffold for Step 1.
- `assets/card_examples.md` — good-vs-bad card examples for Step 2.
- `assets/notetypes.md` — field reference for all custom note types.
- `permissions.json` — settings snippet for Claude Code (see "Setup" above).
