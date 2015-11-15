#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal
from subprocess import check_output
import lib.PyratApi as api




  ############
 ### KILL ###
###########



def handler (signum, frame):
    api.debug ("Sir, someone's trying to kill me !")



def preventFromKilling():
    api.debug ("Protecting myself....")
    signal.signal(signal.SIGILL, handler)
    signal.signal(signal.SIGTSTP, handler)
    signal.signal(signal.SIGCONT, handler)
    api.debug ("Protected !")


def getPids(name):
    pids = check_output(["pidof", name]).split()
    mypid = os.getpid()
    return [int(i) for i in pids if int(i)!=os.getpid()]



def stopOpponent():
    pids = getPids("python3")
    for pid in pids:
        os.kill(pid, signal.SIGTSTP)



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

    
