from networkx import MultiDiGraph, all_simple_paths


def edgesBetweenNodes(graph: MultiDiGraph, nodeA=None, nodeB=None, nodeAB=None) -> list:
    if nodeA and nodeB:
        a = nodeA
        b = nodeB
    elif nodeAB:
        a = nodeAB[0]
        b = nodeAB[1]
    else:
        raise ValueError("pass in nodeA and nodeB or nodeAB")

    edgesNodeAorB = list(graph.edges(a, keys=True)) + list(graph.edges(b, keys=True))
    edgesAB = [edgeAB for edgeAB in edgesNodeAorB if edgeAB[0] == a and edgeAB[1] == b]

    if len(edgesAB) >= 2:
        return edgesAB
    else:
        return []

def nodesBetweenAB(graph: MultiDiGraph, nodeA=None, nodeB=None, tupleAB=None) -> list:
    if nodeA and nodeB:
        pass
    elif tupleAB:
        nodeA = tupleAB[0]
        nodeB = tupleAB[1]
    elif not (nodeA and nodeB) and not tupleAB:
        raise ValueError("pass in nodeA and nodeB or tupleAB")

    nodes = set()
    for path in all_simple_paths(graph, nodeA, nodeB):
        nodes.update(path)
    return list(nodes)