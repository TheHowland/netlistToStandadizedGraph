import schemdrawInskale.elements as elm

from generalizeNetlistDrawing.elements.source import Source


class SourceI(Source):
    def schemdrawElement(self) -> elm.StabilizedSource:
        return elm.SourceI().label(self.name).at(self.endPos.asTuple).to(self.startPos.asTuple)