from backends.schemdraw.draw import DrawWithSchemdraw
DrawWithSchemdraw("test1.txt")

exit(0)

import schemdrawInskale as sd

from generalizeNetlistDrawing.elements.elements import Line
from generalizeNetlistDrawing.vector2D import Vector2D as v

drawing = sd.Drawing(canvas='svg')
line1 = Line(v(0, 0), v(3, 0))
line2 = Line(v(3,0), v(6,0))
line1.rotate(90)
line2.rotate(90)

drawing.add(line1.schemdrawElement())
drawing.add(line2.schemdrawElement())

drawing.draw()