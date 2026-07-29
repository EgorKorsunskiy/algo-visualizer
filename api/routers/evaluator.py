from fastapi import APIRouter
from pytest import Parser

from api.models.evaluator_models import ProgramInput
from api.models.log_models import CommandLogEntry, HintLogEntry
from lexer.main import Lexer
from utils.main import convertLogListIntoDictList
from walker.environment import Environment
from walker.main import Walker

router = APIRouter(prefix="/evaluator")


@router.post("/")
async def evaluate_program(progamInput: ProgramInput) -> CommandLogEntry | HintLogEntry:
    program = progamInput.program
    lexer = Lexer()
    tokens = lexer.parse(program)
    tokens = lexer.tokens_merge_helper(tokens)
    parser = Parser()
    ast = parser.parse(tokens)
    env = Environment()
    walker = Walker()
    walker.eval(ast, env)

    output = convertLogListIntoDictList(walker.log.log)
    return output
