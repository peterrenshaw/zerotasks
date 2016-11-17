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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
#
# name: tools.py
# date: 2016NOV10
# prog: pr
# desc: Zero Tasks: read docs/ABOUT.txt
#======


import os
import json
import time
import glob
import time
import datetime


import IO
import config


#------ misc ------
#------
# clean_str: strips out unwanted chars, enforeces no 
#            spaces in string by replacing with '-'
#------
def clean_str(name, strip_char=config.UNWANTED_CHAR, sep=config.SEP):
    """clean string of non a-z,A-Z chars"""
    clean = ""
    EMPTY = ""
    SPACE = " "

    # strip characters from name
    for ch in strip_char:
        clean = name.replace(ch, EMPTY)
        name = clean

    # reject if empty spaces
    space_count = len(name.replace(SPACE, EMPTY))
    if space_count > 0:
        # replace spaces b/w words with dash
        name = name.replace(SPACE, sep)
        return name
    else:
        return False
#------ misc ------


#------- datetime -------
def get_epoch():
    """get current epoch UTC"""
    t = datetime.datetime.now()
    return time.mktime(t.timetuple())
def fmt_epoch(epoch, strf):
    """given an epoch, convert to strformat string supplied"""
    t = datetime.datetime.fromtimestamp(epoch)
    dt = "{}".format(t.strftime(strf)).upper()
    return dt
def fmt_short_date(epoch, cust_strf=config.DDMMYY):
    """convenience for fmt_epoch"""
    return fmt_epoch(epoch, strf=cust_strf)
#------- datetime -------


#------- task -------
def new(name, 
        comment="",
        priority=1):
    """create a new task, save"""
    # name, comment, priority
    name = name
    if comment: task_comment = comment
    if priority: task_priority = priority
        
    # task limit
    task_limit = config.IVL_MIN

    # rebuild TASKS
    fpn = IO.get_filepathname()
    if fpn:
        tasks = IO.read_all(fpn)
    else:
        tasks = []
        DISERR("Cannot readbuild filepathe name")

    # throttle number of tasks allowed
    if is_taskcount_reached(task_limit):
        DISCOM("tools.new","is_taskcount_reached = <{}>".format(is_taskcount_reached(task_limit)))
        task = new_task(name, comment, priority)
        if task:
            fp = IO.get_path(task)
            fpn = os.path.join(config.FP_HOME, config.FP_TASKS, fp)
            DISCOM("tools.new","fp=<{}>\nfpn=<{}>".format(fp, fpn))
            if IO.write(fpn, task):
                # rebuild to reflect latest changes in 'todo', 'done', 'tasks'
                return rebuild()
            else:
                DISERR("Cannot write new task","task {}\nfpn <{}>".format(task, fpn))
                return False
        else:
            DISERR("Task not created","task: {}\n fpn <{}>".format(task, task))
            return False
    else:
        DISWARN("Cannot add new task. Finish a task first.")
        return False
def new_task(name, 
             description="", 
             priority=1,
             attributes=config.TASK_ATTRIBUTES):
    """build a new task"""
    task = attributes
    if name:
        task['name'] = name
        task['description'] = description
        task['priority'] = priority
        task['created'] = get_epoch()
        return dict(task)
    else:
        return {}
def get_todo_count(filepath=config.FP_TASKS):
    """get tasks from TASKS list"""
    fpn = os.path.join(filepath, "TASKS")
    tasks = IO.read(fpn)
 
    DISCOM("tools.get_todo_count", "fpn=<{}>".format(fpn))
    DISCOM("tools.get_todo_count", "tasks=<{}>".format(tasks))

    count = 1
    for task in tasks:
        DISCOM("tools.get_todo_count", "task=<{}>".format(task))
        if task:
            if 'completed' in task:
                if not task['completed']:
                    count += 1
    return count
def is_taskcount_reached(task_max=config.IVL_MIN):
    """is number of tasks equal or greater than IVL set?"""
    # get current TASKS, size
    count = get_todo_count()
    
    # result is T/F?
    return (count <= task_max)
