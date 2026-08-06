# Tests

Unit tests for the interpreter, organized by the component they exercise,
plus shared comparison helpers used across all of them.

## How it works

Because raw AST nodes and tokens are generally hard to work with, `test_utils.py` provides small helpers the tests rely on:
`compare_tokens`/`compare_lists` compare tokens or lists field by field
(recursing into nested lists), and `in_order_traverse_AST` flattens an
expression tree into a list so a parsed expression can be checked against an
expected sequence of nodes without hand-writing the tree shape.

Each subdirectory targets one pipeline stage and mirrors the source layout:

- `lexer/lexer_test.py` — feeds source snippets into `Lexer.parse` (and the
  merge pass) and asserts on the resulting token list, including that
  multi-character operators and keywords are merged/classified correctly.
- `parser/parser_test.py` — feeds token lists into `BasicParser` and asserts
  on the resulting AST shape for statements and expressions (precedence,
  nested blocks, function declarations, etc.).
- `walker/walker_test.py` — evaluates small programs end-to-end (or evaluates
  ASTs directly) and asserts on the resulting values and side effects
  (variable state, control flow).
- `walker/log_test.py` — asserts that evaluating a program produces the
  expected sequence of `Log` records (sets, inserts, loop/branch markers).

## Files

- `test_utils.py` — shared comparison/traversal helpers described above.
- `lexer/`, `parser/`, `walker/` — per-component test suites.