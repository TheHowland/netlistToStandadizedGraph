from findSubStructures import FindSubStructures
from lcapy import Circuit
from netlistToGraph import NetlistToGraph
from dependencyTree import DependencyTree
from netlistGraph import NetlistGraph
from placeElements import PlaceElements

class DrawingTree:
    def __init__(self):
        cct = Circuit("test1.txt")
        graph = NetlistToGraph(cct).toNetlistGraph()
        self.subStructures = FindSubStructures(graph)
        self.depTree = DependencyTree(self.subStructures.subStructures)

        startNodes = self.depTree.nodesWithNoSuccessor()
        for node in startNodes:
            netGraph = self.subStructures.subStructures[node]
            netGraph.draw_graph()
            netGraph.placeElements()

        predecessors = processedNodes.copy()
        while predecessors:
            node = predecessors.pop()
            netGraph = self.subStructures.subStructures[node]
            netGraph.draw_graph()
            netGraph.placeElements()
            size = netGraph.size

            if not predecessors:
                processedNodes = self.depTree.getPredecessors(processedNodes)
                predecessors = processedNodes.copy()

        pass