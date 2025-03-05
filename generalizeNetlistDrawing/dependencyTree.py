from networkx import MultiDiGraph
from networkx import dfs_successors
from netlistGraph import NetlistGraph
from itertools import chain as flattenList


class DependencyTree:
    def __init__(self, subGraphs: dict[str, NetlistGraph]):
        self.subGraphs: dict[str, NetlistGraph] = subGraphs
        self.depTree = self._makeMakeDependencyTree()
        self.draw_dependencyTree()
        print("finished init DependencyTree")

    def reachableNodes(self, node: any):
        return list(flattenList(*(dfs_successors(self.depTree, node).values())))

    def getPredecessors(self, nodes: list[any]) -> list:
        predecessors = set()
        for node in nodes:
            for predecessor in list(self.depTree.predecessors(node)):
                predecessors.add(predecessor)

        return list(predecessors)

    def _makeMakeDependencyTree(self) -> MultiDiGraph:
        tree = MultiDiGraph()
        keys = list(self.subGraphs.keys())
        keys.reverse()
        for key in keys:
            tree.add_node(key)
            dependsOn = [x[2] for x in list(self.subGraphs[key].graph.edges(keys=True)) if x[2][0] == "G"]
            tree.add_nodes_from(dependsOn)
            for node in dependsOn:
                tree.add_edge(key, node)

        return tree

    def nodesWithNoSuccessor(self) -> list[any]:
        noSucc = []
        for node in self.depTree.nodes:
            if self.depTree.out_degree(node) == 0:
                noSucc.append(node)

        return noSucc

    def draw_dependencyTree(self):
        import matplotlib.pyplot as plt
        import networkx as nx

        # Visualize the graph
        pos = nx.spring_layout(self.depTree)
        nx.draw_networkx_nodes(self.depTree, pos)
        nx.draw_networkx_edges(self.depTree, pos)
        nx.draw_networkx_labels(self.depTree, pos)

        plt.show()