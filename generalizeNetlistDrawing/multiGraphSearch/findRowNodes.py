from networkx import MultiGraph


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
    if graph.degree[node] > 2:
        return []
    else:
        neighbors = list(graph.neighbors(node))
        if not neighbors[0] in foundNodes:
            foundNodes.add(neighbors[0])
            return [neighbors[0]] + findRowChainRecursive(graph, neighbors[0], foundNodes)
        if not neighbors[1] in foundNodes:
            foundNodes.add(neighbors[1])
            return [neighbors[1]] + findRowChainRecursive(graph, neighbors[1], foundNodes)
        return []


def findRowNodeChain(graph: MultiGraph) -> list:
    possibleRowNodes = set(findPossibleRowNodes(graph))
    while possibleRowNodes:
        node = possibleRowNodes.pop()
        foundRowNodes = set()
        neighbors = list(graph.neighbors(node))

        # by defining the first two found nodes it enables to give a search direction
        foundNodes1 = {node, neighbors[0]}
        dir1 = findRowChainRecursive(graph, node, foundNodes1)
        possibleRowNodes -= foundNodes1

        foundNodes2 = {node, neighbors[1]}
        dir2 = findRowChainRecursive(graph, node, foundNodes2)
        possibleRowNodes -= foundNodes2

        if len(dir1) + len(dir2) + 1 > len(foundNodes1.union(foundNodes2)):
            return [node] + dir1
        else:
            dir1.reverse()
            return dir1 + [node] + dir2
    return []

class FindRowNodes:
    def __init__(self):
        super().__init__(MultiGraph)

    @staticmethod
    def findRowNodesSequences(graph: MultiGraph) -> list:
        """
        returns the sequences of nodes that are in a row
        """
        return findRowNodeChain(graph)