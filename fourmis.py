#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lib.PyratApi as api
import lib.travelHeuristics as th
import lib.utils as ut

import time
import operator

BOT_NAME = "fourmis"
PATH = []
METAGRAPH = {}
BESTPATH = {}
MOVING = False
EATENCOINS = []
NB_COINS_TO_COMPUTE = 5



# This function should not return anything, but should be used for a short preprocessing
def initializationCode (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    global METAGRAPH
    global BESTPATHS
    iniTime = time.time()
    METAGRAPH, BESTPATHS = th.generateMetaGraph(mazeMap, playerLocation, coins)
    api.debug(time.time() - iniTime)
    return "Everything seems fine, let's start !"



def updateCoins (metaGraph, eatenCoins, elLocation):

    if elLocation in metaGraph:
        eatenCoins.append(elLocation)
    
    return eatenCoins



def closestCoins(metaGraph, currentNode, eatenCoins):

    temp = metaGraph[currentNode]

    nodesList = [x for x in list(temp.items()) if x[0] not in eatenCoins]

    nodesList.sort(key = operator.itemgetter(1))
    return nodesList



def chooseCoin (metaGraph, playerLocation, eatenCoins):

    # Determination des sommets à calculer avec l'algo naif
    nodesToCompute = closestCoins(metaGraph, playerLocation, eatenCoins)

    
    # Création du chemin par l'algo naif
    besDis, bestPaths =  th.travellingSalesman(playerLocation, nodesToCompute[:NB_COINS_TO_COMPUTE -1], 0, [])

    return bestPaths[0]



# This is where you should write your code to determine the next direction
def determineNextMove (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    global MOVING
    global METAGRAPH
    global BESTPATHS
    global EATENCOINS
    global PATH
    
    EATENCOINS = updateCoins(METAGRAPH, EATENCOINS, opponentLocation)
    EATENCOINS = updateCoins(METAGRAPH, EATENCOINS, playerLocation)

    if MOVING :
        if not PATH :
            MOVING = False
    
    if not MOVING :
        nextCoin = chooseCoin(METAGRAPH, playerLocation, EATENCOINS)

        PATH = BESTPATHS[playerLocation][nextCoin]
        PATH.pop()
        
        MOVING = True
    
    nextPos = PATH.pop()

    return ut.convertPosesToDir(nextPos, playerLocation, mazeMap)



####



if __name__ == "__main__" :

    # We let technical stuff happen
    (mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = api.initGame(BOT_NAME)


    initializationCode(mazeWidth, mazeHeight, mazeMap, preparationTime, playerLocation, opponentLocation, coins)
    
    # We decide how to move and wait for the next step
    while not gameIsOver :
        (playerLocation, opponentLocation, coins, gameIsOver) = api.processNextInformation()
        if gameIsOver :
            break
        nextMove = determineNextMove(mazeWidth, mazeHeight, mazeMap, turnTime, playerLocation, opponentLocation, coins)
        api.writeToPipe(nextMove)
