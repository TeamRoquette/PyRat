#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lib.PyratApi as api

BOT_NAME = "Template"



def initializationCode (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :

    api.debug("\n" + "mazeWidth = " + str(mazeWidth) + "\n"
               + "mazeHeight = " + str(mazeHeight) + "\n"
               + "mazeMap = " + str(mazeMap) + "\n"
               + "timeAllowed = " + str(timeAllowed) + "\n"
               + "playerLocation = " + str(playerLocation) + "\n"
               + "opponentLocation = " + str(opponentLocation) + "\n"
               + "coins = " + str(coins))



def determineNextMove (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :

    return api.UP



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
