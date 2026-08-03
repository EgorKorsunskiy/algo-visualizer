from libraries.vector.paser import VectorParser
from libraries.vector.walker import VectorWalker
from parser.main import BasicParser
from walker.main import BasicWalker

# Monkey patching approach is used here
Parser = lambda: VectorParser(BasicParser())
Walker = lambda: VectorWalker(BasicWalker())
