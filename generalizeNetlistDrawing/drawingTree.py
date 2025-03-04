from findSubStructures import FindSubStructures
from lcapy import Circuit
from netlistToGraph import NetlistToGraph
from netlistGraph import NetlistGraph

class DrawingTree:
    def __init__(self):
        cct = Circuit("test1.txt")
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
        graph = NetlistToGraph(cct).toNetlistGraph()
        self.subStructures = FindSubStructures(graph)
        self.depTree = DependencyTree(self.subStructures.subStructures)
        self.elementPositions = PlaceElements(self.depTree.depTree)
        pass