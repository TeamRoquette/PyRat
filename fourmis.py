#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lib.PyratApi as api
import lib.travelHeuristics as th
import lib.utils as ut

import time
import operator

BOT_NAME = "Antbot"

# Global variable for general behaviour
GLOBALPATH = []
ACTUALPATH = []
METAGRAPH = {}
FORMICMETAGRAPH = {}
BESTPATHES = {}
MOVING = False
EATENCOINS = []


# CONSTANTS for ACO
ACO_NB_ANTS = 50
ACO_NB_GROUPS_ANTS = 50
ACO_FACTOR_PHERO = 1
ACO_FACTOR_DIST = 50
ACO_FACTOR_EVAP = 0.3
ACO_FACTOR_Q = 9



#
def initFormicMetaGraph (metaGraph) :
    """
    This function initalizes and retruns a formic meta graph which is a meta graph containing simultaneously the distance between
    two nodes and the amount of pheromones in the vertice.
    """
    # We realise a deep copy of metaGraph and add a component to the 2nd dim
    fmg = { (pos1) : { pos2 : [metaGraph[pos1][pos2], 0] for pos2 in metaGraph[pos1].keys() } for pos1 in metaGraph.keys() }

    return fmg



#
def addPheroFormicMetaGraph (fmg, path) :
    """
    These functions updates the formic meta graph by assuming a ant realised the path in argument.
    We need the fundamental constant of ACO to be defined in the global scope. 
    """
    lenPath = len(path)
    prevPos = path.pop(0)

    for pos in path:
        fmg[prevPos][pos][1] += ACO_FACTOR_Q/lenPath

        prevPos = pos

    return fmg



#
def evapPheroFormicMetaGraph (fmg) :
    for pos1 in fmg:
        for pos2 in fmg[pos1]:
            fmg[pos1][pos2][1] *= (1-ACO_FACTOR_EVAP)

    return fmg



#
def mypow(a,b):
    if a != 0:
        return a**b
    return 1



#
def antColonyOptimization (metaGraph, startPos) :
    """
    This function is a metaheuristic to solve the travelling salesman problem by simulating a colony of ants.
    It returns the best way provided by these approximation.
    """
    
    formicMetaGraph = initFormicMetaGraph (metaGraph)

    # For each groups of ants
    for i in range (ACO_NB_GROUPS_ANTS) :
        pathes = []

        # For each ants:
        for j in range (ACO_NB_ANTS) :
            pos = startPos
            path = [startPos]
            posesToVisit = list(metaGraph[pos].keys())

            # We use the ant density of probability to determine every next step.
            while posesToVisit :

                probas = [(posToVisit, mypow(formicMetaGraph[pos][posToVisit][1],ACO_FACTOR_PHERO)/mypow(formicMetaGraph[pos][posToVisit][0],ACO_FACTOR_DIST)) for posToVisit in posesToVisit]
                posToGo = ut.weightedChoice(probas)

                path.append (posToGo)
                posesToVisit.remove (posToGo)

            pathes.append (path)
            

        # Finally we update the fmg with all pathes realized
        formicMetaGraph = evapPheroFormicMetaGraph (formicMetaGraph)
        for path in pathes:
            formicMetaGraph = addPheroFormicMetaGraph (formicMetaGraph, path)


    return formicMetaGraph



#
def chooseFormicPath (fmg, startLoc, eatenCoins):

    elLoc = startLoc
    lenPath = len (fmg [elLoc])+1
    bestPath = [elLoc]
    
    # While we haven't got the full path
    while len (bestPath) != lenPath:

        # We get and sort the coins
        nodesList = fmg[elLoc].items ()
        nodesList = [(n[0],n[1][1]) for n in nodesList]
        nodesList.sort (key = operator.itemgetter(1), reverse = True)

        # We append the next coin
        elLoc = nodesList[0][0]
        bestPath.append (elLoc)

    return bestPath

        



# This function should not return anything, but should be used for a short preprocessing
def initializationCode (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    t0 = time.time()
    global METAGRAPH
    global BESTPATHES
    global FORMICMETAGRAPH

    global GLOBALPATH
    global ACTUALPATH
    
    METAGRAPH, BESTPATHES = th.generateMetaGraph(mazeMap, playerLocation, coins)

    t1 = time.time()
    api.debug(t1 - t0)

    
    FORMICMETAGRAPH = antColonyOptimization (METAGRAPH, playerLocation)

    t2 = time.time()
    api.debug(t2 - t1)
    api.debug(t2 - t0)

    GLOBALPATH = chooseFormicPath (FORMICMETAGRAPH, playerLocation, [])

    api.debug (GLOBALPATH)
    GLOBALPATH.pop(0)



# This is where you should write your code to determine the next direction
def determineNextMove (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :

    # Travel heuristics variables
    global METAGRAPH
    global FORMICMETAGRAPH
    global BESTPATHES

    # Pathes variables
    global GLOBALPATH
    global ACTUALPATH

    # General variables
    global MOVING    
    global EATENCOINS

    
    EATENCOINS = ut.updateCoins(METAGRAPH, EATENCOINS, opponentLocation)
    EATENCOINS = ut.updateCoins(METAGRAPH, EATENCOINS, playerLocation)

    if MOVING :
        if not ACTUALPATH :
            MOVING = False
    
    if not MOVING :
        nextCoin = GLOBALPATH.pop (0)

        api.debug(nextCoin)
        
        ACTUALPATH = list(BESTPATHES[playerLocation][nextCoin])
        ACTUALPATH.pop()
        
        MOVING = True
    
    nextPos = ACTUALPATH.pop()

    return ut.convertPosesToDir(nextPos, playerLocation, mazeMap)



####



if __name__ == "__main__" :

    # We let technical stuff happen
    (mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = api.initGame(BOT_NAME)


    initializationCode(mazeWidth, mazeHeight, mazeMap, preparationTime, playerLocation, opponentLocation, coins)

    # Here magic happens
    api.mainLoop (determineNextMove, mazeWidth, mazeHeight, mazeMap, turnTime)    
