import pytest

from lexer.main import Lexer
from lexer.token_lists import TokenTypes
from libraries.main import Parser
from libraries.vector.ast_entities import VectorExprNode
from parser.ast_entities import (
    AtomicExprNode,
)
from tests.test_utils import compare_lists, in_order_traverse_AST
from utils.main import create_token
from walker.log import VAR_TYPE


@pytest.fixture
def lexer():
    return Lexer()


@pytest.fixture
def parser():
    return Parser()


class TestParser:
    def _get_ast(self, lexer, parser, input):
        tokens = lexer.parse(input)
        tokens = lexer.tokens_merge_helper(tokens)
        return parser.parse(tokens)

    def _run_and_compare_expr(self, lexer, parser, input, expected, expr=None):
        if expr is None:
            ast = self._get_ast(lexer, parser, input)
            expr = ast.stmts[0]
        nodes = in_order_traverse_AST(expr)
        print("Actual result: ", nodes)
        print("Expected result: ", expected)
        assert compare_lists(nodes, expected)

    def testVectorInitStmt(self, lexer, parser):
        input = """vector<int> a = {1,6};"""
        ast = self._get_ast(lexer, parser, input)

        assert ast.stmts[0].type_class == VAR_TYPE.VECTOR
        assert ast.stmts[0].name["value"] == "a"

        expected = [
            VectorExprNode(
                create_token(TokenTypes.LBRACE),
                [
                    AtomicExprNode(create_token(TokenTypes.INT, 1)),
                    AtomicExprNode(create_token(TokenTypes.INT, 6)),
                ],
            )
        ]
        self._run_and_compare_expr(lexer, parser, input, expected, ast.stmts[0].value)

    def testVector2DInitStmt(self, lexer, parser):
        input = """vector<vector<int>> b = {{1,6}, {-4}};"""
        ast = self._get_ast(lexer, parser, input)

        assert ast.stmts[0].type_class == VAR_TYPE.VECTOR_2D
        assert ast.stmts[0].name["value"] == "b"

        expected = [
            VectorExprNode(
                create_token(TokenTypes.LBRACE),
                [
                    VectorExprNode(
                        create_token(TokenTypes.LBRACE),
                        [
                            AtomicExprNode(create_token(TokenTypes.INT, 1)),
                            AtomicExprNode(create_token(TokenTypes.INT, 6)),
                        ],
                    ),
                    VectorExprNode(
                        create_token(TokenTypes.LBRACE),
                        [
                            AtomicExprNode(create_token(TokenTypes.INT, -4)),
                        ],
                    ),
                ],
            )
        ]
        self._run_and_compare_expr(lexer, parser, input, expected, ast.stmts[0].value)
