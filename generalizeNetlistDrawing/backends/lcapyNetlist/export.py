from generalizeNetlistDrawing.elementPlacement import ElementPlacement
from generalizeNetlistDrawing.idGenerator import IDGenerator

class ExportAsLcapyNetlist:
    def __init__(self, fileName):
        self.idGen = IDGenerator()
        self.rasterizedNetFile = ElementPlacement(fileName)

        nodeMap = {}
        uniquePoints = set()
        netlist = ""
        for elm in iter(self.rasterizedNetFile.elements):
            if elm.startPos not in uniquePoints:
                uniquePoints.add(elm.startPos)
                nodeMap[elm.startPos] = self.idGen.newId
            if elm.endPos not in uniquePoints:
                uniquePoints.add(elm.endPos)
                nodeMap[elm.endPos] = self.idGen.newId

            netlist += elm.netlistLine(nodeMap, self.idGen)

        self.netlist = netlist

    @property
    def export(self) -> str:
        return self.netlist
