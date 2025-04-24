from lcapyInskale import Circuit
from simplipfy.drawWithSchemdraw import DrawWithSchemdraw as dwsLc
from simplipfy.langSymbols import LangSymbols

from backends.lcapyNetlist.export import ExportAsLcapyNetlist
from backends.schemdraw.draw import DrawWithSchemdraw, Optimize

netlist = ExportAsLcapyNetlist("../Circuits/resistor/07_resistor_row3.txt").export
a = dwsLc(Circuit(netlist),LangSymbols(),"test.svg")
a.draw()
DrawWithSchemdraw("test1.txt")
DrawWithSchemdraw("test1.txt", rotate=90)
DrawWithSchemdraw("test1.txt", rotate=180)

mobile = Optimize.MOBILE
DrawWithSchemdraw("../Circuits/resistor/08_resistor_parallel3.txt", optimize=mobile)