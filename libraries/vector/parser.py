from lexer.token_lists import TokenTypes
from libraries.vector.ast_entities import VectorExprNode, VectorType
from libraries.vector.constants import VECTOR_KEYWORD, VECTOR_TYPES
from libraries.vector.expression_parser import VectorPrattParser
from parser.ast_entities import ArrayExprNode, InitStmt
from parser.expression_parser import BasicPrattParser
from parser.main import BasicParser
from utils.main import get_token_type
from walker.log import VAR_TYPE


class VectorParser:
    def __init__(self, parser: BasicParser) -> None:
        self.parser = parser
        self.parser.pratt_parser = VectorPrattParser(BasicPrattParser())

        self.original_parse_init_stmt = parser.parse_init_stmt
        self.original_parse_init_left_side = parser.parse_init_left_side
        self.original_parse_stmt = parser.parse_stmt

    def parse_init_left_side(self):
        if self.parser.pick()["value"] == VECTOR_KEYWORD:
            init_type_tok = self.parser.pick()
            self.parser.next()
            self.parser.expect(TokenTypes.LT)
            self.parser.next()
            self.parser.indicate_chunk(TokenTypes.GT, TokenTypes.LT)
            vector_type = self.parser.parse_expr()
            self.parser.expect(TokenTypes.GT)
            self.parser.next()
            init_name_tok = self.parser.pick()
            init_node = InitStmt()
            init_node.type = VectorType(init_type_tok, vector_type)
            init_node.name = init_name_tok
            init_node.length = -1

            type_key = ""
            curr_vector_type = init_node.type

            while isinstance(curr_vector_type, VectorType):
                type_key += curr_vector_type.tok["value"]
                curr_vector_type = curr_vector_type.type

            init_node.type_class = VECTOR_TYPES.get(type_key, VAR_TYPE.VECTOR)
            return init_node
        else:
            return self.original_parse_init_left_side()

    def _get_vector_copy(self, values):
        new_values = []
        for value in values:
            if not isinstance(value, ArrayExprNode):
                new_values.append(value)
            else:
                vector_copy = VectorExprNode(
                    value.tok, self._get_vector_copy(value.values), value.type
                )
                new_values.append(vector_copy)
        return new_values

    def parse_init_stmt(self):
        init_stmt = self.original_parse_init_stmt()
        if isinstance(init_stmt.value, ArrayExprNode) and isinstance(
            init_stmt.type, VectorType
        ):
            new_value = VectorExprNode(
                init_stmt.value.tok,
                self._get_vector_copy(init_stmt.value.values),
                init_stmt.type,
            )
            init_stmt.value = new_value
        return init_stmt

    def parse_stmt(self):
        if (
            get_token_type(self.parser.pick()) == TokenTypes.IDENT
            and self.parser.pick()["value"] == VECTOR_KEYWORD
        ):
            return self.parse_init_stmt()
        else:
            return self.original_parse_stmt()

    def parse(self, *args, **kwargs):
        self.parser.parse_stmt = self.parse_stmt
        self.parser.parse_init_stmt = self.parse_init_stmt
        self.parser.parse_init_left_side = self.parse_init_left_side
        return self.parser.parse(*args, **kwargs)
