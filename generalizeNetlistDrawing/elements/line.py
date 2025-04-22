import schemdrawInskale.elements as elm

from generalizeNetlistDrawing.elements.element import Element
from generalizeNetlistDrawing.vector2D import Vector2D


class Line(Element):
    def __init__(self, vec1: Vector2D, vec2: Vector2D, name=""):
        direction = (vec1 - vec2).normalize()
        length = (vec2 - vec1).length()

        angleDeg = direction.angle()
        rotation = angleDeg - 90.0

        super().__init__(vec1.x, vec1.y, rotation=rotation, scaling=length)
        pass

    def rotate(self, degree: float):
        newDirection = (self.direction().angle() - 90 + degree) % 360

        self.rotation = newDirection
        self.vector = self.vector.rotate(degree)

    def schemdrawElement(self) -> elm.Line:
        return elm.Line().label(self.name).at(self.startPos.asTuple).to(self.endPos.asTuple)

    def netlistLine(self):
        raise NotImplemented("Netlist line not implemented for Line class")