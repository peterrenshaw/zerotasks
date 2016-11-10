#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#======
# name: tools.py
# date: 2016NOV10
# prog: pr
# desc: zero task
#======


import json
import time
import glob
import time
import datetime


import IO
import config


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
        epoch = get_epoch()
        task['created'] = epoch
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
#------ task ------


#------ sort -------
def sort(data, key, value):
    """sort data by key and value"""
    s = []
    for task in data:
        if key in task:
            if bool(task[key]) == value:
                s.insert(0, task)
            else:
                pass
        else:
            return False
    return s
def sort_done(data):
    """convenience for sort: sort by completed, done"""
    return sort(data, key="completed",value=True)
def sort_todo(data):
    """convenience for sort: sort by completed, todo"""
    return sort(data, key="completed",value=False)
#------ sort -------


#------ display -------
def display(data, show_count=False, is_raw=False, show=True):
    """lets see if we can itterate thru data as a list"""
    if is_raw:
        for task in data:
            for key in task.keys():
                print("{}=<{}>".format(key, task[key]))
        return True
    else:
        lines = ""
        count = 1
        for task in data:
            # convert epoch to readable format
            epoch = task['created']
            dt = fmt_short_date(epoch)
            dt = "{}{}".format(dt[:2] ,dt[3:])
           
            # name, priority, completed
            name = task['name'].capitalize()
            priority = task['priority']
            if task['completed']: completed = "Y"
            else: completed = "N"

            # build line
            if show_count:
                line = "#{} {} {} {} {}".format(count, dt, priority, completed, name)
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
    fpn = IO.get_filepathname()
    if fpn: tasks = IO.read_all(fpn)
    else: DISERR("Cannot read file content","")
        
    todo = []
    for task in tasks:
         if not task['completed']:
             todo.insert(0, task)
    if not display(todo, show_count=True):
        DISERR("Cannot display filepath","<{}>".format(fnp))

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
