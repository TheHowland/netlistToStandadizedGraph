from idGenerator import IDGenerator
from typing import Union
from lcapy import Circuit
from netlistToGraph import NetlistToGraph
from netlistGraph import NetlistGraph
from drawingTreeEntrie import DrawingTreeEntire
from iterLimiter import IterLimiter

class DrawingTree:
    def __init__(self):
        self._idGen = IDGenerator()
        self.iterLim = IterLimiter(1000)
        # create initial graph
        cct = Circuit("test1.txt")
        graph = NetlistToGraph(cct)
        self.graph = NetlistGraph(graph.MultiDiGraph(), graph.startNode, graph.endNode)
        self.treeStart: Union[DrawingTreeEntire, None] = None
        self.parent: Union[DrawingTreeEntire, None] = None
        self.createTree()
        print("finished init DrawingTree")

    def makeParaSubGraphs(self) -> bool:
        self.iterLim.reInit()
        changed = False
        parent = self.treeStart
        while True:
            newGraph = NetlistGraph(self.graph.graph, self.graph.graphStart, self.graph.graphEnd)
            childGraphs = newGraph.findParallelSubGraphs(self._newID)
            if not childGraphs or self.iterLim.limitReached:
                break
            self.graph = newGraph
            changed = True
        return changed

    def makeRowSubGraphs(self) -> bool:
        self.iterLim.reInit()
        changed = False
        while True:
            newGraph = NetlistGraph(self.graph.graph, self.graph.graphStart, self.graph.graphEnd)
            childGraphs = newGraph.findRowSubGraphs(self._newID)
            if not childGraphs or self.iterLim.limitReached:
                break
            self.graph = newGraph
            changed = True
        return changed

    def makeTreeEntry(self):
        pass

    def createTree(self):
        graph = self.graph
        changed = True
        while changed:
            changed = self.makeParaSubGraphs()
            changed = changed or self.makeRowSubGraphs()

        return graph

    def _newID(self):
        return "G" + str(self._idGen.newId)