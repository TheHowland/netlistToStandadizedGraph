from lcapy.validateCircuitFile import ValidateCircuitFile
from drawingTree import DrawingTree

if not ValidateCircuitFile(["test1.txt"]):
    exit("File not valid")

a = DrawingTree()
# lcapyCir = lcapy.Circuit("..\\Circuits\\resistor\\00_Resistor_Hetznecker.txt")
# a = NetlistGraph(lcapyCir)