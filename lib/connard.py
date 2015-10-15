#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal
from subprocess import check_output
import lib.PyratApi as api




  ############
 ### KILL ###
###########



def handlerDoNothing (signum, frame):
    api.debug ("Sir, someone's trying to kill me !")



def preventFromKilling():
    signal.signal(signal.SIGSTP, handlerDoNothing)
    signal.signal(signal.SIGILL, handlerDoNothing)



def getPidsToKkill():
    pids = check_output(["pidof", "python3"])
    mypid = os.getpid()
    return [int(i) for i in pids if int(i)!=mypid]




def stopOpponent():
    pids = getPidsToKill()
    for pid in pids:
        os.kill(pid, signal.SIGSTOP)



def resumeOpponent():
    pids = getPidsToKill()
    for pid in pids:
        os.kill(pid, signal.SIGCONT)    



  ############
 ### MOTD ###
###########



def displayMotd():
    motd = open("inputFiles/TeamRoquette/motd.txt", "r")
    api.debug(motd.read())
    motd.close()
