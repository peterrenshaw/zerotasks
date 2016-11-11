#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#======
# name: tools.py
# date: 2016NOV10
# prog: pr
# desc: zero task
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
        DISERR("Cannot readbuild filepathe name")
        return False

    # sort tasks, write task lists
    # TASKS is json list in raw format
    fpn = os.path.join(config.FP_HOME, config.FP_TASKS, "TASKS")
    if not IO.write(fpn, tasks):
        DISSERR("Cannot write TASKS")

    # throttle number of tasks allowed
    if is_taskcount_reached(task_limit):
        task = new_task(name, comment, priority)
        if task:
            fp = IO.get_path(task)
            fpn = os.path.join(config.FP_HOME, config.FP_TASKS, fp)
            if IO.write(fpn, task):
                return True
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
    count = 1
    for task in tasks:
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
    if number:
         tasks = []
         fpn = IO.get_filepathname()
         if fpn: tasks = sort_todo(IO.read_all(fpn))
         else: DISERR("Cannot read file content")

         count = 1
         for task in tasks:
             if count == int(number):
                  if key == 'start':
                      task['start'] = get_epoch()
                  elif key == 'end':
                      task['end'] = get_epoch()
                  elif key == 'completed':
                      task['completed'] = True
                  else:
                      pass

                  print("num={} key={} task={}".format(number, key, task[key], task))

                  fpn = IO.get_path(task)
                  DISWARN("tools.update_task","fpn <{}>".format(fpn))
                  DISWARN("tools.update_task","key <{}>".format(key))
                  DISWARN("tools.update_task","task <{}>".format(task))
                  if not IO.write(fpn, task):
                      DISERR("Cannot write task")
                      break

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
        if key in task:
            if bool(task[key]) == value:
                if key:
                    if value:
                        # add task to top of list
                        s.insert(0, task)
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
        tasks = IO.read_all(fpn)

        # TASKS write
        fpn = os.path.join(config.FP_HOME, config.FP_TASKS, "TASKS")
        rend_task = display(tasks, show_count=False, is_raw=False, show=False, is_detailed=True)
        if not IO.write(fpn, rend_task, is_json=False, save_bit='w'):
            DISERR("Cannot write TASKS")
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
        rend_done = display(done, show_count=False, is_raw=False, show=False)
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
        for task in data:
            for key in task.keys():
                print("{}=<{}>".format(key, task[key]))
        return True
    else:
        lines = ""
        count = 1

        # Attention: ZERO TASKS
        if not len(data):
            return False

        # TASKS have been found
        for task in data:
            # convert epoch to readable format
            epoch = task['created']
            dt = fmt_short_date(epoch)
            dt = "{}{}".format(dt[:2] ,dt[3:])
           
            # name, description, priority, completed
            name = task['name'].upper()
            comment = task['description'].capitalize()
            priority = task['priority']
            if task['completed']: completed = "Y"
            else: completed = "N"

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
            
        if show:
            return True
        else:
            return "{}\n".format(lines)

def display_all():
    """display the tasks"""
    tasks = []
    fpn = IO.get_filepathname()
    if fpn: tasks = IO.read_all(fpn)
    else: DISERR("Cannot read file content")
        
    if tasks:
        todo = []
        for task in tasks:
            if not task['completed']:
                todo.insert(0, task)
        if not display(todo, show_count=True):
            DISERR("Cannot display filepath","<{}>".format(fnp))
    else:
        return False
def disbug(title, message, priority, is_debug=config.DEBUG):
    if is_debug:
        if priority == 1:
            print("> ERR : {}".format(title))
        elif priority == 2:
            print("> WARN: {}".format(title))
        else:
            print("> COM: {}".format(title))
        if message:
            print("> {}".format(message))
        return True
    else:
        return False
def DISERR(title, message=""):
    """display error message"""
    return disbug(title, message, priority=1)
def DISWARN(title, message=""):
    """display warning message"""
    return disbug(title, message, priority=2)
def DISCOM(title, message=""):
    """display comment message"""
    return disbug(title, message, priority=3)
#------ display -------


def main():
    """main entry point for cli"""
    pass


# main entry point for cli
if __name__  == "__main__":
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
