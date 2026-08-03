from parser.expression_parser import BasicPrattParser


class VectorPrattParser:
    def __init__(self, pratt_parser: BasicPrattParser):
        self.pratt_parser = pratt_parser

    def set_expr(self, *args, **kwargs):
        return self.pratt_parser.set_expr(*args, **kwargs)

    def parse_expr(self, *args, **kwargs):
        return self.pratt_parser.parse_expr(*args, **kwargs)
