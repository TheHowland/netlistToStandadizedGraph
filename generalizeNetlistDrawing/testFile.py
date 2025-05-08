from backends.schemdraw.draw import DrawWithSchemdraw, Optimize
mobile = Optimize.MOBILE

resistorHetz = open("../Circuits/resistor/net_01_resistor_Felleisen_step_2.txt").read()
DrawWithSchemdraw(resistorHetz, optimize=mobile)