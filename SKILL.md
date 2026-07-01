---
name: lecture-to-anki
description: Turn a lecture's static materials (slides, textbook chapter, answer key) into an interactive self-quiz and then a reviewed, gap-focused Anki deck via AnkiConnect. Use this skill whenever the user wants to study a lecture or course materials and turn them into Anki flashcards — built for the TU Delft math bachelor but applicable to any lecture-based subject. Trigger on mentions of "lecture", "college", "Anki", "flashcards", "kaartjes", "quiz me on this", "study this", a course-materials folder, or any uploaded slides/textbook/answer-key the user wants to learn from — even if they don't say the word "Anki".
---

# Lecture → quiz → reviewed Anki deck

This workflow was refined over several rounds of real user feedback. The decisions below exist because simpler versions were explicitly rejected. Don't re-derive them — follow them unless the user says otherwise.

The throughline: **the user's own brain is the filter.** They self-quiz, mark what they don't know, and only verified gaps become cards. You never push cards without an explicit go-ahead. Growth tracks knowledge, not slide count.

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

The skill talks to AnkiConnect on every run. Add these entries to
`~/.claude/settings.json` under `permissions.allow`:

```json
{
  "permissions": {
    "allow": [
      "Read(~/.claude/skills/lecture-to-anki/**)",
      "Bash(curl -s http://127.0.0.1:8765*)",
      "Bash(python3 /tmp/anki_call.py)"
    ]
  }
}
```

> **Windows note:** `~` conventionally means your user home directory
> (`%USERPROFILE%`). Use PowerShell, Git Bash, or WSL.

**AnkiConnect pattern (recommended):** For reliability with complex payloads
(card content with unicode, quotes, etc.), write them to a temporary script and
execute it:

- Linux/macOS: `/tmp/anki_call.py` + `python3 /tmp/anki_call.py`
- Windows: `%TEMP%\anki_call.py` (or a file in the current lecture folder) +
  `python ...`

The key is using a *predictable fixed location* so allow rules continue to match.

**Web search capability.** For Step 2 resource discovery, use `WebSearch` to find supplementary video explanations for concepts the user didn't know. Prioritize established educational channels (3Blue1Brown, Khan Academy, Professor Leonard) and general high-quality content — language doesn't matter if it's better quality.

## Hard rules (from direct user feedback)

1. **Hold for approval.** Drafted cards stay pending until the user explicitly approves, edits, or cuts. The act of reviewing each card *is* part of the studying — never bypass it by pushing eagerly.
2. **One deck per subject area.** Consolidate into a single broad-subject deck. No `<course>::<lecture>` deck hierarchies — that lives in tags instead (see Step 4). Per-lecture separation happens through tags and the `Source` field, never through deck splitting.
3. **Static sources only.** Extract from slides, textbook chapters, and official answer keys. Never use audio/video recordings (e.g. Collegerama). Cross-reference the textbook to resolve vague slide concepts, and trust official answer keys over your own worked solutions.
4. **Source goes in the Source field, never inline.** Keep the question text clean. Put full context in the dedicated `Source` field, formatted exactly: `<course code> · <course name>, Lecture <n> · <topic>` (e.g. `TW1-11 · Proof Techniques, Lecture 1 · Propositional Logic`). Use whatever word for "lecture" matches the source material's language (e.g. "Les" for Dutch) — the field is for the human reading the card, so it should read naturally in that language. The lecture *tag* (Step 0/4) stays language-neutral regardless.

## Step 0 — preconditions, deck, duplicate check

**Verify AnkiConnect is live.** Run this first, before anything else:

```bash
curl -s http://127.0.0.1:8765 -X POST -d '{"action": "version", "version": 6}'
```

A healthy response looks like `{"result": 6, "error": null}`. If the call fails or errors, **stop** and tell the user Anki desktop must be running with the AnkiConnect add-on installed. Do not generate a static `.apkg`/`.txt` import file as a fallback — that path was deprecated because it broke the review-and-approve loop this skill is built around.

**Resolve the target deck.** Per Hard Rule 2, find the one subject-area deck:
- Check local setup files (`CLAUDE.md`, `GEMINI.md`, project notes, etc.) for an
  already-designated deck. If found, reuse it silently.
- If none is recorded, call `deckNames`, show the user the list, and have them pick an existing deck or name a new one (`createDeck`) — **before** drafting anything.
- Persist the choice to the project's notes file (`CLAUDE.md`, `GEMINI.md`,
  `AGENTS.md`, `.cursorrules`, etc.) so future lectures skip this prompt.

