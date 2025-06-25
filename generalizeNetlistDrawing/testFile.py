from backends.schemdraw.draw import DrawWithSchemdraw, Optimize

mobile = Optimize.MOBILE

resistorHetz = open(r"C:\Users\yannick.wieland\Program-Project-Files\netlistToStandadizedGraph\generalizeNetlistDrawing\thesis1").read()
DrawWithSchemdraw(resistorHetz)