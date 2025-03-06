from vector2D import Vector2D

class ElementPosition:
    def __init__(self, x=0.0, y=0.0, name="", vec: Vector2D = None):
        self.name = name
        self._scaling = 1
        if not vec:
            self.vector = Vector2D(x,y)
        else:
            self.vector = Vector2D(vec.x, vec.y)

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

    @property
    def endPos(self) -> Vector2D:
        return self.vector+Vector2D(0, -1).scaleSelf(self._scaling)

    def __str__(self):
        if self.name != "":
            return f"{self.name}: {str(self.vector)}"
        else:
            return str(self.vector)

    def __add__(self, other: 'ElementPosition'):
        return ElementPosition(vec=self.vector + other.vector)

    def __iadd__(self, other: 'ElementPosition'):
        self.vector += other.vector
        return self

    def __sub__(self, other: 'ElementPosition'):
        return ElementPosition(vec=self.vector - other.vector)

    def __isub__(self, other: 'ElementPosition'):
        self.vector -= other.vector
        return self

    def __mul__(self, other: 'ElementPosition'):
        return ElementPosition(vec=self.vector * other.vector)

    def scale(self, factor: float) -> 'ElementPosition':
        self._scaling = factor
        return ElementPosition(vec=self.vector.scale(factor))

    def scaleSelf(self, factor: float):
        self._scaling = factor
        self.vector.x *= factor
        self.vector.y *= factor
        return self

    def __abs__(self):
        return ElementPosition(vec=abs(self.vector))