import schemdrawInskale as sd

from generalizeNetlistDrawing.backends.positions import Optimize, Positions


class DrawWithSchemdraw(Positions):
    def __init__(self, fileContent: str, rotate: float=None, optimize: Optimize = Optimize.NONE, elementLength: float = 3):
        super().__init__(fileContent=fileContent, rotate=rotate, optimize=optimize, elementLength=elementLength)
        self.d = sd.Drawing(canvas='svg')

        for elmPos in iter(self.placedElems.elements):
            self.d.add(elmPos.schemdrawElement())

        self.d.draw()



if __name__ == '__main__':
    DrawWithSchemdraw("..\\..\\test1.txt")