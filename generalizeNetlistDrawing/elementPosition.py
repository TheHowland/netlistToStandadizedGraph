from vector2D import Vector2D

class ElementPosition:
    def __init__(self, x=0.0, y=0.0, name=""):
        self.name = name
        self.vector = Vector2D(x,y)

    def moveXY(self, delta: 'ElementPosition'):
        deltaX, deltaY = delta.pos
        self.moveX(deltaX)
        self.moveY(deltaY)

    def move(self, deltaX, deltaY):
        self.moveX(deltaX)
        self.moveY(deltaY)

    def moveX(self, deltaX):
        self.vector.x += deltaX

    def moveY(self, deltaY):
        self.vector.y += deltaY

    @property
    def pos(self):
        return self.vector.x, self.vector.y

    def __str__(self):
        if self.name != "":
            return f"{self.name}: {str(self.vector)}"
        else:
            return str(self.vector)

    def __add__(self, other: 'ElementPosition'):
        vec = self.vector + other.vector
        return ElementPosition(vec.x, vec.y)

    def __iadd__(self, other: 'ElementPosition'):
        self.vector += other.vector
        return self

    def __sub__(self, other: 'ElementPosition'):
        vec = self.vector - other.vector
        return ElementPosition(vec.x, vec.y)

    def __isub__(self, other: 'ElementPosition'):
        self.vector -= other.vector
        return self

    def __mul__(self, other: 'ElementPosition'):
        vec = self.vector * other.vector
        return ElementPosition(vec.x, vec.y)

    def scale(self, factor: float) -> 'ElementPosition':
        vec = self.vector.scale(factor)
        return ElementPosition(vec.x, vec.y)

    def scaleSelf(self, factor: float):
        self.vector.x *= factor
        self.vector.y *= factor
        return self

    def __abs__(self):
        return ElementPosition(abs(self.vector.x), abs(self.vector.y))