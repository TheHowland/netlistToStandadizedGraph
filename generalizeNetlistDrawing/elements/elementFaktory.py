from typing import Type

from generalizeNetlistDrawing.elements import resistor, sourceV
from generalizeNetlistDrawing.elements.element import Element
from generalizeNetlistDrawing.vector2D import Vector2D


class ElementFaktory:
    type_map: dict[str, Type[Element]] = {
        "R": resistor.Resistor,
        "L": Element,
        "C": Element,
        "Z": Element,
        "V": sourceV.SourceV,
        "I": Element,
    }
    def makeFromElement(self, element: Element) -> Element:
        elmType = element.type
        if not elmType:
            return element

        x, y = element.vector.asTuple
        name = element.name
        size = element.size
        rotation = element.rotation
        scaling = element._scale
        elmType = element.elmType
        return self.makeFromType(x,y,name=name,size=size,rotation=rotation,scaling=scaling,elmType=elmType)


    def make(self, x=0.0, y=0.0, name="", size: Vector2D = None, rotation=0, scaling=1.0) -> Element:
        """Determines the element type from the first letter of the name R1 -> R type"""
        return self.makeFromType(x,y,name,size,rotation,scaling,name[0])

    def makeFromType(self, x=0.0, y=0.0, name="", size: Vector2D = None, rotation=0, scaling=1.0,
                 elmType:str = None) -> Element:

        element_class = self.type_map.get(elmType, Element)
        if element_class:
            return element_class(x, y, name=name, size=size, rotation=rotation, scaling=scaling)
        else:
            raise NotImplementedError(f"Element type '{elmType}' is not implemented.")