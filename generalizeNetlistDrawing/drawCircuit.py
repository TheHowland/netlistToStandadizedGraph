from lcapy import Circuit
from lcapy.drawWithSchemdraw import DrawWithSchemdraw
from lcapy.solution import Solution
from lcapy.langSymbols import LangSymbols
import os

filePath= "test1.txt"
fileName = os.path.basename(filePath)
cct = Circuit(filePath)
DrawWithSchemdraw(cct, LangSymbols(), fileName=fileName).draw()