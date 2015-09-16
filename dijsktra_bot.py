#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import ast
import sys
import os

CONV_KEY = ['U', 'R', 'D', 'L']
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
# Les directions sont ordonnées dans le sens trigonométrique


TEAM_NAME = "Team Roquette"




  ################
###  API STUFF ###
################


# Writes a message to the shell
def debug (text) :
    # Writes to the stderr channel
    sys.stderr.write(str(text) + "\n")
    sys.stderr.flush()

    
# Reads one line of information sent by the maze application
def readFromPipe () :
    # Reads from the stdin channel and returns the structure associated to the string
    try :
        text = sys.stdin.readline()
        return ast.literal_eval(text.strip())
    except :
        os._exit(-1)


# Sends the text to the maze application
def writeToPipe (text) :    
    # Writes to the stdout channel
    sys.stdout.write(text)
    sys.stdout.flush()



# Reads the initial maze information
def processInitialInformation () :
    # We read from the pipe
    data = readFromPipe()
    return (data['mazeWidth'], data['mazeHeight'], data['mazeMap'], data['preparationTime'], data['turnTime'], data['playerLocation'], data['opponentLocation'], data['coins'], data['gameIsOver'])



# Reads the information after each player moved
def processNextInformation () :
    # We read from the pipe
    data = readFromPipe()
    return (data['playerLocation'], data['opponentLocation'], data['coins'], data['gameIsOver'])




  ##############
### MY STUFF ###
##############



last_directions = []
last_positions = []



def ordonne (best_vert, start, stop, path):
    if start == stop:
        return [start] + path
    debug (best_vert)
    return ordonne (best_vert, start, best_vert[stop][0], [stop] + path) 


def dijkstra (mazeMap, playerLocation, coinLocation) :
    best_vertice = {}
    seen_vertice = []
    to_see_vertice = [playerLocation]
    #while len(seen_vertice) != len(mazeMap) :
    while to_see_vertice :
        vertex = to_see_vertice.pop()
        if vertex not in seen_vertice :
            voisins = mazeMap[vertex]
            dist = best_vertice.get(vertex, ([], float('inf')))[1]
            
            for (v,d) in voisins :
                debug (v)
                if best_vertice.get(v, ([], float('inf')))[1] > d + dist :
                    best_vertice[v] = (vertex, d + dist)
                    
                seen_vertice.append(vertex)
                to_see_vertice.append(v)
    debug(best_vertice)
    return ordonne(best_vertice, playerLocation, coinLocation, [])


# Convertit une direction relative en direction absolue par rapport à une direction de référence
def reltoabs_direction (rel_direction, abs_direction):
    return (rel_direction + abs_direction) % 4


def initializationCode (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :

    path = dijkstra (mazeMap, playerLocation, coins[0])
    last_directions.append(DOWN)
    last_positions.append(playerLocation)

    debug(path)


def determineNextMove (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :

    last_dir = last_directions[-1]
    
    if (playerLocation == last_positions[-1]):
        # On n'a pas pu bouger
        direction = reltoabs_direction (LEFT, last_dir);

    # C'est la première fois qu'on arriv sur cette case
    else :
    	direction = reltoabs_direction (RIGHT, last_dir)
        
    # On ajoute en mémoire notre décision
    last_positions.append(playerLocation)
    last_directions.append(direction)
    return CONV_KEY[direction]



  ##########
### MAIN ###
##########


if __name__ == "__main__" :
    
    # We send the team name
    writeToPipe(TEAM_NAME + "\n")
    
    # We process the initial information and have a delay to compute things using it
    (mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = processInitialInformation()
    initializationCode(mazeWidth, mazeHeight, mazeMap, preparationTime, playerLocation, opponentLocation, coins)
    
    # We decide how to move and wait for the next step
    while not gameIsOver :
        (playerLocation, opponentLocation, coins, gameIsOver) = processNextInformation()
        if gameIsOver :
            break
        nextMove = determineNextMove(mazeWidth, mazeHeight, mazeMap, turnTime, playerLocation, opponentLocation, coins)
        writeToPipe(nextMove)

