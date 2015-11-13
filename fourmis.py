#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import lib.PyratApi as api
import lib.shortestPaths as sp
import lib.travelHeuristics as th
import lib.utils as ut
import lib.antColonyOptimization as aco

import time
import operator

BOT_NAME = "Antbot"

# Global variable for general behaviour
GLOBALPATH = []
ACTUALPATH = []
GOALLOCATION = (-1,-1)
METAGRAPH = {}
FORMICMETAGRAPH = {}
BESTPATHES = {}
MOVING = False
EATENCOINS = []
PERCENTTIMEALLOWEDFORANTS = 0.80        



def chooseNextCoins (fmg, elLoc):
    try : 
        # Just order by pheromone:
        nodesList = fmg[elLoc].items ()
    except KeyError : 
        # Told them there's an error :
        raise AntError

    nodesList.sort (key = operator.itemgetter(1))
    return nodesList



# This function should not return anything, but should be used for a short preprocessing
def initializationCode (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    t0 = time.time()
    global METAGRAPH
    global BESTPATHES
    global FORMICMETAGRAPH

    global GLOBALPATH
    global ACTUALPATH
    global GOALLOCATION
    
    METAGRAPH, BESTPATHES = th.generateMetaGraph(mazeMap, playerLocation, coins)
    GOALLOCATION = playerLocation
    
    t1 = time.time()
    ut.timeline ("Computed meta-graph and best pathes", t0, t0, t1)

    FORMICMETAGRAPH = aco.generateFormicMetaGraph (METAGRAPH, playerLocation, (timeAllowed-(t1-t0))*0.99)
    
    t2 = time.time()
    
    ut.timeline ("Computed formic-meta-graph", t0, t1, t2)



# This is where you should write your code to determine the next direction
def determineNextMove (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :

    t0 = time.time ()

    # Travel heuristics variables
    global METAGRAPH
    global FORMICMETAGRAPH
    global BESTPATHES

    # Pathes variables
    global GLOBALPATH
    global ACTUALPATH
    global GOALLOCATION

    # General variables
    global MOVING    
    global EATENCOINS

    
    # We update eatenCoins except playerLocation
    EATENCOINS = ut.updateCoinsWoPlayerLoc (METAGRAPH, EATENCOINS, coins, playerLocation)

    if GOALLOCATION in EATENCOINS:
        ACTUALPATH = th.findNearestCoin(mazeMap, playerLocation, coins)
        GOALLOCATION = ACTUALPATH[0]
        api.debug("Thief ! We go there : "+str(GOALLOCATION))
        ACTUALPATH.pop ()

    newMetaGraph = ut.metaGraphWithoutEaten (METAGRAPH, EATENCOINS)


    # Let's send some ant. Not too much
    t1 = time.time ()
    FORMICMETAGRAPH = aco.generateFormicMetaGraph (newMetaGraph, GOALLOCATION, (timeAllowed-(t1-t0))*PERCENTTIMEALLOWEDFORANTS, FORMICMETAGRAPH)

    if MOVING :
        # Plus de chemin ou pièce bouffée, on s'arrete.
        if not ACTUALPATH :
            MOVING = False
            EATENCOINS.append (playerLocation)
    
    if not MOVING :
        # We choose the next coin with aco :
        GOALLOCATION = chooseNextCoins(FORMICMETAGRAPH, playerLocation)[0][0]
        
        # Get next path
        try :
            ACTUALPATH = list (BESTPATHES[playerLocation][GOALLOCATION])
        except KeyError: # The path doesn't exist, let's calculate one:
            ACTUALPATH = sp.shortestWay (mazeMap, playerLocation, GOALLOCATION)
         

        ACTUALPATH.pop () # Get rid of the first position wich should be actualPosition
        MOVING = True

    # Let's go !
    nextPos = ACTUALPATH.pop()
    return ut.convertPosesToDir(nextPos, playerLocation, mazeMap)



####



if __name__ == "__main__" :

    # We let technical stuff happen
    (mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = api.initGame(BOT_NAME)


    initializationCode(mazeWidth, mazeHeight, mazeMap, preparationTime, playerLocation, opponentLocation, coins)

    # Here magic happens
    api.mainLoop (determineNextMove, mazeWidth, mazeHeight, mazeMap, turnTime)    
