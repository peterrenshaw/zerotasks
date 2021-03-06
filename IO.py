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
# name: IO.py
# date: 2016NOV10
# prog: pr
# desc: Zero Tasks: read docs/ABOUT.txt
#======


import os
import glob
import json
import time
import datetime


import tools
import config


#======
# name: Filename
# date: 2016NOV02
# prog: pr
# desc: build reliable filenames with/without extensions
#       takes into account spaces
#======
class Filename(object):
    def __init__(self):
        """initialise filename object attributes"""
        self.file_name = ""
        self.ext = ""
    def build(self, name, ext, is_caseupper):
        """build a filename given the name and/not extension"""
        if name:
            # check spaces, reject if spaces
            name_clean = tools.clean_str(name)
            if name_clean:
                # has ext?
                if ext:
                    self.ext = ext
                    filename = "{}.{}".format(name_clean, self.ext)
                else:
                    filename = name_clean

                # change case, does not preserve
                if is_caseupper: # everything uppercase
                    self.file_name = filename.upper()
                else:            # everything lowercase
                    self.file_name = filename.lower()

                return True
            else:
                return False
        else:
            return False
    def getup(self, name, ext=""):
        """filename in uppe rcase"""
        return self.get(name, ext, True)
    def getlo(self, name, ext=config.FN_EXT):
        """filename in lower case"""
        return self.get(name, ext, False)
    def get(self, name, ext, is_caseupper):
        """return a filename or False"""
        if self.build(name, ext, is_caseupper):
            return self.file_name
        else:
            return False


#------
# name: Path
# date: 2016SEP24
# prog: pr
# desc: given an epoch, calculate the filepaths 
#------
class Path(object):
    def __init__(self, rel_path=""):
        """initialise Path object"""
        self.epoch = None
        self.rp = rel_path
        self.fp = ""
    def relpath(self):
        """find relative filepath"""
        return self.rp
    def filepath(self):
        """find absolute filepath"""
        return self.fp
    def build(self, epoch):
        """from supplied epoch, build file paths"""
        self.epoch = epoch
        if self.epoch:
            year = self.fmt_epoch("%Y")
            month = self.fmt_epoch("%b")
            day = self.fmt_epoch("%d")
            fp = os.path.join(self.rp, year, month, day)
            self.fp = "{}".format(fp.upper())

            return True
        else:
            return False
    def get(self, epoch):
        """get the filepath OR F"""
        if self.build(epoch):
            return self.fp
        else:
            return ""
    #------ tool ------
    def fmt_epoch(self, strf):
        """given an epoch, convert to strformat string supplied"""
        t = datetime.datetime.fromtimestamp(self.epoch)
        value = t.strftime(strf)
        return value
    #------ end tool -----


#======
# name: Filepath
# date: 2016NOV02
# prog: pr
# desc: filepath object to create and manipulate valid paths
#======
class Filepath(object):
    def __init__(self,
                 fp_home=config.FP_HOME,
                 base_path=config.FP_TASKS):
        """init Filepath obj attributes"""
        self.fp_home = fp_home
        self.rp = ""
        self.p  = ""
        self.fp = ""
        self.bp = base_path # basepath
    def build(self, path=""):
        """create a filepath from home and relative filepaths"""
        if path:    # update relative path
            self.p = path
            tools.DISCOM("IO.Filepath.build", \
                         "fp_home=<{}>".format(self.fp_home)) 
            tools.DISCOM("IO.Filepath.build", \
                         "bp=<{}>".format(self.bp)) 
            tools.DISCOM("IO.Filepath.build", \
                         "rp=<{}>".format(self.rp))
            tools.DISCOM("IO.Filepath.build", \
                         "path=<{}>".format(path))  
            self.fp = os.path.join(self.fp_home, self.bp, self.rp, path)
        else:           # use existing relative path
            self.fp = os.path.join(self.fp_home, self.bp, self.rp)
        return True
    def get(self, path, no_test=True):
        """build then return the filepath"""
        if self.build(path):
            # use this to avoid test of ^new^ file if
            # file passed in - is this a good idea?
            if no_test:
                return self.fp
            elif self.is_valid():
                return self.fp
            else:
                return False
        else: return False
    def is_valid(self):
        """check validity of current filepath"""
        if os.path.isdir(self.fp): return True
        else: return False


