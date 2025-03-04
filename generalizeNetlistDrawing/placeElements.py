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
        self.elements: list[ElementPosition] = []
        self.createElementPositionsObjects()
        self.size = self.placeElements()
        print("finished init PlaceElements")

    def placeBottom(self):
        startNode = self.netGraph.graphStart
        if self.netGraph.graph.out_degree(startNode) == 1:
            return True
        else:
            return False

    def placeRight(self):
        startNode = self.netGraph.graphStart
        if self.graph.out_degree(startNode) >= 2:
            return True
        else:
            return False

    def createElementPositionsObjects(self):
        for edge in list(self.graph.edges(keys=True)):
            edgeName = edge[2]
            self.elements.append(ElementPosition(name=edgeName))

    def placeElements(self) -> int:
        if self.placeRight():
            size = ElementPosition(1, 1)
            offset = ElementPosition(1, 0)
        else: #self.placeBottom
            size = ElementPosition(1, -1)
            offset = ElementPosition(0, -1)

        for idx, elm in enumerate(self.elements):
            elm += offset.scale(idx)

        return abs(offset + size)


