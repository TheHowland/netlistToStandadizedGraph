from networkx import MultiGraph

from generalizeNetlistDrawing.elements.elementRelation import ElementRelation


def edgesBetweenNodes(graph: MultiGraph, nodeA=None, nodeB=None, nodeAB=None) -> list:
    if nodeA and nodeB:
        a = nodeA
        b = nodeB
    elif nodeAB:
        a = nodeAB[0]
        b = nodeAB[1]
    else:
        raise ValueError("pass in nodeA and nodeB or nodeAB")

    edgesNodeAorB = graph.edges(a, keys=True) # edges between a and b are union set of a and b and therefore included in a and b
    edgesAB = [edgeAB for edgeAB in edgesNodeAorB if edgeAB[0] == b or edgeAB[1] == b]

    return edgesAB

def getEdgesOfSubGraph(subGraph: MultiGraph, rel: ElementRelation, startNode) -> list:
    """
    :param subGraph: the subgraph to get the edges from
    :param rel: the relation type (Row or Parallel)
    :returns: a list of edges in the subgraph

    This is used to get the edges in a specific order for row relation. It asserts to return the edges in the order
    of the Graph nodes from start to end. It is used to avoid reordering the elements in the generated circuit image.
    """
    if rel == ElementRelation.Row:
        # ToDo implement this to walk from startNode to endNode to assert order of edges
        lastNode = None
        edgesToPlace = []
        node = startNode
        while True:
            neighbors = list(subGraph.neighbors(node))
            if lastNode is not None:
                neighbors.remove(lastNode)

            if neighbors:
                assert(len(neighbors) == 1), "Misinterpretation of a row relation, there should be only one neighbor left"
                edge = subGraph[node][neighbors[0]]
                lastNode = node
                node = neighbors[0]
            else:
                break

        return list(subGraph.edges(keys=True))
    else:
        return list(subGraph.edges(keys=True))