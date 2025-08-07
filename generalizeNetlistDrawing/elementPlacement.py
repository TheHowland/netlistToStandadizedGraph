from itertools import chain
from typing import Iterable

from lcapyInskale import Circuit

from generalizeNetlistDrawing.circuitToGraph import CircuitToGraph
from generalizeNetlistDrawing.elements.element import Element
from generalizeNetlistDrawing.graph_backend import GraphType
from generalizeNetlistDrawing.linePlacement import LinePlacement


class ElementPlacement:
    def __init__(self, fileContent: str):
        cct = Circuit(fileContent)
        self.transformer = CircuitToGraph(cct, GraphType)
        self.netGraph = self.transformer.NetlistGraph
        self.netGraph.place()
        self.elementPositions = self.netGraph.elementPositions

        lp = LinePlacement(self.netGraph, self.elementPositions)
        self.linePositions = lp.getLinePositions()
        self.nodePos = lp.nodePos

    @property
    def elements(self) -> Iterable[Element]:
        return chain(self.elementPositions.values(), self.linePositions)
if __name__ == "__main__":
    r = ElementPlacement("test1.txt")
