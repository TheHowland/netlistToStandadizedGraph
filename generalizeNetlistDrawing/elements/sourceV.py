import schemdrawInskale.elements as elm

from generalizeNetlistDrawing.elements.element import Element


class SourceV(Element):
    def schemdrawElement(self) -> elm.StabilizedSource:
        return elm.StabilizedSource().label(self.name).at(self.startPos.asTuple).to(self.endPos.asTuple)

    def netlistLine(self):
        raise NotImplemented("Netlist line not implemented for Line class")