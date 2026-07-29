from typing import Any

from pydantic import BaseModel

from walker.log import COMMAND_TYPE, HINT_TYPE, RECORD_TYPE, VAR_TYPE


class CommandLogEntry(BaseModel):
    recordType: RECORD_TYPE
    commandType: COMMAND_TYPE
    varType: VAR_TYPE
    var: str | None
    value: Any
    index: int


class HintLogEntry(BaseModel):
    recordType: RECORD_TYPE
    hintType: HINT_TYPE
    target: str | None
    values: list[Any]
