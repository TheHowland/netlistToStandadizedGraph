class DrawingTreeEntire:
    def __init__(self, graph, parent: 'DrawingTreeEntire', children: dict[any, 'DrawingTreeEntire']):
        self.parent: 'DrawingTreeEntire' = parent
        self.graph = graph
        self.children: dict[any, 'DrawingTreeEntire'] = children
        self.hasChildren = bool(list(children.values()))
