from backends.schemdraw.draw import DrawWithSchemdraw
DrawWithSchemdraw("test1.txt")
exit(0)

import schemdrawInskale as sd

from generalizeNetlistDrawing.elements.elements import Resistor

line1 = Resistor(0,0, rotation=0, scaling=3, name="R1")
line2 = Resistor(0,0, rotation=90, scaling=3, name="R2")

drawing = sd.Drawing(canvas='svg')
line1.rotate(90)
line2.rotate(90)
drawing.add(line1.schemdrawElement())
drawing.add(line2.schemdrawElement())
drawing.draw()

drawing2 = sd.Drawing(canvas='svg')
line1.rotate(90)
line2.rotate(90)
drawing2.add(line1.schemdrawElement())
drawing2.add(line2.schemdrawElement())
drawing2.draw()

drawing3 = sd.Drawing(canvas='svg')
line1.rotate(90)
line2.rotate(90)
drawing3.add(line1.schemdrawElement())
drawing3.add(line2.schemdrawElement())
drawing3.draw()

drawing4 = sd.Drawing(canvas='svg')
line1.rotate(90)
line2.rotate(90)
drawing4.add(line1.schemdrawElement())
drawing4.add(line2.schemdrawElement())
drawing4.draw()