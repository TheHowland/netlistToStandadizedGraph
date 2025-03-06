from lcapy.validateCircuitFile import ValidateCircuitFile
from rasterisation import Rasterisation
from backends.schemdraw.draw import DrawWithSchemdraw
from backends.lcapyNetlist.export import ExportAsLcapyNetlist

# fileName = "../Circuits/resistor/00_Resistor_Hetznecker.txt"
fileName = "test1.txt"
if not ValidateCircuitFile([fileName]):
    exit("File not valid")

#a = Rasterisation(fileName)
DrawWithSchemdraw(fileName)
# ExportAsLcapyNetlist(fileName)