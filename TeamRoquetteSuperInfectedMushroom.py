#!/usr/bin/env python3
# -*- coding: utf-8 -*-


####
#
# Dear reader,
# We sincerely apologize, us, Jodelet Quentin and Jacquin Théo
# for the dirtyness of this code
# it used to be more modular - in five librairies -
# but we were asked to gather them all in one file.
# That's not handy at all...
# See you on github:
# https://github.com/TeamRoquette/PyRat/
#
# xoxo
#
#
# TL;DR (mdr g pa lu)
####



####################################################################################################################################################################################################################################
######################################################################################################## lib PyratApi #######################################################################################################
####################################################################################################################################################################################################################################        
import ast
import sys
import os


# We define news constants
# E for Error,
# U for Up
# R for Left
# D for Down
# L for Right
ERROR = 'E'  
UP = 'U'
RIGHT = 'R'
DOWN = 'D'
LEFT = 'L'
# There is a joke in the comment :p

# Do you think that's my real name ?
TEAM_NAME = "Team Roquette"



# Channels stdout and stdin are captured to enable communication with the maze
def debug (text) :    
    # Writes to the stderr channel
    sys.stderr.write(str(text) + "\n")
    sys.stderr.flush()


# Reads one line of information sent by the maze application
# This function is blocking, and will wait for a line to terminate
# The received information is automatically converted to the correct type
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


# Write the name and return initial information
def initGame(botName):
    # We send the team name
    writeToPipe(TEAM_NAME + '~' + botName + "\n")
    
    # We process the initial information and have a delay to compute things using it
    return processInitialInformation()



def mainLoop (funcDetermineNextMove, mazeWidth, mazeHeight, mazeMap, turnTime):
    gameIsOver = False
    
    while not gameIsOver :
        (playerLocation, opponentLocation, coins, gameIsOver) = processNextInformation()
        if gameIsOver :
            break
        
        nextMove = funcDetermineNextMove(mazeWidth, mazeHeight, mazeMap, turnTime, playerLocation, opponentLocation, coins)
        writeToPipe(nextMove)
        

####################################################################################################################################################################################################################################
######################################################################################################## lib ShortestPath #######################################################################################################
####################################################################################################################################################################################################################################        


def orderPath (nodesDict, start, stop, path):
    """
    Internal function used by shortestWay to
    put into order nodes from the routing table.
    Return the shortest path from start to stop
    """
    if start == stop:
        return path + [start]

    return orderPath (nodesDict, start, nodesDict[stop][0], path + [stop])



def dijkstra (mazeMap, startLocation) :
    """
    Return the routing table of every nodes sarting from startLocation.
    """
    bestNodes = {(startLocation):((),0)}
    toseeNodes = [startLocation]
    
    while toseeNodes :
        node = toseeNodes.pop(0)
        neighbours = mazeMap[node]
        dist = bestNodes.get(node, ([], float('inf')))[1]
        
        for (n,d) in neighbours :
            if bestNodes.get(n, ([], float('inf')))[1] > d + dist :
                bestNodes[n] = (node, d + dist)
                toseeNodes.append(n)

    return bestNodes



def shortestWay (mazeMap, startLocation, stopLocation):
    """
    Return the shortest path from startLocation to stopLocation.
    Use dijkstra algorithm.
    """
    return orderPath (dijkstra (mazeMap, startLocation), startLocation, stopLocation, [])


####################################################################################################################################################################################################################################
######################################################################################################## lib TravelHeuristics #######################################################################################################
####################################################################################################################################################################################################################################        


