# Parser

Turns the token list produced by the lexer into an AST.

## How it works

`BasicParser` is a hand-written recursive-descent (top-down, LL(2)) parser
that walks the token list with a cursor. `parse_stmt` looks at the current
token (and sometimes one token ahead via `peek_n`) to decide which kind of
statement it's looking at — variable init, function declaration, `if`,
`for`/`while`, `return`, or a bare expression — and dispatches to a
dedicated `parse_*_stmt` method.

Block bodies (`{ ... }`) are handled with a small trick: before parsing a
body, `indicate_body`/`indicate_chunk` scans ahead to find the matching
closing brace (accounting for nested braces) and inserts a synthetic
`PARSE_BREAK` token right before it. `parse_body` then just parses statements
until it hits `PARSE_BREAK`. The same idea is reused for other bounded chunks, such as array dimensions
in `[...]` or the type argument of a hint in `<...>`.

Expressions are not parsed by the statement parser directly. Whenever a
statement needs an expression, the surrounding tokens are collected into a
sub-list and handed off to the **Pratt parser** in `expression_parser.py`,
which understands operator precedence.

### Pratt parser (`expression_parser.py`)

`BasicPrattParser` implements a standard Pratt/precedence-climbing parser:
each token type has an optional prefix parse function (for things that can
start an expression: literals, unary `-`/`!`, grouped `(...)`, array
literals, function calls, ...) and an optional infix parse function (for
things that continue an expression: binary operators, `[]` indexing, `.`
member access, assignment, postfix `++`/`--`). `parse_expr(min_bp)` picks a
prefix function to get a left-hand value, then keeps consuming infix
operators as long as their binding power (`get_infix_binding_power`) is
higher than `min_bp`, recursing for the right-hand side. This is what gives
correct precedence (e.g. `*` before `+`) without an explicit grammar.

Both parsers produce nodes defined in `ast_entities.py` and combine into one
tree, rooted at a `ProgrammeNode`, that the walker later evaluates.

## Files

- `main.py` — `BasicParser`, the statement-level parser.
- `expression_parser.py` — `BasicPrattParser`, the expression-level parser.
- `ast_entities.py` — AST node classes for both statements (`InitStmt`,
  `LoopStmt`, `IfStmt`, `FuncStatement`, `HintStatement`, ...) and
  expressions (`InfixExprNode`, `CallExprNode`, `IndexExprNode`, ...).