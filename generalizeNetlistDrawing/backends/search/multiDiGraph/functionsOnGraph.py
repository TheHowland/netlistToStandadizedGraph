from networkx import MultiDiGraph, all_simple_paths

from generalizeNetlistDrawing.elements.elementRelation import ElementRelation


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

def getEdgesOfSubGraph(subGraph: MultiDiGraph, rel: ElementRelation, startNode) -> list:
    """
    :param subGraph: the subgraph to get the edges from
    :param rel: the relation type (Row or Parallel)
    :returns: a list of edges in the subgraph

    This is used to get the edges in a specific order for row relation. It asserts to return the edges in the order
    of the Graph nodes from start to end. It is used to avoid reordering the elements in the generated circuit image.
    """
    if rel == ElementRelation.Row:
        edgesToPlace = []
        node = startNode
        while True:
           edgeList = list(subGraph.out_edges(node, keys=True))
           if edgeList:
               edge = edgeList[0]
               edgesToPlace.append(edge)
               node = edge[1]
           else:
               return edgesToPlace
    else:
        return list(subGraph.edges(keys=True))