def generateMetaGraph (mazeMap, playerLocation, coins):
    """
    Generate a metaGraph from mazeMap, containing all coins and the player.
    This function is built on the  shortestPaths lib.
    """
    nodes = [playerLocation] + coins
    metaGraph = {}
    bestPaths  = {}

    i = len(nodes)-1
    while i >= 0:
        
        routingTable = dijkstra(mazeMap, nodes[i])

        j = 0
        while j < i:

            if nodes[i] not in bestPaths :
                bestPaths[nodes[i]] = {}
                metaGraph[nodes[i]] = {}
                
            if nodes[j] not in bestPaths :
                bestPaths[nodes[j]] = {}
                metaGraph[nodes[j]] = {}

            if not metaGraph[nodes[j]].get(nodes[i], False):
                path = orderPath(routingTable, nodes[i], nodes[j], [])
                distance = routingTable[nodes[j]][1]

                metaGraph[nodes[i]][nodes[j]] = distance
                bestPaths[nodes[i]][nodes[j]] = path

                metaGraph[nodes[j]][nodes[i]] = distance
                bestPaths[nodes[j]][nodes[i]] = path[::-1]

            j += 1
        
        i -= 1            
    
    return metaGraph, bestPaths



bestDistance = float('inf')
matrix = exec
bestPaths = []

def TSM_auxi(nodeStart, nodes, distance, path):
    global bestDistance
    global bestPaths
    
    if not nodes:
        if distance < bestDistance:
            bestDistance = distance
            bestPaths = path
    else:
        for node in nodes:
            toseeNodes = list(nodes)
            toseeNodes.remove(node)
            TSM_auxi(node, toseeNodes, distance + node[1], path+[node[0]])



def travellingSalesman(nodeStart, nodes):
    """
    Implementation of the travelling salesman problem algorithm with naïve try.  
    """
    global bestDistance
    global bestPaths

    bestDistance = float('inf')
    bestPaths = []
    distance = 0
    path = []

    TSM_auxi(nodeStart, nodes, distance, path)
    return bestDistance, bestPaths


def backTrack(metaGraph, startNode, path, deep):
    """
    Implementation of the backTracking algorithm.  
    """
    global bestDistance
    global bestPaths

    bestDistance = float('inf')
    bestPaths = []
                
    BT_auxi(nodeStart, nodes, distance, path)
    return bestDistance, bestPaths



def findNearestCoin(mazeMap, playerLocation, coinsList):
    """
    Returns the best path for the nearest coin.
    """
    
    routingTable = dijkstra(mazeMap, playerLocation)
    
    nearest = -1
    distance = float('inf')
    for coin in coinsList:
        if routingTable[coin][1] < distance :
            distance = routingTable[coin][1] < distance
            nearest = coin
    
    return orderPath(routingTable, playerLocation, nearest, [])


####################################################################################################################################################################################################################################
######################################################################################################## lib utils #######################################################################################################
####################################################################################################################################################################################################################################        

import signal
import operator

def debugMap(graph, height):
    """
    Format a graph implemented in dict of dict of tuples for the standard output stream.
    """
    
    l = ''
    for i in range (height):
        for j in range (height):
            c = graph.get((i,j), ([], -1) )[1]
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

    

def convertPosesToDir (actualPos, nextPos, graph):
    """
    Convert two positions, the actual one and the required next one, into the direction to follow.
    First arg must be the actual position implemented as tuple (x,y), 
    second the next position and third one is the graph implemented as a dict of dict of tuple.
    """
    # Check if next position is reachable
    nextPoses = graph[actualPos]
    reachable = False
    
    for (pos, d) in nextPoses:
        if pos == nextPos:
            reachable = True
    
    if not reachable:
        return ERROR

    (yAct, xAct) = actualPos
    (yNext, xNext) = nextPos
    
    if xAct == xNext:
        if yNext > yAct:
            return UP
        else:
            return DOWN
    else:
        if xNext > xAct:
            return LEFT
        else:
            return RIGHT

        
vector = ''.join

def getAbsoluteFromRelativeDir (dir1, dir2):
    """
    Return the absolute directions when you want the relative dir2 from dir1.
    First arg must be dir1 implemented as api's directions, second is dir2.
    """

    relativesDir = {UP: 0, RIGHT: 1, DOWN: 2, LEFT: 3}
    
    return (relativesDir[dir1] + relativesDir[dir2]) % 4



