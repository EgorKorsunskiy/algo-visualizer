# Walker

Tree-walking evaluator: takes the AST produced by the parser and executes it,
producing both a return value and a log of what happened during execution.

## How it works

`BasicWalker.eval` is a single dispatch method that pattern-matches on the
AST node type and delegates to a matching `eval_*` method (e.g.
`InfixExprNode` -> `eval_infix_expr`, `IfStmt`/`ConditionStmt` ->
`eval_condition_stmt`). Each `eval_*` method knows how to evaluate that one
kind of node, recursing into `self.eval` for its children. Values are plain
Python values (`int`, `bool`, `list`, ...) — the walker leans on Python's own
types and operators wherever possible instead of a custom value system.

Variable/function storage is handled by `Environment` (`environment.py`): a
simple `{name: value}` dict with a pointer to an `outer` environment, forming
a chain. Looking a name up (`get`) walks outward until it's found; setting a
name recursively (`set(..., recursive=True)`) walks outward to find where it
already lives and updates it there, which is how mutation of an outer-scope
variable from inside a loop or function works. Each function call and each
`for` loop gets its own child `Environment` so their locals don't leak out.
Control flow signals such as "a `return` happened" are also passed through
the environment via a special `_returned` key that block/loop evaluators
check after every statement.

Every state-changing operation (assigning a variable, inserting into an
array, entering a loop or branch, ...) is additionally recorded through
`self.log`, an instance of `Log` (`log.py`). `Log` doesn't interpret
anything — it just appends structured tuples (record type, command type,
variable type, name, value, ...) describing what happened, in order. This
log is the "meaningful execution log" the project description refers to; it
can be replayed/rendered elsewhere without re-running the program.

## Files

- `main.py` — `BasicWalker`, the evaluator described above.
- `environment.py` — `Environment`, the scope-chain variable store.
- `log.py` — `Log` and the enums (`COMMAND_TYPE`, `VAR_TYPE`, `HINT_TYPE`,
  ...) used to classify log entries.