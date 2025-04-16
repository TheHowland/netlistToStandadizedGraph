from math import cos, pi, sin, sqrt


class Vector2D:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"(x:{self.x} y: {self.y})"

    def __add__(self, other: 'Vector2D'):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2D'):
        return self.__add__(other.scale(-1))

    def __iadd__(self, other: 'Vector2D'):
        self.x = self.x + other.x
        self.y = self.y + other.y
        return self

    def __isub__(self, other: 'Vector2D'):
        return self.__iadd__(other.scale(-1))

    def __mul__(self, other: 'Vector2D'):
        return Vector2D(self.x * other.x, self.y * other.y)

    def __hash__(self):
        return hash(self.__str__())

    def scale(self, factor: float) -> 'Vector2D':
        return self.__mul__(Vector2D(factor, factor))

    def scaleSelf(self, factor: float):
        self.x *= factor
        self.y *= factor
        return self

    def __abs__(self):
        return Vector2D(abs(self.x), abs(self.y))

    def length(self) -> float:
        return sqrt(self.x**2 + self.y**2)

    def normalize(self) -> 'Vector2D':
        vecLen = self.length()
        return Vector2D(self.x/vecLen, self.y/vecLen)

    def normalizeSelf(self):
        vec = self.normalize()
        self.x = vec.x
        self.y = vec.y
        return self

    def rotate(self, angleDeg=None, angleRad=None):
        if angleDeg is not None:
            angleRad = pi * angleDeg / 180.0
        else:
            angleRad = angleRad
        # returns: RotMat2D * vec
        newX = self.x * cos(angleRad) - self.y * sin(angleRad)
        newY = self.x * sin(angleRad) + self.y * cos(angleRad)
        return Vector2D(newX, newY)

    @property
    def asTuple(self) -> tuple:
        return self.x, self.y