from pydantic import BaseModel


class ProgramInput(BaseModel):
    program: str
