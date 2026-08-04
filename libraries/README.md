# Libraries

Implementations of C++ standard-library features (things you'd normally get
via `#include <name>`) that aren't part of the core language and are instead
bolted onto the core lexer/parser/walker.

## How it works

The core `BasicParser` and `BasicWalker` know nothing about `vector` or any
other library type — they only understand primitive types and arrays. Each
library here wraps a core parser/walker instance and **monkey-patches** the
methods it needs to change, while falling back to the original method for
everything else. `libraries/main.py` is the composition point: it wires
`VectorParser` around a `BasicParser` and `VectorWalker` around a
`BasicWalker`, and exposes `Parser`/`Walker` factory functions that the rest
of the program uses instead of instantiating the core classes directly. This
keeps the core interpreter generic and lets library support be added or
removed without touching it.

`unions.py` acts as a registry: it maps a `VAR_TYPE` (e.g. `VAR_TYPE.VECTOR`)
to the dict of builtin functions available on values of that type
(`size()`, `push_back()`, ...). The walker's member-access evaluator
(`eval_member_access_expr` in `walker/main.py`) looks a call up here at
runtime based on the evaluated value's tracked type.

## Structure

- `main.py` — composes the library-patched `Parser`/`Walker`.
- `unions.py` — type -> builtin-function-table registry, used at call time.
- `vector/` — the `vector<T>` implementation