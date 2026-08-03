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
from utils.main import get_token_type
from walker.environment import Environment
from walker.log import Log


class BasicWalker:
    def __init__(self) -> None:
        self.log = Log()

    def eval_literal(self, node, env: Environment):
        if get_token_type(node) == TokenTypes.FALSE:
            return False
        if get_token_type(node) == TokenTypes.TRUE:
            return True
        if "value" in node:
            stored_val = env.get(node["value"])
            if stored_val is not None:
                return stored_val
            return node["value"]
        raise Exception("Literal token has no value property")

    def eval_infix_expr(self, node, env: Environment):
        match get_token_type(node.tok):
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

    def eval_prefix_expr(self, node, env: Environment):
        def update_value(node, result):
            if not isinstance(node.right, AtomicExprNode):
                raise Exception(f"Invalid left side of {get_token_type(node.tok)}")
            self.log.set(
                Log.get_var_type_from_values(self.eval(node.right, env), result),
                node.right.tok["value"],
                result,
            )
            env.set(node.right.tok["value"], result, True)

        match get_token_type(node.tok):
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

    def eval_suffix_expr(self, node, env: Environment):
        def update_value(node, result):
            if not isinstance(node.left, AtomicExprNode):
                raise Exception(f"Invalid left side of {get_token_type(node.tok)}")
            self.log.set(
                Log.get_var_type_from_values(self.eval(node.left, env), result),
                node.left.tok["value"],
                result,
            )
            env.set(node.left.tok["value"], result, True)

        match get_token_type(node.tok):
            case TokenTypes.INC:
                result = self.eval(node.left, env) + 1
                update_value(node, result)
                return result
            case TokenTypes.DEC:
                result = self.eval(node.left, env) - 1
                update_value(node, result)
                return result

    def eval_assign_expr(self, node, env: Environment):
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

    def eval_member_access_expr(self, node, env: Environment):
        evaluated_value = self.eval(node.left, env)
        # TODO: make it work with complex expression such as (a&b).size()
        evaluated_value_type = env.get("#type_" + node.left.tok["value"])
        if isinstance(node.right, CallExprNode):
            function_name = node.right.tok["value"]
            params = []
            for param in node.right.params:
                params.append(self.eval(param, env))
            return builtin_functions[evaluated_value_type][function_name](
                evaluated_value, *params, self.log, node.left.tok["value"]
            )

    def eval_array_expr(self, node, _: Environment):
        return list(map(lambda atom: atom.tok["value"], node.values))

    def eval_index_expr(self, node, env: Environment):
        evaluated_right = self.eval(node.right, env)
        if not isinstance(node.left, AtomicExprNode):
            raise Exception(f"{node.left} is not valid left side of =")
        target = env.get(node.left.tok["value"])
        if not isinstance(target, list):
            raise Exception(f"{target} can not be indexed")
        if not isinstance(evaluated_right, int):
            raise Exception(f"Only int can be used for indexing")
        return target[evaluated_right]

    def eval_init_stmt(self, node, env: Environment) -> None:
        evaluated_value = self.eval(node.value, env)
        env.set("#type_" + node.name["value"], node.type_class)
        env.set(node.name["value"], evaluated_value)
        self.log.set(
            Log.get_var_type_from_type(node),
            node.name["value"],
            evaluated_value,
        )

    def eval_fn_literal(self, node, env: Environment) -> None:
        env.set(node.name["value"], node)

    def eval_fn_call_expr(self, node, env: Environment):
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

    def eval_return_stmt(self, node, env: Environment):
        evaluated_value = self.eval(node.right, env)
        env.set("_returned", evaluated_value)
        return self.eval(node.right, env)

    def eval_block_stmt(self, node, env):
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

    def eval_loop_stmt(self, node, env: Environment):
        if isinstance(node.condition, list):
            return self.eval_for_stmt(node, env)
        return self.eval_while_stmt(node, env)

    def eval_while_stmt(self, node, env: Environment):
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

    def eval_for_stmt(self, node, env: Environment):
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

    def eval_condition_stmt(self, node, env: Environment):
        evaluated_condition = self.eval(node.condition, env)
        if evaluated_condition:
            self.log.if_record()
            return self.eval(node.then_body, env)
        for alternative in node.alternatives.stmts:
            evaluated_condition = self.eval(alternative.condition, env)
            if evaluated_condition:
                self.log.elif_record()
                return self.eval(alternative.then_body, env)
        if node.reject_body:
            self.log.else_record()
            return self.eval(node.reject_body, env)

    def eval_hint_stmt(self, node, _: Environment):
        hint_type = node.type
        hint_target = node.target.tok["value"]
        hint_values = list(map(lambda atom: atom.tok["value"], node.values))
        self.log._create_hint_record(hint_type, hint_target, hint_values)

    def eval(self, node, env: Environment):
        match node:
            case AtomicExprNode():
                return self.eval_literal(node.tok, env)
            case InfixExprNode():
                return self.eval_infix_expr(node, env)
            case PrefixExprNode():
                return self.eval_prefix_expr(node, env)
            case SuffixExprNode():
                return self.eval_suffix_expr(node, env)
            case AssignExprNode():
                return self.eval_assign_expr(node, env)
            case ArrayExprNode():
                return self.eval_array_expr(node, env)
            case MemberAccessExprNode():
                return self.eval_member_access_expr(node, env)
            case IndexExprNode():
                return self.eval_index_expr(node, env)
            case InitStmt():
                return self.eval_init_stmt(node, env)
            case FuncStatement():
                return self.eval_fn_literal(node, env)
            case CallExprNode():
                return self.eval_fn_call_expr(node, env)
            case ReturnStatement():
                return self.eval_return_stmt(node, env)
            case LoopStmt():
                return self.eval_loop_stmt(node, env)
            case IfStmt():
                return self.eval_condition_stmt(node, env)
            case ConditionStmt():
                return self.eval_condition_stmt(node, env)
            case HintStatement():
                return self.eval_hint_stmt(node, env)
            case BlockStmt() | ProgrammeNode():
                return self.eval_block_stmt(node, env)
