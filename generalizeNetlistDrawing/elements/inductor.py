import schemdrawInskale.elements as elm

from generalizeNetlistDrawing.elements.element import Element


class Inductor(Element):
    def schemdrawElement(self) -> elm.Resistor:
        return elm.Inductor().label(self.name).at(self.startPos.asTuple).to(self.endPos.asTuple)

    def netlistLine(self):
        raise NotImplemented("Netlist line not implemented for Line class")