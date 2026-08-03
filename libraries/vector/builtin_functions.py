from typing import Any

from walker.log import VAR_TYPE, Log


def size(vector: list[Any]):
    return len(vector)


def push_back(vector: list[Any], value, log: Log, varName: str):
    log.insert(VAR_TYPE.VECTOR, varName, value, len(vector))
    vector.append(value)
    return value


def begin(_: list[Any]):
    return 0


def end(vector: list[Any]):
    return size(vector) - 1


def empty(vector: list[Any]):
    return size(vector) > 0


def pop_back(vector: list[Any]):
    return vector.pop()


def insert(vector: list[Any], index: int, value: Any, log: Log, varName: str):
    log.insert(VAR_TYPE.VECTOR, varName, value, index)
    return vector.insert(index, value)


VECTOR_BUILTIN_FUNCTION = {
    "size": size,
    "push_back": push_back,
    "begin": begin,
    "end": end,
    "empty": empty,
    "pop_back": pop_back,
    "insert": insert,
}
