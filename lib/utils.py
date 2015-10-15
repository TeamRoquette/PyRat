#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lib.PyratApi as api



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
    
