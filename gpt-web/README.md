# Lecture → Anki, GPT Edition

A web-only variant of [`lecture-to-anki`](../SKILL.md) for students who don't have
Claude Code or Anki's AnkiConnect add-on. Same idea — quiz first, cards only for
verified gaps — but everything runs in the ChatGPT web UI and the output is a plain
text file the student imports into Anki by hand.

Works on the **Free plan** via a ChatGPT **Project** — no Plus subscription and no
Custom GPT required. (Creating a Custom GPT via "Explore GPTs → Create" needs Plus+;
Projects don't have that restriction and their Instructions field has the same
~8,000 character budget, so `PROMPT.md` works there unchanged. If you *do* have Plus
and prefer a Custom GPT instead, the same file works there too — paste it into
Instructions and optionally enable the Canvas/Web Search/Code Interpreter
capabilities for a smoother experience.)

## What's different from the Claude Code skill

- **No AnkiConnect.** Nothing is pushed automatically. The GPT prints a plain-text
  block with [Anki's text-import header directives](https://docs.ankiweb.net/importing/text-files.html)
  pre-filled (`#notetype:Basic`, `#deck:...`, `#html:true`, `#tags column:3`), so
  `File → Import` in Anki needs no manual field mapping. The student copies it into
  a local `.txt` file themselves — this works on every plan and isn't subject to
  Code Interpreter's daily rate limits on the Free tier.
- **Basic notes only** — no custom note types (those require desktop Anki add-ons to
  create). Source and resource link are folded into the `Back` field as small HTML,
  instead of living in dedicated `Source` / `Resource` fields.
- **Quiz runs in ChatGPT Canvas** when available, not a downloaded HTML file. Canvas
  renders the self-contained HTML/JS live and in-page, so answering, revealing, and
  rating is instant — no per-click round trip to the model. If Canvas isn't
  available, the GPT prints the HTML as a code block instead for the student to save
  and open locally — same client-side snappiness, no special tools required.

## Setup (one-time, ~1 minute)

1. In ChatGPT, go to **Projects → New**, name it (e.g. your course code).
2. Open the project's **Instructions** and paste the contents of
   [`PROMPT.md`](PROMPT.md) (it's under 6,000 of the ~8,000 character limit — room
   to tweak).
3. Share the project (or just the instructions text) with students, or have each
   student create their own project and paste the same instructions in.

No capability toggles to configure — Projects don't have that panel. The GPT uses
whatever tools (Canvas, web search) are available on the student's own plan, with
fallbacks built into the prompt for when they aren't.

## Using it (student side)

1. In the project, start a new chat and answer the intake questions (course,
   lecture, deck name).
2. Paste or upload the lecture material (slides, textbook excerpt, answer key —
   not a recording).
3. Take the quiz (opens in Canvas, or as a code block to save locally), then paste
   the copied summary back into the chat.
4. Review the card table the GPT proposes, edit or cut anything, then approve.
5. Copy the generated text block into a `.txt` file and import it in Anki:
   **File → Import**.

## Files

- `PROMPT.md` — paste this into the Project's (or Custom GPT's) Instructions field.
