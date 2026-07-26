from lexer.token_lists import TokenTypes
from parser.ast_entities import (
    BlockStmt,
    ConditionStmt,
    FuncStatement,
    IfStmt,
    InitStmt,
    LoopStmt,
    ProgrammeNode,
    ReturnStatement,
)
from parser.expression_parser import LOWEST, PrattParser
from utils.main import getTokenType


class ExpectedError(Exception):
    def __init__(self, token, given) -> None:
        self.message = f"Expected {token}, but given {given}"
        super().__init__(self.message)


class Parser:
    def __init__(self) -> None:
        self.prattParser = PrattParser()
        self.tokens = []
        self.cursor = 0

    def tokens_left(self):
        return self.cursor < len(self.tokens)

    def pick(self):
        return self.tokens[self.cursor]

    def peekN(self, n):
        # returns nth lookahead token, if it exists
        if self.cursor + n < len(self.tokens):
            return self.tokens[self.cursor + n]

    def next(self, n=1):
        self.cursor += n
        if not self.tokens_left():
            raise Exception("Tried to access token outside of the range")

    def expect(self, tok):
        if getTokenType(self.pick()) != tok:
            raise ExpectedError(tok, getTokenType(self.pick()))

    def indicateBody(self):
        # inserts special PARSE_BREAK before the end of a current body
        bracesCnt = 0
        i = 0
        # TODO: quite dangerous statement :). Probably need to be changed
        while True:
            if getTokenType(self.peekN(i)) == TokenTypes.LBRACE:
                bracesCnt += 1
            elif getTokenType(self.peekN(i)) == TokenTypes.RBRACE:
                bracesCnt -= 1
            if bracesCnt < 0:
                break
            i += 1
        self.tokens.insert(self.cursor + i, {"token_type": TokenTypes.PARSE_BREAK})

    def indicateChunk(self, stopToken):
        i = 0
        # TODO: quite dangerous statement :). Probably need to be changed
        while True:
            if getTokenType(self.peekN(i)) == stopToken:
                break
            i += 1
        self.tokens.insert(self.cursor + i, {"token_type": TokenTypes.PARSE_BREAK})

    def parseBody(self):
        bodyStmts = []
        while getTokenType(self.pick()) != TokenTypes.PARSE_BREAK:
            stmt = self.parseStmt()

            if stmt != None:
                bodyStmts.append(stmt)
        self.next()  # skip PARSE_BREAK
        self.next()  # skip closing RBRACE
        return BlockStmt(bodyStmts)

    def parseInitLeftSide(self):
        # TODO: add support for pointers && probably different flow for func args
        initTypeTok = self.pick()
        self.next()
        self.expect(TokenTypes.IDENT)
        initNameTok = self.pick()
        initLength = None
        if getTokenType(self.peekN(1)) == TokenTypes.LBRACKET:
            self.next()
            self.next()
            self.indicateChunk(TokenTypes.RBRACKET)
            initLength = self.parseExpr()

        initNode = InitStmt()
        initNode.type = initTypeTok
        initNode.name = initNameTok
        initNode.length = initLength
        return initNode

    def parseExpr(self):
        expr = []
        while getTokenType(self.pick()) not in [
            TokenTypes.SEMICOL,
            TokenTypes.PARSE_BREAK,
        ]:
            expr.append(self.pick())
            self.next()
        self.next()
        self.prattParser.setExpr(expr)
        exprAST = self.prattParser.parseExpr(LOWEST)
        return exprAST

    def parseInitStmt(self):
        initNode = self.parseInitLeftSide()
        self.next()
        self.expect(TokenTypes.ASSIGN)
        self.next()
        exprAST = self.parseExpr()
        initNode.value = exprAST
        return initNode

    def parseFuncDeclarationStmt(self):
        funcStmt = FuncStatement()
        funcStmt.type = self.pick()
        self.next()
        self.expect(TokenTypes.FN)
        funcStmt.name = self.pick()
        self.next()
        args = []
        while getTokenType(self.pick()) != TokenTypes.RPAREN:
            if getTokenType(self.pick()) == TokenTypes.COMMA:
                self.next()
            argNode = self.parseInitLeftSide()
            args.append(argNode)
            self.next()
        self.next()
        self.expect(TokenTypes.LBRACE)
        self.next()
        self.indicateBody()
        bodyStmts = self.parseBody()

        funcStmt.args = args
        funcStmt.body = bodyStmts
        return funcStmt

    def parseWhileStmt(self):
        self.next()
        self.expect(TokenTypes.LPAREN)
        self.next()
        expr = []
        while getTokenType(self.pick()) != TokenTypes.RPAREN:
            expr.append(self.pick())
            self.next()
        self.prattParser.setExpr(expr)
        exprAST = self.prattParser.parseExpr(LOWEST)
        self.next()
        self.expect(TokenTypes.LBRACE)
        self.next()
        self.indicateBody()
        bodyStmts = self.parseBody()
        loopNode = LoopStmt()
        loopNode.condition = exprAST
        loopNode.body = bodyStmts
        return loopNode

    def parseForStmt(self):
        self.next()
        self.expect(TokenTypes.LPAREN)
        self.next()
        expr = []
        self.indicateChunk(TokenTypes.RPAREN)
        while getTokenType(self.pick()) != TokenTypes.RPAREN:
            if getTokenType(self.pick()) == TokenTypes.SEMICOL:
                self.next()
            expr.append(self.parseStmt())
        self.next()
        self.expect(TokenTypes.LBRACE)
        self.next()
        self.indicateBody()
        bodyStmts = self.parseBody()
        loopNode = LoopStmt()
        loopNode.condition = expr
        loopNode.body = bodyStmts
        return loopNode

    def parseConditionStmt(self):
        self.next()
        self.expect(TokenTypes.LPAREN)
        self.next()
        expr = []
        while getTokenType(self.pick()) != TokenTypes.RPAREN:
            expr.append(self.pick())
            self.next()
        self.prattParser.setExpr(expr)
        exprAST = self.prattParser.parseExpr(LOWEST)
        self.next()
        self.expect(TokenTypes.LBRACE)
        self.next()
        self.indicateBody()
        thenBodyStmts = self.parseBody()
        conditionStmt = ConditionStmt()
        conditionStmt.condition = exprAST
        conditionStmt.thenBody = thenBodyStmts
        return conditionStmt

    def parseIfStmt(self):
        conditionStmt = self.parseConditionStmt()
        alterntatives = BlockStmt()
        rejectBody = BlockStmt()

        while getTokenType(self.pick()) == TokenTypes.ELIF:
            alterntatives.stmts.append(self.parseConditionStmt())
        if getTokenType(self.pick()) == TokenTypes.ELSE:
            self.next()
            self.expect(TokenTypes.LBRACE)
            self.next()
            self.indicateBody()
            rejectBody = self.parseBody()

        ifStmt = IfStmt()
        ifStmt.condition = conditionStmt.condition
        ifStmt.thenBody = conditionStmt.thenBody
        ifStmt.alternatives = alterntatives
        ifStmt.rejectBody = rejectBody
        return ifStmt

    def parseReturnStmt(self):
        self.next()
        expr = self.parseExpr()
        return ReturnStatement(expr)

    def parseStmt(self):
        match getTokenType(self.pick()):
            case TokenTypes.TYPE:
                if getTokenType(self.peekN(1)) == TokenTypes.FN:
                    return self.parseFuncDeclarationStmt()
                else:
                    return self.parseInitStmt()
            case TokenTypes.FOR:
                return self.parseForStmt()
            case TokenTypes.WHILE:
                return self.parseWhileStmt()
            case TokenTypes.IF:
                return self.parseIfStmt()
            case TokenTypes.RETURN:
                return self.parseReturnStmt()
            case TokenTypes.PARSE_BREAK:
                return
            case _:
                return self.parseExpr()

    def parse(self, tokens) -> ProgrammeNode:
        self.cursor = 0
        self.tokens = tokens
        head_node = ProgrammeNode()

        while self.tokens_left() and getTokenType(self.pick()) != TokenTypes.EOF:
            stmt = self.parseStmt()
            if stmt != None:
                head_node.stmts.append(stmt)

        return head_node
