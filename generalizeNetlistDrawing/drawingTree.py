from findSubStructures import FindSubStructures
from lcapy import Circuit
from netlistToGraph import NetlistToGraph
from dependencyTree import DependencyTree
from netlistGraph import NetlistGraph

class DrawingTree:
    def __init__(self):
        cct = Circuit("test1.txt")
        graph = NetlistToGraph(cct).toNetlistGraph()
        self.subStructures = FindSubStructures(graph)
        self.depTree = DependencyTree(self.subStructures.subStructures)
        self.elementPositions = PlaceElements(self.depTree.depTree)
        pass