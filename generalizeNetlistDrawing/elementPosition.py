class ElementPosition:
    def __init__(self, x=0, y=0, name=""):
        self.name = name
        self._xPos = x
        self._yPos = y

    def move(self, deltaX, deltaY):
        self._xPos += deltaX
        self._yPos += deltaY