import schemdrawInskale.elements as elm

from generalizeNetlistDrawing.elements.element import Element
from generalizeNetlistDrawing.vector2D import Vector2D


class Inductor(Element):
    def schemdrawElement(self) -> elm.Resistor:
        return elm.Inductor().label(self.name).at(self.startPos.asTuple).to(self.endPos.asTuple)