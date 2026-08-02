from lexer.main import Lexer
from libraries.main import Parser, Walker
from walker.environment import Environment

FRAGMENT = """
vector<int> a = {1,2,3};
a.push_back(5);
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
    res = walker.eval(ast, env)
    print(res)

if __name__ == "__main__":
    main()
