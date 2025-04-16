from lcapyInskale import Circuit
from networkx import MultiDiGraph, MultiGraph
from simplipfy.netlistLine import NetlistLine

from netlistGraph import NetlistGraph


class CircuitToGraph:
    def __init__(self, lcapyCircuit: Circuit):
        self.cct = lcapyCircuit
        self.startNode: int
        self.endNode: int
        self.cleandUpNetlist: list[NetlistLine] = self._cleanUpNetlist()
        self.graph = None

    def _cleanUpNetlist(self) -> list[NetlistLine]:
        """
        Converts the netlist into an easy-to-use format and removes lines from netlist
        :returns list of NetlistLines
        """
        netLines = [NetlistLine(line) for line in self.cct.netlist().splitlines()]
        cleandUpNetlist = []

        eqNodeMap = {}
        eqNodes = self.cct.equipotential_nodes
        for masterNode in eqNodes.keys():
            for node in eqNodes[masterNode]:
                eqNodeMap[node] = masterNode

        for line in netLines:
            if line.type == "W":
                continue

            line.startNode = int(eqNodeMap[str(line.startNode)])
            line.endNode = int(eqNodeMap[str(line.endNode)])
            cleandUpNetlist.append(line)

            if line.type == "V" or line.type == "I":
                self.startNode = line.startNode
                self.endNode = line.endNode
                self.ac_dc = line.ac_dc
                self.value = line.value
                continue

        return cleandUpNetlist

    def asMultiDiGraph(self) -> 'CircuitToGraph':
        self.graph = MultiDiGraph()
        for line in self.cleandUpNetlist:
            self.graph.add_edge(line.startNode, line.endNode, key=line.label)

        return self

    def asMultiGraph(self) -> 'CircuitToGraph':
        self.graph = MultiGraph()
        for line in self.cleandUpNetlist:
            self.graph.add_edge(line.startNode, line.endNode, key=line.label)

        return self

    def toNetlistGraph(self) -> NetlistGraph:
        if self.graph is None:
            raise RuntimeError("self.graph = None, use to.. functions to convert netlist to graph first")
        return NetlistGraph(self.graph, self.startNode, self.endNode)