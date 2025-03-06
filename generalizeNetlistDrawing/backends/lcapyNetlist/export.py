from generalizeNetlistDrawing.rasterisation import Rasterisation
from generalizeNetlistDrawing.elementPosition import ElementPosition
from generalizeNetlistDrawing.linePositions import LinePosition
from generalizeNetlistDrawing.vector2D import Vector2D
from generalizeNetlistDrawing.idGenerator import IDGenerator
from generalizeNetlistDrawing.drawCircuit import DrawCircuit


class ExportAsLcapyNetlist:
    def __init__(self, fileName):
        self.rasterizedNetFile = Rasterisation(fileName)
        self.elemPositions: dict[str, ElementPosition] = self.rasterizedNetFile.elementPositions
        self.linePositions: [LinePosition] = self.rasterizedNetFile.linePositions
        self.columns = self.sortInColumns()
        for column in self.columns:
            column.sort(key=lambda p:p.startPos.y, reverse=True)
        self.longestColumn = 0
        for column in self.columns:
            if len(column) > self.longestColumn:
                self.longestColumn = len(column)
        self.nodeIDGenerator = IDGenerator()

        self.nodes = self.makeNodes()
        netlist = self.makeNetlist()
        # find top left corner
        # find bottom left corner
        # add voltage source
        print('Finished')

    def makeNodes(self) -> list[list]:
        #make loop up matrix for nodes
        nodes = []
        for column in self.columns:
            row = []
            for i in range(0, self.longestColumn):
                row.append(-1)
            nodes.append(row)

        positions = set()
        for elm in iter(self.elemPositions.keys()):
            positions.add(self.elemPositions[elm].startPos)
        for elm in self.linePositions:
            positions.add(elm.startPos)
            positions.add(elm.endPos)

        for position in positions:
            nodes[int(position.x)][int(position.y)] = self.nodeIDGenerator.newId

        return nodes

    def makeNetlist(self) -> str:
        netlist = ""
        for column in self.columns:
            for elm in column:
                node1 = self.nodes[int(elm.startPos.x)][int(elm.startPos.y)]
                node2 = self.nodes[int(elm.endPos.x)][int(elm.endPos.y)]
                netlist += elm.netLine(str(node1), str(node2))

        return netlist

    def sortInColumns(self) -> list[list]:
        elmsSet = set(self.elemPositions.keys())
        lineSet = set(self.linePositions)
        elms = self.elemPositions.keys()
        lines = self.linePositions
        columns = []
        idx = 0
        while True:
            column = []
            for elm in iter(elms):
                if self.elemPositions[elm].vector.x == idx:
                    column.append(self.elemPositions[elm])
                    elmsSet.remove(elm)

            for elm in lines:
                if elm.a.x == idx:
                    column.append(elm)
                    lineSet.remove(elm)

            columns.append(column)

            if not elmsSet and not lineSet:
                break
            idx += 1

        return columns
