import schemdrawInskale as sd
import schemdrawInskale.elements as elm

from generalizeNetlistDrawing.rastarisation import Rasterisation2 as Rasterisation
from generalizeNetlistDrawing.vector2D import Vector2D


class DrawWithSchemdraw:
    def __init__(self, fileName):
        self.rasterizedNetFile = Rasterisation(fileName)
        self.elemPositions = self.rasterizedNetFile.netGraph.elementPositions

        self.elementLength = 3
        self.transformGridSize(self.elementLength)
        self.d = sd.Drawing(canvas='svg')
        self.length = 0
        for key in iter(self.elemPositions.keys()):
            elmPos = self.elemPositions[key]
            self.d.add(elm.Resistor().down().label(elmPos.name).at(elmPos.startPos.asTuple))

        self.d.draw()
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

    def addSource(self):
        if self.rasterizedNetFile.transformer.ac_dc == "dc":
            source = elm.SourceV().up().label("V1")
        else:
            source = elm.SourceV().up().label("V1")
        bottomLeft = Vector2D(0, self.length)
        topLeft = Vector2D(0, 0)
        sourceMinus = Vector2D(-1, -1).scaleSelf(self.elementLength)
        sourcePlus = sourceMinus + Vector2D(0,1).scaleSelf(self.elementLength)
        endLineBottom = Vector2D(-1*self.elementLength, self.length)
        self.d.add(elm.Line().at(bottomLeft.asTuple).to(endLineBottom.asTuple))
        self.d.add(elm.Line().at(endLineBottom.asTuple).to(sourceMinus.asTuple))
        self.d.add(source).at(sourceMinus.asTuple)
        self.d.add(elm.Line().at(sourcePlus.asTuple).to(topLeft.asTuple))

if __name__ == '__main__':
    DrawWithSchemdraw("..\\..\\test1.txt")