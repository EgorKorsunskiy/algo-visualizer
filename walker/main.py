from lexer.token_lists import TokenTypes
from parser.ast_entities import (
    ArrayExprNode,
    AssignExprNode,
    AtomicExprNode,
    BlockStmt,
    CallExprNode,
    FuncStatement,
    IndexExprNode,
    InfixExprNode,
    InitStmt,
    PrefixExprNode,
    ProgrammeNode,
    ReturnStatement,
    SuffixExprNode,
)
from utils.main import getTokenType
from walker.environment import Environment
from walker.log import VAR_TYPE, Log


class Walker:
    def __init__(self) -> None:
        self.log = Log()

    def evalLiteral(self, node, env: Environment):
        if "value" in node:
            stored_val = env.get(node["value"])
            if stored_val is not None:
                return stored_val
            return node["value"]
        raise Exception("Literal token has no value property")

    def evalInfixExpr(self, node, env: Environment):
        match getTokenType(node.tok):
            case TokenTypes.PLUS:
                return self.eval(node.left, env) + self.eval(node.right, env)
            case TokenTypes.MIN:
                return self.eval(node.left, env) - self.eval(node.right, env)
            case TokenTypes.MUL:
                return self.eval(node.left, env) * self.eval(node.right, env)
            case TokenTypes.DIVIDE:
                return self.eval(node.left, env) // self.eval(node.right, env)
            case TokenTypes.MOD:
                return self.eval(node.left, env) % self.eval(node.right, env)

    def evalPrefixExpr(self, node, env: Environment):
        match getTokenType(node.tok):
            case TokenTypes.MIN:
                return -self.eval(node.right, env)
            case TokenTypes.INC:
                return self.eval(node.right, env) + 1
            case TokenTypes.DEC:
                return self.eval(node.right, env) - 1

    def evalSuffixExpr(self, node, env: Environment):
        match getTokenType(node.tok):
            case TokenTypes.INC:
                return self.eval(node.left, env) + 1
            case TokenTypes.DEC:
                return self.eval(node.left, env) - 1

    def evalAssignExpr(self, node, env: Environment):
        evaluated_value = self.eval(node.right, env)
        if not isinstance(node.left, AtomicExprNode):
            raise Exception("Invalid left side of =")
        env.set(node.left.tok["value"], evaluated_value)
        self.log.set(VAR_TYPE.PRIMITIVE, node.left.tok["value"])

    def evalArrayExpr(self, node, _: Environment):
        return list(map(lambda atom: atom.tok["value"], node.values))

    def evalIndexExpr(self, node, env: Environment):
        evaluated_right = self.eval(node.right, env)
        if not isinstance(node.left, AtomicExprNode):
            raise Exception(f"{node.left} is not valid left side of =")
        target = env.get(node.left.tok["value"])
        if not isinstance(target, list):
            raise Exception(f"{target} can not be indexed")
        if not isinstance(evaluated_right, int):
            raise Exception(f"Only int can be used for indexing")
        return target[evaluated_right]

    def evalInitStmt(self, node, env: Environment) -> None:
        evaluated_value = self.eval(node.value, env)
        env.set(node.name["value"], evaluated_value)

        varType = VAR_TYPE.PRIMITIVE
        match evaluated_value:
            case list():
                varType = VAR_TYPE.ARRAY
        self.log.set(varType, node.name["value"])

    def evalFnLiteral(self, node, env: Environment) -> None:
        env.set(node.name["value"], node)

    def evalFnCallExpr(self, node, env: Environment):
        fn = env.get(node.tok["value"])
        fn_env = Environment(outer=env)
        for i in range(len(node.params)):
            evaluated_value = self.eval(node.params[i], env)
            fn_env.set(fn.args[i].name["value"], evaluated_value)
        return self.eval(fn.body, fn_env)

    def parseReturnStmt(self, node, env: Environment):
        return self.eval(node.right, env)

    def evalBlockStmt(self, node, env):
        output = None
        for stmt in node.stmts:
            result = self.eval(stmt, env)
            if isinstance(stmt, ReturnStatement):
                return result
            if result != None:
                output = result
        return output

    def eval(self, node, env: Environment):
        match node:
            case AtomicExprNode():
                return self.evalLiteral(node.tok, env)
            case InfixExprNode():
                return self.evalInfixExpr(node, env)
            case PrefixExprNode():
                return self.evalPrefixExpr(node, env)
            case SuffixExprNode():
                return self.evalSuffixExpr(node, env)
            case AssignExprNode():
                return self.evalAssignExpr(node, env)
            case ArrayExprNode():
                return self.evalArrayExpr(node, env)
            case IndexExprNode():
                return self.evalIndexExpr(node, env)
            case InitStmt():
                return self.evalInitStmt(node, env)
            case FuncStatement():
                return self.evalFnLiteral(node, env)
            case CallExprNode():
                return self.evalFnCallExpr(node, env)
            case ReturnStatement():
                return self.parseReturnStmt(node, env)
            case BlockStmt() | ProgrammeNode():
                return self.evalBlockStmt(node, env)