def update_task(number, key):
    """start the timeclock on a task"""
    DISCOM("tools.update_task","number={}".format(number))
    if number:
         tasks = []
         fpn = IO.get_filepathname()
         DISCOM("tools.update_task","fpn={}".format(fpn))
         if fpn: tasks = sort_todo(IO.read_all(fpn))
         else: DISERR("Cannot read file content")
         
         count = 1
         DISCOM("tools.update_task", "count={}".format(count))
         DISCOM("tools.update_task", "tasks={}".format(tasks))
         for task in tasks:
             if count == int(number):
                  DISCOM("tools.update_task", 
                         "{} {} {}/{} {}".format(task['start'], task['end'], task['completed'], count, number))
                  if key == 'start':
                      task['start'] = get_epoch()
                  elif key == 'completed':
                      task['completed'] = True

                      # clear up task datetime fields
                      epoch = get_epoch()
                      if not task['start']:       # haven't flagged?
                          task['start'] = epoch   # time started
                      task['end'] = epoch         # time completed
                  else:
                      pass
                  #print("num={} key={} task={}".format(number, key, task[key], task))

                  fpn = IO.get_path(task)
                  DISCOM("tools.update_task","fpn <{}>".format(fpn))
                  DISCOM("tools.update_task","key <{}>".format(key))
                  DISCOM("tools.update_task","task <{}>".format(task))
                  if not IO.write(fpn, task):
                      DISERR("Cannot write task")
                      return False
             else:
                 pass

             # outside loop duffer
             count += 1

         return True
    else:
         DISERR("Cannot read file content")
         return False
def update_start(number):
    return update_task(number, 'start')
def update_end(number):
    return update_task(number, 'end')
def update_completed(number):
    return update_task(number, 'completed')
#------ task ------


#------ sort -------
def sort(data, key, value):
    """sort data by key and value"""
    s = []
    for task in data:
        DISCOM("tools.sort()", "task <{}>".format(task))
        if key in task:
            if bool(task[key]) == value:
                # add task to top of list
                DISCOM("tools.sort()", "--- ADDED task <{}> ADDED ---".format(task))
                #s.insert(0, task)
                s.append(task)
            else:
                pass
        else:
            return False
    return s
def sort_done(data):
    """convenience for sort: sort by completed, true (done)"""
    return sort(data, key="completed",value=True)
def sort_todo(data):
    """convenience for sort: sort by completed, false (todo)"""
    return sort(data, key="completed",value=False)
def rebuild():
    """build lists from archive"""
    # tasks from archive
    fpn = IO.get_filepathname()
    if fpn: 

        # sort tasks, write task list
        # TASKS is json list in raw format
        tasks = IO.read_all(fpn)
        fpn = os.path.join(config.FP_HOME, config.FP_TASKS, "TASKS")
        DISCOM("tools.rebuild","tasks=<{}>".format(tasks))
        DISCOM("tools.rebuild","fpn=<{}>".format(fpn))

        # kill old file
        if os.path.isfile(fpn):
            os.remove(fpn)
        # re-write file
        if not IO.write_tasks(fpn, tasks, 'a'):
            DISERR("tools.rebuild","Cannot write TASKS")
            return False

        # TODOs write
        todo = sort_todo(tasks)
        rend_todo = display(todo, show_count=True, is_raw=False, show=False)
        fpn = os.path.join(config.FP_HOME, config.FP_TASKS, "TODO")
        if rend_todo:
            if not IO.write(fpn, rend_todo, is_json=False, save_bit='w'):
                DISERR("Cannot write TODO")
                return False

        # TODOs written to $HOME
        fpn = os.path.join(config.FP_HOME, "TODO")
        if not IO.write(fpn, rend_todo, is_json=False, save_bit='w'):
            DISERR("Cannot write TODO to home")
            return False

        # DONE write
        done = sort_done(tasks)
        rend_done = display(done, show_count=False, is_raw=False, show=False, is_detailed=True)
        fpn = os.path.join(config.FP_HOME, config.FP_TASKS, "DONE")
        if rend_done:
            if not IO.write(fpn, rend_done, is_json=False, save_bit='w'):
                DISERR("Cannot write DONE")
                return False

        return True
    else:
        DISERR("Cannot read file content")
        return False 

