from idGenerator import IDGenerator
from iterLimiter import IterLimiter
from netlistGraph import NetlistGraph


class FindSubStructures:
    """
    Searches the graph for elements that are in row or in parallel and replaces them with a G<n> edge while saving the
    replaced structure in self.substructures. The graph is split up in substructures that contain either elements that
    are in parallel or in row. This information is used in the Rastarisation class to place the elements.
    """
    def __init__(self, graph: NetlistGraph):
        self._idGen = IDGenerator()
        self.iterLim = IterLimiter(1000)
        self.graph = graph
        self.subStructures: dict[str, NetlistGraph] = {}
        self.createSubstitutions()

    def makeParaSubGraphs(self) -> bool:
        self.iterLim.reInit()
        changed = False
        while True:
            newGraph = NetlistGraph(self.graph.graph.copy(), self.graph.graphStart, self.graph.graphEnd)
            childGraphs = newGraph.findParallelSubGraph(self._newID)
            if not childGraphs or self.iterLim.limitReached:
                break
            self.subStructures.update(childGraphs)
            self.graph = newGraph
            changed = True
        return changed

    def makeRowSubGraphs(self) -> bool:
        self.iterLim.reInit()
        changed = False
        while True:
            newGraph = NetlistGraph(self.graph.graph.copy(), self.graph.graphStart, self.graph.graphEnd)
            childGraphs = newGraph.findRowSubGraph(self._newID)
            if not childGraphs or self.iterLim.limitReached:
                break
            self.subStructures.update(childGraphs)
            self.graph = newGraph
            changed = True
        return changed

    def createSubstitutions(self):
        changed = True
        while changed:
            changed = self.makeParaSubGraphs()
            changed = self.makeRowSubGraphs() or changed

    def _newID(self):
        return "G" + str(self._idGen.newId)