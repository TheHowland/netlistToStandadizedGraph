import schemdrawInskale.elements as elm

from generalizeNetlistDrawing.elements.element import Element
from generalizeNetlistDrawing.vector2D import Vector2D


class Resistor(Element):
    def __init__(self, vec1: Vector2D, vec2: Vector2D, name=""):
        direction = (vec1 - vec2).normalize()
        length = (vec2 - vec1).length()
        self.b = vec2

        angleDeg = direction.angle()
        if angleDeg <= -90:
            rotation = -1 * angleDeg - 90.0
        elif angleDeg < 0:
            rotation = 270 - - angleDeg  # 270 + angleDeg
        else:
            rotation = angleDeg - 90.0

        super().__init__(vec1.x, vec1.y, rotation=rotation, scaling=length)
        pass

    def schemdrawElement(self) -> elm.StabilizedSource:
        return elm.StabilizedSource().label(self.name).at(self.startPos.asTuple).to(self.endPos.asTuple)

    def netlistLine(self):
        pass