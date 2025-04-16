from abc import ABC, abstractmethod

class FindParallelNodesInterface(ABC):
    @staticmethod
    @abstractmethod
    def findParallelNodes(graph) -> list:
        pass