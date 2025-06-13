from typing import Type, Union

from networkx import MultiDiGraph, MultiGraph

NxMultiGraph = Union[MultiDiGraph, MultiGraph]

def setGraphType(graphType: Union[MultiGraph, MultiDiGraph]) -> None:
    global GraphType
    if graphType not in (MultiGraph, MultiDiGraph):
        raise ValueError(f"GraphType has to be of type: {type(MultiGraph)} or {type(MultiDiGraph)}")
    GraphType = graphType


GraphType: Type[NxMultiGraph] = MultiDiGraph

if GraphType == MultiGraph:
    from generalizeNetlistDrawing.backends.search.multiGraph import findParallelNode as fpn
    from generalizeNetlistDrawing.backends.search.multiGraph import findRowNodesSequence as frns
    from generalizeNetlistDrawing.backends.search.multiGraph.functionsOnGraph import edgesBetweenNodes as ebn
    from generalizeNetlistDrawing.backends.search.multiGraph.functionsOnGraph import getEdgesOfSubGraph as geosg

elif GraphType == MultiDiGraph:
    from generalizeNetlistDrawing.backends.search.multiDiGraph import findParallelNode as fpn
    from generalizeNetlistDrawing.backends.search.multiDiGraph import findRowNodesSequence as frns
    from generalizeNetlistDrawing.backends.search.multiDiGraph.functionsOnGraph import edgesBetweenNodes as ebn
    from generalizeNetlistDrawing.backends.search.multiDiGraph.functionsOnGraph import getEdgesOfSubGraph as geosg
else:
    raise ValueError(f"GraphType has to be of type: {type(MultiGraph)} or {type(MultiDiGraph)}")

findParallelNode = fpn
findRowNodesSequence = frns
edgesBetweenNodes = ebn
getEdgesOfSubGraph = geosg