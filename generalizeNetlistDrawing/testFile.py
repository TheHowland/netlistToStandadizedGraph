from backends.schemdraw.draw import DrawWithSchemdraw, Optimize
mobile = Optimize.MOBILE

resistorHetz = open("../Circuits/resistor/00_Resistor_Hetznecker.txt").read()
DrawWithSchemdraw(resistorHetz, optimize=mobile)