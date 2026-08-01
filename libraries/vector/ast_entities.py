from parser.ast_entities import ExprNode


class VectorExprNode(ExprNode):
    def __init__(self, tok=None, values=None) -> None:
        super().__init__(tok)
        if values == None:
            values = []
        self.values = values