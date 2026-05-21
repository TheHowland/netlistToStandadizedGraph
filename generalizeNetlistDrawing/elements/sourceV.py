import schemdrawInskale.elements as elm

from generalizeNetlistDrawing.elements.source import Source

class SourceV(Source):
    def schemdrawElement(self) -> elm.StabilizedSource:
        direction = self.directionToText(self.direction())
        return elm.StabilizedSource(d=direction).label(self.name).at(self.startPos.asTuple).to(self.endPos.asTuple)