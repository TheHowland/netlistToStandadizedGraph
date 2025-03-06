from vector2D import Vector2D

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
            return notAMultipleOf90Deg