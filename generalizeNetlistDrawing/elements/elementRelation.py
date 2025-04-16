from enum import Enum

class ElementRelation(Enum):
    """Enum for different types of element relations in a netlist."""
    NONE = 0
    Parallel = 1
    Row = 2

    def __str__(self):
        return self.name