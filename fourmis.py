#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import lib.PyratApi as api
import lib.travelHeuristics as th
import lib.utils as ut
import lib.antColonyOptimization as aco

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

    
    FORMICMETAGRAPH = aco.generateFormicMetaGraph (METAGRAPH, playerLocation)
    
    t2 = time.time()
    api.debug(t2 - t1)
    api.debug(t2 - t0)

    GLOBALPATH = aco.chooseFormicPath (FORMICMETAGRAPH, playerLocation, [])

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
