import lcapy
import networkx as nx
from networkx import MultiDiGraph
from lcapy import NetlistLine
from maxWidth import MaxWidth
from widestPath import WidestPath
from netlistToGraph import NetlistToGraph

class NetlistGraph:
    def __init__(self, graph: MultiDiGraph, startNode, endNode):
        self.graphStart: int = startNode
        self.graphEnd: int = endNode
        self.graph: MultiDiGraph = graph
        self.subGraphs: list[NetlistGraph] = []

    def _findMaxSpanningWidth(self):
        self._findSpanningWidth(self.graph, self.graphStart, self.graphEnd)

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

            #determine nodes of depth + 1
            nextNodesToCheck = []
            for node in nodesToCheck:
                nextNodesToCheck.extend(list(graph.successors(node)))
            if not nextNodesToCheck:
                break

            #algorithm only works for nodes that have a successor, end node does not have a successor
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

    def _getAllNodesBetweenAB(self, nodeA, nodeB) -> []:
        nodes = set()
        for path in nx.all_simple_paths(self.graph, nodeA, nodeB):
            nodes.update(path)
        return list(nodes)

    def findParallelSubGraphs(self):
        paraSubGraphs = []
        for node in self.graph.nodes:
            if self.graph.out_degree(node) > 1:
                successors = list(self.graph.successors(node))
                for successor in successors:
                    paraSubGraphs.append((node, successor))


        graphs = {}
        graphCount = 1
        newGraph = self.graph.copy()
        for paraSubGraph in paraSubGraphs:
            edgesNodeAorB = list(newGraph.edges(paraSubGraph[0], paraSubGraph[1]))
            edgesAB = [edgeAB for edgeAB in edgesNodeAorB if edgeAB[0] == paraSubGraph[0] and edgeAB[1] == paraSubGraph[1]]
            if len(edgesAB) < 2:
                continue
            subGraphName = "G"+str(graphCount)
            graphs[subGraphName] = self.graph.subgraph(paraSubGraph)
            newGraph.remove_edges_from(edgesAB)
            newGraph.add_edge(paraSubGraph[0], paraSubGraph[1], subGraphName)
            graphCount += 1

        return newGraph, graphs


    def _findRowSubGraphs(self):
        rowNode = []
        for node in self.graph.nodes:
            if self.graph.out_degree(node) == 1 and self.graph.in_degree(node) == 1:
                rowNode.append(node)
        pass

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