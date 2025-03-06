from vector2D import Vector2D
from math import sqrt

class LinePosition:
    def __init__(self, vec1: Vector2D, vec2: Vector2D, name=""):
        self.a = vec1
        self.b = vec2

    def direction(self) -> Vector2D:
        return (self.b - self.a).normalizeSelf()

    def scaleSelf(self, factor: float):
        self.a.scaleSelf(factor)
        self.b.scaleSelf(factor)

    def scale(self, factor: float) -> 'LinePosition':
        return LinePosition(self.a.scale(factor), self.b.scale(factor))

    def translateDirection(self, notAMultipleOf90Deg: any='down'):
        direction = self.direction()
        if direction == Vector2D(1,0):
            return 'right'
        elif direction == Vector2D(-1, 0):
            return 'left'
        elif direction == Vector2D(0, 1):
            return 'up'
        elif direction == Vector2D(0, -1):
            return 'down'
        else:
            from warnings import warn
            warn("got a direction that was not a multiple of 90°")
            return notAMultipleOf90Deg

    @property
    def startPos(self) -> Vector2D:
        return Vector2D(self.a.x, self.a.y)

    @property
    def endPos(self) -> Vector2D:
        return Vector2D(self.b.x, self.b.y)

    def __str__(self):
        return f"start (x:{self.a.x} y:{self.a.y}) end (x:{self.b.x} y:{self.b.y}))"

    def length(self):
        lenVec = self.b - self.a
        return sqrt(lenVec.x**2+lenVec.y**2)

    def netLine(self, node1, node2):
        return f"W {node1} {node2}; {self.translateDirection()}\n"