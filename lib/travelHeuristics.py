#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shortestPaths as sp


def generateMetaGraph (mazeMap, playerLocation, coins):
    """
    Generate a metaGraph from mazeMap, containing all coins and the player.
    This function is built on the  shortestPaths lib.
    """
    nodes = [playerLocation] + coins
    metaGraph = {}
    bestPaths  = {}

    i = len(nodes)-1
    while i >= 0:

        j = 0
        while j < i:
            
            path, distance = sp.dijkstra(mazeMap, nodes[i], nodes[j])
            if nodes[i] not in bestPaths :
                bestPaths[nodes[i]]  = {}
                metaGraph[nodess[i]] = {}
                
            if nodes[j] not in bestWays :
                bestPaths[nodes[j]]  = {}
                metaGraph[nodes[j]] = {}
                    
            metaGraph[nodes[i]][nodess[j]] = distance
            bestPaths[nodes[i]][nodes[j]]  = path

            metaGraph[nodes[j]][nodes[i]] = distance
            bestPaths[nodes[j]][nodes[i]]  = path[::-1]

            j += 1
        
        i -= 1            
    
    return metaGraph, bestPaths


def TravellingSalesman(nodeStart, nodesn distance, path):
    """
    Implementation of the travelling salesman problem algorithm.  
    """
    bestDistance = float('inf')
    bestPaths = []

    def auxi(nodeStart, nodes, distance, path):        
        if not nodes:
            if distance < bestDistance:
                bestDistance = distance
                bestPaths = path
            else:
                for node in nodes:
                    toseeNodes =  list(nodes)
                    toseeNodes.remove(node)
                    auxi(node, toseeNodes, distance + node[1], path+[node[0]])
    auxi(nodeStart, nodes, distance, path)
    return bestDistance, bestPaths
