from ast import stmt
import pytest

from lexer.main import Lexer
from lexer.token_lists import TokenTypes
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
from parser.main import Parser
from tests.test_utils import compareLists, compareTokens, inOrderTraverseAST
from utils.main import createToken
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
        nodes = inOrderTraverseAST(expr)
        print("Actual result: ", nodes)
        print("Expected result: ", expected)
        assert compareLists(nodes, expected)

    def testSimpleExpressions(self, lexer, parser):
        input = """2+2*4;"""
        expected = [
            AtomicExprNode(createToken(TokenTypes.INT, 2)),
            InfixExprNode(createToken(TokenTypes.PLUS)),
            InfixExprNode(createToken(TokenTypes.INT, 2)),
            InfixExprNode(createToken(TokenTypes.MUL)),
            InfixExprNode(createToken(TokenTypes.INT, 4)),
        ]

        self._run_and_compare_expr(lexer, parser, input, expected)

    def testGroupedExpressions(self, lexer, parser):
        input = """(5+(6-2))/7;"""
        expected = [
            AtomicExprNode(createToken(TokenTypes.INT, 5)),
            InfixExprNode(createToken(TokenTypes.PLUS)),
            InfixExprNode(createToken(TokenTypes.INT, 6)),
            InfixExprNode(createToken(TokenTypes.MIN)),
            InfixExprNode(createToken(TokenTypes.INT, 2)),
            InfixExprNode(createToken(TokenTypes.DIVIDE)),
            InfixExprNode(createToken(TokenTypes.INT, 7)),
        ]

        self._run_and_compare_expr(lexer, parser, input, expected)

    def testAssignExpressions(self, lexer, parser):
        input = """b = 123;"""
        expected = [
            AtomicExprNode(createToken(TokenTypes.IDENT, "b")),
            AssignExprNode(createToken(TokenTypes.ASSIGN)),
            AtomicExprNode(createToken(TokenTypes.INT, 123)),
        ]

        self._run_and_compare_expr(lexer, parser, input, expected)

    def testArrayExpressions(self, lexer, parser):
        input = """{5+3, 10, "text"};"""
        ast = self._get_ast(lexer, parser, input)
        assert len(ast.stmts[0].values) == 3
        expected = [
            AtomicExprNode(createToken(TokenTypes.INT, 5)),
            InfixExprNode(createToken(TokenTypes.PLUS)),
            AtomicExprNode(createToken(TokenTypes.INT, 3)),
        ]

        self._run_and_compare_expr(
            lexer, parser, input, expected, ast.stmts[0].values[0]
        )
        expected = [
            AtomicExprNode(createToken(TokenTypes.INT, 10)),
        ]

        self._run_and_compare_expr(
            lexer, parser, input, expected, ast.stmts[0].values[1]
        )
        expected = [
            AtomicExprNode(createToken(TokenTypes.IDENT, "text")),
        ]
        self._run_and_compare_expr(
            lexer, parser, input, expected, ast.stmts[0].values[2]
        )

    def testIndexExpressions(self, lexer, parser):
        input = """someArray[1+1];"""
        expected = [
            AtomicExprNode(createToken(TokenTypes.IDENT, "someArray")),
            IndexExprNode(createToken(TokenTypes.LBRACKET)),
            AtomicExprNode(createToken(TokenTypes.INT, 1)),
            InfixExprNode(createToken(TokenTypes.PLUS)),
            AtomicExprNode(createToken(TokenTypes.INT, 1)),
        ]

        self._run_and_compare_expr(lexer, parser, input, expected)

    def testFnCallExpressions(self, lexer, parser):
        input = """int val = getValue(2+2, 10)+6;"""
        ast = self._get_ast(lexer, parser, input)
        assert ast.stmts[0] == InitStmt(
            createToken(TokenTypes.TYPE, "int"), createToken(TokenTypes.IDENT, "val")
        )
        expected = [
            CallExprNode(createToken(TokenTypes.FN, "getValue")),
            InfixExprNode(createToken(TokenTypes.PLUS)),
            AtomicExprNode(createToken(TokenTypes.INT, 6)),
        ]
        self._run_and_compare_expr(lexer, parser, input, expected, ast.stmts[0].value)

    def testFnCallParams(self, lexer, parser):
        input = """int val = getValue(2+2, 10)+6;"""
        ast = self._get_ast(lexer, parser, input)
        expected_first_param = [
            AtomicExprNode(createToken(TokenTypes.INT, 2)),
            InfixExprNode(createToken(TokenTypes.PLUS)),
            AtomicExprNode(createToken(TokenTypes.INT, 2)),
        ]
        self._run_and_compare_expr(
            lexer,
            parser,
            input,
            expected_first_param,
            ast.stmts[0].value.left.params[0],
        )
        expected_second_param = [AtomicExprNode(createToken(TokenTypes.INT, 10))]
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
            createToken(TokenTypes.TYPE, "string"), createToken(TokenTypes.IDENT, "b")
        )
        expected = [AtomicExprNode(createToken(TokenTypes.IDENT, "Hithere"))]
        self._run_and_compare_expr(lexer, parser, input, expected, ast.stmts[0].value)

    def testArrayInitStatement(self, lexer, parser):
        # TODO: ignore any valid token inside "", allow spaces inside ""
        input = """int b[2] = {100, 23};"""
        ast = self._get_ast(lexer, parser, input)
        assert ast.stmts[0] == InitStmt(
            createToken(TokenTypes.TYPE, "int"),
            createToken(TokenTypes.IDENT, "b"),
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
            createToken(TokenTypes.TYPE, "int"), createToken(TokenTypes.IDENT, "a")
        )
        assert ast.stmts[0].args[1] == InitStmt(
            createToken(TokenTypes.TYPE, "string"), createToken(TokenTypes.IDENT, "b")
        )
        assert ast.stmts[0].body.stmts[0] == InitStmt(
            createToken(TokenTypes.TYPE, "int"), createToken(TokenTypes.IDENT, "c")
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
        stmts = ast.stmts[0].thenBody.stmts
        assert len(stmts) == 3
        assert stmts[0] == InitStmt(
            createToken(TokenTypes.TYPE, "int"), createToken(TokenTypes.IDENT, "a")
        )
        assert stmts[1] == InitStmt(
            createToken(TokenTypes.TYPE, "bool"), createToken(TokenTypes.IDENT, "b")
        )
        assert stmts[2] == InitStmt(
            createToken(TokenTypes.TYPE, "string"), createToken(TokenTypes.IDENT, "c")
        )

    def testConditionStatements(self, lexer, parser):
        input = """
            if(a<4) { int a = 0; }
            else if(a<10) { int b = 1; }
            else { int c = 2; }
        """
        ast = self._get_ast(lexer, parser, input)

        assert len(ast.stmts) == 1
        assert ast.stmts[0].thenBody.stmts[0] == InitStmt(
            createToken(TokenTypes.TYPE, "int"), createToken(TokenTypes.IDENT, "a")
        )
        assert len(ast.stmts[0].alternatives.stmts) == 1
        assert ast.stmts[0].alternatives.stmts[0].thenBody.stmts[0] == InitStmt(
            createToken(TokenTypes.TYPE, "int"), createToken(TokenTypes.IDENT, "b")
        )
        assert ast.stmts[0].rejectBody.stmts[0] == InitStmt(
            createToken(TokenTypes.TYPE, "int"), createToken(TokenTypes.IDENT, "c")
        )

    def testConditionExpressions(self, lexer, parser):
        input = """
            if(a<4) { int a = 0; }
            else if(a<10) { int b = 1; }
            else { int c = 2; }
        """
        ast = self._get_ast(lexer, parser, input)
        expected_if = [
            AtomicExprNode(createToken(TokenTypes.IDENT, "a")),
            InfixExprNode(createToken(TokenTypes.LT)),
            AtomicExprNode(createToken(TokenTypes.INT, 4)),
        ]
        self._run_and_compare_expr(
            lexer, parser, input, expected_if, ast.stmts[0].condition
        )
        expected_elif = [
            AtomicExprNode(createToken(TokenTypes.IDENT, "a")),
            InfixExprNode(createToken(TokenTypes.LT)),
            AtomicExprNode(createToken(TokenTypes.INT, 10)),
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
        assert ast.stmts[0].condition == AtomicExprNode(createToken(TokenTypes.TRUE))
        assert ast.stmts[0].body.stmts[0] == InitStmt(
            createToken(TokenTypes.TYPE, "int"), createToken(TokenTypes.IDENT, "a")
        )

    def testForStatement(self, lexer, parser):
        input = """
            for(int i = 0;i<n;i++) { int a = i; }
        """
        ast = self._get_ast(lexer, parser, input)
        assert len(ast.stmts[0].condition) == 3
        assert ast.stmts[0].condition[0] == InitStmt(
            createToken(TokenTypes.TYPE, "int"), createToken(TokenTypes.IDENT, "i")
        )
        assert ast.stmts[0].body.stmts[0] == InitStmt(
            createToken(TokenTypes.TYPE, "int"), createToken(TokenTypes.IDENT, "a")
        )
        expected_second = [
            AtomicExprNode(createToken(TokenTypes.IDENT, "i")),
            InfixExprNode(createToken(TokenTypes.LT)),
            AtomicExprNode(createToken(TokenTypes.IDENT, "n")),
        ]
        self._run_and_compare_expr(
            lexer, parser, input, expected_second, ast.stmts[0].condition[1]
        )
        expected_third = [
            AtomicExprNode(createToken(TokenTypes.IDENT, "i")),
            SuffixExprNode(createToken(TokenTypes.INC)),
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
            createToken(TokenTypes.IDENT, "someName")
        )
        assert compareLists(
            ast.stmts[0].values,
            [
                AtomicExprNode(createToken(TokenTypes.INT, 2)),
                AtomicExprNode(createToken(TokenTypes.INT, 4)),
            ],
        )
