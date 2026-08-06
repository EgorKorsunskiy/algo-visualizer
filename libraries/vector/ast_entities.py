from parser.ast_entities import ExprNode


class VectorType(ExprNode):
    def __init__(self, tok=None, type=None) -> None:
        super().__init__(tok)
        self.type = type


class VectorExprNode(ExprNode):
    def __init__(self, tok=None, values=None, type=None) -> None:
        super().__init__(tok)
        if values == None:
            values = []
        self.values = values
        self.type = type
