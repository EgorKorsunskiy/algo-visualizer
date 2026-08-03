from libraries.vector.ast_entities import VectorExprNode
from walker.environment import Environment
from walker.main import BasicWalker


class VectorWalker:
    def __init__(self, walker: BasicWalker) -> None:
        self.walker = walker
        self.log = self.walker.log
        self.original_eval = walker.eval

    def eval_vertex_expr(self, node, _: Environment):
        return list(map(lambda atom: atom.tok["value"], node.values))

    def _eval(self, node, env: Environment, *args, **kwargs):
        match node:
            case VectorExprNode():
                return self.eval_vertex_expr(node, env)
            case _:
                return self.original_eval(node, env, *args, **kwargs)
    def eval(self, *args, **kwargs):
        self.walker.eval = self._eval
        return self.walker.eval(*args, **kwargs)