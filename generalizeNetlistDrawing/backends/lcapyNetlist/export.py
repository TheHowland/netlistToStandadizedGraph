from generalizeNetlistDrawing.element import Element
from generalizeNetlistDrawing.line import Line

from generalizeNetlistDrawing.idGenerator import IDGenerator
from generalizeNetlistDrawing.rasterisation_legacy import Rasterisation


class ExportAsLcapyNetlist:
    def __init__(self, fileName):
        self.rasterizedNetFile = Rasterisation(fileName)
        self.elemPositions: dict[str, Element] = self.rasterizedNetFile.elementPositions
        self.linePositions: [Line] = self.rasterizedNetFile.linePositions
        self.columns = self.sortInColumns()

        for column in self.columns:
            column.sort(key=lambda p:p.startPos.y, reverse=True)
        self.longestColumn = 0
        self.length = 0
        for idx, column in enumerate(self.columns):
            if len(column) > self.longestColumn:
                self.longestColumn = len(column)
            if self.length > self.columns[idx][-1].endPos.y:
                self.length = self.columns[idx][-1].endPos.y
        self.nodeIDGenerator = IDGenerator()

        self.nodes = self.makeNodes()
        self.netlist = self.makeNetlist()
        self.addSource()
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

    def addSource(self):
        topLeft = self.nodes[0][0]
        bottomLeft = self.nodes[0][abs(int(self.length))]
        ac_dc = self.rasterizedNetFile.transformer.ac_dc
        value = self.rasterizedNetFile.transformer.value

        node1 = bottomLeft
        node2 = self.nodeIDGenerator.newId
        self.netlist += f"W {node1} {node2}; left\n"
        for i in range(0, abs(int(self.length)) - 1):
            node1 = node2
            node2 = self.nodeIDGenerator.newId
            self.netlist += f"W {node1} {node2}; up\n"
        node1 = node2
        node2 = self.nodeIDGenerator.newId
        self.netlist += f"V1 {node1} {node2} {ac_dc} {value}; up\n"
        self.netlist += f"W {node2} {topLeft}; right\n"

    @property
    def get(self):
        return self.netlist

