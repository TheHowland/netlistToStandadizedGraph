from typing import Any

from generalizeNetlistDrawing.elements.element import Element
from generalizeNetlistDrawing.elements.line import Line
from generalizeNetlistDrawing.netlistGraph import NetlistGraph
from generalizeNetlistDrawing.vector2D import Vector2D


class LinePlacement:
    def __init__(self, netGraph: NetlistGraph, elementPositions: dict[str, Element]):
        self.netGraph = netGraph
        self.elementPositions = elementPositions
        self.linePositions: list[Line] = []
        nodePos = self._findPositionsToNodes()
        self._findVerticalLines(nodePos)
        self._findHorizontalLines(nodePos)

        #self.nodeDepth: dict[str, float] = {}
        #self.leg_findVerticalLines()
        #self.leg_findHorizontalLines()
        pass

    def _findPositionsToNodes(self) -> dict[Any, list[Vector2D]]:
        """
        returns a list with unique positions for each node
        """
        nodePos = {}
        for node in iter(self.netGraph.graph.nodes):
            positionsToNode = set()
            edges = [edge for edge in self.netGraph.graph.edges(data=True) if edge[0] == node or edge[1] == node]

            for edge in edges:
                if edge[0] == node:
                    positionsToNode.add(edge[2]['data'].startPos)
                else:
                    positionsToNode.add(edge[2]['data'].endPos)

            nodePos[node] = list(positionsToNode)

        return nodePos

    def _findVerticalLines(self, nodePos: dict[Any, list[Vector2D]]):

        for node in nodePos.keys():
            # Vertical lines are needed in parallel branches that have a different number of elements.
            # The component with the smallest y value determines the y coordinate of the node.
            # Each element that is connected to this node and has a different y coordinate needs a line that
            # fills the gap between the determined y coordinate and the coordinate of the component.
            ySmallest = min([vec.y for vec in nodePos[node]])
            for pos in nodePos[node]:
                if pos.y != ySmallest:
                    self.linePositions.append(Line(
                        Vector2D(pos.x, ySmallest),
                        Vector2D(pos.x, pos.y)
                    ))

    def _findHorizontalLines(self, nodePos: dict[Any, list[Vector2D]]):
        # this function only works if _findVerticalLines() is called first. With the reasignt y coordinates finding
        # horizontal lines is much easier.
        for node in nodePos.keys():
            positions = nodePos[node]
            if len(positions) > 1:
                # Get the smallest y coordinate that determines the y coordinate of the node
                ySmallest = min([vec.y for vec in nodePos[node]])
                # Sort the positions, this enables to draw lines between two neighboring elements in the list
                positions.sort(key=lambda p: p.x)
                # Draw lines between neighboring elements in the list.
                # It would also work to draw a line from xSmallest to xBiggest. Drawing one line would make it much harder
                # to detect where lines and elements meet if an element meets a line in the middle of the line
                for i in range(0, len(positions)-1):
                    self.linePositions.append(Line(
                        Vector2D(positions[i].x, ySmallest),
                        Vector2D(positions[i+1].x, ySmallest)
                    ))

    def getLinePositions(self):
        return self.linePositions
