from lexer.token_lists import TokenTypes
from parser.ast_entities import (
    BlockStmt,
    ConditionStmt,
    FuncStatement,
    HintStatement,
    IfStmt,
    InitStmt,
    LoopStmt,
    ProgrammeNode,
    ReturnStatement,
)
from parser.expression_parser import LOWEST, BasicPrattParser
from utils.main import get_token_type
from walker.log import VAR_TYPE


class ExpectedError(Exception):
    def __init__(self, token, given) -> None:
        self.message = f"Expected {token}, but given {given}"
        super().__init__(self.message)


class BasicParser:
    def __init__(self) -> None:
        self.pratt_parser = BasicPrattParser()
        self.tokens = []
        self.cursor = 0

    def tokens_left(self):
        return self.cursor < len(self.tokens)

    def pick(self):
        return self.tokens[self.cursor]

    def peek_n(self, n):
        # returns nth lookahead token, if it exists
        if self.cursor + n < len(self.tokens):
            return self.tokens[self.cursor + n]

    def next(self, n=1):
        self.cursor += n
        if not self.tokens_left():
            raise Exception("Tried to access token outside of the range")

    def expect(self, tok):
        if get_token_type(self.pick()) != tok:
            raise ExpectedError(tok, get_token_type(self.pick()))

    def indicate_chunk(self, min_tok, plus_tok=TokenTypes.NONE):
        # inserts special PARSE_BREAK before the end of a current body
        braces_cnt = 0
        i = 0
        # TODO: quite dangerous statement :). Probably need to be changed
        while True:
            if get_token_type(self.peek_n(i)) == plus_tok:
                braces_cnt += 1
            elif get_token_type(self.peek_n(i)) == min_tok:
                braces_cnt -= 1
            if braces_cnt < 0:
                break
            i += 1
        self.tokens.insert(self.cursor + i, {"token_type": TokenTypes.PARSE_BREAK})

    def indicate_body(self):
        self.indicate_chunk(TokenTypes.RBRACE, TokenTypes.LBRACE)

    def parse_body(self):
        bodyStmts = []
        while get_token_type(self.pick()) != TokenTypes.PARSE_BREAK:
            stmt = self.parse_stmt()

            if stmt != None:
                bodyStmts.append(stmt)
        self.next()  # skip PARSE_BREAK
        self.next()  # skip closing RBRACE
        return BlockStmt(bodyStmts)

    def parse_init_left_side(self):
        # TODO: add support for pointers
        init_type_tok = self.pick()
        self.next()
        self.expect(TokenTypes.IDENT)
        init_name_tok = self.pick()
        init_length = None
        init_dim = 0
        while get_token_type(self.peek_n(1)) == TokenTypes.LBRACKET:
            init_dim += 1
            self.next()
            self.next()
            self.indicate_chunk(TokenTypes.RBRACKET)
            init_length = self.parse_expr()

        init_node = InitStmt()
        init_node.type = init_type_tok
        init_node.name = init_name_tok
        init_node.length = init_length
        if init_length is not None:
            match init_dim:
                case 1:
                    init_node.type_class = VAR_TYPE.ARRAY
                case 2:
                    init_node.type_class = VAR_TYPE.ARRAY_2D
        else:
            init_node.type_class = VAR_TYPE.PRIMITIVE
        return init_node

    def parse_expr(self):
        expr = []
        while get_token_type(self.pick()) not in [
            TokenTypes.SEMICOL,
            TokenTypes.PARSE_BREAK,
        ]:
            expr.append(self.pick())
            self.next()
        self.next()
        self.pratt_parser.set_expr(expr)
        exprAST = self.pratt_parser.parse_expr(LOWEST)
        return exprAST

    def parse_init_stmt(self):
        init_node = self.parse_init_left_side()
        self.next()
        if get_token_type(self.pick()) == TokenTypes.ASSIGN:
            self.expect(TokenTypes.ASSIGN)
            self.next()
            expr_AST = self.parse_expr()
            init_node.value = expr_AST
        else:
            self.expect(TokenTypes.SEMICOL)
        return init_node

    def parse_func_declaration_stmt(self):
        func_stmt = FuncStatement()
        func_stmt.type = self.pick()
        self.next()
        self.expect(TokenTypes.FN)
        func_stmt.name = self.pick()
        self.next()
        args = []
        while get_token_type(self.pick()) != TokenTypes.RPAREN:
            if get_token_type(self.pick()) == TokenTypes.COMMA:
                self.next()
            argNode = self.parse_init_left_side()
            args.append(argNode)
            self.next()
        self.next()
        self.expect(TokenTypes.LBRACE)
        self.next()
        self.indicate_body()
        bodyStmts = self.parse_body()

        func_stmt.args = args
        func_stmt.body = bodyStmts
        return func_stmt

    def parse_while_stmt(self):
        self.next()
        self.expect(TokenTypes.LPAREN)
        self.next()
        expr = []
        while get_token_type(self.pick()) != TokenTypes.RPAREN:
            expr.append(self.pick())
            self.next()
        self.pratt_parser.set_expr(expr)
        expr_AST = self.pratt_parser.parse_expr(LOWEST)
        self.next()
        self.expect(TokenTypes.LBRACE)
        self.next()
        self.indicate_body()
        body_stmts = self.parse_body()
        loop_node = LoopStmt()
        loop_node.condition = expr_AST
        loop_node.body = body_stmts
        return loop_node

    def parse_for_stmt(self):
        self.next()
        self.expect(TokenTypes.LPAREN)
        self.next()
        expr = []
        self.indicate_chunk(TokenTypes.RPAREN)
        while get_token_type(self.pick()) != TokenTypes.RPAREN:
            if get_token_type(self.pick()) == TokenTypes.SEMICOL:
                self.next()
            expr.append(self.parse_stmt())
        self.next()
        self.expect(TokenTypes.LBRACE)
        self.next()
        self.indicate_body()
        body_stmts = self.parse_body()
        loop_node = LoopStmt()
        loop_node.condition = expr
        loop_node.body = body_stmts
        return loop_node

    def parse_condition_stmt(self):
        self.next()
        self.expect(TokenTypes.LPAREN)
        self.next()
        expr = []
        while get_token_type(self.pick()) != TokenTypes.RPAREN:
            expr.append(self.pick())
            self.next()
        self.pratt_parser.set_expr(expr)
        expr_AST = self.pratt_parser.parse_expr(LOWEST)
        self.next()
        self.expect(TokenTypes.LBRACE)
        self.next()
        self.indicate_body()
        then_body_stmts = self.parse_body()
        condition_stmt = ConditionStmt()
        condition_stmt.condition = expr_AST
        condition_stmt.then_body = then_body_stmts
        return condition_stmt

    def parse_if_stmt(self):
        condition_stmt = self.parse_condition_stmt()
        alterntatives = BlockStmt()
        reject_body = BlockStmt()

        while get_token_type(self.pick()) == TokenTypes.ELIF:
            alterntatives.stmts.append(self.parse_condition_stmt())
        if get_token_type(self.pick()) == TokenTypes.ELSE:
            self.next()
            self.expect(TokenTypes.LBRACE)
            self.next()
            self.indicate_body()
            reject_body = self.parse_body()

        if_stmt = IfStmt()
        if_stmt.condition = condition_stmt.condition
        if_stmt.then_body = condition_stmt.then_body
        if_stmt.alternatives = alterntatives
        if_stmt.reject_body = reject_body
        return if_stmt

    def parse_return_stmt(self):
        self.next()
        expr = self.parse_expr()
        return ReturnStatement(expr)

    def parse_hint_stmt(self):
        hint_stmt = HintStatement()
        self.next()
        self.expect(TokenTypes.HINT_VALUE)
        curr_token = self.pick()
        self.next()
        if get_token_type(self.pick()) == TokenTypes.LT:
            self.indicate_chunk(TokenTypes.GT)
            values = self.parse_expr()
            self.expect(TokenTypes.GT)
            self.next()
            if len(values) >= 1:
                hint_stmt.target = values[0]
                hint_stmt.values = values[1:]
        hint_stmt.type = curr_token["value"]
        return hint_stmt

    def parse_stmt(self):
        match get_token_type(self.pick()):
            case TokenTypes.TYPE:
                if get_token_type(self.peek_n(1)) == TokenTypes.FN:
                    return self.parse_func_declaration_stmt()
                else:
                    return self.parse_init_stmt()
            case TokenTypes.FOR:
                return self.parse_for_stmt()
            case TokenTypes.WHILE:
                return self.parse_while_stmt()
            case TokenTypes.IF:
                return self.parse_if_stmt()
            case TokenTypes.RETURN:
                return self.parse_return_stmt()
            case TokenTypes.HINT_INIT:
                return self.parse_hint_stmt()
            case TokenTypes.PARSE_BREAK:
                return
            case _:
                return self.parse_expr()

    def parse(self, tokens) -> ProgrammeNode:
        self.cursor = 0
        self.tokens = tokens
        head_node = ProgrammeNode()

        while self.tokens_left() and get_token_type(self.pick()) != TokenTypes.EOF:
            stmt = self.parse_stmt()
            if stmt != None:
                head_node.stmts.append(stmt)

        return head_node
