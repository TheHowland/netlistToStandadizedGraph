from typing import Union
from warnings import warn

from networkx import MultiGraph, draw_networkx_edge_labels, draw_networkx_edges, draw_networkx_labels, \
    draw_networkx_nodes, spring_layout

from generalizeNetlistDrawing.element import Element
from generalizeNetlistDrawing.elementRelation import ElementRelation as rel
from generalizeNetlistDrawing.idGenerator import IDGenerator
from generalizeNetlistDrawing.multiGraphSearch import findParallelNode, findRowNodesSequence
from generalizeNetlistDrawing.multiGraphSearch.functionsOnGraph import edgesBetweenNodes
from generalizeNetlistDrawing.vector2D import Vector2D



class NetlistGraph:
    idGenerator = IDGenerator()

    def __init__(self, graph: MultiGraph, startNode, endNode, subGraph: Union[None, MultiGraph] = None, subGraphName: str = None, relation: rel = rel.NONE):
        self.graphStart: int = startNode
        self.graphEnd: int = endNode

        self.graph: MultiGraph = graph
        self.subGraph: MultiGraph = subGraph
        self.subGraphRelation: rel = relation
        self.subGraphName: Union[None, str] = subGraphName
        self._actualSize = None
        self._elmPlacement = None

    def subGraphs(self) -> dict[any, 'NetlistGraph']:
        subGraphs = {}

        nextGraph = self.findRowSubGraph()
        if not nextGraph:
            nextGraph = self.findParallelSubGraph()

        if nextGraph:
            subGraphs[nextGraph.subGraphName] = nextGraph
            subGraphs.update(nextGraph.subGraphs())

        return subGraphs


    def place(self) -> 'NetlistGraph':
        nextGraph = self.findRowSubGraph()
        if not nextGraph:
            nextGraph = self.findParallelSubGraph()

        if nextGraph:
            nextGraph.place()

        if self.subGraph:
            self._placeSubgraphElements()

        return self

    @staticmethod
    def _getEdgeData(graph, edge: list=None, n1=None, n2=None, key=None):
        if not edge:
            edge = [n1, n2, key]
        return graph[edge[0]][edge[1]][edge[2]]['data']

    def _placeSubgraphElements(self):
        edge = [edge for edge in self.graph.edges(keys=True) if edge[2] == self.subGraphName][0]
        offset: Vector2D = self._getEdgeData(self.graph, edge).startPos
        edgesToPlace = list(self.subGraph.edges(keys=True))
        relation = self.subGraphRelation

        if edgesToPlace:
            curElm: Element = self._getEdgeData(self.subGraph, edgesToPlace[0])
            curElm.move(vec=offset)
            lastElm: Element = curElm
            for edge in edgesToPlace[1:]:
                lastElmPos: Vector2D = lastElm.startPos
                lastElmSize: Vector2D = lastElm.size
                if relation == rel.Row:
                    relOffset = lastElmPos + lastElmSize * Vector2D(0, -1)
                elif relation == rel.Parallel:
                    relOffset = lastElmPos + lastElmSize * Vector2D(1, 0)
                else:
                    warn("SubGraphRelation not set, cannot calculate accurate location")
                    relOffset = Vector2D(1, -1)
                curElm = self._getEdgeData(self.subGraph, edge)
                curElm.move(vec=relOffset)
                lastElm = curElm

    def getSubGraphNames(self):
        subGraphNames = []
        for edge in self.graph.edges(keys=True):
            if edge[2][0] == "G":
                subGraphNames.append(edge[2])
        return subGraphNames

    def copy(self) -> 'NetlistGraph':
        copy = NetlistGraph(
            self.graph.copy(),
            self.graphStart,
            self.graphEnd,
            self.subGraph.copy(),
            self.subGraphName
        )
        copy.nextGraph = self.nextGraph
        return copy

    @staticmethod
    def calcNewSize(relation: rel, elms: list[Element]):
        xVals = []
        yVals = []
        for elm in elms:
            x, y = elm.size.asTuple
            xVals.append(x)
            yVals.append(y)

        if relation == rel.Row:
            # the widest element determines the width (x)
            # sum of each element length determines the height (y)
            return Vector2D(max(xVals), sum(yVals))
        elif relation == rel.Parallel:
            # sum of each element width determines the width (x)
            # the longest element determines the length (y)
            return Vector2D(sum(xVals), max(yVals))
        else:
            warn("relation not set, cannot calculate accurate size, returned standard element size (1,1)")
            return Vector2D(1,1)

    def _replaceEdgesWithSubgraph(self, subGraphName: str, remEdgesAB: list, nodePair: Union[tuple, list], relation: rel):
        """
        nodePair: node pair, max len if list = 2
        """
        subGraph = self.graph.subgraph(nodePair).copy()
        graph = self.graph.copy()
        data = [graph[n1][n2][key]['data'] for n1, n2, key in remEdgesAB]
        size = self.calcNewSize(relation, data)
        graph.remove_edges_from(remEdgesAB)

        graph.add_edge(nodePair[0], nodePair[1], subGraphName, data=Element(name=subGraphName, size=size))

        return NetlistGraph(graph, nodePair[0], nodePair[1], subGraph, subGraphName, relation)

    def _replaceNodesWithSubgraph(self, subGraphName: str, sequence: list, relation: rel):
        subGraph = (self.graph.subgraph(sequence)).copy()
        while (sequence[0], sequence[-1]) in subGraph.edges():
            subGraph.remove_edge(sequence[0], sequence[-1])

        graph = self.graph.copy()

        # this creates one list which contains all edges of the nodes in the sequence except the first and last node
        # those edges are already in the list by their predecessor
        edges = [e for node in sequence[1:-1] for e in graph.edges(node, keys=True)]
        data = [graph[n1][n2][key]['data'] for n1, n2, key in edges]
        size = self.calcNewSize(relation, data)

        graph.remove_nodes_from(sequence[1:-1])
        graph.add_edge(sequence[0], sequence[-1], subGraphName, data=Element(name=subGraphName, size=size))

        return NetlistGraph(graph, sequence[0], sequence[1], subGraph, subGraphName, relation)

    def findParallelSubGraph(self) -> Union[None, 'NetlistGraph']:

        paraSubGraphsNodePair = findParallelNode(self.graph)
        if paraSubGraphsNodePair:
            edgesAB = edgesBetweenNodes(self.graph, nodeAB=paraSubGraphsNodePair)
            assert edgesAB, "edgesAB not found, this is a problem (╯°□°)╯︵ ┻━┻"
            return self._replaceEdgesWithSubgraph("S" + str(self.idGenerator.newId), edgesAB, paraSubGraphsNodePair, rel.Parallel)

        return None

    def findRowSubGraph(self) -> Union[None, 'NetlistGraph']:
        rowNodeSequence = findRowNodesSequence(self.graph)

        if rowNodeSequence:
            return self._replaceNodesWithSubgraph("S" + str(self.idGenerator.newId), rowNodeSequence, rel.Row)

        return None


    def draw_graph(self):
        import matplotlib.pyplot as plt

        # Visualize the graph
        pos = spring_layout(self.graph)
        draw_networkx_nodes(self.graph, pos)
        draw_networkx_edges(self.graph, pos)
        draw_networkx_labels(self.graph, pos)

        # Add edge labels with keys
        edge_labels = {(u, v): k for u, v, k in self.graph.edges(keys=True)}
        draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)

        plt.show()
        print("-------------------------")
        print(self.subGraphName)
        print("Graph edges:" + str(self.graph.edges))
        print("Sub graph edges:" + str(self.subGraph.edges))

    @property
    def elementPositions(self):
        # Expose a dict of name: repr
        items = [self.graph[n1][n2][key]['data'] for n1, n2, key in self.graph.edges(keys=True)]
        return {item.name: item for item in items}