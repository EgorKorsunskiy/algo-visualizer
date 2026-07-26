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

    def _create_record(self, recordType: RECORD_TYPE, varType: VAR_TYPE, var, index=-1):
        self.log.append((recordType, varType, var, varType, index))

    def set(self, varType, var, index=-1):
        self._create_record(RECORD_TYPE.SET, varType, var, index)
    
    def insert(self, varType, var, index=-1):
        self._create_record(RECORD_TYPE.INSERT, varType, var, index)
    
    def update(self, varType, var, index=-1):
        self._create_record(RECORD_TYPE.UPDATE, varType, var, index)
    
    def delete(self, varType, var, index=-1):
        self._create_record(RECORD_TYPE.DELETE, varType, var, index)
    
    def while_record(self):
        self._create_record(RECORD_TYPE.WHILE, VAR_TYPE.NONE, None)
    def for_record(self):
        self._create_record(RECORD_TYPE.FOR, VAR_TYPE.NONE, None)
    