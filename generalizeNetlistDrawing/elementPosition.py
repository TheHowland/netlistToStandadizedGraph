class ElementPosition:
    def __init__(self, x=0.0, y=0.0, name=""):
        self.name = name
        self._xPos = x
        self._yPos = y

    def moveXY(self, delta: 'ElementPosition'):
        deltaX, deltaY = delta.pos
        self.moveX(deltaX)
        self.moveY(deltaY)

    def move(self, deltaX, deltaY):
        self.moveX(deltaX)
        self.moveY(deltaY)

    def moveX(self, deltaX):
        self._xPos += deltaX

    def moveY(self, deltaY):
        self._yPos += deltaY

    @property
    def pos(self):
        return self._xPos, self._yPos

    def __str__(self):
        if self.name != "":
            return f"{self.name}: ({self._xPos};{self._yPos})"
        else:
            return f"x:{self._xPos} y: {self._yPos}"

    def __add__(self, other: 'ElementPosition'):
        otherX, otherY = other.pos
        selfX, selfY = self.pos
        return ElementPosition(selfX + otherX, selfY + otherY)

    def __iadd__(self, other: 'ElementPosition'):
        otherX, otherY = other.pos
        self.move(otherX, otherY)
        return self

    def __sub__(self, other: 'ElementPosition'):
        otherX, otherY = other.pos
        return self.__add__(ElementPosition(-1*otherX, -1*otherY))

    def __isub__(self, other: 'ElementPosition'):
        otherX, otherY = other.pos
        self.move(-1*otherX, -1*otherY)
        return self

    def __mul__(self, other: 'ElementPosition'):
        otherX, otherY = other.pos
        selfX, selfY = self.pos
        return ElementPosition(selfX * otherX, selfY * otherY)

    def scale(self, factor: float) -> 'ElementPosition':
        selfX, selfY = self.pos
        return ElementPosition(selfX * factor, selfY * factor)

    def scaleSelf(self, factor: float):
        self._xPos *= factor
        self._yPos *= factor
        return self

    def __abs__(self):
        selfX, selfY = self.pos
        return ElementPosition(abs(selfX), abs(selfY))