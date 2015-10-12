#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import sys
import os


ERROR = 'E'
UP = 'U'
RIGHT = 'R'
DOWN = 'D'
LEFT = 'L'


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
    
