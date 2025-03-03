from netlistGraph import NetlistGraph


class DrawingTreeEntire:
    def __init__(self, graph, children: dict[any, NetlistGraph]):
        self.graph = graph
        self.subGraphs: dict[any, NetlistGraph] = children
        self.hasChildren = bool(list(children.values()))

    def keys(self):
        return self.subGraphs.keys()
