from abc import ABC, abstractmethod

class FindParallelNodesInterface(ABC):
    def __init__(self, graphType: type):
        self.graphType = graphType

    @staticmethod
    @abstractmethod
    def findParallelNode(graph) -> list:
        pass