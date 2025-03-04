import networkx as nx
from networkx.classes import MultiDiGraph
from idGenerator import IDGenerator
from typing import Union
from lcapy import Circuit
from netlistToGraph import NetlistToGraph
from netlistGraph import NetlistGraph
from drawingTreeEntrie import DrawingTreeEntire
from iterLimiter import IterLimiter
from networkx import MultiGraph

class FindSubStructures:
    def __init__(self, graph: NetlistGraph):
        self._idGen = IDGenerator()
        self.iterLim = IterLimiter(1000)
        self.graph = graph
        self.subStructures: dict[str, NetlistGraph] = {}
        self.createSubstitutions()

        print("finished init DrawingTree")

    def makeParaSubGraphs(self) -> bool:
        self.iterLim.reInit()
        changed = False
        while True:
            newGraph = NetlistGraph(self.graph.graph.copy(), self.graph.graphStart, self.graph.graphEnd)
            childGraphs = newGraph.findParallelSubGraphs(self._newID)
            if not childGraphs or self.iterLim.limitReached:
                break
            self.subStructures.update(childGraphs)
            self.graph = newGraph
            changed = True
        return changed

    def makeRowSubGraphs(self) -> bool:
        self.iterLim.reInit()
        changed = False
        while True:
            newGraph = NetlistGraph(self.graph.graph.copy(), self.graph.graphStart, self.graph.graphEnd)
            childGraphs = newGraph.findRowSubGraphs(self._newID)
            if not childGraphs or self.iterLim.limitReached:
                break
            self.subStructures.update(childGraphs)
            self.graph = newGraph
            changed = True
        return changed

    def createSubstitutions(self):
        changed = True
        while changed:
            changed = self.makeParaSubGraphs()
            changed = changed or self.makeRowSubGraphs()

    def _newID(self):
        return "G" + str(self._idGen.newId)