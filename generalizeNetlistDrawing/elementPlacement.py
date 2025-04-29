from itertools import chain
from typing import Iterable

import networkx as nx
from lcapyInskale import Circuit

from generalizeNetlistDrawing.circuitToGraph import CircuitToGraph
from generalizeNetlistDrawing.elements.element import Element
from generalizeNetlistDrawing.linePlacement import LinePlacement


class ElementPlacement:
    def __init__(self, fileContent: str):
        cct = Circuit(fileContent)
        self.transformer = CircuitToGraph(cct, nx.MultiDiGraph)
        self.netGraph = self.transformer.NetlistGraph
        self.netGraph.place()
        self.elementPositions = self.netGraph.elementPositions
        self.linePositions = LinePlacement(self.netGraph, self.elementPositions).getLinePositions()

    @property
    def elements(self) -> Iterable[Element]:
        return chain(self.elementPositions.values(), self.linePositions)
if __name__ == "__main__":
    r = ElementPlacement("test1.txt")
