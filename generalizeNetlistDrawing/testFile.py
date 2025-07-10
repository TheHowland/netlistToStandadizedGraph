from backends.schemdraw.draw import DrawWithSchemdraw, Optimize

mobile = Optimize.MOBILE

resistorHetz = open(r"testx.txt").read()
DrawWithSchemdraw(resistorHetz)