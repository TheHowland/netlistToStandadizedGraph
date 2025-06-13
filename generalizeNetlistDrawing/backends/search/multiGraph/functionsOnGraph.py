from networkx import MultiGraph

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