# Card design — worked examples

Concrete good-vs-bad cards for each principle in Step 2. The examples below use logic/proof-technique material, but the principles are subject- and language-independent. Write the cards themselves in whatever language the source material uses.

## Atomic: one fact per card

**Bad** (two facts bundled — you can't grade them independently):
> Front: What are a proposition and a tautology?
> Back: A proposition is true or false; a tautology is always true.

**Good** (split into two notes):
> Front: What is a proposition? → Back: A statement that is either true or false, but not both.
> Front: What is a tautology? → Back: A proposition that is true under every valuation.

## Meaningful clozes: blank the load-bearing part

**Bad** (clozes trivial syntax — guessable from context):
> The implication p {{c1::→}} q is false when p is true {{c2::and}} q is false.

**Good** (clozes the actual rule being tested):
> The implication p → q is false if and only if p is {{c1::true}} and q is {{c2::false}}.

The two clozes target independent facts (the truth value of p, the truth value of q), so Anki makes two separate single-blank cards — exactly what you want.

## Standalone context: no orphans

**Bad** (depends on lecture order — meaningless in six months):
> Front: What was the third rule from lecture 1?

**Good** (names the rule):
> Front: What does the contrapositive equivalence state? → Back: p → q is logically equivalent to ¬q → ¬p.

## Type selection

- **Cloze** — formulas, crisp definitions, formal laws. Example: the implication truth condition above.
- **Basic** — pattern matching, judgment, translation, where a cloze boundary would feel forced. Example:
  > Front: Translate into logic: "If it rains, I get wet." → Back: rains → wet

## Clean backs

**Bad:**
> Back: Great question! So really what it comes down to is that the implication is only false in that one case, namely...

**Good:**
> Back: Only when p is true and q is false.

## Math notation: LaTeX once there's real structure

**Fine as plain Unicode** (single glyphs, nothing to typeset):
> Front: What symbol denotes logical negation? → Back: ¬

**Bad** (a real formula forced into Unicode — the exponent and fraction both go flat and ambiguous):
> Front: What is the Gaussian PDF? → Back: f(x) = 1/(σ√(2π)) · e^-(x-μ)²/(2σ²)

**Bad** (LaTeX, but clozing the whole formula — Anki's cloze parser stops at the *first* `}}` it finds, which lands mid-formula inside `\frac{1}{\sigma\sqrt{2\pi}}`, not at the intended end):
> Text: The Gaussian PDF is {{c1::\(f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}\)}}

**Good** (Basic — recalling a whole formula from its name is a translation task, same as the logic-translation example above, and Basic fields aren't cloze-parsed so nested LaTeX braces can't collide with anything):
> Front: State the Gaussian PDF. → Back: \(f(x) = \dfrac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}\)

Same `\(...\)` / `\[...\]` markup works unchanged in both the quiz and the pushed card — write it once. Reserve Cloze for LaTeX only when the blanked span is brace-free (e.g. a single variable or exponent digit); anything with its own `\frac`/`\sqrt` nested inside risks the same `}}` collision.
