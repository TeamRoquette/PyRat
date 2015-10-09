#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal
from subprocess import check_output
import lib.PyratApi as api



def handlerDoNothing (signum, frame):
    api.debug ("Sir, someone's trying to kill me !")



def preventFromKilling():
    signal.signal(signal.SIGSTP, handlerDoNothing)
    signal.signal(signal.SIGILL, handlerDoNothing)


    
def stopOpponent():
    return



def resumeOpponent():
    return


    
def displayMotd():
    motd = open("inputFiles/TeamRoquette/motd.txt", "r")
    api.debug(motd.read())
    motd.close()
