from abc import ABC

from generalizeNetlistDrawing.elements.element import Element
from generalizeNetlistDrawing.vector2D import Vector2D

class Source(Element):
    def schemdrawElement(self):
        raise NotImplementedError("Source is an abstract class and cannot be drawn directly. Use SourceV or SourceI instead.")

    def _ac_type(self, node1, node2, direction):
        if self.netLine.ac_dc != "ac": raise ValueError("Trying to treat something that is not an ac source as such")
        return f"{self.name} {node1} {node2} ac {{{self.netLine.value}}} {{{self.netLine.phase}}} {{{self.netLine.omega}}}; {direction}\n"

    def _dc_type(self, node1, node2, direction):
        if self.netLine.ac_dc != "dc": raise ValueError("Trying to treat something that is not an dc source as such")
        return f"{self.name} {node1} {node2} dc {{{self.netLine.value}}}; {direction}\n"

    def netlistLine(self, nodeMap: dict[Vector2D, int], idGen: 'IDGenerator'):
        # todo give class necessary attributes
        node1 = nodeMap[self.startPos]
        node2 = nodeMap[self.endPos]
        direction = self.directionToText(self.direction())

        if self.netLine.ac_dc == "ac":
            return self._ac_type(node1, node2, direction)
        elif self.netLine.ac_dc == "dc":
            return self._dc_type(node1, node2, direction)
        else:
            raise ValueError(f"Unknown netLine ac_dc type in netlist line: {self.netLine.ac_dc}")