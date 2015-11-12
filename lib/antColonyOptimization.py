#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lib.PyratApi as api
import lib.utils as ut
import operator
import time

# CONSTANTS for ACO
NB_ANTS = 25
NB_ANTS_SAFETY_GAP = 1
FACTOR_PHERO = 1
FACTOR_DIST = 2
FACTOR_EVAP = 0.3
FACTOR_Q = 5*5



# Define the error used
class AntError (ValueError):
    '''
    Raise this when a error happens with ACO.
    '''
#
def initFormicMetaGraph (metaGraph, formicMetaGraph=None) :
    """
    This function initalizes and retruns a formic meta graph which is a meta graph containing simultaneously the distance between
    two nodes and the amount of pheromones in the vertice.
    """
    if formicMetaGraph:
        fmg = { (pos1) : { pos2 : [metaGraph[pos1][pos2], formicMetaGraph[pos1][pos2][1]] for pos2 in metaGraph[pos1].keys() } for pos1 in metaGraph.keys() }
#        api.debug(fmg)
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
def generateFormicMetaGraph (metaGraph, startPos, timeAllowed, formicMetaGraph=None) :
    """
    This function is a metaheuristic to solve the travelling salesman problem by simulating a colony of ants.
    It returns the best way provided by these approximation.
    """
    t0 = time.time ()
    
    formicMetaGraph = initFormicMetaGraph (metaGraph, formicMetaGraph)

    timeAnts = 0
    nbAnts = 0
    last = False
    
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
                probas = [(p[0],p[1]/su) for p in probas]
                posToGo = ut.weightedChoice(probas)

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
        #debugFormicMetaGraph (formicMetaGraph, 5)
            
    api.debug ("\tSent "+str(nbAnts)+" for a total of "+str(timeAnts)+"s :" +str(nbAnts/timeAnts))
    return formicMetaGraph



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

    
    
