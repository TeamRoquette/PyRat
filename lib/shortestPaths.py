#!/usr/bin/env python3
# -*- coding: utf-8 -*-



def orderPath (nodesDict, start, stop, path):
    """
    Internal function used by dijkstra search or Breadth-first search.
    Put into order nodes from dictionnary.
    """
    if start == stop:
        return path + [start]

    return orderPath (nodesDict, start, nodesDict[stop][0], path + [stop])



def dijkstra (mazeMap, startLocation, stopLocation) :
    bestNodes = {(startLocation):((),0)}
    toseeNodes = [startLocation]
    
    while toseeNodes :
        node = toseeNodes.pop(0)
        neighbours = mazeMap[node]
        dist = bestNodes.get(node, ([], float('inf')))[1]
        
        for (n,d) in neighbours :
            if bestNodes.get(n, ([], float('inf')))[1] > d + dist :
                bestNodes[n] = (node, d + dist)
                toseeNodes.append(n)

    return orderPath(bestNodes, startLocation, stopLocation, []), bestNodes[stopLocation][1]


