import pytest

from lexer.main import Lexer
from lexer.token_lists import TokenTypes
from libraries.main import Parser
from parser.ast_entities import (
    ArrayExprNode,
    AssignExprNode,
    AtomicExprNode,
    CallExprNode,
    HintStatement,
    IndexExprNode,
    InfixExprNode,
    InitStmt,
    SuffixExprNode,
)
from tests.test_utils import compare_lists, in_order_traverse_AST
from utils.main import create_token
from walker.log import HINT_TYPE


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

    def testSimpleExpressions(self, lexer, parser):
        input = """2+2*4;"""
        expected = [
            AtomicExprNode(create_token(TokenTypes.INT, 2)),
            InfixExprNode(create_token(TokenTypes.PLUS)),
            InfixExprNode(create_token(TokenTypes.INT, 2)),
            InfixExprNode(create_token(TokenTypes.MUL)),
            InfixExprNode(create_token(TokenTypes.INT, 4)),
        ]

        self._run_and_compare_expr(lexer, parser, input, expected)

    def testSimpleBitExpressions(self, lexer, parser):
        input = """(1<<4)^(2&7);"""
        expected = [
            AtomicExprNode(create_token(TokenTypes.INT, 1)),
            InfixExprNode(create_token(TokenTypes.B_LSHIFT)),
            InfixExprNode(create_token(TokenTypes.INT, 4)),
            InfixExprNode(create_token(TokenTypes.B_XOR)),
            InfixExprNode(create_token(TokenTypes.INT, 2)),
            InfixExprNode(create_token(TokenTypes.B_AND)),
            InfixExprNode(create_token(TokenTypes.INT, 7)),
        ]

        self._run_and_compare_expr(lexer, parser, input, expected)

    def testGroupedExpressions(self, lexer, parser):
        input = """(5+(6-2))/7;"""
        expected = [
            AtomicExprNode(create_token(TokenTypes.INT, 5)),
            InfixExprNode(create_token(TokenTypes.PLUS)),
            InfixExprNode(create_token(TokenTypes.INT, 6)),
            InfixExprNode(create_token(TokenTypes.MIN)),
            InfixExprNode(create_token(TokenTypes.INT, 2)),
            InfixExprNode(create_token(TokenTypes.DIVIDE)),
            InfixExprNode(create_token(TokenTypes.INT, 7)),
        ]

        self._run_and_compare_expr(lexer, parser, input, expected)

    def testAssignExpressions(self, lexer, parser):
        input = """b = 123;"""
        expected = [
            AtomicExprNode(create_token(TokenTypes.IDENT, "b")),
            AssignExprNode(create_token(TokenTypes.ASSIGN)),
            AtomicExprNode(create_token(TokenTypes.INT, 123)),
        ]

        self._run_and_compare_expr(lexer, parser, input, expected)

    def testArrayExpressions(self, lexer, parser):
        input = """{5+3, 10, "text"};"""
        ast = self._get_ast(lexer, parser, input)
        assert len(ast.stmts[0].values) == 3
        expected = [
            AtomicExprNode(create_token(TokenTypes.INT, 5)),
            InfixExprNode(create_token(TokenTypes.PLUS)),
            AtomicExprNode(create_token(TokenTypes.INT, 3)),
        ]

        self._run_and_compare_expr(
            lexer, parser, input, expected, ast.stmts[0].values[0]
        )
        expected = [
            AtomicExprNode(create_token(TokenTypes.INT, 10)),
        ]

        self._run_and_compare_expr(
            lexer, parser, input, expected, ast.stmts[0].values[1]
        )
        expected = [
            AtomicExprNode(create_token(TokenTypes.IDENT, "text")),
        ]
        self._run_and_compare_expr(
            lexer, parser, input, expected, ast.stmts[0].values[2]
        )

    def testIndexExpressions(self, lexer, parser):
        input = """someArray[1+1];"""
        expected = [
            AtomicExprNode(create_token(TokenTypes.IDENT, "someArray")),
            IndexExprNode(create_token(TokenTypes.LBRACKET)),
            AtomicExprNode(create_token(TokenTypes.INT, 1)),
            InfixExprNode(create_token(TokenTypes.PLUS)),
            AtomicExprNode(create_token(TokenTypes.INT, 1)),
        ]

        self._run_and_compare_expr(lexer, parser, input, expected)

    def testFnCallExpressions(self, lexer, parser):
        input = """int val = getValue(2+2, 10)+6;"""
        ast = self._get_ast(lexer, parser, input)
        assert ast.stmts[0] == InitStmt(
            create_token(TokenTypes.TYPE, "int"), create_token(TokenTypes.IDENT, "val")
        )
        expected = [
            CallExprNode(create_token(TokenTypes.FN, "getValue")),
            InfixExprNode(create_token(TokenTypes.PLUS)),
            AtomicExprNode(create_token(TokenTypes.INT, 6)),
        ]
        self._run_and_compare_expr(lexer, parser, input, expected, ast.stmts[0].value)

    def testFnCallParams(self, lexer, parser):
        input = """int val = getValue(2+2, 10)+6;"""
        ast = self._get_ast(lexer, parser, input)
        expected_first_param = [
            AtomicExprNode(create_token(TokenTypes.INT, 2)),
            InfixExprNode(create_token(TokenTypes.PLUS)),
            AtomicExprNode(create_token(TokenTypes.INT, 2)),
        ]
        self._run_and_compare_expr(
            lexer,
            parser,
            input,
            expected_first_param,
            ast.stmts[0].value.left.params[0],
        )
        expected_second_param = [AtomicExprNode(create_token(TokenTypes.INT, 10))]
        self._run_and_compare_expr(
            lexer,
            parser,
            input,
            expected_second_param,
            ast.stmts[0].value.left.params[1],
        )

    def testSimpleInitStatement(self, lexer, parser):
        # TODO: ignore any valid token inside "", allow spaces inside ""
        input = """string b = "Hithere";"""
        ast = self._get_ast(lexer, parser, input)
        assert ast.stmts[0] == InitStmt(
            create_token(TokenTypes.TYPE, "string"), create_token(TokenTypes.IDENT, "b")
        )
        expected = [AtomicExprNode(create_token(TokenTypes.IDENT, "Hithere"))]
        self._run_and_compare_expr(lexer, parser, input, expected, ast.stmts[0].value)

    def testArrayInitStatement(self, lexer, parser):
        # TODO: ignore any valid token inside "", allow spaces inside ""
        input = """int b[2] = {100, 23};"""
        ast = self._get_ast(lexer, parser, input)
        assert ast.stmts[0] == InitStmt(
            create_token(TokenTypes.TYPE, "int"),
            create_token(TokenTypes.IDENT, "b"),
            None,
            2,
        )
        assert ast.stmts[0].length.tok["value"] == 2

    def testFnDeclarationStatement(self, lexer, parser):
        input = """
            void fn_name(int a, string b) { int c = 0; }
        """
        ast = self._get_ast(lexer, parser, input)
        assert len(ast.stmts[0].args) == 2
        assert ast.stmts[0].args[0] == InitStmt(
            create_token(TokenTypes.TYPE, "int"), create_token(TokenTypes.IDENT, "a")
        )
        assert ast.stmts[0].args[1] == InitStmt(
            create_token(TokenTypes.TYPE, "string"), create_token(TokenTypes.IDENT, "b")
        )
        assert ast.stmts[0].body.stmts[0] == InitStmt(
            create_token(TokenTypes.TYPE, "int"), create_token(TokenTypes.IDENT, "c")
        )

    def testBlockStatements(self, lexer, parser):
        input = """
            if(true){
                int a = 1;
                bool b = false;
                string c = "hello";
            }
        """
        ast = self._get_ast(lexer, parser, input)
        stmts = ast.stmts[0].then_body.stmts
        assert len(stmts) == 3
        assert stmts[0] == InitStmt(
            create_token(TokenTypes.TYPE, "int"), create_token(TokenTypes.IDENT, "a")
        )
        assert stmts[1] == InitStmt(
            create_token(TokenTypes.TYPE, "bool"), create_token(TokenTypes.IDENT, "b")
        )
        assert stmts[2] == InitStmt(
            create_token(TokenTypes.TYPE, "string"), create_token(TokenTypes.IDENT, "c")
        )

    def testConditionStatements(self, lexer, parser):
        input = """
            if(a<4) { int a = 0; }
            else if(a<10) { int b = 1; }
            else { int c = 2; }
        """
        ast = self._get_ast(lexer, parser, input)

        assert len(ast.stmts) == 1
        assert ast.stmts[0].then_body.stmts[0] == InitStmt(
            create_token(TokenTypes.TYPE, "int"), create_token(TokenTypes.IDENT, "a")
        )
        assert len(ast.stmts[0].alternatives.stmts) == 1
        assert ast.stmts[0].alternatives.stmts[0].then_body.stmts[0] == InitStmt(
            create_token(TokenTypes.TYPE, "int"), create_token(TokenTypes.IDENT, "b")
        )
        assert ast.stmts[0].reject_body.stmts[0] == InitStmt(
            create_token(TokenTypes.TYPE, "int"), create_token(TokenTypes.IDENT, "c")
        )

    def testConditionExpressions(self, lexer, parser):
        input = """
            if(a<4) { int a = 0; }
            else if(a<10) { int b = 1; }
            else { int c = 2; }
        """
        ast = self._get_ast(lexer, parser, input)
        expected_if = [
            AtomicExprNode(create_token(TokenTypes.IDENT, "a")),
            InfixExprNode(create_token(TokenTypes.LT)),
            AtomicExprNode(create_token(TokenTypes.INT, 4)),
        ]
        self._run_and_compare_expr(
            lexer, parser, input, expected_if, ast.stmts[0].condition
        )
        expected_elif = [
            AtomicExprNode(create_token(TokenTypes.IDENT, "a")),
            InfixExprNode(create_token(TokenTypes.LT)),
            AtomicExprNode(create_token(TokenTypes.INT, 10)),
        ]
        self._run_and_compare_expr(
            lexer,
            parser,
            input,
            expected_elif,
            ast.stmts[0].alternatives.stmts[0].condition,
        )

    def testWhileStatement(self, lexer, parser):
        input = """
            while(true) { int a = 1; }
        """
        ast = self._get_ast(lexer, parser, input)
        assert ast.stmts[0].condition == AtomicExprNode(create_token(TokenTypes.TRUE))
        assert ast.stmts[0].body.stmts[0] == InitStmt(
            create_token(TokenTypes.TYPE, "int"), create_token(TokenTypes.IDENT, "a")
        )

    def testForStatement(self, lexer, parser):
        input = """
            for(int i = 0;i<n;i++) { int a = i; }
        """
        ast = self._get_ast(lexer, parser, input)
        assert len(ast.stmts[0].condition) == 3
        assert ast.stmts[0].condition[0] == InitStmt(
            create_token(TokenTypes.TYPE, "int"), create_token(TokenTypes.IDENT, "i")
        )
        assert ast.stmts[0].body.stmts[0] == InitStmt(
            create_token(TokenTypes.TYPE, "int"), create_token(TokenTypes.IDENT, "a")
        )
        expected_second = [
            AtomicExprNode(create_token(TokenTypes.IDENT, "i")),
            InfixExprNode(create_token(TokenTypes.LT)),
            AtomicExprNode(create_token(TokenTypes.IDENT, "n")),
        ]
        self._run_and_compare_expr(
            lexer, parser, input, expected_second, ast.stmts[0].condition[1]
        )
        expected_third = [
            AtomicExprNode(create_token(TokenTypes.IDENT, "i")),
            SuffixExprNode(create_token(TokenTypes.INC)),
        ]
        self._run_and_compare_expr(
            lexer, parser, input, expected_third, ast.stmts[0].condition[2]
        )

    def testHintStatement(self, lexer, parser):
        input = """
            //@index<someName,2,4>
        """
        ast = self._get_ast(lexer, parser, input)
        assert isinstance(ast.stmts[0], HintStatement)
        assert ast.stmts[0].type == HINT_TYPE.INDEX
        assert ast.stmts[0].target == AtomicExprNode(
            create_token(TokenTypes.IDENT, "someName")
        )
        assert compare_lists(
            ast.stmts[0].values,
            [
                AtomicExprNode(create_token(TokenTypes.INT, 2)),
                AtomicExprNode(create_token(TokenTypes.INT, 4)),
            ],
        )