#------ sort -------


#------ display -------
def display(data, 
            show_count=False, 
            is_raw=False, 
            show=True,
            is_detailed=False):
    """lets see if we can itterate thru data as a list"""
    if is_raw:
        raw_tasks = []
        for task in data:
            if show: 
                print("{}=<{}>".format(key, task[key]))
            else:
                raw_tasks.insert(0, task)
        return raw_tasks
    else:
        lines = ""
        count = 1

        # Attention: ZERO TASKS
        if not len(data):
            return lines   # empty, False

        # TASKS have been found
        for task in data:
            # convert epoch to readable format
            epoch = task['created']
            dt = fmt_short_date(epoch)
            dt = "{}{}".format(dt[:2] ,dt[3:])
           
            # name, description, priority, completed
            name = task['name'].upper()
            if task['description']:                   # what about no comment?
                comment = task['description'].lower()
            else:
                comment = ""
            priority = task['priority']
            if task['completed']:
                completed = "Y"
            else:
                completed = "N"

            # build line
            if show_count:
                line = "#{} {} {} {} {}".format(count, dt, priority, completed, name)
            else:
                # detailed with comment OR short line?
                if is_detailed and comment:
                    spaces = " " * 11   # HACK: exactly 11 spaces
                    line = "{} {} {} {}\n{}{}".format(dt, priority, completed, name, spaces, comment)
                else:
                    line = "{} {} {} {}".format(dt, priority, completed, name)
            if lines: lines = "{}\n{}".format(lines, line)
            else: lines = "{}".format(line)
          
            count += 1

            # do we want to print?
            if show: print("{}".format(line.upper()))
            
        return "{}\n".format(lines)

def display_all():
    """display the tasks"""
    tasks = []
    fpn = IO.get_filepathname()
    if fpn: 
        tasks = IO.read_all(fpn)
    else:
        fpn = "No filepath found" 
        DISERR("Cannot read file content")
        return False

    if tasks:
        todo = []
        for task in tasks:
            if not task['completed']:
                #todo.insert(0, task)
                todo.append(task)
        if not display(todo, show_count=True):
            DISERR("Cannot display filepath","<{}>".format(fpn))
        else:
            return True
    else:
        return False
#------ display debug messages ------
def disbug(title, message, priority, is_debug=config.DEBUG):
    """display debug messages with DEBUG=True set"""
    if is_debug:
        if priority == 1:
            print("> ERR : {}".format(title))
        elif priority == 2:
            print("> WARN: {}".format(title))
        elif priority == 3:
            print("> COM: {}".format(title))
        else: # no meta title
            print(">    : {}".format(title))
        return True

        # display message if entered
        if message:
            print("> {}".format(message))
        return True
    else:
        # show nothing
        return False
def DISERR(title, message=""):
    """display debug error message"""
    return disbug(title, message, priority=1)
def DISWARN(title, message=""):
    """display debug warning message"""
    return disbug(title, message, priority=2)
def DISCOM(title, message=""):
    """display debug comment message"""
    return disbug(title, message, priority=3)
#------ display user message ------
def disuser(title, message=""):
    """display direct user message, supply title, optional message"""
    if title:
        msg = "{}".format(title)
        if message:
            print("{}: {}".format(msg, message))
        else:
            print(msg)
    else:
        print("> Err: tools.disuser\ncannot display user message")
        return False
def MSG(title, message=""):
    """display direct user message"""
    return disuser(title, message)
#------ display -------


def main():
    """main entry point for cli"""
    pass


# main entry point for cli
if __name__  == "__main__":
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
