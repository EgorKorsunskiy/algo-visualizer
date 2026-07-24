import pytest
from lexer.main import Lexer
from lexer.token_lists import TokenTypes
from tests.test_utils import compareLists
from utils.main import getTokenType

@pytest.fixture
def lexer():
        return Lexer()

class TestLexer:

    def _run_and_compare_lexer(self, lexer, input, expected_tokens):
        tokens = lexer.parse(input)
        tokens = lexer.tokens_merge_helper(tokens)
        print("Actual result: ", list(map(lambda token: getTokenType(token), tokens)))
        print("Expected result: ", expected_tokens)
        assert compareLists(list(map(lambda token: getTokenType(token), tokens)), expected_tokens)

    def testTokens(self, lexer):
        input = '''<;>,!<=;!=;='"true false'''
        expected_tokens = [
            TokenTypes.LT,
            TokenTypes.SEMICOL,
            TokenTypes.GT,
            TokenTypes.COMMA,
            TokenTypes.NOT,
            TokenTypes.LTE,
            TokenTypes.SEMICOL,
            TokenTypes.NEQ,
            TokenTypes.SEMICOL,
            TokenTypes.ASSIGN,
            TokenTypes.QUOTE,
            TokenTypes.DOUBLE_QUOTE,
            TokenTypes.TRUE,
            TokenTypes.FALSE,
            TokenTypes.EOF
        ]
        self._run_and_compare_lexer(lexer, input, expected_tokens)

    def testLiterals(self, lexer):
        input = '''(2+3546)-5*66/70;"test"'''
        expected_tokens = [
            TokenTypes.LPAREN,
            TokenTypes.INT,
            TokenTypes.PLUS,
            TokenTypes.INT,
            TokenTypes.RPAREN,
            TokenTypes.MIN,
            TokenTypes.INT,
            TokenTypes.MUL,
            TokenTypes.INT,
            TokenTypes.DIVIDE,
            TokenTypes.INT,
            TokenTypes.SEMICOL,
            TokenTypes.IDENT,
            TokenTypes.EOF
        ]
        self._run_and_compare_lexer(lexer, input, expected_tokens)

    def testConditions(self, lexer):
        input = """
            if(var >= 5) {}
            else if(a == 232) {}
            else {}
        """
        expected_tokens = [
            TokenTypes.IF,
            TokenTypes.LPAREN,
            TokenTypes.IDENT,
            TokenTypes.GTE,
            TokenTypes.INT,
            TokenTypes.RPAREN,
            TokenTypes.LBRACE,
            TokenTypes.RBRACE,
            TokenTypes.ELIF,
            TokenTypes.LPAREN,
            TokenTypes.IDENT,
            TokenTypes.EQ,
            TokenTypes.INT,
            TokenTypes.RPAREN,
            TokenTypes.LBRACE,
            TokenTypes.RBRACE,
            TokenTypes.ELSE,
            TokenTypes.LBRACE,
            TokenTypes.RBRACE,
            TokenTypes.EOF
        ]
        self._run_and_compare_lexer(lexer, input, expected_tokens)
    
    def testLoops(self, lexer):
        input = """
            for(int i = 0;i<n;++i) {}
            while(a==0) {}
        """
        expected_tokens = [
            TokenTypes.FOR,
            TokenTypes.LPAREN,
            TokenTypes.TYPE,
            TokenTypes.IDENT,
            TokenTypes.ASSIGN,
            TokenTypes.INT,
            TokenTypes.SEMICOL,
            TokenTypes.IDENT,
            TokenTypes.LT,
            TokenTypes.IDENT,
            TokenTypes.SEMICOL,
            TokenTypes.INC,
            TokenTypes.IDENT,
            TokenTypes.RPAREN,
            TokenTypes.LBRACE,
            TokenTypes.RBRACE,
            TokenTypes.WHILE,
            TokenTypes.LPAREN,
            TokenTypes.IDENT,
            TokenTypes.EQ,
            TokenTypes.INT,
            TokenTypes.RPAREN,
            TokenTypes.LBRACE,
            TokenTypes.RBRACE,
            TokenTypes.EOF
        ]

        self._run_and_compare_lexer(lexer, input, expected_tokens)
    
    def testFunctionDeclarations(self, lexer):
        input = """
            void fn(int a, string b) {}
        """
        expected_tokens = [
            TokenTypes.TYPE,
            TokenTypes.FN,
            TokenTypes.TYPE,
            TokenTypes.IDENT,
            TokenTypes.COMMA,
            TokenTypes.TYPE,
            TokenTypes.IDENT,
            TokenTypes.RPAREN,
            TokenTypes.LBRACE,
            TokenTypes.RBRACE,
            TokenTypes.EOF
        ]

        self._run_and_compare_lexer(lexer, input, expected_tokens)

    def testFunctionCalls(self, lexer):
        input = """
            bool a = isOkay(2);
        """
        expected_tokens = [
            TokenTypes.TYPE,
            TokenTypes.IDENT,
            TokenTypes.ASSIGN,
            TokenTypes.FN,
            TokenTypes.INT,
            TokenTypes.RPAREN,
            TokenTypes.SEMICOL,
            TokenTypes.EOF
        ]

        self._run_and_compare_lexer(lexer, input, expected_tokens)