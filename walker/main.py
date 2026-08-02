from lexer.token_lists import TokenTypes
from libraries.unions import builtin_functions
from parser.ast_entities import (
    ArrayExprNode,
    AssignExprNode,
    AtomicExprNode,
    BlockStmt,
    CallExprNode,
    ConditionStmt,
    FuncStatement,
    HintStatement,
    IfStmt,
    IndexExprNode,
    InfixExprNode,
    InitStmt,
    LoopStmt,
    MemberAccessExprNode,
    PrefixExprNode,
    ProgrammeNode,
    ReturnStatement,
    SuffixExprNode,
)
from utils.main import getTokenType
from walker.environment import Environment
from walker.log import Log


class BasicWalker:
    def __init__(self) -> None:
        self.log = Log()

    def evalLiteral(self, node, env: Environment):
        if getTokenType(node) == TokenTypes.FALSE:
            return False
        if getTokenType(node) == TokenTypes.TRUE:
            return True
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
            # bool op
            case TokenTypes.LT:
                return self.eval(node.left, env) < self.eval(node.right, env)
            case TokenTypes.LTE:
                return self.eval(node.left, env) <= self.eval(node.right, env)
            case TokenTypes.GT:
                return self.eval(node.left, env) > self.eval(node.right, env)
            case TokenTypes.GTE:
                return self.eval(node.left, env) >= self.eval(node.right, env)
            case TokenTypes.EQ:
                return self.eval(node.left, env) == self.eval(node.right, env)

    def evalPrefixExpr(self, node, env: Environment):
        def update_value(node, result):
            if not isinstance(node.right, AtomicExprNode):
                raise Exception(f"Invalid left side of {getTokenType(node.tok)}")
            self.log.set(
                Log.get_var_type_from_values(self.eval(node.right, env), result),
                node.right.tok["value"],
                result,
            )
            env.set(node.right.tok["value"], result, True)

        match getTokenType(node.tok):
            case TokenTypes.MIN:
                return -self.eval(node.right, env)
            case TokenTypes.INC:
                result = self.eval(node.right, env) + 1
                update_value(node, result)
                return result
            case TokenTypes.DEC:
                result = self.eval(node.right, env) - 1
                update_value(node, result)
                return result

    def evalSuffixExpr(self, node, env: Environment):
        def update_value(node, result):
            if not isinstance(node.left, AtomicExprNode):
                raise Exception(f"Invalid left side of {getTokenType(node.tok)}")
            self.log.set(
                Log.get_var_type_from_values(self.eval(node.left, env), result),
                node.left.tok["value"],
                result,
            )
            env.set(node.left.tok["value"], result, True)

        match getTokenType(node.tok):
            case TokenTypes.INC:
                result = self.eval(node.left, env) + 1
                update_value(node, result)
                return result
            case TokenTypes.DEC:
                result = self.eval(node.left, env) - 1
                update_value(node, result)
                return result

    def evalAssignExpr(self, node, env: Environment):
        evaluated_value = self.eval(node.right, env)
        if isinstance(node.left, AtomicExprNode):
            env.set(node.left.tok["value"], evaluated_value, True)
            varValue = self.eval(node.left, env)
            self.log.set(
                Log.get_var_type_from_values(varValue, evaluated_value),
                node.left.tok["value"],
                evaluated_value,
            )
        elif isinstance(node.left, IndexExprNode):
            index = self.eval(node.left.right, env)
            varValue = self.eval(node.left.left, env)
            self.log.insert(
                Log.get_var_type_from_values(varValue, evaluated_value),
                node.left.left.tok["value"],
                evaluated_value,
                index,
            )
        else:
            raise Exception("Invalid left side of =")

    def evalMemberAccessExpr(self, node, env: Environment):
        evaluated_value = self.eval(node.left, env)
        # TODO: make it work with complex expression such as (a&b).size()
        evaluated_value_type = env.get("#type_" + node.left.tok["value"])
        if isinstance(node.right, CallExprNode):
            function_name = node.right.tok["value"]
            params = []
            for param in node.right.params:
                params.append(self.eval(param, env))
            return builtin_functions[evaluated_value_type][function_name](
                evaluated_value, *params
            )

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
        env.set("#type_" + node.name["value"], node.typeClass)
        env.set(node.name["value"], evaluated_value)
        self.log.set(
            Log.get_var_type_from_type(node),
            node.name["value"],
            evaluated_value,
        )

    def evalFnLiteral(self, node, env: Environment) -> None:
        env.set("#type_" + node.name["value"], node.typeClass)
        env.set(node.name["value"], node)

    def evalFnCallExpr(self, node, env: Environment):
        fn = env.get(node.tok["value"])
        fn_env = Environment(outer=env)
        for i in range(len(node.params)):
            evaluated_value = self.eval(node.params[i], env)
            argName = fn.args[i].name["value"]
            fn_env.set(argName, evaluated_value)
            if (
                isinstance(node.params[i], AtomicExprNode)
                and env.get(node.params[i].tok["value"]) is not None
            ):
                continue
            self.log.set(
                Log.get_var_type_from_values(evaluated_value), argName, evaluated_value
            )
        return self.eval(fn.body, fn_env)

    def evalReturnStmt(self, node, env: Environment):
        evaluated_value = self.eval(node.right, env)
        env.set("_returned", evaluated_value)
        return self.eval(node.right, env)

    def evalBlockStmt(self, node, env):
        output = None
        for stmt in node.stmts:
            returned = env.get("_returned")
            if returned != False:
                return returned
            result = self.eval(stmt, env)
            if isinstance(stmt, ReturnStatement):
                return result
            if result != None:
                output = result
        return output

    def evalLoopStmt(self, node, env: Environment):
        if isinstance(node.condition, list):
            return self.evalForStmt(node, env)
        return self.evalWhileStmt(node, env)

    def evalWhileStmt(self, node, env: Environment):
        condition = node.condition
        evaluated_condition = self.eval(condition, env)
        output = None
        self.log.while_record()
        while evaluated_condition:
            returned = env.get("_returned")
            if returned != False:
                return returned
            output = self.eval(node.body, env)
            evaluated_condition = self.eval(condition, env)
        return output

    def evalForStmt(self, node, env: Environment):
        initStmt = node.condition[0]
        condition = node.condition[1]
        stepExpr = node.condition[2]

        for_env = Environment(outer=env)
        self.eval(initStmt, for_env)
        self.log.for_record()
        evaluated_condition = self.eval(condition, for_env)
        output = None
        while evaluated_condition:
            returned = env.get("_returned")
            if returned != False:
                return returned
            output = self.eval(node.body, for_env)
            self.eval(stepExpr, for_env)
            evaluated_condition = self.eval(condition, for_env)
        return output

    def evalConditionStmt(self, node, env: Environment):
        evaluated_condition = self.eval(node.condition, env)
        if evaluated_condition:
            self.log.if_record()
            return self.eval(node.thenBody, env)
        for alternative in node.alternatives.stmts:
            evaluated_condition = self.eval(alternative.condition, env)
            if evaluated_condition:
                self.log.elif_record()
                return self.eval(alternative.thenBody, env)
        if node.rejectBody:
            self.log.else_record()
            return self.eval(node.rejectBody, env)

    def evalHintStmt(self, node, _: Environment):
        hintType = node.type
        hintTarget = node.target.tok["value"]
        hintValues = list(map(lambda atom: atom.tok["value"], node.values))
        self.log._create_hint_record(hintType, hintTarget, hintValues)

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
            case MemberAccessExprNode():
                return self.evalMemberAccessExpr(node, env)
            case IndexExprNode():
                return self.evalIndexExpr(node, env)
            case InitStmt():
                return self.evalInitStmt(node, env)
            case FuncStatement():
                return self.evalFnLiteral(node, env)
            case CallExprNode():
                return self.evalFnCallExpr(node, env)
            case ReturnStatement():
                return self.evalReturnStmt(node, env)
            case LoopStmt():
                return self.evalLoopStmt(node, env)
            case IfStmt():
                return self.evalConditionStmt(node, env)
            case ConditionStmt():
                return self.evalConditionStmt(node, env)
            case HintStatement():
                return self.evalHintStmt(node, env)
            case BlockStmt() | ProgrammeNode():
                return self.evalBlockStmt(node, env)
