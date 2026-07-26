import pytest

from lexer.main import Lexer
from parser.main import Parser
from walker.environment import Environment
from walker.main import Walker


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

    def testSimpleExpressions(self, lexer, parser, walker):
        inputs = [
            "18 / (2 * 3);",
            "10 % 3 + 2;",
            "4 * 5 - 6;",
            "9 + 8 / 2;",
            "(9 + 8) / 2;",
        ]
        outputs = [3, 3, 14, 13, 8]
        for i in range(len(inputs)):
            assert (
                self._eval(walker, self._getAst(lexer, parser, inputs[i])) == outputs[i]
            )

    def testPefixExpressions(self, lexer, parser, walker):
        inputs = [
            "-5;",
            "-(3+2);",
            "++2;",
            "4--;",
        ]
        outputs = [-5, -5, 3, 3]
        for i in range(len(inputs)):
            assert (
                self._eval(walker, self._getAst(lexer, parser, inputs[i])) == outputs[i]
            )

    def testFnExpressions(self, lexer, parser, walker):
        inputs = [
            """
                int square(int x) {
                    return x * x;
                }

                square(5);
            """,
            """
                int add(int a, int b) {
                    return a + b;
                }

                add(7, 3);
            """,
            """
                int add(int a, int b) {
                    return a + b;
                }

                int square(int x) {
                    return x * x;
                }

                square(add(2, 3));
            """,
            """
                int add(int a, int b) {
                    return a + b;
                }

                int mul(int a, int b) {
                    return a * b;
                }

                mul(add(2, 3), 4);
            """,
        ]
        outputs = [25, 10, 25, 20]
        for i in range(len(inputs)):
            assert (
                self._eval(walker, self._getAst(lexer, parser, inputs[i])) == outputs[i]
            )

    def testInitStatements(self, lexer, parser, walker):
        inputs = [
            """
                int a = 23;
                int b = 13;
                a*b;
            """
        ]
        outputs = [299]
        for i in range(len(inputs)):
            assert (
                self._eval(walker, self._getAst(lexer, parser, inputs[i])) == outputs[i]
            )

    def testAssignExpressions(self, lexer, parser, walker):
        inputs = [
            """
                int a = 23;
                int b = 13;
                b=10;
                a*b;
            """
        ]
        outputs = [230]
        for i in range(len(inputs)):
            assert (
                self._eval(walker, self._getAst(lexer, parser, inputs[i])) == outputs[i]
            )

    def testArrayExpressions(self, lexer, parser, walker):
        inputs = [
            """
                a = [1,2,3];
                a[0];
            """
        ]
        assert self._eval(walker, self._getAst(lexer, parser, inputs[0])) == 1
    
    def testWhileStatements(self, lexer, parser, walker):
        inputs = [
            """
                int a = 1;
                while(a<10) {
                    a++;
                }
                a;
            """
        ]
        assert self._eval(walker, self._getAst(lexer, parser, inputs[0])) == 10

    def testForStatements(self, lexer, parser, walker):
        inputs = [
            """
                int n = 20;
                int counter = 0;
                for(int i = 0;i<n;i++) {
                    ++counter;
                }
                counter;
            """
        ]
        assert self._eval(walker, self._getAst(lexer, parser, inputs[0])) == 20