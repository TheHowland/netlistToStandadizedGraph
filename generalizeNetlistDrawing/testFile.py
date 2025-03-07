from lcapy.validateCircuitFile import ValidateCircuitFile
from backends.schemdraw.draw import DrawWithSchemdraw

# fileName = "../Circuits/resistor/00_Resistor_Hetznecker.txt"
# fileName = "test1.txt"
# if not ValidateCircuitFile([fileName]):
#     exit("File not valid")

DrawWithSchemdraw("step0.txt")
DrawWithSchemdraw("step1.txt")
DrawWithSchemdraw("step2.txt")
DrawWithSchemdraw("step3.txt")
DrawWithSchemdraw("step4.txt")
