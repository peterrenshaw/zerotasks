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




# main entry point for cli
if __name__  == "__main__":
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
