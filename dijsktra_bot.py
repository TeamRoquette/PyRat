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



path = []
last_directions = []
last_positions = []



def ordonne (best_vert, start, stop, path):
    if start == stop:
        return [start] + path

    return ordonne (best_vert, start, best_vert[stop][0], [stop] + path) 


def dijkstra (mazeMap, playerLocation, coinLocation) :
    best_vertice = {(playerLocation):((),0)}
    seen_vertice = []
    to_see_vertice = [playerLocation]
    #while len(seen_vertice) != len(mazeMap) :
    while to_see_vertice :
        vertex = to_see_vertice.pop()
        if vertex not in seen_vertice :
            voisins = mazeMap[vertex]
            dist = best_vertice.get(vertex, ([], float('inf')))[1]
            
            for (v,d) in voisins :
                if best_vertice.get(v, ([], float('inf')))[1] > d + dist :
                    best_vertice[v] = (vertex, d + dist)
                    
                seen_vertice.append(vertex)
                to_see_vertice.append(v)

    return ordonne(best_vertice, playerLocation, coinLocation, [])


# Convertit une direction relative en direction absolue par rapport à une direction de référence
def reltoabs_direction (rel_direction, abs_direction):
    return (rel_direction + abs_direction) % 4


def nextpostodir (next_pos, actual_pos, mazeMap):
    # Check if next position is reachable
    next_poses = mazeMap[actual_pos]
    if next_pos not in next_poses:
        return -1

    (x_act, y_act) = actual_pos
    (x_next, y_next) = next_pos

    #if x_act == x_next:
        #if :
    


def initializationCode (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :

    global path

    path = dijkstra (mazeMap, playerLocation, coins[0])
    debug (path)
    st = path.pop()
    
    if (st != playerLocation):
        return "BUG!"
    return "Everything seems fine, let's start !"


def determineNextMove (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :

    global path
    nextPos = path.pop()
    return 



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

