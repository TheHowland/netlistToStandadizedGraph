from enum import Enum

import schemdrawInskale as sd

from generalizeNetlistDrawing.elementPlacement import ElementPlacement


class Optimize(Enum):
    NONE = None
    DESKTOP = 'desktop'
    MOBILE = 'mobile'

class DrawWithSchemdraw:
    def __init__(self, fileName, rotate: float=None, optimize: Optimize = Optimize.NONE):

        self.placedElems = ElementPlacement(fileName)

        self.elementLength = 3
        self.transformGridSize(self.elementLength)
        self.d = sd.Drawing(canvas='svg')
        self.length = 0

        if rotate:
            self.rotate(rotate)

        if optimize.value:
            self.optimize(optimize)

        for elmPos in iter(self.placedElems.elements):
            self.d.add(elmPos.schemdrawElement())

        self.d.draw()

    def transformGridSize(self, GRID_SIZE=3):
        """
        Transforms the Grid from one arbitrary unit to a specific spacing.
        One unit in schemdraw is 0.5 inches and this therefore is the standard value
        :param GRID_SIZE: scaling factor, spacing of the grid
        :return:
        """
        for elm in iter(self.placedElems.elements):
            elm.scaleSelf(GRID_SIZE)

    def rotate(self, degree: float):
        for elm in iter(self.placedElems.elements):
            elm.rotate(degree)

    def maxXMaxY(self):
        globMaxX, globMaxY = 0, 0
        for elm in iter(self.placedElems.elements):
            x1, y1 = elm.startPos.asTuple
            x2, y2 = elm.endPos.asTuple
            maxX = max(x1, x2)
            maxY = max(y1, y2)
            if maxX > globMaxX:
                globMaxX = maxX
            if maxY > globMaxY:
                globMaxY = maxY

        return globMaxX, globMaxY

    def optimize(self, optimize: Optimize):
        if optimize == Optimize.MOBILE:
            self.optimizeMobile()
        elif optimize == Optimize.DESKTOP:
            self.optimizeDesktop()
        else:
            return


    def optimizeMobile(self):
        globMaxX, globMaxY = self.maxXMaxY()

        if globMaxX > globMaxY:
            self.rotate(90)

    def optimizeDesktop(self):
        globMaxX, globMaxY = self.maxXMaxY()

        if globMaxY > globMaxX:
            self.rotate(90)

if __name__ == '__main__':
    DrawWithSchemdraw("..\\..\\test1.txt")