#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import ast
import sys
import os
import time
import operator
from multiprocessing.pool import ThreadPool as Pool
#import _thread as thd



CONV_KEY = ['U', 'R', 'D', 'L']
ERROR = -1
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
# Les directions sont ordonnées dans le sens trigonométrique


TEAM_NAME = "Team Roquette"

NB_COINS_TO_COMPUTE = 5
POOL_SIZE = 5



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


# Comportement général
moving = False
path = []

# Parcours du meta_graphe
eaten_coins = []
meta_graph = {}
best_pathes = {}
best_path_cost = float('inf')
best_path_nodes = [] 

# Multi-tasking
pool = Pool(POOL_SIZE)



###
### ALGO POUR LE CALCUL DU PLUS COURT CHEMIN
###



# Fonction intermédiaire pour dijkstra
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



###
### ALGO POUR PROBLEME DU VOYAGEUR
###



# Crée le méta_graph des pièces, renvoie le méta graphe et les meilleurs chemins
def make_meta_graph (mazeMap, playerLocation, coins):
    #if thread okay
    make_meta_graph_multithread (mazeMap, playerLocation, coins)

    
    
def make_meta_graph_monothread (mazeMap, playerLocation, coins):
    sommets = [playerLocation] + coins
    
    meta_graph = {}
    best_ways  = {}

    i = len(sommets)-1
    while i >= 0:

        j = 0
        while j < i:
            
            chemin, distance = dijkstra(mazeMap, sommets[i], sommets[j])
            if sommets[i] not in best_ways :
                best_ways[sommets[i]]  = {}
                meta_graph[sommets[i]] = {}
                
            if sommets[j] not in best_ways :
                best_ways[sommets[j]]  = {}
                meta_graph[sommets[j]] = {}
                    
            meta_graph[sommets[i]][sommets[j]] = distance
            best_ways[sommets[i]][sommets[j]]  = chemin

            meta_graph[sommets[j]][sommets[i]] = distance
            best_ways[sommets[j]][sommets[i]]  = chemin[::-1]

            j += 1
        
        i -= 1            
    
    return meta_graph, best_ways



def updateMetaGraph_thread_fun (start, stop):
    global meta_graph
    global best_pathes
    
    chemin, distance = dijkstra(mazeMap, start, stop)
    if start not in best_ways :
        best_pathes[start]  = {}
        meta_graph[stop] = {}
        
    if stop not in best_ways :
        best_pathes[stop]  = {}
        meta_graph[stop] = {}
        
    meta_graph[start][stop] = distance
    best_pathes[start][stop]  = chemin
    
    meta_graph[start][stop] = distance
    best_pathes[start][stop]  = chemin[::-1]

    debug("Finish!")


    
def make_meta_graph_multithread (mazeMap, playerLocation, coins):
    sommets = [playerLocation] + coins
    
    #meta_graph = {}
    #best_ways  = {}

    i = len(sommets)-1
    while i >= 0:

        j = 0
        while j < i:

            pool.apply_async( updateMetaGraph_thread_fun, (sommets[i], sommets[j],))

            j += 1
        
        i -= 1            

    pool.close()
    pool.join()
    
    #return meta_graph, best_ways



# Résoud de manière naive le probleme du voyageur, modifie les variables globales pour le meilleur chemin
def voyageur_naif(node_start, nodes, cost, path):
    global best_path_cost
    global best_path_nodes

    if not nodes:
        if cost < best_path_cost:
            best_path_cost = cost
            best_path_nodes = path
    else:
        for node in nodes:
            nodes_to_see = list(nodes)
            nodes_to_see.remove(node)
            voyageur_naif(node, nodes_to_see, cost + node[1], path+[node[0]])



###
### ALGOS DE COMPORTEMENTS GENERAUX
###



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



# Ordonne les noeuds selon la distance en pcc depuis le currentNode, retourne une liste de tuples (noeuds, distance)
def ordonneNodes(metaGraph, currentNode):
    temp = metaGraph[currentNode]

    nodesList = [x for x in list(temp.items()) if x[0] not in eaten_coins]

    nodesList.sort(key = operator.itemgetter(1))
    return nodesList



# Mets à jour la liste des pièces mangées en fonction de la position d'un joueur
def update_coins (eaten_coins, elLocation):

    if elLocation in meta_graph:
        eaten_coins.append(elLocation)
    
    return eaten_coins



# Détermine les prochaines pièces et renvoie la prochaine pièce
def chooseCoin (playerLocation):
    global best_path_nodes
    global best_path_cost

    best_path_cost = float('inf')
    best_path_nodes = []

    # Determination des sommets à calculer avec l'algo naif
    nodes_to_compute = ordonneNodes(meta_graph, playerLocation)

    
    # Création du chemin par l'algo naif
    voyageur_naif(playerLocation, nodes_to_compute[:NB_COINS_TO_COMPUTE -1], 0, [])

    return best_path_nodes[0]

###
###
###



def initializationCode (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    t0 = time.time() #timer initial

    global meta_graph
    global best_pathes

    # Construction d'un meta-graphe
    #meta_graph, best_pathes = make_meta_graph(mazeMap, playerLocation, coins)
    make_meta_graph(mazeMap, playerLocation, coins)
    
    t3 = time.time() #timers finaux
    debug(t3-t0) 

        
    return "Everything seems fine, let's start !"



###
###
###



def determineNextMove (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    global path
    global moving
    global meta_graph
    global best_pathes
    global best_path_nodes
    global eaten_coins

    # Si l'ennemi mange une pièce en chocolat, on la comp(o)te
    eaten_coins = update_coins(eaten_coins, opponentLocation)
    # Si on a mangé une pièce en chocolat, on la comp(o)te
    eaten_coins = update_coins(eaten_coins, playerLocation)


    if moving: 
        if not path :
            moving = False

    # Si on n'a plus d'objectif
    if not moving :

        # On choisit la prochaine plus proche pièce
        nextCoin = chooseCoin(playerLocation)

        # On récupère le chemin pour aller a cette pièce
        path = best_pathes[playerLocation][nextCoin]
        ## TODO: faire des testes ici...
        path.pop() # on enlève le premier élt qui est la position actuelle

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
