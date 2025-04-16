import networkx as nx
from lcapyInskale import Circuit

from generalizeNetlistDrawing.circuitToGraph import CircuitToGraph


class Rasterisation2:
    def __init__(self, fileName):
        cct = Circuit(fileName)
        self.transformer = CircuitToGraph(cct, nx.MultiDiGraph)
        self.netGraph = self.transformer.NetlistGraph
        self.netGraph.place()
        print("Finished Rastarisation2 init")

if __name__ == "__main__":
    r = Rasterisation2("test1.txt")
