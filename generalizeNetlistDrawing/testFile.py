from backends.schemdraw.draw import DrawWithSchemdraw, Optimize

mobile = Optimize.MOBILE

resistorHetz = open(r"C:\Users\yanni\Programm-Projekt-Files\PyCharm\Thesis\generalizeNetlistDrawing\test1.txt").read()
DrawWithSchemdraw(resistorHetz)