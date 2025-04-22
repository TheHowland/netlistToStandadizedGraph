import schemdrawInskale.elements as elm

from generalizeNetlistDrawing.elements.element import Element


class SourceV(Element):
    def schemdrawElement(self) -> elm.StabilizedSource:
        return elm.SourceI().label(self.name).at(self.endPos.asTuple).to(self.startPos.asTuple)

    def netlistLine(self):
        raise NotImplemented("Netlist line not implemented for Line class")