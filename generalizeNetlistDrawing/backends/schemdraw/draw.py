import schemdraw as sd
import schemdraw.elements as elm

from generalizeNetlistDrawing.linePositions import LinePosition
from generalizeNetlistDrawing.rasterisation import Rasterisation
from generalizeNetlistDrawing.elementPosition import ElementPosition

class DrawWithSchemdraw:
    def __init__(self, fileName):
        rasterizedNetFile = Rasterisation(fileName)
        self.elemPositions: dict[str, ElementPosition] = rasterizedNetFile.elementPositions
        self.linePositions: [LinePosition] = rasterizedNetFile.linePositions

        self.elementLength = 3
        self.transformGridSize(self.elementLength)
        d = sd.Drawing(backend='svg')
        for key in iter(self.elemPositions.keys()):
            elmPos = self.elemPositions[key]
            d.add(elm.Resistor().down().label(elmPos.name).at(elmPos.pos))
        for line in self.linePositions:
            d.add(elm.Line().at(line.a.asTuple).to(line.b.asTuple))
        d.draw()
        pass

    def transformGridSize(self, GRID_SIZE=3):
        """
        Transforms the Grid from one arbitrary unit to a specific spacing.
        One unit in schemdraw is 0.5 inches and this therefore is the standard value
        :param GRID_SIZE: scaling factor, spacing of the grid
        :return:
        """
        for key in iter(self.elemPositions.keys()):
            self.elemPositions[key].scaleSelf(GRID_SIZE)

        for line in self.linePositions:
            line.scaleSelf(GRID_SIZE)

