import networkx as nx

from findSubStructures import FindSubStructures
from lcapy import Circuit

from generalizeNetlistDrawing.elementPosition import ElementPosition
from netlistToGraph import NetlistToGraph
from dependencyTree import DependencyTree
from netlistGraph import NetlistGraph
from itertools import chain as flattenList

class DrawingTree:
    def __init__(self, fileName):
        cct = Circuit(fileName)
        graph = NetlistToGraph(cct).toNetlistGraph()
        self.SubStructure = FindSubStructures(graph)
        self.DepTree = DependencyTree(self.SubStructure.subStructures)

        resolved = []
        startNodes = self.DepTree.nodesWithNoSuccessor()
        for node in startNodes:
            netGraph = self.SubStructure.subStructures[node]
            netGraph.placeElements()
            netGraph.actualSize = netGraph.elementPlacement.size
            resolved.append(node)

        predecessors = self.DepTree.getPredecessors(startNodes)
        processedNodes = predecessors.copy()
        while predecessors:
            node = predecessors.pop()
            netGraph = self.SubStructure.subStructures[node]
            netGraph.placeElements()
            size = netGraph.size
            subGraphNames = netGraph.getSubGraphNames()
            if all(subGraphName in resolved for subGraphName in subGraphNames):
                start = netGraph.graphStart
                end = netGraph.graphEnd
                edgePath = list(nx.all_simple_edge_paths(netGraph.graph, start, end))
                edgeNames = [edge[2] for edge in list(flattenList(*edgePath))]
                if netGraph.graph.out_degree(start) == 1:
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
                    pass
                else:
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
                    pass

                resolved.append(node)

            if not predecessors:
                processedNodes = self.DepTree.getPredecessors(processedNodes)
                predecessors = processedNodes.copy()

        pass

    def compareSize(self, val1: tuple[int, int],val2: tuple[int,int]):
        pass