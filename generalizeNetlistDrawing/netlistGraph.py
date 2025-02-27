import lcapy
import networkx as nx
from networkx import MultiDiGraph
from lcapy import NetlistLine
from maxWidth import MaxWidth
from widestPath import WidestPath
from netlistToGraph import NetlistToGraph
from typing import Union

class NetlistGraph:
    def __init__(self, graph: MultiDiGraph, startNode, endNode):
        self.graphStart: int = startNode
        self.graphEnd: int = endNode
        self.graph: MultiDiGraph = graph
        self.subGraphs: list = []

        print("------------------------")
        self.spanningWidth, self.subGraphs = self._findSpanningWidth()
        print(f"GraphWidth: {self.spanningWidth.width}, nodes: {self.graph.nodes}")
        print("------------------------")
        self.paths = self._findPaths()
        for path in self.paths:
            nodesList = list(path)
            pathWidth, _ = self._findPathWidth(self.graph.subgraph(nodesList), nodesList[0], nodesList[-1])
            print(f"pathWidth: {pathWidth.width}, path: {nodesList}")
        print("------------------------")
        self.longestPath = self._findLongestPath()
        print("------------------------")
        self._findParallelSubGraphs()

    def _findMaxSpanningWidth(self):
        return self._findSpanningWidth()[0]

    def _findBranchWidth(self, branch: MultiDiGraph, startNode, endNode) -> MaxWidth:
        return self._findSpanningWidth(branch, startNode, endNode)

    def _findWidestBranch(self) -> WidestPath:
        maxWidth = MaxWidth(0, 0)
        index = 0
        for idx, path in iter(self.paths):
            nodesList = list(path)
            width = self._findBranchWidth(self.graph.subgraph(nodesList), nodesList[0], nodesList[-1])
            if width.width > maxWidth.width:
                maxWidth = width
                index = idx
        return WidestPath(maxWidth.width, maxWidth.depth, index, self.graph)

    def _findSpanningWidth(self, graph: MultiDiGraph=None, startNode=None, endNode=None) -> (MaxWidth, list[tuple]):
        """
        calculate the maximum count of concurrent branches to determine the needed raster width to draw netlist
        :return: MaxWidth object -> maxWidth and depth
        """
        if self:
            graph = self.graph
            startNode = self.graphStart
            endNode = self.graphEnd
        if not (graph and startNode and endNode):
            raise ValueError("pass in graph startNode and endNode or self")

        # there has to be one branch and
        # instead of removing the endNode increase by one, the endNode has no outgoing edges therefore its result is -1
        nodesToCheck = [startNode]
        maxWidth = MaxWidth(0, 0)
        depth = 0

        width = 1
        diffOutIn = 0

        parallelSubGraphs = []
        parallelSubGraphStart:Union[int, None] = None

        while True:

            for node in nodesToCheck:
                newBranches = (graph.out_degree(node) - 1)
                width += newBranches
                diffOutIn += (graph.out_degree(node) - graph.in_degree(node))

                if not parallelSubGraphStart and diffOutIn > 1:
                    parallelSubGraphStart = node

            if width > maxWidth.width:
                maxWidth = MaxWidth(width, depth)

            # if the sum of out_edges - in_edges is 1 this means there is no concurrent branch and the counting
            # has to be reset
            if diffOutIn == 1:
                width = 1
                if parallelSubGraphStart:
                    # if the difference of in out is 1 all concurrent branches have to merge in this node
                    parallelSubGraphs.append((parallelSubGraphStart, nodesToCheck[0]))
                    parallelSubGraphStart = None


            #determine nodes of depth + 1
            nextNodesToCheck = []
            for node in nodesToCheck:
                nextNodesToCheck.extend(list(graph.successors(node)))
            #algorithm only works for nodes that have a successor, end node does not have a successor
            if endNode in nextNodesToCheck:
                nextNodesToCheck.remove(endNode)
            if not nextNodesToCheck:
                if parallelSubGraphStart:
                    parallelSubGraphs.append((parallelSubGraphStart, endNode))
                break
            nodesToCheck = nextNodesToCheck

            depth += 1

        return maxWidth, parallelSubGraphs

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

    def _getAllNodesBetweenAB(self, nodeA, nodeB) -> []:
        nodes = set()
        for path in nx.all_simple_paths(self.graph):
            nodes.update(path)
        return list(nodes)

    @property
    def maxPathLength(self):
        return len(self.longestPath)

    def draw_graph(self):
        import matplotlib.pyplot as plt

        # Visualize the graph
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx_nodes(self.graph, pos)
        nx.draw_networkx_edges(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos)

        plt.show()