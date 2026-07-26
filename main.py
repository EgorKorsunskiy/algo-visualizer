from lexer.main import Lexer
from parser.main import Parser
from tests.test_utils import inOrderTraverseAST
from walker.environment import Environment
from walker.main import Walker

FRAGMENT = """
        int a = 1;
        while(a<10) {
            a++;
        }
        a;
"""


def main():
    lexer = Lexer()
    tokens = lexer.parse(FRAGMENT)
    tokens = lexer.tokens_merge_helper(tokens)
    parser = Parser()
    ast = parser.parse(tokens)
    env = Environment()
    walker = Walker()
    outputs = walker.eval(ast, env)
    print(outputs)


if __name__ == "__main__":
    main()
