from lexer.token_lists import TokenTypes
from parser.ast_entities import (
    ArrayExprNode,
    AssignExprNode,
    AtomicExprNode,
    CallExprNode,
    IndexExprNode,
    InfixExprNode,
    PrefixExprNode,
    SuffixExprNode,
    TypeExprNode,
)
from utils.main import createToken, getTokenType

PREFIX = 100
LOWEST = 0


# Parser for expressions
class BasicPrattParser:
    def __init__(self):
        self.infixParseFnc = {}
        self.prefixParseFnc = {}

        self.prefixParseFnc[TokenTypes.INC] = self.parsePrefixExpr
        self.prefixParseFnc[TokenTypes.DEC] = self.parsePrefixExpr
        self.prefixParseFnc[TokenTypes.MIN] = self.parsePrefixExpr
        self.prefixParseFnc[TokenTypes.NOT] = self.parsePrefixExpr
        self.prefixParseFnc[TokenTypes.LBRACE] = self.parseArrayExpr
        self.prefixParseFnc[TokenTypes.IDENT] = self.parseAtomicExpr
        self.prefixParseFnc[TokenTypes.INT] = self.parseAtomicExpr
        self.prefixParseFnc[TokenTypes.TRUE] = self.parseAtomicExpr
        self.prefixParseFnc[TokenTypes.FALSE] = self.parseAtomicExpr
        self.prefixParseFnc[TokenTypes.TYPE] = self.parseTypeExpr
        self.prefixParseFnc[TokenTypes.LPAREN] = self.parseGroupedExpr
        self.prefixParseFnc[TokenTypes.FN] = self.parseCallExpr
        self.prefixParseFnc[TokenTypes.LT] = self.parseListExpr

        self.infixParseFnc[TokenTypes.PLUS] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.MIN] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.MUL] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.DIVIDE] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.MOD] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.GTE] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.LTE] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.GT] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.LT] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.EQ] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.LBRACKET] = self.parseIndexExpr

        self.infixParseFnc[TokenTypes.ASSIGN] = self.parseAssignExpr

        self.infixParseFnc[TokenTypes.INC] = self.parseSuffixExpr
        self.infixParseFnc[TokenTypes.DEC] = self.parseSuffixExpr

        self.size = None
        self.cursor = None
        self.expr = None

    def parseListExpr(self):
        self.next()
        # we can't use TokenTypes.GT because it's already registred as infixParseFunc
        return self.parseCommaSeparatedList(TokenTypes.EOF)

    def parseCommaSeparatedList(self, stopToken):
        values = []
        while getTokenType(self.pick()) != stopToken:
            if getTokenType(self.pick()) == TokenTypes.COMMA:
                self.next()
            expr = self.parseExpr(LOWEST)
            values.append(expr)
        return values

    def parseIndexExpr(self, left):
        currToken = self.pick()
        self.next()

        right = self.parseExpr(LOWEST)
        # skip RBRACKET
        self.next()
        return IndexExprNode(currToken, left, right)

    def parseArrayExpr(self):
        currToken = self.pick()
        self.next()

        values = self.parseCommaSeparatedList(TokenTypes.RBRACE)
        return ArrayExprNode(currToken, values)

    def parseAssignExpr(self, left):
        currToken = self.pick()
        self.next()

        right = self.parseExpr(LOWEST)
        return AssignExprNode(currToken, left, right)

    def parseCallExpr(self):
        currToken = self.pick()
        self.next()
        params = self.parseCommaSeparatedList(TokenTypes.RPAREN)

        return CallExprNode(currToken, params)

    def parseGroupedExpr(self):
        self.next()

        expr = self.parseExpr(LOWEST)  # "sucks" everything inside braces
        # There is no infix function for RBRACE so parseExpr will terminate after its appearance
        # Since the whole expr is now a  prefix, next() will be called so RBRACE token will be skipped

        return expr

    def parseAtomicExpr(self):
        currToken = self.pick()
        return AtomicExprNode(currToken)

    def parseTypeExpr(self):
        currToken = self.pick()
        return TypeExprNode(currToken)

    def parsePrefixExpr(self):
        currToken = self.pick()
        self.next()

        right = self.parseExpr(PREFIX)
        return PrefixExprNode(currToken, right)

    def parseSuffixExpr(self, left):
        currToken = self.pick()
        self.next()

        return SuffixExprNode(currToken, left)

    def parseInfixExpr(self, left):
        token = self.pick()
        bp = self.getInfixBindingPower(getTokenType(token))
        self.next()

        right = self.parseExpr(bp)

        return InfixExprNode(token, left, right)

    def setExpr(self, expr: list):
        self.size = len(expr)
        self.cursor = 0
        self.expr = expr

    def next(self):
        self.cursor += 1

    def getTokensLeft(self):
        return self.cursor < self.size

    def pick(self):
        if not self.getTokensLeft():
            return createToken(TokenTypes.EOF)
        return self.expr[self.cursor]

    def parseExpr(self, min_bp):
        if not self.getTokensLeft():
            return None
        prefixFunc = self.prefixParseFnc[getTokenType(self.pick())]
        left = prefixFunc()
        self.next()
        currToken = getTokenType(self.pick())
        if currToken not in self.infixParseFnc:
            return left
        while self.getTokensLeft() and self.getInfixBindingPower(currToken) > min_bp:
            infixFunc = self.infixParseFnc[currToken]
            left = infixFunc(left)
            currToken = getTokenType(self.pick())
        return left

    def getInfixBindingPower(self, op: TokenTypes) -> tuple[int, int]:
        match op:
            case TokenTypes.ASSIGN:
                return 1
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
            case _:
                return LOWEST
