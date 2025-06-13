from networkx import MultiDiGraph

from generalizeNetlistDrawing.interfaces.findParallelNodesInterface import FindParallelNodesInterface


def potParaNodes(graph: MultiDiGraph) -> list:
    """returns a list of nodes that are potentially nodes that have parallel edges"""
    paraNodePairs = []
    for node in graph.nodes:
        if graph.out_degree(node) > 1:
            successors = list(graph.successors(node))
            for successor in successors:
                paraNodePairs.append((node, successor))

    return paraNodePairs

def isParaNodePair(graph: MultiDiGraph, node1, node2) -> bool:
    return len([edge for edge in graph.out_edges(node1) if edge[0] == node1 and edge[1] == node2]) >= 2

class FindParallelNodes(FindParallelNodesInterface):
    def __init__(self):
        super().__init__(MultiDiGraph)

    @staticmethod
    def findParallelNode(graph: MultiDiGraph) -> list:
        potNodes = potParaNodes(graph)
        for node in potNodes:
            if isParaNodePair(graph, *node):
                return [node[0], node[1]]

        return []