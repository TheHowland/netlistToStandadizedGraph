from typing import Type

from generalizeNetlistDrawing.elements import capacitor, inductor, resistor, sourceI, sourceV
from generalizeNetlistDrawing.elements.element import Element
from generalizeNetlistDrawing.vector2D import Vector2D


class ElementFaktory:
    type_map: dict[str, Type[Element]] = {
        "R": resistor.Resistor,
        "L": inductor.Inductor,
        "C": capacitor.Capacitor,
        "Z": resistor.Resistor,
        "V": sourceV.SourceV,
        "I": sourceI.SourceI,
    }

    def make(self, x=0.0, y=0.0, name="", size: Vector2D = None, rotation=0, scaling=1.0, default: Element=Element) -> Element:
        """Determines the element type from the first letter of the name R1 -> R type"""
        return self.makeFromType(x,y,name,size,rotation,scaling,name[0], default)

    def makeFromType(self, x=0.0, y=0.0, name="", size: Vector2D = None, rotation=0, scaling=1.0,
                 elmType:str = None, default: Element=Element) -> Element:

        element_class = self.type_map.get(elmType, default)
        if element_class:
            return element_class(x, y, name=name, size=size, rotation=rotation, scaling=scaling)
        else:
            raise NotImplementedError(f"Element type '{elmType}' is not implemented.")