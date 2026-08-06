from lexer.token_lists import TokenTypes
from libraries.vector.ast_entities import VectorType
from libraries.vector.constants import VECTOR_KEYWORD
from parser.expression_parser import LOWEST, BasicPrattParser


class VectorPrattParser:
    def __init__(self, pratt_parser: BasicPrattParser):
        self.pratt_parser = pratt_parser
        self.pratt_parser.prefix_parse_fnc[TokenTypes.IDENT] = (
            self.parse_ident_atomic_expr
        )

    def parse_ident_atomic_expr(self):
        curr_token = self.pratt_parser.pick()
        if curr_token["value"] == VECTOR_KEYWORD:
            self.pratt_parser.next()
            local_pratt_parser = BasicPrattParser()
            local_tokens = []

            count = -1
            for i in range(self.pratt_parser.cursor, len(self.pratt_parser.expr)):
                if self.pratt_parser.expr[i] == TokenTypes.GT:
                    count -= 1
                elif self.pratt_parser.expr[i] == TokenTypes.LT:
                    count += 1
                if count < 0:
                    break
                self.pratt_parser.next()
                local_tokens.append(self.pratt_parser.expr[i])
            self.pratt_parser.next()
            self.pratt_parser.next()

            local_pratt_parser.set_expr(local_tokens)
            vector_type = VectorType(curr_token)
            vector_type.type = local_pratt_parser.parse_expr(LOWEST)
            return vector_type
        else:
            return self.pratt_parser.parse_atomic_expr()

    def set_expr(self, *args, **kwargs):
        return self.pratt_parser.set_expr(*args, **kwargs)

    def parse_expr(self, *args, **kwargs):
        return self.pratt_parser.parse_expr(*args, **kwargs)
