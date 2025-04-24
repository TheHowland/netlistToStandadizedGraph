import schemdrawInskale.elements as elm

from generalizeNetlistDrawing.elements.element import Element


class Resistor(Element):
    def schemdrawElement(self) -> elm.Resistor:
        return elm.Resistor().label(self.name).at(self.startPos.asTuple).to(self.endPos.asTuple)