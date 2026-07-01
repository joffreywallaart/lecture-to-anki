# lecture-to-anki

A skill for turning a lecture's materials into a quick self-quiz, and then a small,
reviewed Anki deck — via Claude Code.

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
   not with how many slides there were. For concepts you didn't know, also finds one
   high-quality video explaining them from a different angle.
4. Shows you every candidate card - front, back, source, tags - plus supplementary
   resources for gaps, before any of it goes into Anki. Nothing gets added without
   you saying yes.
5. Pushes the approved cards into a single deck via AnkiConnect, with a `Source` field
   on each card and clickable video links where found.

The full workflow and the reasoning behind it lives in [`SKILL.md`](SKILL.md).

## Requirements

- [Anki](https://apps.ankiweb.net/) desktop, running
- The [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on
- Claude Code
- Python 3 (for `assets/anki.py`)

## Install

On Windows, use PowerShell, Git Bash, or WSL, and substitute `~` with
`$env:USERPROFILE` if your shell doesn't expand it.

```bash
git clone https://github.com/joffreywallaart/lecture-to-anki.git ~/.claude/skills/lecture-to-anki
```

Merge [`permissions.json`](permissions.json) into `~/.claude/settings.json`
(`permissions.allow`) to avoid repeated permission prompts.

## Use

From a folder with lecture materials, describe the task ("turn this lecture into
Anki cards") or invoke `/lecture-to-anki` directly. The first time it runs it asks
which deck to use and records the choice in `CLAUDE.md`. Later runs reuse it.

## Design notes

- One deck per subject, not per course or per lecture. Tags carry the course/lecture/
  topic instead. Splitting into lots of decks is what breaks a daily review habit.
- Cards follow the usual spaced-repetition advice: atomic facts, short backs, clozes
  that test something real instead of guessable syntax. Worked examples are in
  [`assets/card_examples.md`](assets/card_examples.md).
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
