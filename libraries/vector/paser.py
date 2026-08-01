from lexer.token_lists import TokenTypes
from libraries.vector.ast_entities import VectorExprNode
from libraries.vector.expression_parser import VectorPrattParser
from parser.ast_entities import ArrayExprNode, InitStmt
from parser.expression_parser import BasicPrattParser
from parser.main import BasicParser
from utils.main import getTokenType
from walker.log import VAR_TYPE


class VectorParser:
    def __init__(self, parser: BasicParser) -> None:
        self.keyword = "vector"
        self.parser = parser
        self.parser.prattParser = VectorPrattParser(BasicPrattParser())

        self.original_parsInitStmt = parser.parseInitStmt
        self.original_parseInitLeftSide = parser.parseInitLeftSide
        self.original_parseStmt = parser.parseStmt

    def parseInitLeftSide(self):
        if self.parser.pick()["value"] == self.keyword:
            initTypeTok = self.parser.pick()
            self.parser.next()
            self.parser.expect(TokenTypes.LT)
            self.parser.indicateChunk(TokenTypes.GT)
            _ = self.parser.parseExpr()
            self.parser.expect(TokenTypes.GT)
            self.parser.next()
            initNameTok = self.parser.pick()
            initNode = InitStmt()
            initNode.type = initTypeTok
            initNode.name = initNameTok
            initNode.length = -1
            initNode.typeClass = VAR_TYPE.VECTOR
            return initNode
        else:
            return self.original_parseInitLeftSide()

    def parseInitStmt(self):
        initStmt = self.original_parsInitStmt()
        if (
            isinstance(initStmt.value, ArrayExprNode)
            and initStmt.type["value"] == self.keyword
        ):
            newValue = VectorExprNode(initStmt.value.tok, initStmt.value.values)
            initStmt.value = newValue
        return initStmt

    def parseStmt(self):
        if (
            getTokenType(self.parser.pick()) == TokenTypes.IDENT
            and self.parser.pick()["value"] == self.keyword
        ):
            return self.parseInitStmt()
        else:
            return self.original_parseStmt()

    def parse(self, *args, **kwargs):
        self.parser.parseStmt = self.parseStmt
        self.parser.parseInitStmt = self.parseInitStmt
        self.parser.parseInitLeftSide = self.parseInitLeftSide
        return self.parser.parse(*args, **kwargs)
