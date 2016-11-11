#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#======
# name: config.py
# date: 2016NOV10
# prog: pr
# desc: Zero Tasks: read docs/ABOUT.txt
#======


import os


#------- config -------
TITLE = """
 _____                      ______           __       
/__  /  ___  _________     /_  __/___ ______/ /_______
  / /  / _ \/ ___/ __ \     / / / __ `/ ___/ //_/ ___/
 / /__/  __/ /  / /_/ /    / / / /_/ (__  ) ,< (__  ) 
/____/\___/_/   \____/    /_/  \__,_/____/_/|_/____/  

"""

DEBUG = False

IVL_MIN = 6
IVL_MAX = 10

DDMMYY = "%a%d%m"
DMY = "%D%M%Y"
DD = "%a"

APP_NAME = "Zero Tasks"
APP_DIR = "zerotasks"
FN_EXT = "tsk"
FP_HOME = "/Users/pr"
FP_TASKS = os.path.join(FP_HOME, "work/code", APP_DIR)
TASKS_ARCHIVE = os.path.join(FP_TASKS, "2016")
TASK_ATTRIBUTES = dict(name="",            # name of task
                       description="",     # task comment (optional)
                       priority=0,         # priority of task given (1-3)
                       completed=False,    # is task completed flag
                       created=0.0,        # when task initiated in epoch UTC
                       start=0.0,          # when task started in epoch UTC
                       end=0.0)            # when task completed in epoch UTC

UNWANTED_CHAR = ['~','!','@','#','$','%','^','&','*','(',')','_','+','=',
                 '`',"'",'"','?','>','<',',','.','-','/','\\','|']
SEP = "-"
DDMMYY = "%a%d%m" 

#------ config ------


def main():
    """main entry point for cli"""
    pass


# main entry point for cli
if __name__  == "__main__":
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
