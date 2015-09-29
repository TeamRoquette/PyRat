#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import ast
import sys
import os
import time

CONV_KEY = ['U', 'R', 'D', 'L']
ERROR = -1
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


# Fonction intermédiaire pour parcours_en_largeur
# trie le dictionnaire des meilleurs sommets pour en faire une liste compréhensible plus facilement
def ordonne (best_vert, start, stop, path, dist):
    if start == stop:
        return path + [start], dist

    return ordonne (best_vert, start, best_vert[stop][0], path + [stop], dist+best_vert[stop][1]) 



# Réalise le parcours en largeur de la map et retourne la liste ordonée des sommets à suivre
def dijkstra (mazeMap, startLocation, stopLocation) :
    best_vertice = {(startLocation):((),0)}
    to_see_vertice = [startLocation]
    
    while to_see_vertice :
        vertex = to_see_vertice.pop(0)
        voisins = mazeMap[vertex]
        dist = best_vertice.get(vertex, ([], float('inf')))[1]
        
        for (v,d) in voisins :
            if best_vertice.get(v, ([], float('inf')))[1] > d + dist :
                best_vertice[v] = (vertex, d + dist)
                to_see_vertice.append(v)

    return ordonne(best_vertice, startLocation, stopLocation, [], 0)



def debugmap(best_vertice,height_map):
    l = ''
    for i in range (height_map):
        for j in range (height_map):
            c = best_vertice.get((i,j), ([], -1) )[1]
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



# Détermine la direction pour rallier next_pos depuis actual_pos, 
# Renvoie ERROR si cela n'est pas possible
def nextpostodir (next_pos, actual_pos, mazeMap):
    # Check if next position is reachable
    next_poses = mazeMap[actual_pos]
    reachable = False
    for (pos, d) in next_poses:
        if pos == next_pos:
            reachable = True
    
    if not reachable:
        return ERROR

    (y_act, x_act) = actual_pos
    (y_next, x_next) = next_pos
    
    if x_act == x_next:
        if y_next > y_act:
            return DOWN
        else:
            return UP
    else:
        if x_next > x_act:
            return RIGHT
        else:
            return LEFT
    


def initializationCode (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    to = time.time()
    global path

    # Construction d'un meta-graphe
    sommets = [playerLocation] + coins
    
    meta_graphe = {}
    meilleurs_chemins = {}

    for i in sommets:
        for j in sommets:
            if j != i:
                chemin, distance = dijkstra(mazeMap, i,j)
                meilleurs_chemins[i].append((j,chemin))
                meta_graphe[i].append((j, distance))

        sommets.remove(i)

    elapsed = time.time() - to
    debug(elapsed)

    debug(meta_graphe)

    return "Everything seems fine, let's start !"


def determineNextMove (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    global path
    nextPos = path.pop()
    nextDir = CONV_KEY[nextpostodir(nextPos, playerLocation, mazeMap)] 

    return nextDir
    



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
        # ICI preDetermineNextMove 
        #  fork 
        #  pipe pour discuter
