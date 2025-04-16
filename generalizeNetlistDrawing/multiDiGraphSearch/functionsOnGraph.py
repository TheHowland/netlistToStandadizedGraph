from networkx import MultiDiGraph, all_simple_paths

from generalizeNetlistDrawing.maxWidth import MaxWidth


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

def findSpanningWidth(graph: MultiDiGraph, startNode, endNode) -> MaxWidth:
    """
    calculate the maximum count of concurrent branches to determine the needed raster width to draw netlist
    :return: MaxWidth object -> maxWidth and depth
    """

    # there has to be one branch and
    # instead of removing the endNode increase by one, the endNode has no outgoing edges therefore its result is -1
    nodesToCheck = [startNode]
    maxWidth = MaxWidth(0, 0)
    depth = 0

    width = 1
    diffOutIn = 0
    while True:

        for node in nodesToCheck:
            newBranches = (graph.out_degree(node) - 1)
            width += newBranches
            diffOutIn += (graph.out_degree(node) - graph.in_degree(node))

        if width > maxWidth.width:
            maxWidth = MaxWidth(width, depth)

        # if the sum of out_edges - in_edges is 1 this means there is no concurrent branch and the counting
        # has to be reset
        if diffOutIn == 1:
            width = 1

        # determine nodes of depth + 1
        nextNodesToCheck = []
        for node in nodesToCheck:
            nextNodesToCheck.extend(list(graph.successors(node)))
        if not nextNodesToCheck:
            break

        # algorithm only works for nodes that have a successor, end node does not have a successor
        if endNode in nextNodesToCheck:
            nextNodesToCheck.remove(endNode)
        nodesToCheck = nextNodesToCheck

        depth += 1

    return maxWidth