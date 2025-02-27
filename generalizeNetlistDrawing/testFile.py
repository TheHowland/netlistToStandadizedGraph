import lcapy
from lcapy.validateCircuitFile import ValidateCircuitFile
from lcapy import Circuit
from lcapy import DrawWithSchemdraw
from lcapy.langSymbols import LangSymbols
from netlistGraph import NetlistGraph
from netlistToGraph import NetlistToGraph

if not ValidateCircuitFile(["test1.txt"]):
    exit("File not valid")

cct = Circuit("test1.txt")
DrawWithSchemdraw(cct, LangSymbols()).draw()
graph = NetlistToGraph(cct)
b = NetlistGraph(graph.MultiDiGraph(), graph.startNode, graph.endNode)
b.draw_graph()
idx = 0
for graph in b.getSubGraphs():
    a = NetlistGraph(graph, b.subGraphs[idx][0], b.subGraphs[idx][1])
    a.draw_graph()
    print(a.graph.edges)
    idx += 1

# lcapyCir = lcapy.Circuit("..\\Circuits\\resistor\\00_Resistor_Hetznecker.txt")
# a = NetlistGraph(lcapyCir)