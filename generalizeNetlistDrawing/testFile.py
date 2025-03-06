from lcapy.validateCircuitFile import ValidateCircuitFile
from rasterisation import Rasterisation
from backends.schemdraw.draw import DrawWithSchemdraw

fileName = "../Circuits/resistor/00_Resistor_Hetznecker.txt"
if not ValidateCircuitFile([fileName]):
    exit("File not valid")

#a = Rasterisation(fileName)
DrawWithSchemdraw(fileName)
# lcapyCir = lcapy.Circuit("..\\Circuits\\resistor\\00_Resistor_Hetznecker.txt")
# a = NetlistGraph(lcapyCir)