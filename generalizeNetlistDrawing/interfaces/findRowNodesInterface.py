from abc import ABC, abstractmethod

class FindRowNodesInterface(ABC):
    @staticmethod
    @abstractmethod
    def findRowNodesSequences(graph) -> list:
        pass