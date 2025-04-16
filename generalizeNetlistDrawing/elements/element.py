from abc import abstractmethod
from enum import Enum

from generalizeNetlistDrawing.vector2D import Vector2D


class Direction(Enum):
    down = 0
    up = 180
    left = 90
    right = 270

class Element:
    def __init__(self, x=0.0, y=0.0, name="", vec: Vector2D = None, size: Vector2D = None, rotation=0, scaling=1.0):
        """
        :param x: x coordinate of the element
        :param y: y coordinate of the element
        :param vec: Vector2D object representing x and y
        :param name: name of the element
        :param size: size of the element, equals the length of an element if it isn't a combination of multiple elements
        :param rotation: rotation of the element in degrees, 0 is oriented downward from (0,0) to (0,-1), rotation counterclockwise
        """
        self.name = name
        self._scale = scaling
        self.rotation = rotation
        if not vec:
            self.vector = Vector2D(x,y)
        else:
            self.vector = Vector2D(vec.x, vec.y)
        self.size: Vector2D = Vector2D(1,1) if size is None else size

    def direction(self) -> Vector2D:
        return (self.startPos - self.endPos).normalize()

    @property
    def length(self) -> float:
        return self.vector.length()

    def translateDirection(self):
        """
        give back a string that represents the direction the element points in. Empty string if the element has no direction.
        This may happen if the scaling (length) is 0.
        returns: 'up', 'down', 'left', 'right', ''
        """
        direction = self.direction()
        if direction.y == 0 and not direction.x == 0:
            if direction.x > 0:
                return 'right'
            else: # direction.x < 0 :
                return 'left'
        elif direction.x == 0 and not direction.y == 0:
            if direction.y > 0:
                return 'up'
            else: # direction.y < 0:
                return 'down'
        else:
            return ''

    def netLine(self, node1:str, node2:str):
        return f"{self.name} {node1} {node2}; down\n"

    def moveXY(self, delta: 'Element'):
        deltaX, deltaY = delta.startPos.asTuple
        self.moveX(deltaX)
        self.moveY(deltaY)

    def move(self, deltaX=None, deltaY=None, vec: Vector2D = None):
        if not (deltaX and deltaY):
            deltaX, deltaY = vec.asTuple
        self.moveX(deltaX)
        self.moveY(deltaY)

    def moveX(self, deltaX):
        self.vector.x += deltaX

    def moveY(self, deltaY):
        self.vector.y += deltaY

    @property
    def startPos(self) -> Vector2D:
        return Vector2D(self.vector.x, self.vector.y)

    @property
    def endPos(self) -> Vector2D:
        return self.vector+(Vector2D(0, -1).rotate(angleDeg=self.rotation)).scaleSelf(self._scale)

    def __str__(self):
        if self.name != "":
            return f"{self.name}: {str(self.vector)}"
        else:
            return str(self.vector)

    def __add__(self, other: 'Element'):
        return Element(vec=self.vector + other.vector)

    def __iadd__(self, other: 'Element'):
        self.vector += other.vector
        return self

    def __sub__(self, other: 'Element'):
        return Element(vec=self.vector - other.vector)

    def __isub__(self, other: 'Element'):
        self.vector -= other.vector
        return self

    def __mul__(self, other: 'Element'):
        return Element(vec=self.vector * other.vector)

    def scale(self, factor: float) -> 'Element':
        self._scale = factor
        return Element(vec=self.vector.scale(factor))

    def scaleSelf(self, factor: float):
        self._scale *= factor
        self.vector.x *= factor
        self.vector.y *= factor
        return self

    def __abs__(self):
        return Element(vec=abs(self.vector))

    def rotation(self) -> float:
        angleDeg = self.direction().angle()
        if angleDeg <= -90:
            return -1*angleDeg - 90.0
        if angleDeg < 0:
            return 270 - - angleDeg # 270 + angleDeg

        return angleDeg - 90.0

    def getPosWhere(self, lamdaFkt) -> Vector2D:
        """the lambda function get self.startPos and self.endPos as arguments and checks if
        the lambda fkt is true for (startPos, endPos) or (endPos, startPos) if true for (startPos, endPos) returns
        startPos else returns endPos"""
        if lamdaFkt(self.startPos, self.endPos):
            return self.startPos
        else:
            return self.endPos

    @property
    def getMinY(self) -> Vector2D:
        return self.getPosWhere(lambda a,b: a.y < b.y).y

    @abstractmethod
    def schemdrawElement(self):
        pass

    @abstractmethod
    def netlistLine(self):
        pass
