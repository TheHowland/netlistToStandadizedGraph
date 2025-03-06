from elementPosition import ElementPosition

class LinePosition:
    def __init__(self, x1=0.0, y1=0.0, name1="", x2=0.0, y2=0.0, name2=""):
        self.A = ElementPosition(x1, y1, name1)
        self.B = ElementPosition(x2, y2, name2)

    def direction(self):
        return (self.B - self.A).pos
