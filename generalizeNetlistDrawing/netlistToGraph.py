from lcapy import Circuit
from lcapy.netlistLine import NetlistLine
from networkx import MultiDiGraph
from netlistGraph import NetlistGraph

class NetlistToGraph:
    def __init__(self, lcapyCircuit: Circuit):
        self.cct = lcapyCircuit
        self.startNode: int
        self.endNode: int
        self.cleandUpNetlist: list[NetlistLine] = self._cleanUpNetlist()

    def _cleanUpNetlist(self) -> list[NetlistLine]:
        """
        Converts the netlist into an easy-to-use format and removes lines from netlist
        :returns list of NetlistLines
        """
        netLines = [NetlistLine(line) for line in self.cct.netlist().splitlines()]
        print("------------------------")
        cleandUpNetlist = []
        for line in netLines:
            if line.type == "W":
                continue
            if line.type == "V" or line.type == "I":
                self.startNode = line.startNode
                self.endNode = line.endNode
                continue

            nodesToReplaceWith = self.cct.equipotential_nodes.keys()
            for replaceNodeWith in nodesToReplaceWith:
                shallBeReplaced = self.cct.equipotential_nodes[replaceNodeWith]

                if str(self.startNode) in shallBeReplaced:
                    self.startNode = int(replaceNodeWith)
                if str(self.endNode) in shallBeReplaced:
                    self.endNode = int(replaceNodeWith)

                if str(line.startNode) in shallBeReplaced:
                    line.startNode = int(replaceNodeWith)
                if str(line.endNode) in shallBeReplaced:
                    line.endNode = int(replaceNodeWith)
            cleandUpNetlist.append(line)

        return cleandUpNetlist

    def toMultiDiGraph(self) -> MultiDiGraph:
        graph = MultiDiGraph()
        for line in self.cleandUpNetlist:
            graph.add_edge(line.startNode, line.endNode, key=line.label)

        return graph

    def toNetlistGraph(self) -> NetlistGraph:
        graph = self.toMultiDiGraph()
        return NetlistGraph(graph, self.startNode, self.endNode)