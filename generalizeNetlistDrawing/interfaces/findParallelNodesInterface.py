from abc import ABC, abstractmethod

class FindParallelNodesInterface(ABC):
    def __init__(self, graphType: type):
        self.graphType = graphType

    @staticmethod
    @abstractmethod
    def findParallelNodes(graph) -> list:
        pass