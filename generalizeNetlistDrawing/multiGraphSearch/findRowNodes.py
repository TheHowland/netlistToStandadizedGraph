from networkx import MultiGraph

from generalizeNetlistDrawing.interfaces.findRowNodesInterface import FindRowNodesInterface


def findPossibleRowNodes(graph: MultiGraph) -> list:
    """
    find nodes that have a possible
    """
    rowNodes = []
    for node in graph.nodes:
        if graph.degree[node] == 2:
            rowNodes.append(node)

    return rowNodes

def findRowChainRecursive(graph: MultiGraph, node, foundNodes: set):
    neighbors = list(graph.neighbors(node))
    if len(neighbors) > 2:
        return []
    else:
        if not neighbors[0] in foundNodes:
            foundNodes.add(neighbors[0])
            return [neighbors[0]] + findRowChainRecursive(graph, neighbors[0], foundNodes)
        if not neighbors[1] in foundNodes:
            foundNodes.add(neighbors[1])
            return [neighbors[1]] + findRowChainRecursive(graph, neighbors[1], foundNodes)
        return []


def findRowNodeChains(graph: MultiGraph) -> list:
    possibleRowNodes = set(findPossibleRowNodes(graph))
    rowNodeChains = []
    while possibleRowNodes:
        node = possibleRowNodes.pop()
        foundRowNodes = set()
        neighbors = list(graph.neighbors(node))

        foundNodes1 = {node, neighbors[0]}
        dir1 = findRowChainRecursive(graph, node, foundNodes1)
        possibleRowNodes -= foundNodes1

        foundNodes2 = {node, neighbors[1]}
        dir2 = findRowChainRecursive(graph, node, foundNodes2)
        possibleRowNodes -= foundNodes2

        if foundNodes1 == foundNodes2:
            rowNodeChains.append([node] + dir1)
        else:
            dir1.reverse()
            rowNodeChains.append(dir1 + [node] + dir2)


    return rowNodeChains

class FindRowNodes(FindRowNodesInterface):
    def __init__(self):
        super().__init__(MultiGraph)

    @staticmethod
    def findRowNodesSequences(graph: MultiGraph) -> list:
        """
        returns the sequences of nodes that are in a row
        """
        return findRowNodeChains(graph)