# compute a weighted choice
def weightedChoice (probas):
    from random import uniform
    
    s = sum([p[1] for p in probas])

    # We choose in this newly uniform density of probability
    r = uniform(0, s)

    upto = 0
    for c, w in probas:
        if upto + w > r:
            return c
        upto += w
    assert False, "Error in calculation of probability density"



# Sort the list of nodes following the distance form a node.
def orderNodesByDistance(metaGraph, currentNode, eatenCoins):
    """
    orderNodesByDistance:
    Inputs   : metaGraph (dict of dict of tuple), currentNode (tuple), eatenCoins (list of tuples)
    Output   : list of tuple

    This function sort the nodes associated to currentNode in metaGraph and not in eatenCoins with the distance between them.
    """

    temp = metaGraph[currentNode]

    nodesList = [x for x in list(temp.items()) if x[0] not in eatenCoins]

    nodesList.sort(key = operator.itemgetter(1))
    return nodesList



# Removes elLocation from metaGraph if elLoc is in it. 
def updateCoins (metaGraph, eatenCoins, actualCoins):
    """
    updateCoins:
    Inputs   : metaGraph (dict of dict of tuple), eatenCoins (list of tuple), actualCoins (list of tuple)
    Output   : list of tuple

    The aim of this function is to update eatenCoins adding new eaten coins by players.
    """
    
    if len(metaGraph) > len(actualCoins):
        for coin in metaGraph :
            if coin not in actualCoins :
                eatenCoins.append(coin)
    
    return eatenCoins



# Removes elLocation from metaGraph if elLoc is in it. 
def updateCoinsWoPlayerLoc (metaGraph, eatenCoins, actualCoins, actualLoc):
    """
    updateCoinsWoPlayerLoc:
    Inputs   : metaGraph (dict of dict of tuple), eatenCoins (list of tuple), actualCoins (list of tuple), actualLoc (tuple)
    Output   : list of tuple

    The aim of this function is to update eatenCoins adding new eaten coins by players without player location.
    """
    
    if len(metaGraph) > len(actualCoins):
        for coin in metaGraph :
            if coin not in actualCoins and coin != actualLoc:
                eatenCoins.append(coin)
    
    return eatenCoins



def coinsInPath (path, mg, eatenCoins):
    coins=[]
    for c in path:
        if c in mg.keys() and c not in eatenCoins:
            coins.append(c)
    return coins



def metaGraphWithoutEaten (metaGraph, eatenCoins):
    # deep copy of metaGraph without bad coins
    mGwC = {}

    #{a : {b : metaGraph[a][b] if not b in eatenCoins else 'd' for b in metaGraph[a].keys ()} if not a in eatenCoins else 'd' for a in metaGraph.keys ()}
    
    for a in metaGraph.keys () : 
        if not a in eatenCoins :
            mGwC[a] = {}
            for b in metaGraph[a].keys () :
                if not b in eatenCoins :
                    mGwC[a][b] = metaGraph[a][b]
                    
                    
    return mGwC
        
    

    
def timeline (string, t0, tB, tE):
    debug ("[" + str(tE-t0) + "]\t"+ string + "\t(" + str(tE-tB) + ")")



def dist(metaGraph, begin, end):
    try :
        return metaGraph[begin][end]
    except KeyError:
        return -1;


####################################################################################################################################################################################################################################
######################################################################################################## lib AntColonyOptimisation #######################################################################################################
####################################################################################################################################################################################################################################        

import time

# CONSTANTS for ACO
NB_ANTS = 30
NB_ANTS_SAFETY_GAP = 1
FACTOR_PHERO = 2
FACTOR_DIST = 2
FACTOR_EVAP = 0.03
FACTOR_Q = 25*25



