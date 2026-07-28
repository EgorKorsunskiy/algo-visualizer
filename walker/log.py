from enum import Enum, auto


class RECORD_TYPE(Enum):
    COMMAND = auto()
    HINT = auto()


class COMMAND_TYPE(Enum):
    SET = auto()
    INSERT = auto()
    UPDATE = auto()
    DELETE = auto()
    FOR = auto()
    WHILE = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    NONE = auto()


class VAR_TYPE(Enum):
    NONE = auto()
    PRIMITIVE = auto()
    ARRAY = auto()
    MAP = auto()
    GRAPH = auto()


class HINT_TYPE(Enum):
    NONE = auto()
    INDEX = auto()


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
    def get_var_type(value, assignValue=None):
        varType = VAR_TYPE.NONE
        match value:
            case list():
                varType = VAR_TYPE.ARRAY
            case int() | str():
                varType = VAR_TYPE.PRIMITIVE
            case _:
                if assignValue:
                    varType = Log.get_var_type(assignValue)
        return varType
