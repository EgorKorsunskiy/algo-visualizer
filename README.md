# Description

This repository contains a lexer, parser, and evaluator for a subset of C++ syntax written in Python. 
The main goal of this project is to interpret C++ code and generate meaningful logs based on the program's execution flow.

## Project structure
- `lexer` directory contains the lexer and the list of token definitions. It also defines a set of merge rules used to combine two neighboring tokens, which simplifies the parser logic.
- `parser` directory contains two parsers: a general top-down LL(2) parser and a Pratt parser used for parsing expressions while taking operator precedence into account. Both parsers accept a list of tokens as input. Their combined output is an AST that is evaluated later.
- `walker` directory contains a tree-walking evaluator. It receives the AST and evaluates it, performing Python type conversions and built-in function calls in the background. Declared variables, functions, and other objects are stored in an Environment class and managed by the Walker.
- `walker/log.py` file contains the `Log` class, which is used to store the execution history of the program.
- `tests` directory contains unit tests for the `Lexer`, `Parser`, `Walker`, and `Log` components.
- `libraries` directory contains implementations of additional C++ features that are normally provided via `#include <name>`, such as vector. These features are integrated into the existing system using monkey patching.

Additionally, each directory has its own README.md file where the logic is described in greater detail.

## How to run
Current root `main.py` file contains an example of how to combine and use different pieces of interpreter's logic.
It's recommended to use `uv` project manager, though it's perfectly possible to run it using `pip`. The steps below use `uv`.
- `uv sync` - this creates a virtual environment if none exitsted before and installs there all the project dependencies
- `uv run main.py`
To manually run the tests, the following command can be used:
- `uv run python -m pytest`

## Limitations
Error handling throughout the project is minimal. This is a deliberate trade-off — the interpreter 
currently assumes it's being fed syntactically valid C++ subset code, rather than trying to report malformed input.