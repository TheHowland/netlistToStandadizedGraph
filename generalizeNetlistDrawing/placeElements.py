import networkx as nx

from elementPosition import ElementPosition
from dependencyTree import DependencyTree

class PlaceElements:
    def __init__(self, depTree: DependencyTree):
        self.depTree = depTree
        self.elements: dict[str, list[ElementPosition]] = {}
        self.sizeOfSubGraph: dict[str, tuple[int, int]] = {}
        self.startNodes = depTree.nodesWithNoSuccessor()
        self.setSizeOfStartNodes()
        self.createElementPositions()
        self.placeElementsInSubGraphs()
        self.placeElementsSubsequently()
        print("finished init PlaceElements")

    def placeBottom(self, subGraphName):
        startNode = self.depTree.subGraphs[subGraphName].graphStart
        if self.depTree.subGraphs[subGraphName].graph.out_degree(startNode) == 1:
            return True
        else:
            return False

    def placeRight(self, subGraphName):
        startNode = self.depTree.subGraphs[subGraphName].graphStart
        if self.depTree.subGraphs[subGraphName].graph.out_degree(startNode) >= 2:
            return True
        else:
            return False

    def createElementPositions(self):
        for node in list(self.depTree.subGraphs.keys()):
            elements: list[ElementPosition] = []
            for edge in list(self.depTree.subGraphs[node].graph.edges(keys=True)):
                if edge[2][0] == "G":
                    continue
                else:
                    edgeName = edge[2]
                    elements.append(ElementPosition(name=edgeName))

            if elements:
                self.elements[node] = elements

    def placeElementsInSubGraphs(self):
        for key in list(self.elements.keys()):
            if self.placeRight(key):
                offset = ElementPosition(1, 0)
            else:
                offset = ElementPosition(0, -1)

            subNetGraph = self.depTree.subGraphs[key].graph
            elmAndGraphs = [x[2] for x in subNetGraph.edges(keys=True)]
            for elm in self.elements[key]:
                elm += offset.scale(elmAndGraphs.index(elm.name))

    def setSizeOfStartNodes(self):
        for key in self.startNodes:
            subNetGraph = self.depTree.subGraphs[key]
            x = subNetGraph.width
            y = subNetGraph.length - 1
            self.sizeOfSubGraph[key] = (x, y)

    def getPredecessors(self, nodes: list[any]) -> list:
        predecessors = set()
        for node in nodes:
            for predecessor in list(self.depTree.depTree.predecessors(node)):
                predecessors.add(predecessor)

        return list(predecessors)

    def placeElementsSubsequently(self):
        nextNodes = self.getPredecessors(self.startNodes)
        for node in nextNodes:
            subNetGraph = self.depTree.subGraphs[node]
            edges = list(subNetGraph.graph.edges(keys=True))
            for edge in edges:
                pass



