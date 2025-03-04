from typing import Union

import networkx as nx
from networkx import MultiDiGraph
from maxWidth import MaxWidth
from widestPath import WidestPath
from placeElements import PlaceElements

class NetlistGraph:
    def __init__(self, graph: MultiDiGraph, startNode, endNode):
        self.graphStart: int = startNode
        self.graphEnd: int = endNode
        self.graph: MultiDiGraph = graph
        self.paths = None
        self.longestPath = None
        self.width = self._findWidestBranch().width
        self.length = self.maxPathLength
        self.elmPlacement = PlaceElements

        # todo remove if not needed
        self.subGraphs: list[NetlistGraph] = []


    def copy(self) -> 'NetlistGraph':
        return NetlistGraph(
            self.graph.copy(),
            self.graphStart,
            self.graphEnd
        )

    def _findMaxSpanningWidth(self):
        return self._findSpanningWidth()[0]

    @staticmethod
    def _findPathWidth(branch: MultiDiGraph, startNode, endNode) -> MaxWidth:
        return NetlistGraph._findSpanningWidth(branch, startNode, endNode)

    def _findWidestBranch(self) -> WidestPath:
        if not self.paths:
            self.paths = self._findPaths()

        maxWidth = MaxWidth(0, 0)
        index = 0
        for idx, path in enumerate(self.paths):
            nodesList = list(path)
            width = self._findPathWidth(self.graph.subgraph(nodesList), nodesList[0], nodesList[-1])
            if width.width > maxWidth.width:
                maxWidth = width
                index = idx
        return WidestPath(maxWidth.width, maxWidth.depth, index, self.graph)

    @staticmethod
    def _findSpanningWidth(graph: MultiDiGraph, startNode, endNode) -> MaxWidth:
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

    def _findPaths(self) -> list[list]:
        return list(nx.all_simple_paths(self.graph, self.graphStart, self.graphEnd))

    def _findLongestPath(self):
        maxPathLen = 0
        foundPath = None
        for path in self.paths:
            curPathLen = len(path)
            if curPathLen > maxPathLen:
                foundPath = path
                maxPathLen = curPathLen

        return foundPath or list(self.paths)[0]

    def _getAllNodesBetweenAB(self, nodeA=None, nodeB=None, tupleAB=None) -> []:
        if nodeA and nodeB:
            pass
        elif tupleAB:
            nodeA = tupleAB[0]
            nodeB = tupleAB[1]
        elif not (nodeA and nodeB) and not tupleAB:
            raise ValueError("pass in nodeA and nodeB or tupleAB")

        nodes = set()
        for path in nx.all_simple_paths(self.graph, nodeA, nodeB):
            nodes.update(path)
        return list(nodes)

    def _edgesBetweenNodes(self, nodeA=None, nodeB=None, nodeAB=None) -> Union[list, None]:
        if nodeA and nodeB:
            a = nodeA
            b = nodeB
        elif nodeAB:
            a = nodeAB[0]
            b = nodeAB[1]
        else:
            raise ValueError("pass in nodeA and nodeB or nodeAB")

        edgesNodeAorB = list(self.graph.edges(a, b))
        edgesAB = [edgeAB for edgeAB in edgesNodeAorB if edgeAB[0] == a and edgeAB[1] == b]

        if len(edgesAB) >= 2:
            return edgesAB
        else:
            return None

    def _parallelSubGraphNodes(self) -> list:
        paraSubGraphs = []
        for node in self.graph.nodes:
            if self.graph.out_degree(node) > 1:
                successors = list(self.graph.successors(node))
                for successor in successors:
                    paraSubGraphs.append((node, successor))
        return paraSubGraphs

    def _replaceEdgesWithSubgraph(self, subGraphName: str, remEdgesAB: list, nodePair: tuple):
        subGraph = self.graph.subgraph(nodePair).copy()
        self.graph.remove_edges_from(remEdgesAB)
        self.graph.add_edge(nodePair[0], nodePair[1], subGraphName)

        return NetlistGraph(subGraph, nodePair[0], nodePair[1])

    def _replaceNodesWithSubgraph(self, subGraphName: str, remNodes: list, nodePair: tuple):
        subGraph = (self.graph.subgraph(list(nodePair) + remNodes)).copy()
        while nodePair in subGraph.edges():
            subGraph.remove_edge(nodePair[0], nodePair[1])

        self.graph.remove_nodes_from(remNodes)
        self.graph.add_edge(nodePair[0], nodePair[1], subGraphName)

        return NetlistGraph(subGraph, nodePair[0], nodePair[1])

    def findParallelSubGraphs(self, idGenerator):

        paraSubGraphsNodePairs = self._parallelSubGraphNodes()

        childGraphs = {}

        for paraSubGraphNodePair in paraSubGraphsNodePairs:
            edgesAB = self._edgesBetweenNodes(nodeAB=paraSubGraphNodePair)
            if not edgesAB:
                continue
            subGraphName = idGenerator()
            childGraphs[subGraphName] = self._replaceEdgesWithSubgraph(subGraphName, edgesAB, paraSubGraphNodePair)


        return childGraphs

    def _successorPredecessorOfNodeInSet(self, node, nodeSet):
        rowNodeSequences = []
        successor = list(self.graph.successors(node))
        successor = successor[0] if len(successor) == 1 else None
        predecessors = list(self.graph.predecessors(node))
        predecessors = predecessors[0] if len(predecessors) == 1 else None

        if successor in nodeSet:
            rowNodeSequences.append(successor)
            nodeSet.remove(successor)
            rowNodeSequences.extend(self._successorPredecessorOfNodeInSet(successor, nodeSet))
        if predecessors in nodeSet:
            rowNodeSequences.append(predecessors)
            nodeSet.remove(predecessors)
            rowNodeSequences.extend(self._successorPredecessorOfNodeInSet(predecessors, nodeSet))

        return rowNodeSequences

    def findRowSubGraphs(self, idGenerator):
        rowNodes = set()
        for node in self.graph.nodes:
            if self.graph.out_degree(node) == 1 and self.graph.in_degree(node) == 1:
                rowNodes.add(node)

        rowNodeSequences = []
        while rowNodes:
            node = rowNodes.pop()
            rowNodeSequence = [node]
            rowNodeSequence.extend(self._successorPredecessorOfNodeInSet(node, rowNodes))
            rowNodeSequences.append(rowNodeSequence)

        childGraphs = {}
        for sequence in rowNodeSequences:
            edgesAB = []
            for elm in sequence:
                edgesAB.extend(self.graph.in_edges(elm))
                edgesAB.extend(self.graph.out_edges(elm))

            nodeAB = []
            for elm in sequence:
                pre = list(self.graph.predecessors(elm))
                pre = pre[0] if pre else None
                suc = list(self.graph.successors(elm))
                suc = suc[0] if suc else None

                if pre not in sequence and pre is not None:
                    nodeAB.append(pre)
                if suc not in sequence and suc is not None:
                    nodeAB.append(suc)

            if not nx.has_path(self.graph, nodeAB[0], nodeAB[1]):
                nodeAB = (nodeAB[1], nodeAB[0])
            nodeAB = (nodeAB[0], nodeAB[1])

            subGraphName = idGenerator()
            childGraphs[subGraphName] = self._replaceNodesWithSubgraph(subGraphName, sequence, nodeAB)

        return childGraphs

    @property
    def maxPathLength(self) -> int:
        if not self.longestPath:
            self.longestPath = self._findLongestPath()
        return len(self.longestPath)

    def draw_graph(self):
        import matplotlib.pyplot as plt

        # Visualize the graph
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx_nodes(self.graph, pos)
        nx.draw_networkx_edges(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos)

        # Add edge labels with keys
        edge_labels = {(u, v): k for u, v, k in self.graph.edges(keys=True)}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)

        plt.show()