**Check for duplicates from this exact lecture.** Before generating, scan the deck so you don't silently re-add a lecture the user already studied. Prefer the **tag** — it's language-neutral and exact, unlike matching against the human-readable `Source` text:

```
findNotes  query:  deck:"<deck>" tag:<CourseCode>::L<n>
```

If matches turn up, report the **count** and the matched `Source` string, then ask whether to supplement, revise the existing cards, or skip this lecture. Never add silent duplicates and never skip without the user's say-so.

## Step 1 — interactive quiz (not a static markdown file)

Write a self-contained `quiz.html` into the lecture-materials directory. Use the template in `assets/quiz_template.html` **verbatim** — change only the `<title>`, the `<h1>`, and the `questions` array. Keeping the layout, CSS, and interactive behaviour identical across lectures is deliberate: the user has built muscle memory around it.

The questions array is a list of `[question, answer]` string pairs:

```js
const questions = [
  ["What is a proposition?", "A statement that is either true or false, but not both."],
  ["When is p → q false?", "Only when p is true and q is false."]
];
```

Answers may contain HTML (`<br>`, `<code>`, etc.) and render as-is. Match the **language of the source material** for both the questions and the on-screen labels — the template's built-in UI text (button labels, summary) is English by default; translate those strings too if the lecture material is in another language (e.g. Dutch). Escape any literal `<`, `>`, `&` in math so it doesn't break the markup.

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
- **Meaningful clozes / desirable difficulty.** Blank out the load-bearing concept, operator, or rule — not structural syntax or filler words you could guess from context.
- **Standalone context (no orphans).** The front must name the theorem/rule/boundary condition so it's unambiguous months later, with no reliance on lecture order.
- **Clean backs.** No conversational filler on the back.
- **Type selection.** Use **Cloze** for formulas, crisp definitions, and formal laws; use **Basic** for pattern-matching, judgment calls, and translations where cloze boundaries feel forced.
- **Independent clozes are encouraged.** `{{c1::...}}` and `{{c2::...}}` targeting *independent* facts in one note is good — Anki splits them into separate single-blank cards.

See `references/card_examples.md` for worked good-vs-bad examples covering each principle.

**Discover supplementary resources.** For every question the user self-rated `no`, find **one** high-quality video that explains the same concept from a different angle:
- Extract the core concept from the question (e.g., "implication truth conditions", "contrapositive equivalence")
- Use `WebSearch` to find one video — prioritize established educational channels, then general quality content. Language doesn't matter if it's better quality.
- Extract or generate a descriptive label for the video (e.g., "CrashCourse: Logic & Reasoning #5" instead of raw YouTube URL)
- Present both label and link in Step 3

This turns the skill from pure memorization into a complete learning loop: quiz → identify gaps → alternative explanations → cards for retention.

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
- **`Cloze (Source + Resource)`** — fields `Text`, `Back Extra`, `Source`, `Resource`

Run `modelNames` first. If either custom type is missing on the active profile, create it with `createModel` using the layout in `references/notetypes.md` (CSS + card templates). The `Source` field renders small and grey at the bottom of every card. The `Resource` field renders as a clickable link below Source when present.

**Tags** combine the lecture locator with topic descriptors:
- Lecture: `<CourseCode>::L<n>` (e.g. `TW1-11::L1`)
- Topics: lowercase, specific (e.g. `implication`, `definitions`, `equivalences`, `translation`)

**Push and verify.** `createModel`, `addNotes`, and any other call carrying card content (cloze text, Dutch/accented characters, embedded quotes) should use a predictable temp script location as described in the Setup section above (e.g. `/tmp/anki_call.py` on Unix or a file in the lecture folder). Push into the exact deck from Step 0, then immediately confirm with `findNotes` + `notesInfo` that the added count matches what was approved and the `Source`/fields are populated. Report the result — e.g. "added 6 cards to `Mathematics`, all with Source `TW1-11 · Proof Techniques, Les 1 · Propositional Logic`." If `addNotes` returns any `null` (a duplicate Anki rejected), say which card and why rather than reporting silent success.

## Files in this skill

- `assets/quiz_template.html` — the verbatim quiz scaffold for Step 1.
- `references/card_examples.md` — good-vs-bad card examples for Step 2.
- `references/notetypes.md` — `createModel` payloads + CSS for all custom note types (including `Cloze (Source + Resource)`).
- `permissions.json` — settings snippet for Claude Code (see "Setup" above).
