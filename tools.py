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
import datetime


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
def fmt_short_date(epoch, cust_strf=DDMMYY):
    """convenience for fmt_epoch"""
    return fmt_epoch(epoch, strf=cust_strf)
#------- datetime -------


def main():
    """main entry point for cli"""
    pass


# main entry point for cli
if __name__  == "__main__":
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
