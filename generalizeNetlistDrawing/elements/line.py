import schemdrawInskale.elements as elm

from generalizeNetlistDrawing.elements.element import Element
from generalizeNetlistDrawing.idGenerator import IDGenerator
from generalizeNetlistDrawing.vector2D import Vector2D


class Line(Element):
    def __init__(self, vec1: Vector2D, vec2: Vector2D, netLine=""):
        direction = (vec1 - vec2).normalize()
        length = (vec2 - vec1).length()

        angleDeg = direction.angle()
        rotation = angleDeg - 90.0

        super().__init__(vec1.x, vec1.y, netLine=netLine, rotation=rotation, scaling=length)
        pass

    def rotate(self, degree: float):
        newDirection = (self.direction().angle() + 90 + degree) % 360

        self.rotation = newDirection
        self.vector = self.vector.rotate(degree)

    def schemdrawElement(self) -> elm.Line:
        return elm.Line().at(self.startPos.asTuple).to(self.endPos.asTuple)

    def netlistLine(self, nodeMap: dict[Vector2D, int], idGen: 'IDGenerator') -> str:
        # if line isn't a multiple of 1 it cant be represented in the lcapy netlist
        node1 = nodeMap[self.startPos]
        node2 = nodeMap[self.endPos]
        
        if self.length % 1:
            raise RuntimeError("Line length is not a multiple of 1, cannot be represented in the lcapy netlist")
        lines = ""
        direction = self.translateDirection()
        if self.length == 1:
            return f"W {node1} {node2}; {direction}\n"
        else:
            lastID = idGen.newId
            lines += f"W {node1} {lastID}; {direction}\n"
            for i in range(1, int(self.length)-1):
                newID = idGen.newId
                lines += f"W {lastID} {newID}; {direction}\n"
                lastID = newID
            lines += f"W {lastID} {node2}; {direction}\n"
            return lines