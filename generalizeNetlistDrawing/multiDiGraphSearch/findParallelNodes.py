from networkx import MultiDiGraph
from generalizeNetlistDrawing.interfaces.findParallelNodesInterface import FindParallelNodesInterface


class FindParallelNodes(FindParallelNodesInterface):
    def __init__(self):
        super().__init__(MultiDiGraph)

    @staticmethod
    def findParallelNodes(graph: MultiDiGraph) -> list:
        paraNodePairs = []
        for node in graph.nodes:
            if graph.out_degree(node) > 1:
                successors = list(graph.successors(node))
                for successor in successors:
                    paraNodePairs.append((node, successor))
        return paraNodePairs