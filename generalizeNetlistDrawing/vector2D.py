from math import atan2, cos, pi, sin, sqrt


class Vector2D:
    def __init__(self, x=0.0, y=0.0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return float(self._x)

    @property
    def y(self):
        return float(self._y)

    def __str__(self):
        return f"(x:{self.x} y: {self.y})"

    def __add__(self, other: 'Vector2D'):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2D'):
        return self.__add__(other.scale(-1))

    def __iadd__(self, other: 'Vector2D'):
        self._x = self.x + other.x
        self._y = self.y + other.y
        return self

    def __isub__(self, other: 'Vector2D'):
        return self.__iadd__(other.scale(-1))

    def __mul__(self, other: 'Vector2D'):
        return Vector2D(self.x * other.x, self.y * other.y)

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        return isinstance(other, Vector2D) and self.x == other.x and self.y == other.y

    def scale(self, factor: float) -> 'Vector2D':
        return self.__mul__(Vector2D(factor, factor))

    def scaleSelf(self, factor: float):
        self._x *= factor
        self._y *= factor
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
        self._x = vec.x
        self._y = vec.y
        return self

    def rotate(self, angleDeg=None, angleRad=None):
        """
        Rotate the vector by a given angle in degrees or radians counter clock wise, rounds to 10 decimal digits.
        returns: Rotation Matrix 2D * vec
        """
        if angleDeg is not None:
            angleRad = pi * angleDeg / 180.0
        else:
            angleRad = angleRad
        #
        newX = round(self.x * cos(angleRad) - self.y * sin(angleRad), 10)
        newY = round(self.x * sin(angleRad) + self.y * cos(angleRad), 10)
        return Vector2D(newX, newY)

    @property
    def asTuple(self) -> tuple:
        return self.x, self.y

    def angle(self, deg=True, rad=False) -> float:
        if deg and rad:
            raise ValueError("Only one of deg or rad can be True")
        angle = atan2(self.y, self.x)

        if angle < 0:
            angle = pi - angle

        if rad:
            return angle
        else:
            return angle * 180 / pi

