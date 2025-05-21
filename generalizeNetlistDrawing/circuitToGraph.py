from typing import Type

import networkx as nx
from lcapyInskale import Circuit
from simplipfy.helpers.netlistLine import NetlistLine

from generalizeNetlistDrawing.elements.elementFaktory import ElementFaktory
from generalizeNetlistDrawing.netlistGraph import NetlistGraph


class CircuitToGraph:
    def __init__(self, lcapyCircuit: Circuit, graphType: Type[nx.Graph], eqNodeMap: dict[str, str] = None):
        self.cct = lcapyCircuit
        self.startNode: int
        self.endNode: int
        self.eqNodeMap: dict[str, str] = self.makeEqNodeMap() if eqNodeMap is None else eqNodeMap
        self.cleandUpNetlist: list[NetlistLine] = self._cleanUpNetlist()
        self.graphType = graphType
        self.factory = ElementFaktory().make

    def makeEqNodeMap(self):
        eqNodeMap = {}
        eqNodes = self.cct.equipotential_nodes
        for masterNode in eqNodes.keys():
            for node in eqNodes[masterNode]:
                eqNodeMap[node] = masterNode

        return eqNodeMap

    def _cleanUpNetlist(self) -> list[NetlistLine]:
        """
        Converts the netlist into an easy-to-use format and removes lines from netlist
        :returns list of NetlistLines
        """
        netLines = [NetlistLine(line) for line in self.cct.netlist().splitlines()]
        cleandUpNetlist = []

        for line in netLines:
            if line.type == "W":
                continue

            line.posNode = self.eqNodeMap[line.posNode]
            line.negNode = self.eqNodeMap[line.negNode]
            cleandUpNetlist.append(line)

            if line.type == "V" or line.type == "I":
                self.startNode = line.posNode
                self.endNode = line.negNode
                self.ac_dc = line.ac_dc
                self.value = line.value
                continue

        return cleandUpNetlist

    @property
    def Graph(self) -> nx.Graph:
        graph = self.graphType()
        for line in self.cleandUpNetlist:
            name = line.label
            netLine = str(line)
            graph.add_edge(line.posNode, line.negNode, key=name, data=self.factory(name=name, netLine=netLine))
        return graph

    @property
    def NetlistGraph(self) -> NetlistGraph:
        graph: nx.MultiGraph = self.Graph
        if not isinstance(graph, nx.MultiGraph):
            raise TypeError("Graph is not a MultiGraph")
        return NetlistGraph(graph, self.startNode, self.endNode)