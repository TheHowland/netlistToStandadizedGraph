from backends.schemdraw.draw import DrawWithSchemdraw, Optimize
test1Content = open("test1.txt").read()
DrawWithSchemdraw(test1Content)
DrawWithSchemdraw(test1Content, rotate=90)
DrawWithSchemdraw(test1Content, rotate=180)
DrawWithSchemdraw(test1Content, rotate=270)

mobile = Optimize.MOBILE
resistor08 = open("../Circuits/resistor/08_resistor_parallel3.txt").read()
DrawWithSchemdraw(resistor08)
DrawWithSchemdraw(resistor08, optimize=mobile)