from enum import Enum, auto
from lexer.token_lists import TokenTypes


class GrammarTypes(Enum):
    EXPR = auto()
    BODY = auto()


grammar_rules = {
    TokenTypes.FOR: [
        TokenTypes.FOR,
        TokenTypes.LPAREN,
        GrammarTypes.EXPR,
        TokenTypes.SEMICOL,
        GrammarTypes.EXPR,
        TokenTypes.SEMICOL,
        GrammarTypes.EXPR,
        TokenTypes.RPAREN,
        TokenTypes.LBRACE,
        GrammarTypes.BODY,
        TokenTypes.RBRACE,
    ],
    TokenTypes.ASSIGN: [TokenTypes.ASSIGN, GrammarTypes.EXPR, TokenTypes.SEMICOL],
}
