from parser.expression_parser import BasicPrattParser


class VectorPrattParser:
    def __init__(self, prattParser: BasicPrattParser):
        self.prattParser = prattParser

    def setExpr(self, *args, **kwargs):
        return self.prattParser.setExpr(*args, **kwargs)

    def parseExpr(self, *args, **kwargs):
        return self.prattParser.parseExpr(*args, **kwargs)
