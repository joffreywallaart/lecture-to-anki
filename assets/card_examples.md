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
