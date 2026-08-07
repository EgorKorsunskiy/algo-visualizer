from enum import Enum, auto

from parser.ast_entities import InitStmt
from walker.environment import Environment


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
    ARRAY_2D = "ARRAY_2D"
    VECTOR = "VECTOR"
    VECTOR_2D = "VECTOR_2D"
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
        command_type: COMMAND_TYPE = COMMAND_TYPE.NONE,
        var_type: VAR_TYPE = VAR_TYPE.NONE,
        var=None,
        value=None,
        index=-1,
    ):
        self.log.append(
            (RECORD_TYPE.COMMAND, command_type, var_type, var, value, index)
        )

    def _create_hint_record(
        self, hintType: HINT_TYPE = HINT_TYPE.NONE, target=None, values=None
    ):
        if values is None:
            values = []
        self.log.append((RECORD_TYPE.HINT, hintType, target, values))

    def set(self, var_type, var, value, index=-1):
        self._create_command_record(COMMAND_TYPE.SET, var_type, var, value, index)

    def insert(self, var_type, var, value, index=-1):
        self._create_command_record(COMMAND_TYPE.INSERT, var_type, var, value, index)

    def update(self, var_type, var, value, index=-1):
        self._create_command_record(COMMAND_TYPE.UPDATE, var_type, var, value, index)

    def delete(self, var_type, var, value, index=-1):
        self._create_command_record(COMMAND_TYPE.DELETE, var_type, var, value, index)

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

    # this method is limitied because it's unable to distinguish
    # between complex datatypes such as array and vector, so
    # get_var_type_from_ident is preffered to this method when dealing with initialized variable
    @staticmethod
    def get_var_type_from_values(value, assignValue=None):
        var_type = VAR_TYPE.NONE
        match value:
            case list():
                var_type = VAR_TYPE.ARRAY
            case int() | str():
                var_type = VAR_TYPE.PRIMITIVE
            case _:
                if assignValue:
                    var_type = Log.get_var_type_from_values(assignValue)
        return var_type

    @staticmethod
    def get_var_type_from_ident(ident, env: Environment):
        var_type = env.get("#type_" + ident)
        return var_type

    # the method works only with InitStmt because only it contains type information
    @staticmethod
    def get_var_type_from_type(node: InitStmt):
        return node.type_class
