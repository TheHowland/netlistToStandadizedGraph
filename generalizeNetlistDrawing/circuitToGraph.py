from typing import Type

import networkx as nx
from lcapyInskale import Circuit
from simplipfy.netlistLine import NetlistLine

from generalizeNetlistDrawing.element import Element
from generalizeNetlistDrawing.netlistGraph import NetlistGraph


class CircuitToGraph:
    def __init__(self, lcapyCircuit: Circuit, graphType: Type[nx.Graph]):
        self.cct = lcapyCircuit
        self.startNode: int
        self.endNode: int
        self.cleandUpNetlist: list[NetlistLine] = self._cleanUpNetlist()
        self.graphType = graphType

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

    @property
    def Graph(self) -> nx.Graph:
        graph = self.graphType()
        for line in self.cleandUpNetlist:
            name = line.label
            graph.add_edge(line.startNode, line.endNode, key=name, data=Element(name=name))
        return graph

    @property
    def NetlistGraph(self) -> NetlistGraph:
        graph: nx.MultiGraph = self.Graph
        if not isinstance(graph, nx.MultiGraph):
            raise TypeError("Graph is not a MultiGraph")
        return NetlistGraph(graph, self.startNode, self.endNode)