from backends.schemdraw.draw import DrawWithSchemdraw, Optimize

mobile = Optimize.MOBILE

resistorHetz = open(r"21_Monolied.txt").read()
DrawWithSchemdraw(resistorHetz)