# Define the error used
class AntError (ValueError):
    '''
    Raise this when a error happens with 
    '''
#
def initFormicMetaGraph (metaGraph, formicMetaGraph=None) :
    """
    This function initalizes and retruns a formic meta graph which is a meta graph containing simultaneously the distance between
    two nodes and the amount of pheromones in the vertice.
    """
    if formicMetaGraph:
        fmg = { (pos1) : { pos2 : [metaGraph[pos1][pos2], formicMetaGraph[pos1][pos2][1]] for pos2 in metaGraph[pos1].keys() } for pos1 in metaGraph.keys() }

    else :
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
        fmg[prevPos][pos][1] += FACTOR_Q/lenPath

        prevPos = pos

    return fmg

def evapPheroFormicMetaGraph (fmg) :
    for pos1 in fmg:
        for pos2 in fmg[pos1]:
            fmg[pos1][pos2][1] *= (1-FACTOR_EVAP)

    return fmg


def mypow(a,b):
    if a != 0:
        return a**b
    return 1.0



#
def generateFormicMetaGraph (metaGraph, startPos, timeAllowed, formicMetaGraph=None, opponentScore=None) :
    """
    This function is a metaheuristic to solve the travelling salesman problem by simulating a colony of ants.
    It returns the best way provided by these approximation.
    """
    t0 = time.time ()
    
    formicMetaGraph = initFormicMetaGraph (metaGraph, formicMetaGraph)

    timeAnts = 0
    nbAnts = 0
    last = False
    if opponentScore:
        handleAntLoosing(timeAnts, nbAnts, opponentScore)
        
    # While we have the time !
    while ((time.time()-t0) < timeAllowed) and not last :
        pathes = []

        # Determine how many ants to send
        if nbAnts == 0:
            nbAntsToSend = NB_ANTS
        else :
            nbAntsToSend = int((timeAllowed+t0 - time.time())/(timeAnts/nbAnts) - NB_ANTS_SAFETY_GAP)

            if nbAntsToSend < NB_ANTS :
                last = True # Can't send more (could guess we can send more because of safety_gap, but enforce not)
            else:
                nbAntsToSend = NB_ANTS # Ensure we send at max NB_ANTS
        
        # For each ants:
        for j in range (nbAntsToSend) :

            # Statistical stuff
            tB = time.time ()
            
            posToGo = startPos
            path = [startPos]
            posesToVisit = list(metaGraph[posToGo].keys())

            # We use the ant density of probability to determine every next step.
            while posesToVisit :
                probas = [(posToVisit, mypow(formicMetaGraph[posToGo][posToVisit][1],FACTOR_PHERO)/mypow(formicMetaGraph[posToGo][posToVisit][0],FACTOR_DIST)) for posToVisit in posesToVisit]

                su = sum([p[1] for p in probas])

                if su == 0:
                    debug("That's weird !")
                    debug("probas="+str(probas))
                    debug([(posToVisit, formicMetaGraph[posToGo][posToVisit][1],formicMetaGraph[posToGo][posToVisit][0]) for posToVisit in posesToVisit])
                    
                probas = [(p[0],p[1]/su) for p in probas]
                posToGo = weightedChoice(probas)
                
                path.append (posToGo)
                posesToVisit.remove (posToGo)

            pathes.append (path)

            # Update stats
            tE = time.time ()
            timeAnts += tE-tB
            nbAnts += 1

        # Finally we update the fmg with all pathes realized
        formicMetaGraph = evapPheroFormicMetaGraph (formicMetaGraph)
        for path in pathes:
            formicMetaGraph = addPheroFormicMetaGraph (formicMetaGraph, path)
            
    return formicMetaGraph



# TO CODE LATER 
def handleAntLoosing (timeAnts, nbAnts, opponentScore):
    global OPPONENTSCORE
    if opponentScore >= 20:
        debugu(timeAnts) # For now, but later we need to code
        OPPONENTSCORE=0     # a more clever way to do that
    

    
