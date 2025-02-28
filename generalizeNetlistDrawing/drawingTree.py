from idGenerator import IDGenerator


class DrawingTree:
    def __init__(self):
        self._idGen = IDGenerator()

    @property
    def _newID(self):
        return "G" + str(self._idGen.newId)