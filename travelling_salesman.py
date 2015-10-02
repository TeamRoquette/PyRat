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


moving = False
path = []
last_directions = []
last_positions = []
eaten_coins = []
meta_graphe = {}
meilleurs_chemins = {}

# Fonction intermédiaire pour parcours_en_largeur
# trie le dictionnaire des meilleurs sommets pour en faire une liste compréhensible plus facilement
def ordonne (best_vert, start, stop, path):
    if start == stop:
        return path + [start]

    return ordonne (best_vert, start, best_vert[stop][0], path + [stop]) 



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

    return ordonne(best_vertice, startLocation, stopLocation, []), best_vertice[stopLocation][1]



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



def make_meta_graph (mazeMap, playerLocation, coins):
    sommets = [playerLocation] + coins
    
    meta_graph = {}
    best_ways = {}
    for i in sommets:
        for j in sommets:
            if j != i:

                chemin, distance = dijkstra(mazeMap, i,j)
                if i not in best_ways :
                    best_ways[i] = {}
                    meta_graph[i] = {}

                if j not in best_ways :
                    best_ways[j] = {}
                    meta_graph[j] = {}

                meta_graph[i][j]= distance
                best_ways[i][j] = chemin

                meta_graph[j][i]= distance
                best_ways[j][i] = chemin[::-1]


        sommets.remove(i)
    
    return meta_graph, best_ways



def update_coins (eaten_coins, elLocation):

    if elLocation in meta_graphe:
        eaten_coins.append(elLocation)
    
    return eaten_coins


    
def initializationCode (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    to = time.time()

    global meta_graphe
    global meilleurs_chemins

    # Construction d'un meta-graphe
    meta_graphe, meilleurs_chemins = make_meta_graph(mazeMap, playerLocation, coins)

    elapsed = time.time() - to
    debug(elapsed) 
    
    return "Everything seems fine, let's start !"



def determineNextMove (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    global path
    global moving
    global meta_graphe
    global meilleurs_chemins
    global eaten_coins

    # Si l'ennemi mange une pièce en chocolat, on la comp(o)te
    eaten_coins = update_coins(eaten_coins, opponentLocation)

    if moving: 
        if not path :
            moving = False

    # Si on n'a plus d'objectif, on cherche la plus proche pièce
    if not moving :

        # On choisit la prochaine plus proche pièce
        plusprochepiece = ((-1,-1),float('inf'))
        for locationCoin in meta_graphe[playerLocation]:
            if meta_graphe[playerLocation][locationCoin] < plusprochepiece[1] and locationCoin not in eaten_coins  :
                plusprochepiece = (locationCoin, meta_graphe[playerLocation][locationCoin])

        # On récupère le chemin pour aller a cette pièce

        path = meilleurs_chemins[playerLocation][plusprochepiece[0]]
        
        path.pop() # on enlève le premier élt qui est la position actuelle

        # Si on a mangé une pièce en chocolat, on la comp(o)te
        eaten_coins = update_coins(eaten_coins, playerLocation)

        moving = True
                
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
