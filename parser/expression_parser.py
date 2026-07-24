from typing import List, Tuple
from lexer.token_lists import TokenTypes
from parser.ast_entities import AtomicExprNode, CallExprNode, InfixExprNode, PrefixExprNode, SuffixExprNode
from utils.main import createToken, getTokenType

PREFIX = 100
LOWEST = 0

# Parser for expressions
class PrattParser:
    def __init__(self):
        self.infixParseFnc = {}
        self.prefixParseFnc = {}

        self.prefixParseFnc[TokenTypes.MIN] = self.parsePrefixExpr
        self.prefixParseFnc[TokenTypes.NOT] = self.parsePrefixExpr
        self.prefixParseFnc[TokenTypes.IDENT] = self.parseAtomicExpr
        self.prefixParseFnc[TokenTypes.INT] = self.parseAtomicExpr
        self.prefixParseFnc[TokenTypes.TRUE] = self.parseAtomicExpr
        self.prefixParseFnc[TokenTypes.FALSE] = self.parseAtomicExpr
        self.prefixParseFnc[TokenTypes.LPAREN] = self.parseGroupedExpr
        self.prefixParseFnc[TokenTypes.FN] = self.parseCallExpr

        self.infixParseFnc[TokenTypes.PLUS] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.MIN] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.MUL] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.DIVIDE] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.GTE] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.LTE] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.GT] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.LT] = self.parseInfixExpr
        self.infixParseFnc[TokenTypes.EQ] = self.parseInfixExpr

        self.infixParseFnc[TokenTypes.INC] = self.parseSuffixExpr
        self.infixParseFnc[TokenTypes.DEC] = self.parseSuffixExpr

        self.size = None
        self.cursor = None
        self.expr = None

    def parseCallExpr(self):
        currToken = self.pick()
        params = []
        self.next()
        while getTokenType(self.pick()) != TokenTypes.RPAREN:
            if getTokenType(self.pick()) == TokenTypes.COMMA:
                self.next()
            expr = self.parseExpr(LOWEST)
            params.append(expr)

        return CallExprNode(currToken, params)

    def parseGroupedExpr(self):
        self.next()

        expr = self.parseExpr(LOWEST) # "sucks" everything inside braces
        # There is no infix function for RBRACE so parseExpr will terminate after its appearance
        self.next()

        return expr

    def parseAtomicExpr(self):
        currToken = self.pick()
        return AtomicExprNode(currToken)

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


    def setExpr(self, expr: List):
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
    #getValue(2+2, 10)+6;
    def parseExpr(self, min_bp):
        if not self.getTokensLeft():
            return None
        prefixFunc = self.prefixParseFnc[getTokenType(self.pick())]
        left = prefixFunc()
        self.next()
        currToken = getTokenType(self.pick())
        if currToken not in self.infixParseFnc:
                return left
        while self.getTokensLeft() and  self.getInfixBindingPower(currToken) > min_bp:
            infixFunc = self.infixParseFnc[currToken]
            left = infixFunc(left)
            currToken = self.pick()
        return left
        

    def getInfixBindingPower(self, op: TokenTypes) -> Tuple[int,int]:
        match op:
            case TokenTypes.INC | TokenTypes.DEC:
                return 2
            case TokenTypes.PLUS | TokenTypes.MIN:
                return 3
            case TokenTypes.MUL | TokenTypes.DIVIDE:
                return 4
            case TokenTypes.LTE | TokenTypes.GTE | TokenTypes.EQ | TokenTypes.LT | TokenTypes.GT:
                return 5
            case _:
                return LOWEST