#!/usr/bin/env python3
# -*- coding: utf-8 -*-



def orderPath (nodesDict, start, stop, path):
    """
    Internal function used by shortestWay to
    put into order nodes from the routing table.
    Return the shortest path from start to stop
    """
    if start == stop:
        return path + [start]

    return orderPath (nodesDict, start, nodesDict[stop][0], path + [stop])



def dijkstra (mazeMap, startLocation) :
    """
    Return the routing table of every nodes sarting from startLocation.
    """
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

    return bestNodes



def shortestWay (mazeMap, startLocation, stopLocation):
    """
    Return the shortest path from startLocation to stopLocation.
    Use dijkstra algorithm.
    """
    return orderPath (dijkstra (mazeMap, startLocation), startLocation, stopLocation, [])

