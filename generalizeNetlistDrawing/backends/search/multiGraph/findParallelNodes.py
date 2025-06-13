from networkx import MultiGraph

from generalizeNetlistDrawing.interfaces.findParallelNodesInterface import FindParallelNodesInterface


def edgesAreParallel(edge1, edge2) -> bool:
    if edge1[0] == edge2[0] and edge1[1] == edge2[1]:
        return True
    elif edge1[1] == edge2[0] and edge1[0] == edge2[1]:
        return True
    else:
        return False

def findPotParallelNodes(graph: MultiGraph) -> list:
    """returns a list of nodes that are potentially nodes that have parallel edges"""
    paraNode = []
    for node in graph.nodes:
        if graph.degree[node] > 2:
            paraNode.append(node)
    return paraNode

def findParallelEndNode(graph: MultiGraph, node) -> list:
    getEndNode = lambda edgeNodes, node: edgeNodes[0] if node != edgeNodes[0] else edgeNodes[1]
    edges = graph.edges(node)
    endNodes = [getEndNode(edgeNodes, node) for edgeNodes in edges]
    countDict = {}

    for endNode in endNodes:
        countDict[endNode] = countDict.get(endNode, 0) + 1

    for key in countDict.keys():
        if countDict[key] > 1:
            return [node, key]

    return []


class FindParallelNodes(FindParallelNodesInterface):
    def __init__(self):
        super().__init__(MultiGraph)

    @staticmethod
    def findParallelNode(graph: MultiGraph) -> list:
        potParaNodes = findPotParallelNodes(graph)

        for node in potParaNodes:
            paraNodePairs = findParallelEndNode(graph, node)
            if paraNodePairs:
                return paraNodePairs

        return []