from lcapy.validateCircuitFile import ValidateCircuitFile
from drawingTree import DrawingTree

fileName = "test1.txt"
if not ValidateCircuitFile([fileName]):
    exit("File not valid")

a = DrawingTree(fileName)
# lcapyCir = lcapy.Circuit("..\\Circuits\\resistor\\00_Resistor_Hetznecker.txt")
# a = NetlistGraph(lcapyCir)