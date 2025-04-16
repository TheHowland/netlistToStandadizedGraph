from networkx import MultiGraph

from generalizeNetlistDrawing.interfaces.findSeriesNodesInterface import FindSeriesNodesInterface


def findPossibleSeriesNodes(graph: MultiGraph) -> list:
    """
    find nodes that have a possible
    """
    seriesNodes = []
    for node in graph.nodes:
        if graph.degree[node] == 2:
            seriesNodes.append(node)

    return seriesNodes

def findSeriesChainRecursive(graph: MultiGraph, node, foundNodes: set):
    if graph.degree[node] > 2:
        return []
    else:
        neighbors = list(graph.neighbors(node))
        if not neighbors[0] in foundNodes:
            foundNodes.add(neighbors[0])
            return [neighbors[0]] + findSeriesChainRecursive(graph, neighbors[0], foundNodes)
        if not neighbors[1] in foundNodes:
            foundNodes.add(neighbors[1])
            return [neighbors[1]] + findSeriesChainRecursive(graph, neighbors[1], foundNodes)
        return []


def findSeriesNodeChain(graph: MultiGraph) -> list:
    possibleSeriesNodes = set(findPossibleSeriesNodes(graph))
    while possibleSeriesNodes:
        node = possibleSeriesNodes.pop()
        neighbors = list(graph.neighbors(node))

        # by defining the first two found nodes it enables to give a search direction
        foundNodes1 = {node, neighbors[0]}
        dir1 = findSeriesChainRecursive(graph, node, foundNodes1)
        possibleSeriesNodes -= foundNodes1

        foundNodes2 = {node, neighbors[1]}
        dir2 = findSeriesChainRecursive(graph, node, foundNodes2)
        possibleSeriesNodes -= foundNodes2

        if len(dir1) + len(dir2) + 1 > len(foundNodes1.union(foundNodes2)):
            return [node] + dir1
        else:
            dir1.reverse()
            return dir1 + [node] + dir2
    return []

class FindSeriesNodes(FindSeriesNodesInterface):

    def __init__(self):
        super().__init__(MultiGraph)

    @staticmethod
    def findSeriesNodesSequence(graph: MultiGraph) -> list:
        """
        returns a sequences of nodes that are in a series
        """
        return findSeriesNodeChain(graph)