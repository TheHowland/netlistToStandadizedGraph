from elementPosition import ElementPosition
from dependencyTree import DependencyTree

class PlaceElements:
    def __init__(self, depTree: DependencyTree):
        self.depTree = depTree
        self.elements: dict[str, ElementPosition]
        self.startNodes = depTree.nodesWithNoSuccessor()
        print("finished init PlaceElements")

