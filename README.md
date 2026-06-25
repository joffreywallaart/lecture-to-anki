# lecture-to-anki

A skill (Claude Code, Grok Build, Gemini CLI, Cursor) for turning a lecture's
materials into a quick self-quiz, and then a small, reviewed Anki deck.

## Why

I've used Anki for years, but at some point I'd let it shrink down to just one or two
narrow use cases, because making decent cards for anything else always felt like too
much work. Binging Youtube lately made me reconsider.

- [I Reviewed 28,655 Flashcards Every Day for 17 Years. I Barely Had to Study.](https://www.youtube.com/watch?v=7WtznlsP6M8)
- [This Claude Code Setup Changed My Life](https://www.youtube.com/watch?v=1sMHcJMxYqo)
- [How I Use Claude Code + Anki to Memorize Anything (My Agentic Learning System)](https://www.youtube.com/watch?v=RocA3wA3QjU)

This skill is what came out of trying that on a university course (a TU Delft
math class) and adjusting the workflow until it stopped annoying me.

## What it does

1. Reads a lecture's static materials: slides, textbook chapter, lecture notes, if available.
   Not the recording.
2. Builds a short interactive HTML quiz (12-15 questions) to figure out what you don't
   actually know, rather than re-testing what's already solid.
3. Drafts cards for the gaps the quiz found. The deck grows with what you're missing,
   not with how many slides there were.
4. Shows you every candidate card - front, back, source, tags - before any of it goes
   into Anki. Nothing gets added without you saying yes.
5. Pushes the approved cards into a single deck via AnkiConnect, with a `Source` field
   on each card so you can trace it back later.

The full workflow and the reasoning behind it lives in [`SKILL.md`](SKILL.md).

## Requirements

- [Anki](https://apps.ankiweb.net/) desktop, running
- The [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on
- One of: Claude Code, Grok Build, Gemini CLI, or Cursor

## Install

### Claude Code

Clone into the Claude skills folder:

```bash
git clone https://github.com/joffreywallaart/lecture-to-anki.git ~/.claude/skills/lecture-to-anki
```

Then merge the contents of [`permissions.json`](permissions.json) into
`~/.claude/settings.json` under `permissions.allow`. This prevents repeated
permission prompts for reading the skill's own files and talking to AnkiConnect.

### Grok Build

Grok discovers skills from both `~/.claude/skills/` (for compatibility) and `~/.grok/skills/`.

You can install to the Claude-compatible location (recommended if you use both tools):

```bash
git clone https://github.com/joffreywallaart/lecture-to-anki.git ~/.claude/skills/lecture-to-anki
```

Or install to Grok's native location:

```bash
git clone https://github.com/joffreywallaart/lecture-to-anki.git ~/.grok/skills/lecture-to-anki
```

Grok uses interactive approvals instead of a static allowlist file. When the skill
needs to read its own files or call AnkiConnect it will prompt; choose "Always allow"
for the relevant commands (or for the whole session) to avoid repeated prompts.
No changes to `~/.grok/config.toml` are required for basic use.

### Gemini CLI

Gemini CLI has native `gemini skills` management and discovers skills in
`~/.gemini/skills/` (and the portable `~/.agents/skills/` alias).

**Easiest:** Install directly from the repo:

```bash
gemini skills install https://github.com/joffreywallaart/lecture-to-anki.git
```

**Manual / development:**

```bash
git clone https://github.com/joffreywallaart/lecture-to-anki.git ~/.gemini/skills/lecture-to-anki
# or the portable alias:
# git clone ... ~/.agents/skills/lecture-to-anki
```

Or link a local checkout:

```bash
gemini skills link /path/to/lecture-to-anki
```

Gemini will prompt for consent the first time the skill is activated in a
session (it gets access to the skill directory). Use `/skills list` inside Gemini
to see installed skills.

Use `--scope workspace` with `install` or `link` if you want it project-scoped
(placed in `.gemini/skills/` or `.agents/skills/` inside the repo).

### Cursor

Cursor discovers skills for compatibility from `~/.cursor/skills/` and project
`.cursor/skills/`, as well as the portable `.agents/skills/` alias.

Clone or link the skill:

```bash
git clone https://github.com/joffreywallaart/lecture-to-anki.git ~/.cursor/skills/lecture-to-anki
```

Or for workspace/project scope (recommended when working inside a course repo):

```bash
git clone https://github.com/joffreywallaart/lecture-to-anki.git .cursor/skills/lecture-to-anki
```

Cursor also respects `~/.agents/skills/lecture-to-anki`.

Cursor handles approvals in the IDE (chat composer / agent mode). No separate
permissions file is needed. The skill activates when your prompt matches the
description (e.g. "turn this lecture into Anki cards") or you reference it
explicitly. You can manage Cursor rules and context in the usual `.cursor/rules/`
or settings UI alongside this.

## Use

From a folder with lecture materials, describe the task in natural language
(e.g. "turn this lecture into Anki cards") or invoke the skill directly:

- Claude Code: `/lecture-to-anki`
- Grok Build: `/lecture-to-anki`
- Gemini CLI: Describe the task (skill activates on matching description); manage
  with `/skills` or `gemini skills`
- Cursor: Describe the task in Agent / Composer (or reference the skill name)

The first time it runs it will ask which deck to use and record the choice (in
`CLAUDE.md`, `GEMINI.md`, or equivalent project notes). Subsequent runs reuse it.

## Design notes

- One deck per subject, not per course or per lecture. Tags carry the course/lecture/
  topic instead. Splitting into lots of decks is what breaks a daily review habit.
- Cards follow the usual spaced-repetition advice: atomic facts, short backs, clozes
  that test something real instead of guessable syntax. Worked examples are in
  [`references/card_examples.md`](references/card_examples.md).
- The quiz template ([`assets/quiz_template.html`](assets/quiz_template.html)) stays
  the same every lecture, on purpose.

### Sources

- Piotr Wozniak, [*Effective learning: Twenty rules of formulating knowledge*](https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge)
  (SuperMemo, 1999). Where the atomicity and minimum-information rules come from, plus
  the idea of citing sources as a context cue rather than part of the question.
- [*Rules for Designing Precise Anki Cards*](https://controlaltbackspace.org/precise/)
  (controlaltbackspace.org). Unambiguous questions, and the same source-as-context-cue
  point made a different way.
- Roediger, H. L., & Karpicke, J. D. (2006). [Test-enhanced learning: Taking memory
  tests improves long-term retention](https://doi.org/10.1111/j.1467-9280.2006.01693.x).
  *Psychological Science*, 17(3), 249-255. Why the quiz comes before the cards: the
  retrieval practice itself is doing a lot of the work, not just the deck you end up
  with.

## License

MIT, see [`LICENSE`](LICENSE).
