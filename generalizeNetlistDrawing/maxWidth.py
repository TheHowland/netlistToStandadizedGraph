class MaxWidth:
    def __init__(self, width: int, depth: int):
        self._width = width
        self._depth = depth

    def toList(self):
        return [self.width, self.depth]

    def toTuple(self):
        return self.width, self.depth

    @property
    def width(self) -> int:
        return self._width

    @property
    def depth(self) -> int:
        return self._depth