from generalizeNetlistDrawing.elements.element import Element
from generalizeNetlistDrawing.elements.line import Line
from generalizeNetlistDrawing.netlistGraph import NetlistGraph
from generalizeNetlistDrawing.vector2D import Vector2D


class LinePlacement:
    def __init__(self, netGraph: NetlistGraph, elementPositions: dict[str, Element]):
        self.netGraph = netGraph
        self.elementPositions = elementPositions
        self.linePositions: list[Line] = []
        self.nodeDepth: dict[str, float] = {}
        self.findVerticalLines()
        self.findHorizontalLines()
        pass

    def findVerticalLines(self):
        for node in iter(self.netGraph.graph.nodes):
            inEdges = self.netGraph.graph.in_edges(node, keys=True)
            if len(inEdges) >= 2:
                elmNames = [edgeInfo[2] for edgeInfo in iter(inEdges)]
                lastElmName = elmNames.pop()
                ySmallest = self.elementPositions[lastElmName].endPos.y
                yBiggest = self.elementPositions[lastElmName].endPos.y
                for elmName in elmNames:
                    newElmY = self.elementPositions[elmName].endPos.y
                    if ySmallest < newElmY:
                        ySmallest = newElmY
                    if yBiggest > newElmY:
                        yBiggest = newElmY

                self.nodeDepth[node] = yBiggest
                if ySmallest == yBiggest:
                    continue

                elmNames.append(lastElmName)
                for elmName in elmNames:
                    elmEndPos = self.elementPositions[elmName].endPos
                    if elmEndPos.y > yBiggest:
                        self.linePositions.append(Line(elmEndPos, Vector2D(elmEndPos.x, yBiggest)))

    def findHorizontalLines(self):
        for node in iter(self.netGraph.graph.nodes):
            if self.netGraph.graph.in_degree(node) >= 2:
                edges = self.netGraph.graph.in_edges(node, keys=True)
                elmNames = [edgeInfo[2] for edgeInfo in iter(edges)]
                elmPositions: list[Element] = [self.elementPositions[elmName] for elmName in elmNames]
                elmPositions.sort(key=lambda p: p.vector.x)
                for i in range(0, len(elmPositions)-1):
                    # semantically correct would be to use the end positions but the y component, which changes
                    # in the end position isn't used anyway
                    elm1X = self.elementPositions[elmNames[i]].vector.x
                    elm2X = self.elementPositions[elmNames[i+1]].vector.x
                    self.linePositions.append(Line(
                        Vector2D(elm1X, self.nodeDepth[node]),
                        Vector2D(elm2X, self.nodeDepth[node])
                    ))

            if self.netGraph.graph.out_degree(node) >= 2:
                edges = self.netGraph.graph.out_edges(node, keys=True)
                elmNames = [edgeInfo[2] for edgeInfo in iter(edges)]
                elmPositions: list[Element] = [self.elementPositions[elmName] for elmName in elmNames]
                # this has to be equal for each element because of the way they are placed
                # and they all have to be connected otherwise they would be placed elsewhere
                nodeDepth = elmPositions[0].vector.y
                elmPositions.sort(key=lambda p: p.vector.x)
                for i in range(0, len(elmPositions)-1):
                    elm1X = self.elementPositions[elmNames[i]].vector.x
                    elm2X = self.elementPositions[elmNames[i+1]].vector.x
                    self.linePositions.append(Line(
                        Vector2D(elm1X, nodeDepth),
                        Vector2D(elm2X, nodeDepth)
                    ))

    def getLinePositions(self):
        return self.linePositions
