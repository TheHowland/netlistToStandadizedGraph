from backends.schemdraw.draw import DrawWithSchemdraw, Optimize

mobile = Optimize.MOBILE

resistorHetz = open(r"21_Thesis_Killer.txt").read()
DrawWithSchemdraw(resistorHetz)