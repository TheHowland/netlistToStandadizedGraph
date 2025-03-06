from elementPosition import ElementPosition

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
        self.graph = self.netGraph.graph
        self.elements: dict[str, ElementPosition] = {}
        self.createElementPositionsObjects()
        self.size = self.placeElements()
        print("finished init PlaceElements")

    def placeBottom(self):
        startNode = self.netGraph.graphStart
        if self.netGraph.graph.out_degree(startNode) == 1:
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

    def getPositions(self, exclude: set) -> dict[str, ElementPosition]:
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

    def getElementPositions(self) -> dict[str, ElementPosition]:
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
        for edge in list(self.graph.edges(keys=True)):
            edgeName = edge[2]
            self.elements[edgeName] = ElementPosition(name=edgeName)

    def placeElements(self) -> tuple[int, int]:
        if self.placeRight():
            size = ElementPosition(1, 1)
            offset = ElementPosition(1, 0)
        else: #self.placeBottom
            size = ElementPosition(1, -1)
            offset = ElementPosition(0, -1)

        for idx, key in enumerate(self.elements.keys()):
            self.elements[key] += offset.scale(idx)

        return (abs(offset + size)).pos

    def moveElements(self, delta: ElementPosition):
        for key in iter(self.elements.keys()):
            self.elements[key].moveXY(delta)


