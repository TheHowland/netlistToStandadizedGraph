from networkx import MultiDiGraph

from generalizeNetlistDrawing.interfaces.findSeriesNodesInterface import FindSeriesNodesInterface


def findPossibleRowNodes(graph):
    """
    find nodes that have a possible
    """
    seriesNodes = set()
    for node in graph.nodes:
        if graph.out_degree(node) == 1 and graph.in_degree(node) == 1:
            seriesNodes.add(node)

    return seriesNodes


def makeRowNodeSequences(graph, seriesNodes) -> list:
    node = seriesNodes.pop()
    seriesNodeSequence = [node]
    seriesNodeSequence.extend(successorPredecessorOfNodeInSet(graph, node, seriesNodes))
    return seriesNodeSequence


def successorPredecessorOfNodeInSet(graph, node, nodeSet):
    seriesNodeSequences = []
    successor = list(graph.successors(node))
    successor = successor[0] if len(successor) == 1 else None
    predecessors = list(graph.predecessors(node))
    predecessors = predecessors[0] if len(predecessors) == 1 else None

    if successor in nodeSet:
        seriesNodeSequences.append(successor)
        nodeSet.remove(successor)
        seriesNodeSequences.extend(successorPredecessorOfNodeInSet(graph, successor, nodeSet))
    if predecessors in nodeSet:
        seriesNodeSequences.append(predecessors)
        nodeSet.remove(predecessors)
        seriesNodeSequences.extend(successorPredecessorOfNodeInSet(graph, predecessors, nodeSet))

    return seriesNodeSequences



def findSuccessorAndPredecessorOfNodeSequence(graph, sequence) -> tuple[any, any]:
    """
    :returns: (predecessor, successor) of the node sequence
    """
    predecessor = None
    successor = None
    for elm in sequence:
        pre = list(graph.predecessors(elm))
        pre = pre[0] if pre else None
        suc = list(graph.successors(elm))
        suc = suc[0] if suc else None

        if pre not in sequence and pre is not None:
            predecessor = pre
        if suc not in sequence and suc is not None:
            successor = suc

    assert predecessor is not None and successor is not None, "predecessor and successor of node sequence are None"

    return predecessor, successor


class FindSeriesNodes(FindSeriesNodesInterface):
    def __init__(self):
        super().__init__(MultiDiGraph)

    @staticmethod
    def findSeriesNodesSequence(graph: MultiDiGraph) -> list:
        """
        returns a sequence of nodes that are in a series
        """
        seriesNodes = findPossibleRowNodes(graph)
        if not seriesNodes or len(graph.nodes) <= 2:
            # if there are no series nodes or the graph has only two nodes, return an empty list
            # with only two nodes in the graph findSuccessorAndPredecessorOfNodeSequence will crash the
            # program after returning an empty list
            return []

        seriesNodeSequence = makeRowNodeSequences(graph, seriesNodes)
        nodeA, nodeB = findSuccessorAndPredecessorOfNodeSequence(graph, seriesNodeSequence)
        seriesNodeSequence.insert(0, nodeA)
        seriesNodeSequence.append(nodeB)
        return seriesNodeSequence