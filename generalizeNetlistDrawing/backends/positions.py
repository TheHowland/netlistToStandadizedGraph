from enum import Enum

from generalizeNetlistDrawing.elementPlacement import ElementPlacement


class Optimize(Enum):
    NONE = None
    DESKTOP = 'desktop'
    MOBILE = 'mobile'

class Positions:
    def __init__(self, fileContent: str, rotate: float = None, optimize: Optimize = Optimize.NONE, elementLength: float = 3):
        self.placedElems = ElementPlacement(fileContent)

        self.elementLength = elementLength
        self.transformGridSize(self.elementLength)
        self.length = 0

        if rotate:
            self.rotate(rotate)

        if optimize.value:
            self.optimize(optimize)

    def transformGridSize(self, GRID_SIZE: float=3.0):
        """
        Transforms the Grid from one arbitrary unit to a specific spacing.
        One unit in schemdraw is 3 and this therefore is the standard value
        :param GRID_SIZE: scaling factor, spacing of the grid
        :return:
        """
        for elm in iter(self.placedElems.elements):
            elm.scaleSelf(GRID_SIZE)

    def rotate(self, degree: float):
        for elm in iter(self.placedElems.elements):
            elm.rotate(degree)

        for nodeOccList in iter(self.placedElems.nodePos.values()):
            for dot in nodeOccList:
                dot.rotateSelf(degree)

    def maxXMaxY(self):
        globMaxX, globMaxY = 0, 0
        for elm in iter(self.placedElems.elements):
            x1, y1 = elm.startPos.asTuple
            x2, y2 = elm.endPos.asTuple
            maxX = max(abs(x1), abs(x2))
            maxY = max(abs(y1), abs(y2))
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