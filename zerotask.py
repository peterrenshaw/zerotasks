#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#======
# name: tsk.py
# date: 2016NOV07
# prog: pr
# desc: zero task
#======


import os
import argparse


import tools
import config


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
    parser.add_argument("-e","--end",help="task ended")
    parser.add_argument("-f","--finish",help="task finished")
    # ------ task options ------
    options = parser.parse_args()


    if options.new:
        if not tools.new(options.new, options.comment, options.priority):
            tools.DISERR("Cannot add new task")
 
    if options.start:
        if not tools.update_start(options.start):
            tools.DISERR("Cannot update start on task","#{}".format(options.start))

    if options.end:
        if not tools.update_end(options.end):
            tools.DISERR("Cannot update end on task","#{}".format(options.start))

    if options.finish:
        if not tools.update_completed(options.finish):
            tools.DISERR("Cannot update end on task","#{}".format(options.start))

    if options.rebuild:
        if not tools.rebuild():
            tools.DISERR("Cannot rebuild tasks")

    if options.display:
        if tools.display_all():
            tools.DISERR("Cannot display tasks")

    if not (options.new or options.start or options.end or options.finish or options.rebuild or options.display):
        parser.print_help()


# main entry point for cli
if __name__  == "__main__":
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
