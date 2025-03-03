from networkx.classes import MultiDiGraph

from idGenerator import IDGenerator
from typing import Union
from lcapy import Circuit
from netlistToGraph import NetlistToGraph
from netlistGraph import NetlistGraph
from drawingTreeEntrie import DrawingTreeEntire
from iterLimiter import IterLimiter
from networkx import MultiGraph

class DrawingTree:
    def __init__(self):
        self._idGen = IDGenerator()
        self.iterLim = IterLimiter(1000)
        # create initial graph
        cct = Circuit("test1.txt")
        graph = NetlistToGraph(cct)
        self.graph = NetlistGraph(graph.MultiDiGraph(), graph.startNode, graph.endNode)
        self.childGraphs: dict[str, NetlistGraph] = {}
        self.createSubstitutions()
        self.dependencyTree = self._makeMakeDependencyTree()

        print("finished init DrawingTree")

    def makeParaSubGraphs(self) -> bool:
        self.iterLim.reInit()
        changed = False
        while True:
            newGraph = NetlistGraph(self.graph.graph.copy(), self.graph.graphStart, self.graph.graphEnd)
            childGraphs = newGraph.findParallelSubGraphs(self._newID)
            if not childGraphs or self.iterLim.limitReached:
                break
            self.childGraphs.update(childGraphs)
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
            self.childGraphs.update(childGraphs)
            self.graph = newGraph
            changed = True
        return changed

    def _makeMakeDependencyTree(self) -> MultiDiGraph:
        tree = MultiDiGraph()
        keys = list(self.childGraphs.keys())
        keys.reverse()
        for key in keys:
            tree.add_node(key)
            dependsOn = [x[2] for x in list(self.childGraphs[key].graph.edges(keys=True)) if x[2][0] == "G"]
            tree.add_nodes_from(dependsOn)
            for node in dependsOn:
                tree.add_edge(key, node)

        return tree

    def draw_dependencyTree(self):
        import matplotlib.pyplot as plt
        import networkx as nx

        # Visualize the graph
        pos = nx.spring_layout(self.dependencyTree)
        nx.draw_networkx_nodes(self.dependencyTree, pos)
        nx.draw_networkx_edges(self.dependencyTree, pos)
        nx.draw_networkx_labels(self.dependencyTree, pos)

        plt.show()

    def createSubstitutions(self):
        graph = self.graph
        changed = True
        while changed:
            changed = self.makeParaSubGraphs()
            changed = changed or self.makeRowSubGraphs()

    def _newID(self):
        return "G" + str(self._idGen.newId)