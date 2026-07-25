from lexer.token_lists import TokenTypes
from parser.ast_entities import AtomicExprNode, BlockStmt, InfixExprNode, InitStmt, ProgrammeNode
from utils.main import getTokenType
from walker.environment import Environment

class Walker:
    def __init__(self) -> None:
        self.log = []

    def evalLiteral(self, node, env: Environment):
        if 'value' in node:
            stored_val = env.get(node['value'])
            if stored_val is not None:
                return stored_val
            return node['value']
        raise Exception('Literal token has no value property')
    
    def evalInfixExpr(self, node, env: Environment):
        match getTokenType(node.tok):
            case TokenTypes.PLUS:
                return self.eval(node.right, env) + self.eval(node.left, env)
            case TokenTypes.MIN:
                return self.eval(node.right, env) - self.eval(node.left, env)
            case TokenTypes.MUL:
                return self.eval(node.right, env) * self.eval(node.left, env)
            case TokenTypes.DIVIDE:
                return self.eval(node.right, env) / self.eval(node.left, env)
    
    def evalInitStmt(self, node, env: Environment) -> None:
        evaluated_value = self.eval(node.value, env)
        env.set(node.name['value'], evaluated_value)

    def evalBlockStmt(self, node, env):
        outputs = []
        for stmt in node.stmts:
            output = self.eval(stmt, env)
            outputs.append(output)
        return outputs

    def eval(self, node, env: Environment):
        match node:
            case AtomicExprNode():
                return self.evalLiteral(node.tok, env)
            case InfixExprNode():
                return self.evalInfixExpr(node, env)
            case InitStmt():
                return self.evalInitStmt(node, env)
            case BlockStmt() | ProgrammeNode():
                return self.evalBlockStmt(node, env)