#------ IO -------
def get_path(task, basepath=config.TASKS_ARCHIVE):
    """build filepath from task data"""
    if 'name' in task: 
        name = task['name']
        epoch = task['created']

        fp = Filepath().get(basepath)
        ymd  = Path().get(epoch)
        fn = Filename().getlo(name)
        fpn = os.path.join(fp, ymd, fn)
        tools.DISCOM("fn = {}".format(fn))
        tools.DISCOM("ymd = {}".format(ymd))
        tools.DISCOM("fp = {}".format(fp))
        tools.DISCOM("fpn = {}".format(fpn))

        return fpn
    else:
        return False
def read(filepathname):
    """read a file, return content"""
    data = []
    tools.DISCOM("IO.read","fpn=<{}>".format(filepathname))
    if os.path.isfile(filepathname):
        try:
            for line in open(filepathname, 'r'):
                tools.DISCOM("IO.read","line=<{}>".format(line))
                task = json.loads(line)
                data.append(task)
                #data.insert(0, task)
        except IOError as e:
            tools.DISERR("IO.read", "error reading file <{}>".format(filepathname))
            return data
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
            tools.DISCOM("IO.write","mkdir <{}>".format(fp))
            os.makedirs(fp)
        try:
            f = open(filepathname, save_bit)
            tools.DISCOM("IO.write","open <{}> to <{}>".format(filepathname, save_bit)) 

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
            tools.DISCOM("IO.write", "written to file {}\n\{}".format(filepathname, data))
        except IOError as e:
            f = None
            tools.DISERR("IO.write", "Error writing file <{}>".format(filepathname))
            return False
        else:
            pass
        return True
def write_tasks(fpn, data, save_bit='a'):
    """write all the tasks to a directory"""
    for task in data:
        if not fpn:
            fpn = path(task)

        tools.DISCOM("IO.write_tasks","fpn={}".format(fpn)) 
        tools.DISCOM("IO.write_tasks","task={}".format(task)) 
        if not write(fpn, task, is_json=True, save_bit=save_bit):
            tools.DISERR("IO.write_tasks", "Error cannot save task to <{}>".format(options.output))
            return False

    return True
def read_all(file_list):
    """read all the tasks in given directory"""
    tasks = []
    for fpn in file_list:
        task = read(fpn)
        if task:
            # task sent to top allowing
            # sort by date created
            tasks.append(task)
        else:
            return tasks
    return tasks
def get_filepathname(filepath=config.TASKS_ARCHIVE, ext=config.FN_EXT):
    """extract all filepath names from the archive"""
    paths = []
    fp = "{}/*".format(filepath)
    filepaths = glob.glob(fp)

    tools.DISCOM("IO.get_filepathname","fp=<{}>".format(fp))
    tools.DISCOM("IO.get_filepathname","filepaths=<{}>".format(filepaths))


    #-------
    # explanation:
    #
    # the code below looks into the TASKS_ARCHIVE directory
    # and looks for multiple YYYY/ directories for child months
    # and days, slurping up all the files with the FN_EXT extension
    # stored as a list of filenamepaths.
    # 
    #     TASKS_ARCHIVE/
    #         2016/
    #             DEC/
    #                 09/
    #                     zt-fix-forth-field.tsk
    #         YYYY/
    #             MMM/
    #                 NN/
    #                     zt-filename.FN_EXT
    #-------

    # extract filepaths by glob
    for dirs in filepaths:
        # TASKS_ARCHIVE dir
        directories = "{}/*".format(dirs)
        # YYYY dirs
        for d in glob.glob(directories):
            # filenames
            for fp in glob.glob("{}/*".format(d)):
                if ext:
                    # only grab files with extension
                    fn = "{}/*.{}".format(fp, ext)
                else:
                    # no extension/junk data
                    fn = "{}/*".format(fp)

                tools.DISCOM("IO.get_filepathname","fn=<{}>".format(fn))

                # extract filenames
                fpn = os.path.join(fp, fn)
                tools.DISCOM("IO.get_filepathname","fpn=<{}>".format(fpn))
                for tfn in glob.glob(fpn):
                    if os.path.isfile(tfn):
                        paths.insert(0, tfn)

    tools.DISCOM("IO.get_filepathname","paths=<{}>".format(paths))
    return paths
#------ IO -------




def main():
    """main entry point for cli"""
    pass


# main entry point for cli
if __name__  == "__main__":
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
