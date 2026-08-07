from fastapi import APIRouter

from api.models.evaluator_models import ProgramInput
from api.models.log_models import CommandLogEntry, HintLogEntry
from lexer.main import Lexer
from libraries.main import Parser, Walker
from utils.main import convert_log_list_into_dict_list
from walker.environment import Environment

router = APIRouter(prefix="/evaluator")


@router.post("/", response_model=list[CommandLogEntry | HintLogEntry])
async def evaluate_program(progamInput: ProgramInput):
    program = progamInput.program
    lexer = Lexer()
    tokens = lexer.parse(program)
    tokens = lexer.tokens_merge_helper(tokens)
    parser = Parser()
    ast = parser.parse(tokens)
    env = Environment()
    walker = Walker()
    walker.eval(ast, env)

    output = convert_log_list_into_dict_list(walker.log.log)
    return output
