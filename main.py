from lexer.main import Lexer
from parser.main import Parser

FRAGMENT = """
void fn_name(int a, string b) { int c = 0; }
"""

def main():
    lexer = Lexer()
    tokens = lexer.parse(FRAGMENT)
    tokens = lexer.tokens_merge_helper(tokens)
    parser = Parser()
    ast = parser.parse(tokens)
    print(ast)
if __name__ == "__main__":
    main()
