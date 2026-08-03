from tests.test_utils import compare_lists, compare_tokens

class ExprNode:
    def __init__(self, tok=None) -> None:
        self.tok = tok

    def __repr__(self) -> str:
        return f"{self.tok}"

    def __eq__(self, other: object) -> bool:
        if not hasattr(other, "tok"):
            return False
        # for now it's enough to just compare tokens
        return compare_tokens(self.tok, other.tok)


class InfixExprNode(ExprNode):
    def __init__(self, tok=None, left=None, right=None) -> None:
        super().__init__(tok)
        self.left = left
        self.right = right


class PrefixExprNode(ExprNode):
    def __init__(self, tok=None, right=None) -> None:
        super().__init__(tok)
        self.right = right


class SuffixExprNode(ExprNode):
    def __init__(self, tok=None, left=None) -> None:
        super().__init__(tok)
        self.left = left


class ArrayExprNode(ExprNode):
    def __init__(self, tok=None, values=None) -> None:
        super().__init__(tok)
        if values == None:
            values = []
        self.values = values


class IndexExprNode(ExprNode):
    def __init__(self, tok=None, left=None, right=None) -> None:
        super().__init__(tok)
        self.left = left
        self.right = right


class AssignExprNode(ExprNode):
    def __init__(self, tok, left=None, right=None) -> None:
        super().__init__(tok)
        self.left = left
        self.right = right


class MemberAccessExprNode(ExprNode):
    def __init__(self, tok, left=None, right=None) -> None:
        super().__init__(tok)
        self.left = left
        self.right = right

class CallExprNode(ExprNode):
    def __init__(self, tok=None, params=None) -> None:
        super().__init__(tok)
        self.params = params


class AtomicExprNode(ExprNode):
    def __init__(self, tok=None) -> None:
        super().__init__(tok)


class TypeExprNode(ExprNode):
    def __init__(self, tok=None) -> None:
        super().__init__(tok)


class BlockStmt:
    def __init__(self, stmts=None) -> None:
        if stmts == None:
            stmts = []
        self.stmts = stmts


class ProgrammeNode(BlockStmt):
    def __init__(self) -> None:
        super().__init__()


class InitStmt:
    def __init__(
        self, type=None, name=None, value=None, length=None, type_class=None
    ) -> None:
        self.type = type
        self.name = name
        self.value = value
        self.is_array = bool(length)
        self.type_class = type_class
        self.length = length

    def __repr__(self) -> str:
        return f"type: {self.type} name: {self.name} value: {self.value}"

    def __eq__(self, other: object) -> bool:
        if (
            not hasattr(other, "type")
            or not hasattr(other, "name")
            or not hasattr(other, "length")
        ):
            return False
        return self.type == other.type and self.name == other.name


class LoopStmt:
    def __init__(self) -> None:
        self.condition = None
        self.body = None

    def __repr__(self) -> str:
        return f"condition: {self.condition}\n"


class ConditionStmt:
    def __init__(self) -> None:
        self.condition = None
        self.then_body = None

    def __repr__(self) -> str:
        return f"{self.condition}\n"


class IfStmt(ConditionStmt):
    def __init__(self) -> None:
        super().__init__()
        self.reject_body = None
        self.alternatives: ConditionStmt = None

    def __repr__(self) -> str:
        base = super().__repr__()
        return f"{base}\n"


class ReturnStatement:
    def __init__(self, right) -> None:
        self.right = right

    def __eq__(self, other: object) -> bool:
        if not hasattr(other, "right"):
            return False
        return self.right == other.right


class FuncStatement:
    def __init__(self) -> None:
        self.type = None
        self.name = None
        self.args = []
        self.body = None

    def __repr__(self) -> str:
        return f"{self.name}\n"


class HintStatement:
    def __init__(self, type=None, target=None, values=None) -> None:
        if values is None:
            values = []
        self.type = type
        self.target = target
        self.values = values

    def __eq__(self, other: object) -> bool:
        if (
            not hasattr(other, "type")
            or not hasattr(other, "target")
            or not hasattr(other, "values")
        ):
            return False
        return (
            self.type == other.type
            and self.target == other.target
            and compare_lists(self.values, other.values)
        )