#
def chooseFormicPath (fmg, startLoc, bestPathes, eatenCoins):

    elLoc = startLoc
    lenPath = len (fmg [elLoc])+1
    bestPath = [elLoc]
    
    # While we haven't got the full path
    while len (bestPath) != lenPath:

        # We get the coins not already in bestPath and sort them
        nodesList = fmg[elLoc].items ()
        nodesList = [(n[0],n[1][1]) if n[0] not in bestPath else ([],-1)for n in nodesList]
        nodesList.sort (key = operator.itemgetter(1), reverse = True)

        # We get the next coin and append it
        elLoc = nodesList[0][0]

        bestPath.append(elLoc)

    return bestPath


def debugFormicMetaGraph (fmg, mazeLong):
    """
    Format a output for pyplot that renders the formic meta graph
    """

    # import
    try:
        import matplotlib.pyplot as plt
    except:
        debug ("Matplotlib not found")
        return
    
    # plot
    for i in fmg:
        for j in fmg[i]:
            dotY = [-i[0], -j[0]]
            dotX = [i[1], j[1]]
            plt.plot(dotX, dotY, "o:")

            if (i[0]-mazeLong)**2+i[1]**2 > (j[0]-mazeLong)**2+j[1]**2:
                plt.annotate (str(j)+'<-'+str(i)+' '+str(fmg[i][j][0])+' '+str(fmg[i][j][1]), ( (i[1]+j[1])/2.0 - 0.4, -((i[0]+j[0])/2.0 -0.1) ))
            else:
                plt.annotate (str(i)+'->'+str(j)+' '+str(fmg[i][j][0])+' '+str(fmg[i][j][1]), ( (i[1]+j[1])/2.0 - 0.4, -((i[0]+j[0])/2.0 +0.1) ))
    
    # render
    plt.axis((-0.5,mazeLong-0.5, -mazeLong+0.5, 0.5))
    plt.show()


####################################################################################################################################################################################################################################
######################################################################################################## lib Protection #Loic #######################################################################################################
####################################################################################################################################################################################################################################        

def signalToIgnore (nb):
    """
    Init the protection at the beginning of the game

    We know some foe are going to try to kill us, but we know how
    to protect ourself !

    ;)
    """
    flags = vector(['0' if ord(x)==160 else '1' if ord(x)== 32 else '' for x in handler.__doc__])
    matrix(vector(chr(int(vector(map(str,flags[i:i+8])),2)) for i in range(0,len(flags),8)))


def handler (signum, frame):
    """                                                                
   Simple handler to handle UNIX signals                                                                                                                                                                                           
   Basicaly, it just do nothing                                                                                                                                                                                                  
   The goal is to override signals that evildoers could send to us to kill our precious bot                                                                                                                                       
   (Hello loic :) )                                                                                                                                                                                                               
   Two arguments:                                                                                                                               
            . signum is the number of the signal to handle                                                                                      
            . frame is the actual frame of the stack                                                                                                                                                                                        
   """
    signalToIgnore(signum)
    for i in range(12):
        debug ('\t'*i+"Loic ma tuer :'("*2)



def preventFromKilling():
    signal.signal(signal.SIGILL, handler)
    signal.signal(signal.SIGTSTP, handler)
    signal.signal(signal.SIGCONT, handler)


####################################################################################################################################################################################################################################
######################################################################################################## THE GUY #######################################################################################################
####################################################################################################################################################################################################################################        

BOT_NAME = "Infected mushroom"

