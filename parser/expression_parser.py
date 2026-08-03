from lexer.token_lists import TokenTypes
from parser.ast_entities import (
    ArrayExprNode,
    AssignExprNode,
    AtomicExprNode,
    CallExprNode,
    IndexExprNode,
    InfixExprNode,
    MemberAccessExprNode,
    PrefixExprNode,
    SuffixExprNode,
    TypeExprNode,
)
from utils.main import create_token, get_token_type

PREFIX = 100
LOWEST = 0


# Parser for expressions
class BasicPrattParser:
    def __init__(self):
        self.infix_parse_fnc = {}
        self.prefix_parse_fnc = {}

        self.prefix_parse_fnc[TokenTypes.INC] = self.parse_prefix_expr
        self.prefix_parse_fnc[TokenTypes.DEC] = self.parse_prefix_expr
        self.prefix_parse_fnc[TokenTypes.MIN] = self.parse_prefix_expr
        self.prefix_parse_fnc[TokenTypes.NOT] = self.parse_prefix_expr
        self.prefix_parse_fnc[TokenTypes.LBRACE] = self.parse_array_expr
        self.prefix_parse_fnc[TokenTypes.IDENT] = self.parse_atomic_expr
        self.prefix_parse_fnc[TokenTypes.INT] = self.parse_atomic_expr
        self.prefix_parse_fnc[TokenTypes.TRUE] = self.parse_atomic_expr
        self.prefix_parse_fnc[TokenTypes.FALSE] = self.parse_atomic_expr
        self.prefix_parse_fnc[TokenTypes.TYPE] = self.parse_type_expr
        self.prefix_parse_fnc[TokenTypes.LPAREN] = self.parse_grouped_expr
        self.prefix_parse_fnc[TokenTypes.FN] = self.parse_call_expr
        self.prefix_parse_fnc[TokenTypes.LT] = self.parse_list_expr

        self.infix_parse_fnc[TokenTypes.PLUS] = self.parse_infix_expr
        self.infix_parse_fnc[TokenTypes.MIN] = self.parse_infix_expr
        self.infix_parse_fnc[TokenTypes.MUL] = self.parse_infix_expr
        self.infix_parse_fnc[TokenTypes.DIVIDE] = self.parse_infix_expr
        self.infix_parse_fnc[TokenTypes.MOD] = self.parse_infix_expr
        self.infix_parse_fnc[TokenTypes.GTE] = self.parse_infix_expr
        self.infix_parse_fnc[TokenTypes.LTE] = self.parse_infix_expr
        self.infix_parse_fnc[TokenTypes.GT] = self.parse_infix_expr
        self.infix_parse_fnc[TokenTypes.LT] = self.parse_infix_expr
        self.infix_parse_fnc[TokenTypes.EQ] = self.parse_infix_expr
        self.infix_parse_fnc[TokenTypes.LBRACKET] = self.parse_index_expr

        self.infix_parse_fnc[TokenTypes.DOT] = self.parse_member_access_expr

        self.infix_parse_fnc[TokenTypes.ASSIGN] = self.parse_assign_expr

        self.infix_parse_fnc[TokenTypes.INC] = self.parse_suffix_expr
        self.infix_parse_fnc[TokenTypes.DEC] = self.parse_suffix_expr

        self.size = None
        self.cursor = None
        self.expr = None

    def parse_list_expr(self):
        self.next()
        # we can't use TokenTypes.GT because it's already registred as infixParseFunc
        return self.parse_comma_separated_list(TokenTypes.EOF)

    def parse_comma_separated_list(self, stopToken):
        values = []
        while get_token_type(self.pick()) != stopToken:
            if get_token_type(self.pick()) == TokenTypes.COMMA:
                self.next()
            expr = self.parse_expr(LOWEST)
            values.append(expr)
        return values

    def parse_index_expr(self, left):
        curr_token = self.pick()
        self.next()

        right = self.parse_expr(LOWEST)
        # skip RBRACKET
        self.next()
        return IndexExprNode(curr_token, left, right)

    def parse_array_expr(self):
        curr_token = self.pick()
        self.next()

        values = self.parse_comma_separated_list(TokenTypes.RBRACE)
        return ArrayExprNode(curr_token, values)

    def parse_assign_expr(self, left):
        curr_token = self.pick()
        self.next()

        right = self.parse_expr(LOWEST)
        return AssignExprNode(curr_token, left, right)

    def parse_member_access_expr(self, left):
        curr_token = self.pick()
        self.next()

        right = self.parse_expr(LOWEST)
        return MemberAccessExprNode(curr_token, left, right)

    def parse_call_expr(self):
        curr_token = self.pick()
        self.next()
        params = self.parse_comma_separated_list(TokenTypes.RPAREN)

        return CallExprNode(curr_token, params)

    def parse_grouped_expr(self):
        self.next()

        expr = self.parse_expr(LOWEST)  # "sucks" everything inside braces
        # There is no infix function for RBRACE so parse_expr will terminate after its appearance
        # Since the whole expr is now a  prefix, next() will be called so RBRACE token will be skipped

        return expr

    def parse_atomic_expr(self):
        curr_token = self.pick()
        return AtomicExprNode(curr_token)

    def parse_type_expr(self):
        curr_token = self.pick()
        return TypeExprNode(curr_token)

    def parse_prefix_expr(self):
        curr_token = self.pick()
        self.next()

        right = self.parse_expr(PREFIX)
        return PrefixExprNode(curr_token, right)

    def parse_suffix_expr(self, left):
        curr_token = self.pick()
        self.next()

        return SuffixExprNode(curr_token, left)

    def parse_infix_expr(self, left):
        token = self.pick()
        bp = self.get_infix_binding_power(get_token_type(token))
        self.next()

        right = self.parse_expr(bp)

        return InfixExprNode(token, left, right)

    def set_expr(self, expr: list):
        self.size = len(expr)
        self.cursor = 0
        self.expr = expr

    def next(self):
        self.cursor += 1

    def get_tokens_left(self):
        return self.cursor < self.size

    def pick(self):
        if not self.get_tokens_left():
            return create_token(TokenTypes.EOF)
        return self.expr[self.cursor]

    def parse_expr(self, min_bp):
        if not self.get_tokens_left():
            return None
        prefix_func = self.prefix_parse_fnc[get_token_type(self.pick())]
        left = prefix_func()
        self.next()
        curr_token = get_token_type(self.pick())
        if curr_token not in self.infix_parse_fnc:
            return left
        while self.get_tokens_left() and self.get_infix_binding_power(curr_token) > min_bp:
            infix_func = self.infix_parse_fnc[curr_token]
            left = infix_func(left)
            curr_token = get_token_type(self.pick())
        return left

    def get_infix_binding_power(self, op: TokenTypes) -> tuple[int, int]:
        match op:
            case TokenTypes.ASSIGN:
                return 2
            case TokenTypes.PLUS | TokenTypes.MIN:
                return 3
            case TokenTypes.MUL | TokenTypes.DIVIDE | TokenTypes.MOD:
                return 4
            case (
                TokenTypes.LTE
                | TokenTypes.GTE
                | TokenTypes.EQ
                | TokenTypes.LT
                | TokenTypes.GT
            ):
                return 5
            case TokenTypes.INC | TokenTypes.DEC | TokenTypes.LBRACKET:
                return 6
            case TokenTypes.DOT:
                return 7
            case _:
                return LOWEST
