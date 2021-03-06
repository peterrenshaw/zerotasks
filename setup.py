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
# name: zerotask.py
# date: 2016NOV07
# prog: pr
# desc: Setup script. Zero Tasks: read docs/ABOUT.txt
# usag: 
# 
#       # known to work python 3.5
#       $ python3.5 setup.py install
#
#                  OR try
#
#       # experimental python 2.7
#       $ python setup.py install
#======



import os
from setuptools import setup
from setuptools import find_packages


from zerotasks import __url__
from zerotasks import __email__
from zerotasks import __author__
from zerotasks import __license__
from zerotasks import __version__
from zerotasks import __description__


def read(fname):
    """read the specified file into a field, in this case description"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name = "zerotasks",
      version = __version__,
      description = __description__,
      long_description=read('README'),
      license = __license__,
      author = __author__,
      author_email = __email__,
      url = __url__,
      packages = find_packages(),
      keywords = ['realtime','data','local','tasks','todo'],
      zip_safe = True)


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
