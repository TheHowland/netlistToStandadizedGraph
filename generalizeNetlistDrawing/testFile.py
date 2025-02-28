import lcapy
from lcapy.validateCircuitFile import ValidateCircuitFile
from lcapy import Circuit
from lcapy import DrawWithSchemdraw
from lcapy.langSymbols import LangSymbols
from netlistGraph import NetlistGraph
from netlistToGraph import NetlistToGraph
from lcapy.solution import Solution

if not ValidateCircuitFile(["test1.txt"]):
    exit("File not valid")

cct = Circuit("test1.txt")
graph = NetlistToGraph(cct)
b = NetlistGraph(graph.MultiDiGraph(), graph.startNode, graph.endNode)
b.findParallelSubGraphs()
print(b.subGraphs)
# lcapyCir = lcapy.Circuit("..\\Circuits\\resistor\\00_Resistor_Hetznecker.txt")
# a = NetlistGraph(lcapyCir)