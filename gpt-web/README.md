# Lecture → Anki, GPT Edition

A web-only variant of [`lecture-to-anki`](../SKILL.md) for students who don't have
Claude Code or Anki's AnkiConnect add-on. Same idea — quiz first, cards only for
verified gaps — but everything runs in the ChatGPT web UI and the output is a plain
text file the student imports into Anki by hand.

## What's different from the Claude Code skill

- **No AnkiConnect.** Nothing is pushed automatically. The GPT hands the student a
  downloadable `.txt` file with [Anki's text-import header directives](https://docs.ankiweb.net/importing/text-files.html)
  pre-filled (`#notetype:Basic`, `#deck:...`, `#html:true`, `#tags column:3`), so
  `File → Import` in Anki needs no manual field mapping.
- **Basic notes only** — no custom note types (those require desktop Anki add-ons to
  create). Source and resource link are folded into the `Back` field as small HTML,
  instead of living in dedicated `Source` / `Resource` fields.
- **Quiz runs in ChatGPT Canvas**, not a downloaded HTML file. Canvas renders the
  self-contained HTML/JS live and in-page, so answering, revealing, and rating is
  instant — no per-click round trip to the model. If Canvas isn't available, the GPT
  falls back to a downloadable HTML file (same client-side behavior, opened locally).

## Setup (one-time, ~2 minutes)

1. In ChatGPT, go to **Explore GPTs → Create** (GPT Builder).
2. On the **Configure** tab, set a name and short description, then paste the
   contents of [`PROMPT.md`](PROMPT.md) into **Instructions** (it's ~5,500 of the
   8,000 character limit — room to tweak).
3. Under **Capabilities**, enable: **Web Search**, **Canvas**, and
   **Code Interpreter & Data Analysis**. (File upload for slides/notes is included
   automatically once Code Interpreter is on.)
4. Save, and share the GPT link with students.

## Using it (student side)

1. Open the GPT, answer its intake questions (course, lecture, deck name).
2. Paste or upload the lecture material (slides, textbook excerpt, answer key —
   not a recording).
3. Take the quiz that opens in Canvas, then paste the copied summary back into chat.
4. Review the card table the GPT proposes, edit or cut anything, then approve.
5. Download the generated `.txt` file and import it in Anki: **File → Import**.

## Files

- `PROMPT.md` — paste this into the Custom GPT's Instructions field.
