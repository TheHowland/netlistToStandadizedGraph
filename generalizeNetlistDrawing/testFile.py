from backends.schemdraw.draw import DrawWithSchemdraw, Optimize
from backends.lcapyNetlist.export import ExportAsLcapyNetlist

mobile = Optimize.MOBILE

resistorHetz = open(r"../Circuits/mixed/02_mixed_RCL_series.txt").read()
#DrawWithSchemdraw(resistorHetz)

a = ExportAsLcapyNetlist(resistorHetz)
print(a.export)