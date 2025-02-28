from idGenerator import IDGenerator
from lcapy import Circuit
from netlistToGraph import NetlistToGraph
from netlistGraph import NetlistGraph
from drawingTreeEntrie import DrawingTreeEntire

class DrawingTree:
    def __init__(self):
        self._idGen = IDGenerator()
        self.tree: list[DrawingTreeEntire] = []
        # create initial graph
        cct = Circuit("test1.txt")
        graph = NetlistToGraph(cct)
        self.graph = NetlistGraph(graph.MultiDiGraph(), graph.startNode, graph.endNode)
        self.createTree()
        print("test")

    def createTree(self):
        # create first element
        newGraph = NetlistGraph(self.graph.graph, self.graph.graphStart, self.graph.graphEnd)
        childGraphs = newGraph.findParallelSubGraphs(self._newID)

        newGraph2 = NetlistGraph(newGraph.graph, newGraph.graphStart, newGraph.graphEnd)
        childGraphs = newGraph2.findRowSubGraphs(self._newID)



    def _newID(self):
        return "G" + str(self._idGen.newId)