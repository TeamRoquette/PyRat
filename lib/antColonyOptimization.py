#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lib.PyratApi as api
import lib.utils as ut
import operator


# CONSTANTS for ACO
NB_ANTS = 6
NB_GROUPS_ANTS = 6
FACTOR_PHERO = 3
FACTOR_DIST = 4
FACTOR_EVAP = 0.3
FACTOR_Q = 9



#
def initFormicMetaGraph (metaGraph) :
    """
    This function initalizes and retruns a formic meta graph which is a meta graph containing simultaneously the distance between
    two nodes and the amount of pheromones in the vertice.
    """
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



#
def evapPheroFormicMetaGraph (fmg) :
    for pos1 in fmg:
        for pos2 in fmg[pos1]:
            fmg[pos1][pos2][1] *= (1-FACTOR_EVAP)

    return fmg



#
def mypow(a,b):
    if a != 0:
        return a**b
    return 1.0



#
def generateFormicMetaGraph (metaGraph, startPos) :
    """
    This function is a metaheuristic to solve the travelling salesman problem by simulating a colony of ants.
    It returns the best way provided by these approximation.
    """
    
    formicMetaGraph = initFormicMetaGraph (metaGraph)


    # For each groups of ants
    for i in range (NB_GROUPS_ANTS) :
        pathes = []

        # For each ants:
        for j in range (NB_ANTS) :
            api.debug("I am ant "+str(i)+str(j)+". Proud to serve U !")
            
            posToGo = startPos
            path = [startPos]
            posesToVisit = list(metaGraph[posToGo].keys())

            # We use the ant density of probability to determine every next step.
            while posesToVisit :
                probas = [(posToVisit, mypow(formicMetaGraph[posToGo][posToVisit][1],FACTOR_PHERO)/mypow(formicMetaGraph[posToGo][posToVisit][0],FACTOR_DIST)) for posToVisit in posesToVisit]

                posToGo = ut.weightedChoice(probas)

                path.append (posToGo)
                posesToVisit.remove (posToGo)

            api.debug("\tFinally I went there : "+str(path))
            pathes.append (path)

        debugFormicMetaGraph(formicMetaGraph, 5)
        # Finally we update the fmg with all pathes realized
        formicMetaGraph = evapPheroFormicMetaGraph (formicMetaGraph)
        for path in pathes:
            formicMetaGraph = addPheroFormicMetaGraph (formicMetaGraph, path)


    return formicMetaGraph



#
def chooseFormicPath (fmg, startLoc, eatenCoins):

    elLoc = startLoc
    lenPath = len (fmg [elLoc])+1
    bestPath = [elLoc]
    
    # While we haven't got the full path
    while len (bestPath) != lenPath:

        # We get and sort the coins
        nodesList = fmg[elLoc].items ()
        nodesList = [(n[0],n[1][1]) for n in nodesList]
        nodesList.sort (key = operator.itemgetter(1), reverse = True)

        # We append the next coin
        elLoc = nodesList[0][0]
        bestPath.append (elLoc)

    return bestPath



def debugFormicMetaGraph (fmg, mazeLong):
    """
    Format a output for pyplot that renders the formic meta graph
    """

    # import
    try:
        import matplotlib.pyplot as plt
    except:
        api.debug ("Matplotlib not found")
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

    
    
