import schemdrawInskale as sd

from generalizeNetlistDrawing.elementPlacement import ElementPlacement


class DrawWithSchemdraw:
    def __init__(self, fileName):
        self.placedElems = ElementPlacement(fileName)

        self.elementLength = 3
        self.transformGridSize(self.elementLength)
        self.d = sd.Drawing(canvas='svg')
        self.length = 0

        for elmPos in iter(self.placedElems.elements):
            self.d.add(elmPos.schemdrawElement())

        drawing2 = sd.Drawing(canvas='svg')
        for elmPos in iter(self.placedElems.elements):
            elmPos.rotate(270)
            drawing2.add(elmPos.schemdrawElement())

        self.d.draw()
        drawing2.draw()
        pass

    def transformGridSize(self, GRID_SIZE=3):
        """
        Transforms the Grid from one arbitrary unit to a specific spacing.
        One unit in schemdraw is 0.5 inches and this therefore is the standard value
        :param GRID_SIZE: scaling factor, spacing of the grid
        :return:
        """
        for elm in iter(self.placedElems.elements):
            elm.scaleSelf(GRID_SIZE)

if __name__ == '__main__':
    DrawWithSchemdraw("..\\..\\test1.txt")