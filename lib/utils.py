#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lib.PyratApi as api
import operator


def debugMap(graph, height):
    """
    Format a graph implemented in dict of dict of tuples for the standard output stream.
    """
    
    l = ''
    for i in range (height):
        for j in range (height):
            c = graph.get((i,j), ([], -1) )[1]
            if c == -1:
                l += '---'
            elif c < 10:
                l += ' '+str(c)+' '
            elif c < 100:
                l += ' '+str(c)
            else:
                l += str(c)
                
            l+= ' '
                
        l+='\n'
                
    debug(l+'\n\n\n')

    

def convertPosesToDir (actualPos, nextPos, graph):
    """
    Convert two positions, the actual one and the required next one, into the direction to follow.
    First arg must be the actual position implemented as tuple (x,y), 
    second the next position and third one is the graph implemented as a dict of dict of tuple.
    """
    # Check if next position is reachable
    nextPoses = graph[actualPos]
    reachable = False
    
    for (pos, d) in nextPoses:
        if pos == nextPos:
            reachable = True
    
    if not reachable:
        return api.ERROR

    (yAct, xAct) = actualPos
    (yNext, xNext) = nextPos
    
    if xAct == xNext:
        if yNext > yAct:
            return api.UP
        else:
            return api.DOWN
    else:
        if xNext > xAct:
            return api.LEFT
        else:
            return api.RIGHT

        

def getAbsoluteFromRelativeDir (dir1, dir2):
    """
    Return the absolute directions when you want the relative dir2 from dir1.
    First arg must be dir1 implemented as api's directions, second is dir2.
    """

    relativesDir = {api.UP: 0, api.RIGHT: 1, api.DOWN: 2, api.LEFT: 3}
    
    return (relativesDir[dir1] + relativesDir[dir2]) % 4



# compute a weighted choice
def weightedChoice (probas):
    from random import uniform
    
    s = sum([p[1] for p in probas])

    # We choose in this newly uniform density of probability
    r = uniform(0, s)

    upto = 0
    for c, w in probas:
        if upto + w > r:
            return c
        upto += w
    assert False, "Error in calculation of probability density"



# Sort the list of nodes following the distance form a node.
def orderNodesByDistance(metaGraph, currentNode, eatenCoins):
    """
    orderNodesByDistance:
    Inputs   : metaGraph (dict of dict of tuple), currentNode (tuple), eatenCoins (list of tuples)
    Output   : list of tuple

    This function sort the nodes associated to currentNode in metaGraph and not in eatenCoins with the distance between them.
    """

    temp = metaGraph[currentNode]

    nodesList = [x for x in list(temp.items()) if x[0] not in eatenCoins]

    nodesList.sort(key = operator.itemgetter(1))
    return nodesList



# Removes elLocation from metaGraph if elLoc is in it. 
def updateCoins (metaGraph, eatenCoins, actualCoins):
    """
    updateCoins:
    Inputs   : metaGraph (dict of dict of tuple), eatenCoins (list of tuple), actualCoins (list of tuple)
    Output   : list of tuple

    The aim of this function is to update eatenCoins adding new eaten coins by players.
    """
    
    if len(metaGraph) > len(actualCoins):
        for coin in metaGraph :
            if coin not in actualCoins :
                eatenCoins.append(coin)
    
    return eatenCoins



# Removes elLocation from metaGraph if elLoc is in it. 
def updateCoinsWoPlayerLoc (metaGraph, eatenCoins, actualCoins, actualLoc):
    """
    updateCoinsWoPlayerLoc:
    Inputs   : metaGraph (dict of dict of tuple), eatenCoins (list of tuple), actualCoins (list of tuple), actualLoc (tuple)
    Output   : list of tuple

    The aim of this function is to update eatenCoins adding new eaten coins by players without player location.
    """
    
    if len(metaGraph) > len(actualCoins):
        for coin in metaGraph :
            if coin not in actualCoins and coin != actualLoc:
                eatenCoins.append(coin)
    
    return eatenCoins



def coinsInPath (path, mg, eatenCoins):
    coins=[]
    for c in path:
        if c in mg.keys() and c not in eatenCoins:
            coins.append(c)
    return coins



def metaGraphWithoutEaten (metaGraph, eatenCoins):
    # deep copy of metaGraph without bad coins
    mGwC = {}

    #{a : {b : metaGraph[a][b] if not b in eatenCoins else 'd' for b in metaGraph[a].keys ()} if not a in eatenCoins else 'd' for a in metaGraph.keys ()}
    
    for a in metaGraph.keys () : 
        if not a in eatenCoins :
            mGwC[a] = {}
            for b in metaGraph[a].keys () :
                if not b in eatenCoins :
                    mGwC[a][b] = metaGraph[a][b]
                    
                    
    return mGwC
        
    

    
def timeline (string, t0, tB, tE):
    api.debug ("[" + str(tE-t0) + "]\t"+ string + "\t(" + str(tE-tB) + ")")



def dist(metaGraph, begin, end):
    try :
        return metaGraph[begin][end]
    except KeyError:
        return -1;
