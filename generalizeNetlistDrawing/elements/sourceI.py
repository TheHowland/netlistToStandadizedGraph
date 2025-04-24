import schemdrawInskale.elements as elm

from generalizeNetlistDrawing.elements.element import Element
from generalizeNetlistDrawing.vector2D import Vector2D


class SourceI(Element):
    def schemdrawElement(self) -> elm.StabilizedSource:
        return elm.SourceI().label(self.name).at(self.endPos.asTuple).to(self.startPos.asTuple)

    def netlistLine(self, nodeMap: dict[Vector2D, int], idGen: 'IDGenerator'):
        # todo give class necessary attributes
        node1 = nodeMap[self.startPos]
        node2 = nodeMap[self.endPos]
        direction = self.directionToText(self.direction()*Vector2D(-1, -1))
        return f"{self.name} {node2} {node1} dc {{{self.name}}}; {direction}\n"