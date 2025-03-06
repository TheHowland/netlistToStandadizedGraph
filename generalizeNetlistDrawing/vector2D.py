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

    def scale(self, factor: float) -> 'Vector2D':
        return Vector2D(self.x * factor, self.y * factor)

    def scaleSelf(self, factor: float):
        self.x *= factor
        self.y *= factor
        return self

    def __abs__(self):
        return Vector2D(abs(self.x), abs(self.y))