from networkx import MultiDiGraph
from generalizeNetlistDrawing.interfaces.findRowNodesInterface import FindRowNodesInterface

def findPossibleRowNodes(graph):
    """
    find nodes that have a possible
    """
    rowNodes = set()
    for node in graph.nodes:
        if graph.out_degree(node) == 1 and graph.in_degree(node) == 1:
            rowNodes.add(node)

    return rowNodes


def makeRowNodeSequences(graph, rowNodes) -> list:
    rowNodeSequences = []
    while rowNodes:
        node = rowNodes.pop()
        rowNodeSequence = [node]
        rowNodeSequence.extend(successorPredecessorOfNodeInSet(graph, node, rowNodes))
        rowNodeSequences.append(rowNodeSequence)
    return rowNodeSequences


def successorPredecessorOfNodeInSet(graph, node, nodeSet):
    rowNodeSequences = []
    successor = list(graph.successors(node))
    successor = successor[0] if len(successor) == 1 else None
    predecessors = list(graph.predecessors(node))
    predecessors = predecessors[0] if len(predecessors) == 1 else None

    if successor in nodeSet:
        rowNodeSequences.append(successor)
        nodeSet.remove(successor)
        rowNodeSequences.extend(successorPredecessorOfNodeInSet(graph, successor, nodeSet))
    if predecessors in nodeSet:
        rowNodeSequences.append(predecessors)
        nodeSet.remove(predecessors)
        rowNodeSequences.extend(successorPredecessorOfNodeInSet(graph, predecessors, nodeSet))

    return rowNodeSequences


def findSuccessorAndPredecessorOfNodeSequence(graph, sequence) -> list:
    nodeAB = []
    for elm in sequence:
        pre = list(graph.predecessors(elm))
        pre = pre[0] if pre else None
        suc = list(graph.successors(elm))
        suc = suc[0] if suc else None

        if pre not in sequence and pre is not None:
            nodeAB.append(pre)
        if suc not in sequence and suc is not None:
            nodeAB.append(suc)

    return nodeAB


class FindRowNodes(FindRowNodesInterface):
    @staticmethod
    def findRowNodesSequences(graph: MultiDiGraph) -> list:
        """
        returns the sequences of nodes that are in a row
        """
        rowNodes = findPossibleRowNodes(graph)
        rowNodeSequences = makeRowNodeSequences(graph, rowNodes)
        nodeSequences = []
        for sequence in rowNodeSequences:
            nodeA, nodeB = findSuccessorAndPredecessorOfNodeSequence(graph, sequence)
            sequence.insert(0, nodeA)
            sequence.append(nodeB)
            nodeSequences.append(sequence)

        return nodeSequences