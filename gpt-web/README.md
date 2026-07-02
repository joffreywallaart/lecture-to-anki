# Lecture → Anki, GPT Edition

A web-only variant of [`lecture-to-anki`](../SKILL.md) for students who don't have
Claude Code or Anki's AnkiConnect add-on. Same idea — quiz first, cards only for
verified gaps — but everything runs in the ChatGPT web UI and the output is a plain
text file the student imports into Anki by hand.

Works on the **Free plan** via a ChatGPT **Project** — no Plus subscription and no
Custom GPT required. (Creating a Custom GPT via "Explore GPTs → Create" needs Plus+;
Projects don't have that restriction and their Instructions field has the same
~8,000 character budget, so `PROMPT.md` works there unchanged. The same file also
works pasted into a Custom GPT's Instructions if you have Plus and prefer that
route.)

## What's different from the Claude Code skill

- **No AnkiConnect.** Nothing is pushed automatically. The GPT writes a `.txt` file
  with [Anki's text-import header directives](https://docs.ankiweb.net/importing/text-files.html)
  pre-filled (`#notetype:Basic`, `#deck:...`, `#html:true`, `#tags column:3`), so
  `File → Import` in Anki needs no manual field mapping.
- **Basic notes only** — no custom note types (those require desktop Anki add-ons to
  create). Source and resource link are folded into the `Back` field as small HTML,
  instead of living in dedicated `Source` / `Resource` fields.
- **Deck stays domain-based, not per-course or per-lecture.** The GPT asks for a
  deck name once per subject and reuses it across lectures (course/lecture context
  lives in the tag and the `Source` line instead). A pile of tiny decks is what kills
  a daily review habit, so don't let students name a new deck per course — this is
  also why the ChatGPT *project* name (setup step 1) shouldn't be a course code
  either; conflating the two invites exactly that.
- **Quiz is a standalone HTML file**, not a back-and-forth chat. The GPT writes it
  via its file/code tool and attaches it, which — verified live in a Free-tier
  Project — makes ChatGPT render it as an interactive inline preview (clickable
  reveal/rating buttons, working right there in the chat) alongside a real download
  link, so the student can use it either way. Answering, revealing, and rating all
  run client-side — no per-click round trip to the model. (An earlier attempt to
  invoke ChatGPT's separate "Canvas" tool by name for this was unreliable — it
  degraded to a plain chat Q&A with no reveal mechanic in testing, so the prompt
  asks for a written/attached file instead and only falls back to a plain code
  block if file-writing genuinely isn't available.)

## Setup (one-time, ~1 minute)

1. In ChatGPT, go to **Projects → New**, name it something generic like
   `lecture-to-anki` — not a course code. The project name is just a label for the
   chat; it's unrelated to the Anki deck, and reusing one project across every
   course keeps that distinction clear (see the deck-per-domain note above).
2. Open the project's **Instructions** and paste the contents of
   [`PROMPT.md`](PROMPT.md) (it's under 6,000 of the ~8,000 character limit — room
   to tweak).
3. Share the project (or just the instructions text) with students, or have each
   student create their own project and paste the same instructions in.

No capability toggles to configure — Projects don't have that panel. The GPT uses
whatever file/code and web-search tools are available on the student's own plan,
with a plain-text fallback built into the prompt for when they aren't.

## Using it (student side)

1. In the project, start a new chat and answer the intake questions (course,
   lecture, deck name).
2. Paste or upload the lecture material (slides, textbook excerpt, answer key —
   not a recording).
3. Take the quiz where it renders (inline in the chat, or open the downloaded
   `quiz.html`), then paste the copied summary back into the chat.
4. Review the card table the GPT proposes, edit or cut anything, then approve.
5. Download the generated `.txt` file (or copy the printed block into one) and
   import it in Anki: **File → Import**.

## Files

- `PROMPT.md` — paste this into the Project's (or Custom GPT's) Instructions field.
