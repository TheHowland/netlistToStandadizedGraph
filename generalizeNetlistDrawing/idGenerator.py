class IDGenerator:
    _counter = 0

    @property
    def newId(self):
        self._counter += 1
        return self._counter