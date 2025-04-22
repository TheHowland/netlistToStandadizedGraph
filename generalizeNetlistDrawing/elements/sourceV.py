import schemdrawInskale.elements as elm

from generalizeNetlistDrawing.elements.element import Element


class SourceV(Element):
    def schemdrawElement(self) -> elm.StabilizedSource:
        direction = self.translateDirection()
        return elm.StabilizedSource(d=direction).label(self.name).at(self.endPos.asTuple)


    def netlistLine(self):
        raise NotImplemented("Netlist line not implemented for Line class")