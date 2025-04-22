# from backends.schemdraw.draw import DrawWithSchemdraw
import schemdrawInskale as sd

from generalizeNetlistDrawing.elements.element import Direction as d
from generalizeNetlistDrawing.elements.sourceV import SourceV

drawing = sd.Drawing(canvas='svg')
down = SourceV(0, 0, "V1", rotation=d.down.value, scaling=3.0)
left = SourceV(0, 0, "V2", rotation=d.left.value, scaling=3.0)
up = SourceV(0, 0, "V3", rotation=d.up.value, scaling=3.0)
right = SourceV(0, 0, "V4", rotation=d.right.value, scaling=3.0)

drawing.add(up.schemdrawElement())
drawing.add(left.schemdrawElement())
drawing.add(right.schemdrawElement())
drawing.add(down.schemdrawElement())

drawing.draw()

#DrawWithSchemdraw("test1.txt")