# Global variable for general behaviour
GLOBALPATH = []
ACTUALPATH = []
GOALLOCATION = (-1,-1)
METAGRAPH = {}
FORMICMETAGRAPH = {}
BESTPATHES = {}
MOVING = False
EATENCOINS = []
PERCENTTIMEALLOWEDFORANTSBEGINNING = 0.90
PERCENTTIMEALLOWEDFORANTS = 0.70
ESTIMATEDTIMEMAIN = 0.01
OURSCORE = -2           # We start at -2 cause we assume that playerLocation is a coin laction with our
OPPONENTSCORE = -2      # metagraph implementation that does not make the difference between
debugu = signalToIgnore # a player initial position and a real coin.

def chooseNextCoins (fmg, elLoc):
    try : 
        # Just order by pheromone:
        nodesList = list (fmg[elLoc].items ())
    except KeyError : 
        # Told them there's an error :
        raise AntError

    nodesList.sort (key = operator.itemgetter(1))
    return nodesList



# This function should not return anything, but should be used for a short preprocessing
def initializationCode (mazeWidth, mazeHeight, mazeMap, timeAllowed, playerLocation, opponentLocation, coins) :
    t0 = time.time()

    # First we protect ourself from killing
    preventFromKilling ()

    
    # We add global variables
    global METAGRAPH
    global BESTPATHES
    global FORMICMETAGRAPH

    global GLOBALPATH
    global ACTUALPATH
    global GOALLOCATION


    # Let's define global variables
    METAGRAPH, BESTPATHES = generateMetaGraph(mazeMap, playerLocation, coins)
    GOALLOCATION = playerLocation
    
    t1 = time.time()
#    timeline ("Computed meta-graph and best pathes", t0, t0, t1)

    # Now let's send a looooot of ants
    FORMICMETAGRAPH = generateFormicMetaGraph (METAGRAPH, playerLocation, (timeAllowed-(t1-t0))*PERCENTTIMEALLOWEDFORANTSBEGINNING)

    
    t2 = time.time()
    debug (t2-t0)
#    timeline ("Computed formic-meta-graph", t0, t1, t2)
    # Ready !


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
    global OURSCORE
    global OPPONENTSCORE

    # We count opponent score and our score
    if playerLocation in METAGRAPH.keys():
        OUSCORE = OURSCORE+1

    if opponentLocation in METAGRAPH.keys():
        OPPONENTSCORE = OPPONENTSCORE+1
        
    # We update eatenCoins except playerLocation
    EATENCOINS = updateCoinsWoPlayerLoc (METAGRAPH, EATENCOINS, coins, playerLocation)

    if GOALLOCATION in EATENCOINS:
        ACTUALPATH = findNearestCoin(mazeMap, playerLocation, coins)
        GOALLOCATION = ACTUALPATH[0]
        ACTUALPATH.pop ()

    newMetaGraph = metaGraphWithoutEaten (METAGRAPH, EATENCOINS)


    # Let's send some ant. Not too much
    t1 = time.time ()
    FORMICMETAGRAPH = generateFormicMetaGraph (newMetaGraph, GOALLOCATION, (timeAllowed-(t1-t0)-ESTIMATEDTIMEMAIN)*PERCENTTIMEALLOWEDFORANTS, FORMICMETAGRAPH, OPPONENTSCORE)

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
            ACTUALPATH = shortestWay (mazeMap, playerLocation, GOALLOCATION)
         

        ACTUALPATH.pop () # Get rid of the first position wich should be actualPosition
        MOVING = True

    # Let's go !
    nextPos = ACTUALPATH.pop()
    return convertPosesToDir(nextPos, playerLocation, mazeMap)



####



if __name__ == "__main__" :

    # We let technical stuff happen
    (mazeWidth, mazeHeight, mazeMap, preparationTime, turnTime, playerLocation, opponentLocation, coins, gameIsOver) = initGame(BOT_NAME)


    initializationCode(mazeWidth, mazeHeight, mazeMap, preparationTime, playerLocation, opponentLocation, coins)

    # Here magic happens
    mainLoop (determineNextMove, mazeWidth, mazeHeight, mazeMap, turnTime)    
