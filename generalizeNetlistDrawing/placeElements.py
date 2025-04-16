from networkx import all_simple_edge_paths

from element import Element


class PlaceElements:
    def __init__(self, graph: 'NetlistGraph'):
        """
        This class is used to determine element positions in simple graphs where edges only
        occur beside each other, horizontally or vertically. Two nodes with multiple edges between them or n nodes with
        that only have one incoming and one outgoing edge except the start and end node which only have
        an incoming or outgoing edge. It does not check if the structure it is used on is simple enough to work.

        :param graph:
        """
        self.netGraph = graph
        self.graph = self.netGraph.Graph
        self.elements: dict[str, Element] = {}
        self.createElementPositionsObjects()
        self.size = self.placeElements()

    def placeBottom(self):
        startNode = self.netGraph.graphStart
        if self.netGraph.Graph.out_degree(startNode) == 1:
            return True
        else:
            return False

    @property
    def excludeGraphs(self) -> set:
        exclude = set()
        for key in self.elements:
            if key[0] == 'G':
                exclude.add(key)
        return exclude

    def getPositions(self, exclude: set) -> dict[str, Element]:
        """
        :param exclude: a set of keys that shall be excluded from the returned dict and is part of the keys
         from self.elements
        :return: all positions, including created sub graphs
        """
        keys = set(self.elements.keys()) - exclude
        elements = {}
        for key in keys:
            elements[key] = self.elements[key]

        return elements

    def getElementPositions(self) -> dict[str, Element]:
        """
        :return: all positions of elements that where in the original graph, and excludes the graphs needed for the
        rasterisation process
        """
        return self.getPositions(self.excludeGraphs)

    def placeRight(self):
        startNode = self.netGraph.graphStart
        if self.graph.out_degree(startNode) >= 2:
            return True
        else:
            return False

    def createElementPositionsObjects(self):
        if self.placeRight():
            for edge in list(self.graph.edges(keys=True)):
                edgeName = edge[2]
                self.elements[edgeName] = Element(name=edgeName)
        else:
            for edge in list(all_simple_edge_paths(self.graph, self.netGraph.graphStart, self.netGraph.graphEnd))[0]:
                edgeName = edge[2]
                self.elements[edgeName] = Element(name=edgeName)


    def placeElements(self) -> tuple[int, int]:
        if self.placeRight():
            size = Element(1, 1)
            offset = Element(1, 0)
        else: #self.placeBottom
            size = Element(1, -1)
            offset = Element(0, -1)

        for idx, key in enumerate(self.elements.keys()):
            self.elements[key] += offset.scale(idx)

        return (abs(offset + size)).startPos.asTuple

    def moveElements(self, delta: Element):
        for key in iter(self.elements.keys()):
            self.elements[key].moveXY(delta)


