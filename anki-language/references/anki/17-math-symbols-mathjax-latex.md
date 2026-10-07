# 17 — Math, Symbols, MathJax, and LaTeX

This workflow focuses on languages, but the Anki reference library covers math/symbol rendering for completeness and for mixed-material decks.

## MathJax

Modern Anki supports MathJax-style mathematical notation in cards.

Use MathJax when:
- equations need scalable rendering;
- mathematical symbols/formulas are part of the content;
- portability across clients is important.

## LaTeX

Anki also supports LaTeX workflows, but they may require external LaTeX tooling depending on the feature/path used.

For new content, verify the current official recommendation before building a LaTeX-dependent deck.

## Template interaction

Math/symbol content still follows normal template rules:
- keep data in fields;
- use templates for layout;
- avoid dynamic media hacks;
- test target clients.

## Language learning

MathJax/LaTeX is normally unnecessary for language cards. Do not introduce it unless the source material truly requires mathematical/scientific notation.

## Sources

- https://docs.ankiweb.net/manual/math
- https://docs.ankiweb.net/faqs/customizing-mathjax
