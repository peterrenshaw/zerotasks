#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#=======
#  _____                      ______           __       
# /__  /  ___  _________     /_  __/___ ______/ /_______
#   / /  / _ \/ ___/ __ \     / / / __ `/ ___/ //_/ ___/
#  / /__/  __/ /  / /_/ /    / / / /_/ (__  ) ,< (__  ) 
# /____/\___/_/   \____/    /_/  \__,_/____/_/|_/____/  
#
# name: zerotask.py
# date: 2016NOV07
# prog: pr
# desc: Zero Tasks: read docs/ABOUT.txt
#======


import os
import argparse


import tools
import config


__version__ = '0.0.1'
__author__ = 'Peter Renshaw'
__license__ = 'GNU GPL 3.0'
__email__ = 'peterenshaw@seldomlogical.com'
__url__ = 'https://github.com/peterrenshaw/zerotasks'
__description__ = """This is a TODO system that I want to display the latest things I'm doing on both console and webpage AND/OR service online. In the example above, the TODO list is integrated into bash and the console."""


def main():
    """main entry point for cli"""
    parser = argparse.ArgumentParser(description="")


    # ------ verb task -------
    parser.add_argument("-d","--display", action="store_true",
                        help="display file content")
    parser.add_argument("-r","--rebuild", action="store_true",
                        help="rebuild the TASK, DONE lists")    
    # ------ new task -------
    parser.add_argument("-n","--new",help="create a new task")
    parser.add_argument("-c","--comment",help="comment for new task")
    parser.add_argument("-p","--priority",help="priority for new task")
    # ------ task timing -------
    parser.add_argument("-s","--start",help="task started")
    parser.add_argument("-f","--finish",help="task finished")
    # ------ task options ------
    options = parser.parse_args()


    if options.new:
        if not tools.new(options.new, options.comment, options.priority):
            tools.MSG("Warning","Cannot add new task. Maximum number of tasks entered.\nComplete a task, enter again.")
    
    if options.start:
        if not tools.update_start(options.start):
            tools.MSG("Error", "Cannot update start on task #{}".format(options.start))

    if options.finish:
        if not tools.update_completed(options.finish):
            tools.MSG("Error", "Cannot update end of task and completion #{}".format(options.start))

    if options.rebuild:
        if not tools.rebuild():
            tools.MSG("Error", "Cannot rebuild tasks")
            
    if options.display:
        if not tools.display_all():
            tools.MSG(config.APP_NAME)

    if not (options.new or options.start or options.finish or options.rebuild or options.display):
        tools.MSG(config.TITLE)
        parser.print_help()


# main entry point for cli
if __name__  == "__main__":
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
