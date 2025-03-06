from lcapy import Circuit
from lcapy.drawWithSchemdraw import DrawWithSchemdraw
from lcapy.solution import Solution
from lcapy.langSymbols import LangSymbols
import os

def DrawCircuit(fileContent):
    cct = Circuit(fileContent)
    DrawWithSchemdraw(cct, LangSymbols(), fileName="test").draw()