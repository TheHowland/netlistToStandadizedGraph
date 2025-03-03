import warnings
from idGenerator import IDGenerator
from lcapy import Circuit
from netlistToGraph import NetlistToGraph
from netlistGraph import NetlistGraph
from drawingTreeEntrie import DrawingTreeEntire
from iterLimiter import IterLimiter

class DrawingTree:
    def __init__(self):
        self._idGen = IDGenerator()
        self.tree: list[DrawingTreeEntire] = []
        self.iterLim = IterLimiter(1000)
        # create initial graph
        cct = Circuit("test1.txt")
        graph = NetlistToGraph(cct)
        self.graph = NetlistGraph(graph.MultiDiGraph(), graph.startNode, graph.endNode)
        self.createTree()
        print("finished init DrawingTree")

    def makeParaSubGraphs(self, graph: NetlistGraph) -> (NetlistGraph, bool):
        self.iterLim.reInit()
        changed = False
        while True:
            newGraph = NetlistGraph(graph.graph, graph.graphStart, graph.graphEnd)
            childGraphs = newGraph.findParallelSubGraphs(self._newID)
            if not childGraphs or self.iterLim.limitReached:
                break
            graph = newGraph
            changed = True
        return graph, changed

    def makeRowSubGraphs(self, graph: NetlistGraph) -> (NetlistGraph, bool):
        self.iterLim.reInit()
        changed = False
        while True:
            newGraph = NetlistGraph(graph.graph, graph.graphStart, graph.graphEnd)
            childGraphs = newGraph.findRowSubGraphs(self._newID)
            if not childGraphs or self.iterLim.limitReached:
                break
            graph = newGraph
            changed = True
        return graph, changed

    def makeTreeEntry(self):
        pass

    def createTree(self):
        graph = self.graph
        changed = True
        while changed:
            graph, changed = self.makeParaSubGraphs(graph)
            graph, changed = self.makeRowSubGraphs(graph)

        return graph

    def _newID(self):
        return "G" + str(self._idGen.newId)