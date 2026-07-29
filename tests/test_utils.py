def compareLists(listA, listB):
    if len(listA) != len(listB):
        return False
    for i in range(len(listA)):
        if isinstance(listA[i], (list, tuple)):
            if not compareLists(listA[i], listB[i]):
                return False
        elif listA[i] != listB[i]:
            return False
    return True


def inOrderTraverseAST(node, nodes=None):
    if nodes is None:
        nodes = []
    if getattr(node, "left", None) is not None:
        inOrderTraverseAST(node.left, nodes)
    nodes.append(node)
    if getattr(node, "right", None) is not None:
        inOrderTraverseAST(node.right, nodes)
    return nodes


def compareTokens(tokenA, tokenB):
    return compareLists(list(tokenA.values()), list(tokenB.values()))
