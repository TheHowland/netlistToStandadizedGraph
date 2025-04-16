from abc import ABC, abstractmethod

class FindSeriesNodesInterface(ABC):
    @staticmethod
    @abstractmethod
    def findSeriesNodesSequence(graph) -> list:
        pass