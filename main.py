from lexer.main import Lexer
from libraries.main import Parser, Walker
from walker.environment import Environment

FRAGMENT = """
a = {{1,2,3}, {-1,-2,-4}};
a[0][1];
"""


def main():
    lexer = Lexer()
    tokens = lexer.parse(FRAGMENT)
    tokens = lexer.tokens_merge_helper(tokens)
    parser = Parser()
    ast = parser.parse(tokens)
    env = Environment()
    walker = Walker()
    res = walker.eval(ast, env)
    print(res)
    print(walker.log.log)

if __name__ == "__main__":
    main()
