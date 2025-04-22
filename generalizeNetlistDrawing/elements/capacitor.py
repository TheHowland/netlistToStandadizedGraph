import schemdrawInskale.elements as elm

from generalizeNetlistDrawing.elements.element import Element


class Capacitor(Element):
    def schemdrawElement(self) -> elm.Resistor:
        return elm.Capacitor().label(self.name).at(self.startPos.asTuple).to(self.endPos.asTuple)

    def netlistLine(self):
        raise NotImplemented("Netlist line not implemented for Line class")