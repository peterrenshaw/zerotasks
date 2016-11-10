#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#======
# name: IO.py
# date: 2016NOV10
# prog: pr
# desc: zero task
#======


import os
import glob
import json


import tools
import config


#------ IO -------
def path(task, basepath=config.FP_TASKS):
    """build filepath from task data"""
    if 'name' in task: 
        name = task['name']
        epoch = task['created']

        filename = Filename().getlo(name)
        dir_ymd  = Path().get(epoch)
        filepath = Filepath().get(name)
        fpn = os.path.join(basepath, dir_ymd, filename)

        return fpn
    else:
        return False
def read(filepathname):
    """read a file, return content"""
    data = []
    if os.path.isfile(filepathname):
        try:
            for line in open(filepathname, 'r'):
                task = json.loads(line)
                data.append(task)
        except IOError as e:
            print("error reading file <{}>".format(filepathname))
            return False
        else:
            pass
        if data:
            # multiple or single lines read?
            if len(data) == 1:
                return data[0]    # single line
            else:
                return data       # multiple lines
        else:
            return data
    else:
        return data
def write(filepathname, data, is_json=True, save_bit='w'):
    """write task data to a file"""
    if filepathname:
        fp = os.path.dirname(filepathname)
        if not os.path.isdir(fp):
            os.makedirs(fp)
        try:
            f = open(filepathname, save_bit)
  
            # write as json or raw file
            if is_json:
                task = "{}\n".format(json.dumps(data, 
                                 sort_keys=True,
                                 separators=(',',': ')))
            else:
                task = "{}".format(data)

            f.flush()
            f.write(task)
            f.close()
            #print("written to file {}\n\{}".format(filepathname, data))
        except IOError as e:
            f = None
            print("Error writing file <{}>".format(filepathname))
            return False
        else:
            pass
        return True
def write_tasks(data, fpn=""):
    """write all the tasks to a directory"""
    for task in data:
        if not fpn:
            fpn = path(task)
            
        if not write(fpn, task):
            print("Error cannot save task to <{}>".format(options.output))
            return False
    return True
def read_all(file_list):
    """read all the tasks in given directory"""
    tasks = []
    for fpn in file_list:
        task = read(fpn)
        if task:
            tasks.append(task)
        else:
            return False
    return tasks
def get_filepathname(filepath=config.TASKS_ARCHIVE, ext=config.FN_EXT):
    """extract all filepath names from the archive"""
    paths = []
    fp = "{}/*".format(filepath)
    filepaths = glob.glob(fp)

    # extact filepaths by glob
    for dirs in filepaths:
        d = "{}/*".format(dirs)
        for fp in glob.glob(d):
            if ext:
                # only grab files with extension
                fn = "{}/*.{}".format(fp, ext)
            else:
                # no extension/junk data
                fn = "{}/*".format(fp)

            # extract filenames
            fpn = os.path.join(fp, fn)
            for tfn in glob.glob(fpn):
                 if os.path.isfile(tfn):
                     paths.append(tfn)
    return paths
#------ IO -------




def main():
    """main entry point for cli"""
    pass


# main entry point for cli
if __name__  == "__main__":
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
