import networkx as nx
from networkx import MultiDiGraph
from maxWidth import MaxWidth
from widestPath import WidestPath
from placeElements import PlaceElements

from multiDiGraphSearch.functionsOnGraph import edgesBetweenNodes, findSpanningWidth
from multiDiGraphSearch import findParallelNodes, findRowNodesSequences

class NetlistGraph:
    def __init__(self, graph: MultiDiGraph, startNode, endNode):
        self.graphStart: int = startNode
        self.graphEnd: int = endNode
        self.graph: MultiDiGraph = graph
        self.paths = None
        self.longestPath = None
        self.width = self._findWidestBranch().width
        self._elmPlacement = None
        self._actualSize = None

    def getSubGraphNames(self):
        subGraphNames = []
        for edge in self.graph.edges(keys=True):
            if edge[2][0] == "G":
                subGraphNames.append(edge[2])
        return subGraphNames

    @property
    def actualSize(self) -> tuple[int, int]:
        if not self._actualSize:
            raise RuntimeError("set actualSize based on substitution process, before using it")
        return self._actualSize

    @actualSize.setter
    def actualSize(self, size: tuple[int, int]):
        self._actualSize = size

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.maxPathLength - 1

    @property
    def elementPlacement(self):
        if not self._elmPlacement:
            self._elmPlacement = PlaceElements(self)

        return self._elmPlacement

    def placeElements(self):
        self._elmPlacement = PlaceElements(self)

    def copy(self) -> 'NetlistGraph':
        return NetlistGraph(
            self.graph.copy(),
            self.graphStart,
            self.graphEnd
        )

    def _findMaxSpanningWidth(self):
        return findSpanningWidth(self.graph, self.graphStart, self.graphEnd)

    @staticmethod
    def _findPathWidth(branch: MultiDiGraph, startNode, endNode) -> MaxWidth:
        return findSpanningWidth(branch, startNode, endNode)

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

        paraSubGraphsNodePairs = findParallelNodes(self.graph)
        childGraphs = {}

        for paraSubGraphNodePair in paraSubGraphsNodePairs:
            edgesAB = edgesBetweenNodes(self.graph, nodeAB=paraSubGraphNodePair)
            if not edgesAB:
                continue
            subGraphName = idGenerator()
            childGraphs[subGraphName] = self._replaceEdgesWithSubgraph(subGraphName, edgesAB, paraSubGraphNodePair)


        return childGraphs

    def findRowSubGraphs(self, idGenerator):
        rowNodeSequences = findRowNodesSequences(self.graph)

        childGraphs = {}
        for sequence in rowNodeSequences:

            nodeAB = (sequence.pop(0), sequence.pop())
            if not nx.has_path(self.graph, nodeAB[0], nodeAB[1]):
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