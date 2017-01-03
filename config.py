#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#=======
#  _____                      ______           __       
# /__  /  ___  _________     /_  __/___ ______/ /_______
#   / /  / _ \/ ___/ __ \     / / / __ `/ ___/ //_/ ___/
#  / /__/  __/ /  / /_/ /    / / / /_/ (__  ) ,< (__  ) 
# /____/\___/_/   \____/    /_/  \__,_/____/_/|_/____/  
#
# This file is part of Zero Tasks.
#
# Zero Tasks is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zero Tasks is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zero Tasks.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
#
# name: config.py
# date: 2016NOV10
# prog: pr
# desc: Zero Tasks: read docs/ABOUT.txt
#======


import os
import sys
import machine
#import datetime


#------- config -------
DEBUG = False

IVL_MIN = 6    # number of tasks are restricted to MIN at a time
IVL_MAX = 10   # number of task can be stretched to MAX at a time

DDMMYY = "%a%d%m"
DMY = "%D%M%Y"
DD = "%a"

APP_NAME = "Zero Tasks"

FP_HOME = machine.HOME
APP_DIR = machine.APP_DIR 
FP_REL_PATH = machine.REL_PATH

FN_EXT = "tsk"
FP_TASKS = os.path.join(FP_HOME, FP_REL_PATH, APP_DIR)


FP_TASKS_DATA_PATH = "ztdata"
TASKS_ARCHIVE = os.path.join(FP_TASKS, FP_TASKS_DATA_PATH)

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


TITLE = """
 _____                      ______           __       
/__  /  ___  _________     /_  __/___ ______/ /_______
  / /  / _ \/ ___/ __ \     / / / __ `/ ___/ //_/ ___/
 / /__/  __/ /  / /_/ /    / / / /_/ (__  ) ,< (__  ) 
/____/\___/_/   \____/    /_/  \__,_/____/_/|_/____/  

"""
#------ config ------


def main():
    """main entry point for cli"""

# main entry point for cli
if __name__  == "__main__":
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
