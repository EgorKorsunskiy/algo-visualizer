import pytest

from lexer.main import Lexer
from libraries.main import Parser, Walker
from tests.test_utils import compare_lists
from walker.environment import Environment
from walker.log import COMMAND_TYPE, HINT_TYPE, RECORD_TYPE, VAR_TYPE


@pytest.fixture
def lexer():
    return Lexer()


@pytest.fixture
def parser():
    return Parser()


@pytest.fixture
def walker():
    return Walker()


class TestLog:
    def _getAst(self, lexer, parser, input):
        tokens = lexer.parse(input)
        tokens = lexer.tokens_merge_helper(tokens)
        return parser.parse(tokens)

    def _getLog(self, walker, input):
        env = Environment()
        walker.eval(input, env)
        return walker.log

    def testSimpleExpressions(self, lexer, parser, walker):
        input = """
            int a = 1;
            a = a + 2;
            a = 10;
        """
        expected = [
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "a", 1, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "a", 3, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "a", 10, -1),
        ]
        assert compare_lists(
            self._getLog(walker, self._getAst(lexer, parser, input)).log, expected
        )

    def testArrayExpressions(self, lexer, parser, walker):
        input = """
            int a[3] = {1,2,3};
            a[1] = 22;
        """
        expected = [
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.ARRAY, "a", [1, 2, 3], -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.INSERT, VAR_TYPE.ARRAY, "a", 22, 1),
        ]

        assert compare_lists(
            self._getLog(walker, self._getAst(lexer, parser, input)).log, expected
        )

    def testArray2DExpressions(self, lexer, parser, walker):
        input = """
            int a[2][3] = {{1,2,3}, {5,9,0}};
            a[1][2] = 22;
        """
        expected = [
            (
                RECORD_TYPE.COMMAND,
                COMMAND_TYPE.SET,
                VAR_TYPE.ARRAY_2D,
                "a",
                [[1, 2, 3], [5, 9, 0]],
                -1,
            ),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.INSERT, VAR_TYPE.ARRAY, "a", 22, [1,2]),
        ]

        assert compare_lists(
            self._getLog(walker, self._getAst(lexer, parser, input)).log, expected
        )

    def testWhileStatement(self, lexer, parser, walker):
        input = """
            int g = 0;
            while(g<5) {
                g++;
            }
        """
        expected = [
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "g", 0, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.WHILE, VAR_TYPE.NONE, None, None, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "g", 1, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "g", 2, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "g", 3, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "g", 4, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "g", 5, -1),
        ]
        assert compare_lists(
            self._getLog(walker, self._getAst(lexer, parser, input)).log, expected
        )

    def testForStatement(self, lexer, parser, walker):
        input = """
            int g = 0;
            for(int i = 0;i<5;i++) {
                g = g + 1;
            }
        """
        expected = [
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "g", 0, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "i", 0, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.FOR, VAR_TYPE.NONE, None, None, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "g", 1, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "i", 1, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "g", 2, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "i", 2, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "g", 3, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "i", 3, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "g", 4, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "i", 4, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "g", 5, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.SET, VAR_TYPE.PRIMITIVE, "i", 5, -1),
        ]

        assert compare_lists(
            self._getLog(walker, self._getAst(lexer, parser, input)).log, expected
        )

    def testIfConditionStatement(self, lexer, parser, walker):
        input = """
            int c[3] = {1,4,10};
            if(c[2] == 10) {
                c[0] = 200;
            }
            else {
                c[0] = 0;
            }
        """
        expected = [
            (
                RECORD_TYPE.COMMAND,
                COMMAND_TYPE.SET,
                VAR_TYPE.ARRAY,
                "c",
                [1, 4, 10],
                -1,
            ),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.IF, VAR_TYPE.NONE, None, None, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.INSERT, VAR_TYPE.ARRAY, "c", 200, 0),
        ]

        assert compare_lists(
            self._getLog(walker, self._getAst(lexer, parser, input)).log, expected
        )

    def testElifConditionStatement(self, lexer, parser, walker):
        input = """
            int c[3] = {1,4,10};
            if(c[1] == 10) {
                c[0] = 200;
            }
            else if(c[1] <= 5) {
                c[0] = c[2] / 5; 
            }
            else {
                c[0] = 0;
            }
        """
        expected = [
            (
                RECORD_TYPE.COMMAND,
                COMMAND_TYPE.SET,
                VAR_TYPE.ARRAY,
                "c",
                [1, 4, 10],
                -1,
            ),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.ELIF, VAR_TYPE.NONE, None, None, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.INSERT, VAR_TYPE.ARRAY, "c", 2, 0),
        ]

        assert compare_lists(
            self._getLog(walker, self._getAst(lexer, parser, input)).log, expected
        )

    def testElseConditionStatement(self, lexer, parser, walker):
        input = """
            int c[3] = {1,4,10};
            if(c[1] == 10) {
                c[0] = 200;
            }
            else if(c[1] < 4) {
                c[0] = c[2] / 5; 
            }
            else {
                c[0] = 0;
            }
        """
        expected = [
            (
                RECORD_TYPE.COMMAND,
                COMMAND_TYPE.SET,
                VAR_TYPE.ARRAY,
                "c",
                [1, 4, 10],
                -1,
            ),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.ELSE, VAR_TYPE.NONE, None, None, -1),
            (RECORD_TYPE.COMMAND, COMMAND_TYPE.INSERT, VAR_TYPE.ARRAY, "c", 0, 0),
        ]

        assert compare_lists(
            self._getLog(walker, self._getAst(lexer, parser, input)).log, expected
        )

    def testHintStatements(self, lexer, parser, walker):
        inputs = [
            """
                //@index<someName,2,4>
            """
        ]
        outputs = [[(RECORD_TYPE.HINT, HINT_TYPE.INDEX, "someName", [2, 4])]]
        for i in range(len(inputs)):
            assert compare_lists(
                self._getLog(walker, self._getAst(lexer, parser, inputs[i])).log,
                outputs[i],
            )
