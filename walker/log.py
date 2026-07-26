from enum import Enum, auto


class RECORD_TYPE(Enum):
    SET = auto()
    INSERT = auto()
    UPDATE = auto()
    DELETE = auto()
    FOR = auto()
    WHILE = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()


class VAR_TYPE(Enum):
    NONE = auto()
    PRIMITIVE = auto()
    ARRAY = auto()
    MAP = auto()
    GRAPH = auto()


class Log:
    def __init__(self) -> None:
        self.log = []

    def _create_record(self, recordType: RECORD_TYPE, varType: VAR_TYPE, var, value=None, index=-1):
        self.log.append((recordType, varType, var, value, index))

    def set(self, varType, var, value, index=-1):
        self._create_record(RECORD_TYPE.SET, varType, var, value, index)

    def insert(self, varType, var, value, index=-1):
        self._create_record(RECORD_TYPE.INSERT, varType, var, value, index)

    def update(self, varType, var, value, index=-1):
        self._create_record(RECORD_TYPE.UPDATE, varType, var, value, index)

    def delete(self, varType, var, value, index=-1):
        self._create_record(RECORD_TYPE.DELETE, varType, var, value, index)

    def while_record(self):
        self._create_record(RECORD_TYPE.WHILE, VAR_TYPE.NONE, None)

    def for_record(self):
        self._create_record(RECORD_TYPE.FOR, VAR_TYPE.NONE, None)

    def if_record(self):
        self._create_record(RECORD_TYPE.IF, VAR_TYPE.NONE, None)

    def elif_record(self):
        self._create_record(RECORD_TYPE.ELIF, VAR_TYPE.NONE, None)

    def else_record(self):
        self._create_record(RECORD_TYPE.ELSE, VAR_TYPE.NONE, None)

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
