from tests.test_utils import compareTokens

class ExprNode:
    def __init__(self, tok=None) -> None:
        self.tok = tok
    def __repr__(self) -> str:
        return f"{self.tok}"
    def __eq__(self, other: object) -> bool:
        if not hasattr(other, 'tok'):
            return False
        # for now it's enough to just compare tokens
        return compareTokens(self.tok, other.tok)
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
class CallExprNode(ExprNode):
    def __init__(self, tok=None, params=None) -> None:
        super().__init__(tok)
        self.params = params

class AtomicExprNode(ExprNode):
    def __init__(self, tok=None) -> None:
        super().__init__(tok)

class ProgrammeNode:
    def __init__(self) -> None:
        self.stmts = []
    def __repr__(self) -> str:
        return "\n".join(str(stmt) for stmt in self.stmts)

class InitStmt:
    def __init__(self, type=None, name=None, value=None) -> None:
        self.type = type
        self.name = name
        self.value = value
    def __repr__(self) -> str:
        return f"type: {self.type} name: {self.name} value: {self.value}"
    def __eq__(self, other: object) -> bool:
        if not hasattr(other, 'type') or not hasattr(other, 'name'):
            return False
        return self.type == other.type and self.name == other.name

class LoopStmt:
    def __init__(self) -> None:
        self.condition = None
        self.body = []
    def __repr__(self) -> str:
        return f"condition: {self.condition}\n {"\n".join(str(stmt) for stmt in self.body)}\n"

class ConditionStmt:
    def __init__(self) -> None:
        self.condition = None
        self.thenBody = []
    def __repr__(self) -> str:
        return f"{self.condition}\n {"\n".join(str(stmt) for stmt in self.thenBody)}\n"

class IfStmt(ConditionStmt):
    def __init__(self) -> None:
        super().__init__()
        self.rejectBody = []
        self.alternatives: ConditionStmt = []
    def __repr__(self) -> str:
        base = super().__repr__()
        return f"{base}{"\n".join(str(stmt) for stmt in self.rejectBody)}\n {"\n".join(str(stmt) for stmt in self.alternatives)}\n"

class FuncStatement:
    def __init__(self) -> None:
        self.type = None
        self.name = None
        self.args = []
        self.body = []
    def __repr__(self) -> str:
        return f"{self.type}\n {self.name}\n {" ".join(str(arg) for arg in self.args)} {"\n".join(str(stmt) for stmt in self.body)}"
