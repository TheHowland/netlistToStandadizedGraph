from netlistGraph import NetlistGraph
from elementPosition import ElementPosition

class LinePlacement:
    def __init__(self, netGraph: NetlistGraph, elementPositions: dict[str, ElementPosition]):
        self.netGraph = netGraph
        self.elementPositions = elementPositions