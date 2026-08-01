from enum import Enum, auto

from parser.ast_entities import InitStmt


class RECORD_TYPE(Enum):
    COMMAND = "COMMAND"
    HINT = "HINT"


class COMMAND_TYPE(Enum):
    SET = "SET"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    FOR = "FOR"
    WHILE = "WHILE"
    IF = "IF"
    ELIF = "ELIF"
    ELSE = "ELSE"
    NONE = "NONE"


class VAR_TYPE(Enum):
    NONE = "NONE"
    PRIMITIVE = "PRIMITIVE"
    ARRAY = "ARRAY"
    VECTOR = "VECTOR"
    MAP = "MAP"
    GRAPH = "GRAPH"


class HINT_TYPE(Enum):
    NONE = "NONE"
    INDEX = "INDEX"
    SELECT = "SELECT"


class Log:
    def __init__(self) -> None:
        self.log = []

    def _create_command_record(
        self,
        commandType: COMMAND_TYPE = COMMAND_TYPE.NONE,
        varType: VAR_TYPE = VAR_TYPE.NONE,
        var=None,
        value=None,
        index=-1,
    ):
        self.log.append((RECORD_TYPE.COMMAND, commandType, varType, var, value, index))

    def _create_hint_record(
        self, hintType: HINT_TYPE = HINT_TYPE.NONE, target=None, values=None
    ):
        if values is None:
            values = []
        self.log.append((RECORD_TYPE.HINT, hintType, target, values))

    def set(self, varType, var, value, index=-1):
        self._create_command_record(COMMAND_TYPE.SET, varType, var, value, index)

    def insert(self, varType, var, value, index=-1):
        self._create_command_record(COMMAND_TYPE.INSERT, varType, var, value, index)

    def update(self, varType, var, value, index=-1):
        self._create_command_record(COMMAND_TYPE.UPDATE, varType, var, value, index)

    def delete(self, varType, var, value, index=-1):
        self._create_command_record(COMMAND_TYPE.DELETE, varType, var, value, index)

    def while_record(self):
        self._create_command_record(COMMAND_TYPE.WHILE, VAR_TYPE.NONE, None)

    def for_record(self):
        self._create_command_record(COMMAND_TYPE.FOR, VAR_TYPE.NONE, None)

    def if_record(self):
        self._create_command_record(COMMAND_TYPE.IF, VAR_TYPE.NONE, None)

    def elif_record(self):
        self._create_command_record(COMMAND_TYPE.ELIF, VAR_TYPE.NONE, None)

    def else_record(self):
        self._create_command_record(COMMAND_TYPE.ELSE, VAR_TYPE.NONE, None)

    def index_record(self, target, values):
        self._create_hint_record(HINT_TYPE.INDEX, target, values)

    @staticmethod
    def get_var_type_from_values(value, assignValue=None):
        varType = VAR_TYPE.NONE
        match value:
            case list():
                varType = VAR_TYPE.ARRAY
            case int() | str():
                varType = VAR_TYPE.PRIMITIVE
            case _:
                if assignValue:
                    varType = Log.get_var_type_from_values(assignValue)
        return varType

    # the method works only with InitStmt because only it contains type information
    @staticmethod
    def get_var_type_from_type(node: InitStmt):
        return node.typeClass
