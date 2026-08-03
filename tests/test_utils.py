def compare_lists(list_a, list_b):
    if len(list_a) != len(list_b):
        return False
    for i in range(len(list_a)):
        if isinstance(list_a[i], (list, tuple)):
            if not compare_lists(list_a[i], list_b[i]):
                return False
        elif list_a[i] != list_b[i]:
            return False
    return True


def in_order_traverse_AST(node, nodes=None):
    if nodes is None:
        nodes = []
    if getattr(node, "left", None) is not None:
        in_order_traverse_AST(node.left, nodes)
    nodes.append(node)
    if getattr(node, "right", None) is not None:
        in_order_traverse_AST(node.right, nodes)
    return nodes


def compare_tokens(token_a, token_b):
    return compare_lists(list(token_a.values()), list(token_b.values()))
