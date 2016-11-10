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
    # ------ new task -------
    parser.add_argument("-n","--new",help="create a new task")
    parser.add_argument("-c","--comment",help="comment for new task")
    parser.add_argument("-p","--priority",help="priority for new task")
    parser.add_argument("-f","--finish",help="task finished")
    parser.add_argument("-s","--start",help="task started")
    parser.add_argument("-e","--end",help="task ended")
    # ------ IO -------
    parser.add_argument("-o","--output",action="store_true",
                        help="save a file")
    # ------ verb task -------
    parser.add_argument("-d","--display", action="store_true",
                        help="display file content")
    parser.add_argument("-r","--rebuild", action="store_true",
                        help="rebuild the TASK, DONE lists")
    parser.add_argument("-i", "--increase", action="store_true",
                        help="increase maximum numnber of tasks")
    options = parser.parse_args()


    if options.new:
        print("new")
        
        if options.comment:
            print("comment")
        if options.priority:
            print("priority")

    if options.start:
        if not tools.update_task(options.start, 'start'):
            tools.DISERR("Cannot update start on task","#{}".format(options.start))
 
    if options.end:
        if not tools.update_task(options.end, 'end'):
            tools.DISERR("Cannot update end on task","#{}".format(options.start))

    if options.finish:
        if not tools.update_task(options.finish, 'completed'):
            tools.DISERR("Cannot update end on task","#{}".format(options.start))

    if options.rebuild:
        print("rebuild")
        if not tools.rebuild():
            tools.DISERR("Cannot rebuild tasks")


    if options.display:
        if tools.display_all():
            tools.DISERR("Cannot display tasks")

    if options.output:
        print("output")


# main entry point for cli
if __name__  == "__main__":
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
