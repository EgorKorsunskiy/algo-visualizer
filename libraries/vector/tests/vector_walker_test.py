import pytest

from lexer.main import Lexer
from libraries.main import Parser, Walker
from walker.environment import Environment


@pytest.fixture
def lexer():
    return Lexer()


@pytest.fixture
def parser():
    return Parser()


@pytest.fixture
def walker():
    return Walker()


class TestWalker:
    def _getAst(self, lexer, parser, input):
        tokens = lexer.parse(input)
        tokens = lexer.tokens_merge_helper(tokens)
        return parser.parse(tokens)

    def _eval(self, walker, input):
        env = Environment()
        return walker.eval(input, env)

    def testVectorExpressions(self, lexer, parser, walker):
        inputs = [
            """
                vector<int> a = {1,2,3};
                a[1] = 24-13;
                a[1];
            """
        ]
        assert self._eval(walker, self._getAst(lexer, parser, inputs[0])) == 11

    def testVector2DExpressions(self, lexer, parser, walker):
        inputs = [
            """
                vector<vector<int>> a = {{1,2,3}, {-1,-2,-4}};
                a[1][2];
            """
        ]
        assert self._eval(walker, self._getAst(lexer, parser, inputs[0])) == -4
