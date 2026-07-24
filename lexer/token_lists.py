from binascii import Incomplete
from enum import Enum,auto

class TokenTypes(Enum):
    # operations
    MUL = auto()
    DIVIDE = auto()
    MIN = auto()
    PLUS = auto()
    ASSIGN = auto()
    EQ = auto()
    NEQ = auto()
    GTE = auto()
    LTE = auto()
    GT = auto()
    LT = auto()
    INC = auto()
    DEC = auto()
    # syntax tokens
    SEMICOL = auto()
    COMMA = auto()
    RBRACE = auto()
    LBRACE = auto()
    RPAREN = auto()
    LPAREN = auto()
    NOT = auto()
    QUOTE = auto()
    DOUBLE_QUOTE = auto()
    # keywords
    TYPE = auto()
    FOR = auto()
    WHILE = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    RETURN = auto()
    BREAK = auto()
    CONTINUE = auto()
    # every number is int & every string is IDENT. It's up to parser to determine which is identifier and which is literal
    IDENT = auto()
    INT = auto()
    TRUE = auto()
    FALSE = auto()
    # internal tokens
    PARSE_BREAK = auto()
    EOF = auto()
    FN = auto()

string_to_token_map = {
    "for": {"token_type": TokenTypes.FOR},
    "while": {"token_type": TokenTypes.WHILE},
    "if": {"token_type": TokenTypes.IF},
    "else": {"token_type": TokenTypes.ELSE},
    "int": {"token_type": TokenTypes.TYPE},
    "float": {"token_type": TokenTypes.TYPE},
    "bool": {"token_type": TokenTypes.TYPE},
    "string": {"token_type": TokenTypes.TYPE},
    "char": {"token_type": TokenTypes.TYPE},
    "void": {"token_type": TokenTypes.TYPE},
    "return": {"token_type": TokenTypes.RETURN},
    "break": {"token_type": TokenTypes.BREAK},
    "continue": {"token_type": TokenTypes.CONTINUE},
    "ident": {"token_type": TokenTypes.IDENT},
    "true": {"token_type": TokenTypes.TRUE},
    "false": {"token_type": TokenTypes.FALSE},
    "=": {"token_type": TokenTypes.ASSIGN},
    ">": {"token_type": TokenTypes.GT},
    "<": {"token_type": TokenTypes.LT},
    "+": {"token_type": TokenTypes.PLUS},
    "-": {"token_type": TokenTypes.MIN},
    "*": {"token_type": TokenTypes.MUL},
    "/": {"token_type": TokenTypes.DIVIDE},
    ";": {"token_type": TokenTypes.SEMICOL},
    ",": {"token_type": TokenTypes.COMMA},
    "{": {"token_type": TokenTypes.LBRACE},
    "}": {"token_type": TokenTypes.RBRACE},
    "(": {"token_type": TokenTypes.LPAREN},
    ")": {"token_type": TokenTypes.RPAREN},
    "!": {"token_type": TokenTypes.NOT},
    "'": {"token_type": TokenTypes.QUOTE},
    '"': {"token_type": TokenTypes.DOUBLE_QUOTE},
}

merge_rules = {
    f'{TokenTypes.LT}_{TokenTypes.ASSIGN}': {"token_type": TokenTypes.LTE},
    f'{TokenTypes.GT}_{TokenTypes.ASSIGN}': {"token_type": TokenTypes.GTE},
    f'{TokenTypes.ASSIGN}_{TokenTypes.ASSIGN}': {"token_type": TokenTypes.EQ},
    f'{TokenTypes.NOT}_{TokenTypes.ASSIGN}': {"token_type": TokenTypes.NEQ},
    f'{TokenTypes.PLUS}_{TokenTypes.PLUS}': {"token_type": TokenTypes.INC},
    f'{TokenTypes.MIN}_{TokenTypes.MIN}': {"token_type": TokenTypes.DEC},
    f'{TokenTypes.ELSE}_{TokenTypes.IF}': {"token_type": TokenTypes.ELIF},
    f'{TokenTypes.IDENT}_{TokenTypes.LPAREN}': {"token_type": TokenTypes.FN},
    f'{TokenTypes.IDENT}_{TokenTypes.LPAREN}': {"token_type": TokenTypes.FN},
    f'{TokenTypes.QUOTE}_{TokenTypes.IDENT}': {"token_type": TokenTypes.IDENT},
    f'{TokenTypes.DOUBLE_QUOTE}_{TokenTypes.IDENT}': {"token_type": TokenTypes.IDENT},
    f'{TokenTypes.IDENT}_{TokenTypes.QUOTE}': {"token_type": TokenTypes.IDENT},
    f'{TokenTypes.IDENT}_{TokenTypes.DOUBLE_QUOTE}': {"token_type": TokenTypes.IDENT},
}
