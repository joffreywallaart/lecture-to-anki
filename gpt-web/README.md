# Lecture → Anki, GPT Edition

A web-only variant of [`lecture-to-anki`](../SKILL.md), for students without
Claude Code or Anki's AnkiConnect add-on. Same idea: quiz first, cards only for
verified gaps. Everything runs in the ChatGPT web UI, and the output is a plain
text file the student imports into Anki by hand.

Works on the Free plan through a ChatGPT Project. No Plus subscription and no
Custom GPT needed. Creating a Custom GPT through "Explore GPTs → Create" requires
Plus, but Projects don't have that restriction, and their Instructions field has
the same ~8,000 character budget. `PROMPT.md` works there unchanged. It also works
pasted into a Custom GPT's Instructions if you have Plus and prefer that route.

## What's different from the Claude Code skill

- **No AnkiConnect.** Nothing is pushed automatically. The GPT writes a `.txt` file
  with [Anki's text-import header directives](https://docs.ankiweb.net/importing/text-files.html)
  pre-filled (`#notetype:Basic`, `#deck:...`, `#html:true`, `#tags column:3`), so
  `File → Import` in Anki needs no manual field mapping.
- **Basic notes only.** No custom note types, since those require desktop Anki
  add-ons to create. Source and resource link go into the `Back` field as small
  HTML instead of living in dedicated `Source` / `Resource` fields.
- **Deck stays domain-based, not per-course or per-lecture.** The GPT asks for a
  deck name once per subject and reuses it across lectures; course and lecture
  context lives in the tag and the `Source` line instead. That's also why the
  ChatGPT project name (setup step 1) shouldn't be a course code: the project name
  and the Anki deck are unrelated, and naming both after the course makes it easy
  to end up with a deck per course instead of one deck per subject.
- **Quiz is a standalone HTML file, not a back-and-forth chat.** The GPT writes it
  with its file/code tool and attaches it. In testing on the Free plan, ChatGPT
  then renders it as an interactive inline preview, with working reveal and rating
  buttons in the chat, plus a real download link. Answering, revealing, and rating
  all run client-side, with no per-click round trip to the model. An earlier
  version tried invoking ChatGPT's separate "Canvas" tool by name for this; that
  was unreliable and degraded to a plain chat Q&A with no reveal mechanic. The
  prompt now asks for a written/attached file instead, and only falls back to a
  plain code block if file-writing isn't available.

## Setup (about a minute)

1. In ChatGPT, go to Projects → New. Name it something generic, like
   `lecture-to-anki`, not a course code (see the deck-per-domain note above).
2. Open the project's Instructions and paste in the contents of
   [`PROMPT.md`](PROMPT.md). It's under 7,000 of the ~8,000 character limit.
3. Share the project, or just the instructions text, with students. Or have each
   student create their own project and paste in the same instructions.

There are no capability toggles to configure; Projects don't have that panel. The
GPT uses whatever file/code and web-search tools are available on the student's
plan, with a plain-text fallback built into the prompt for when they aren't.

## Using it (student side)

1. In the project, start a new chat and answer the intake questions: course,
   lecture, deck name.
2. Paste or upload the lecture material: slides, textbook excerpt, answer key.
   Not a recording.
3. Take the quiz where it renders, inline in the chat or in the downloaded
   `quiz.html`, then paste the copied summary back into the chat.
4. Review the card table the GPT proposes. Edit or cut anything, then approve.
5. Download the generated `.txt` file, or copy the printed block into one, and
   import it in Anki: File → Import.

## Files

- `PROMPT.md`: paste this into the Project's (or Custom GPT's) Instructions field.
