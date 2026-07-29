from lexer.main import Lexer
from parser.main import Parser
from walker.environment import Environment
from walker.main import Walker

# FRAGMENT = """
# bool binarySearch(int v, int target) {
	
#     int low = 0;
#     int high = 9;
  	
#     while (low <= high) {
      
#         int mid = ((high - low) / 2) + low;

#         if (v[mid] == target) {
#             return true;
#         }

#         if (v[mid] > target) {
#             high = mid - 1;
#         }
        
#         else {
#             low = mid + 1;
#         }
#     }
#   	return false;
# }

# int v[10] = {1, 2, 3, 4, 5, 8, 9, 11};
# binarySearch(v, 9);
# """

FRAGMENT = """
    //@index<someName,2,4>
"""

def main():
    lexer = Lexer()
    tokens = lexer.parse(FRAGMENT)
    tokens = lexer.tokens_merge_helper(tokens)
    parser = Parser()
    ast = parser.parse(tokens)
    env = Environment()
    walker = Walker()
    walker.eval(ast, env)
    output = []
    for log in walker.log.log:
        output.append(
            {
                "recordType": str(log[0]),
                "varType": str(log[1]),
                "var": log[2],
                "value": log[3],
                "index": log[4],
            }
        )
    print(len(output))


if __name__ == "__main__":
    main()
