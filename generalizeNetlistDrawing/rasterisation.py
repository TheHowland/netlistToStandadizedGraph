from itertools import chain as flattenList

import networkx as nx
from lcapyInskale import Circuit

from circuitToGraph import CircuitToGraph
from dependencyTree import DependencyTree
from findSubStructures import FindSubStructures
from generalizeNetlistDrawing.elementPosition import ElementPosition
from generalizeNetlistDrawing.linePlacement import LinePlacement
from generalizeNetlistDrawing.linePositions import LinePosition
from generalizeNetlistDrawing.vector2D import Vector2D


class Rasterisation:
    """
    places the Elements of a Netlist (electrical circuit) on a raster. The elements are placed next to each other if
    they are in parallel and underneath each other if they are in row. Basically this transforms the Elements from their
    local coordinate system into a global one.
    """
    def __init__(self, fileName):
        cct = Circuit(fileName)
        self.transformer = CircuitToGraph(cct)
        graph = self.transformer.asMultiGraph().toNetlistGraph()
        self.SubStructure = FindSubStructures(graph)
        self.DepTree = DependencyTree(self.SubStructure.subStructures)

        if self.DepTree.startNode:
            resolved = []
            startNodes = self.DepTree.nodesWithNoSuccessor()
            self.createElementsForStartNodes(startNodes, resolved)
            self.subsequentlyMoveElementsBeginningAtStartNodes(resolved, startNodes)
            self.elementPositions = self.collectElements()
            self.linePositions = LinePlacement(graph, self.elementPositions).getLinePositions()
        else:
            # if there is only one element left the drawing always is the same and the whole substrucutre
            # replacement does not work because there are non...
            elmName = list(graph.graph.edges(keys=True))[0][2]
            self.elementPositions = {'G1': ElementPosition(name=elmName)}
            self.linePositions = [LinePosition(Vector2D(0, -1), Vector2D(-1, -1))]
        pass

    def collectElements(self) -> dict[str, ElementPosition]:
        elementPositions = {}
        for key in iter(self.SubStructure.subStructures.keys()):
            elementPositions.update(
                self.SubStructure.subStructures[key].elementPlacement.getElementPositions()
            )
        return elementPositions

    def subsequentlyMoveElementsBeginningAtStartNodes(self, resolved, startNodes):
        predecessors = self.DepTree.getPredecessors(startNodes)
        processedNodes = predecessors.copy()
        while predecessors:
            node = predecessors.pop()
            netGraph = self.SubStructure.subStructures[node]
            netGraph.placeElements()
            subGraphNames = netGraph.getSubGraphNames()
            if self.necessarySubGraphsResolved(resolved, subGraphNames) and not node in resolved:
                self.moveElements(netGraph, subGraphNames)
                resolved.append(node)

            if not predecessors:
                processedNodes = self.DepTree.getPredecessors(processedNodes)
                predecessors = processedNodes.copy()
        pass

    def createElementsForStartNodes(self,startNodes, resolved):
        for node in startNodes:
            netGraph = self.SubStructure.subStructures[node]
            netGraph.placeElements()
            netGraph.actualSize = netGraph.elementPlacement.size
            resolved.append(node)

    @staticmethod
    def necessarySubGraphsResolved(resolved, subGraphNames) -> bool:
        return all(subGraphName in resolved for subGraphName in subGraphNames)

    def moveElements(self, netGraph, subGraphNames):
        start = netGraph.graphStart
        end = netGraph.graphEnd
        edgePath = list(nx.all_simple_edge_paths(netGraph.graph, start, end))
        edgeNames = [edge[2] for edge in list(flattenList(*edgePath))]
        if self.graphHasVerticalElements(netGraph, start):
            self.moveVerticalElements(edgeNames, netGraph, subGraphNames)
        else:
            self.moveHorizontalElements(edgeNames, netGraph, subGraphNames)

    @staticmethod
    def graphHasVerticalElements(netGraph, start) -> bool:
        return netGraph.graph.out_degree(start) == 1

    @staticmethod
    def graphHasHorizontalElements(netGraph, start) -> bool:
        return netGraph.graph.out_degree(start) >= 2

    def moveHorizontalElements(self, edgeNames, netGraph, subGraphNames):
        # para Graph
        deltaX = 0
        for edgeName in edgeNames:
            if edgeName in subGraphNames:
                pos = netGraph.elementPlacement.elements[edgeName] + ElementPosition(deltaX, 0)
                children = self.DepTree.reachableNodes(edgeName)
                children.append(edgeName)
                for child in children:
                    self.SubStructure.subStructures[child].elementPlacement.moveElements(pos)
                deltaX += (self.SubStructure.subStructures[edgeName].actualSize[0] - 1)
            else:
                netGraph.elementPlacement.elements[edgeName].moveX(deltaX)
        xSize = netGraph.size[0] + deltaX
        ySize = netGraph.size[1]
        netGraph.actualSize = (xSize, ySize)

    def moveVerticalElements(self, edgeNames, netGraph, subGraphNames):
        # row Graph
        deltaY = 0
        for edgeName in edgeNames:
            if edgeName in subGraphNames:
                pos = netGraph.elementPlacement.elements[edgeName] - ElementPosition(0, deltaY)
                children = self.DepTree.reachableNodes(edgeName)
                children.append(edgeName)
                for child in children:
                    self.SubStructure.subStructures[child].elementPlacement.moveElements(pos)
                deltaY += (self.SubStructure.subStructures[edgeName].actualSize[1] - 1)
            else:
                netGraph.elementPlacement.elements[edgeName].moveY(deltaY)
        xSize = netGraph.size[0]
        ySize = netGraph.size[1] + deltaY
        netGraph.actualSize = (xSize, ySize)

    def compareSize(self, val1: tuple[int, int],val2: tuple[int,int]):
        pass