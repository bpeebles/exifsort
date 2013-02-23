#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""exifsort.py

Copy or move digital pictures or movies using EXIF or filesystem
timestamps in a way that was idiosyncratic to the author.

Usage: exifsort.py [options] src-dir dest-dir

Options:
  --version   show program's version number and exit
  -h, --help  show this help message and exit
  -m, --move

See LICENSE.txt for licensing."""

__version__ = '0.1'

import sys
from glob import iglob
from optparse import OptionParser
import os
import os.path
import datetime
import shutil
import pyexiv2

allowed_extentions = set(['jpg', 'nef', 'mov', 'avi'])

def sort_dir(src, dest, move=False):
    for file in iglob(os.path.join(src, "*.[jJnNmMaA][pPeEoOvV][gGfFvViI]")):
        if file[-3:].lower() not in allowed_extentions:
            continue
        try:
            image = pyexiv2.Image(file)
            image.readMetadata()
            when = image['Exif.Image.DateTime']
        except IOError:
            s = os.stat(file)
            when = datetime.datetime.fromtimestamp(s.st_mtime)
        dest_dir = os.path.join(dest, when.strftime('%Y_%m_%d'))
        dest_file = os.path.join(dest_dir, os.path.basename(file))
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)
        if not os.path.exists(dest_file):
            if move:
                print "moving from " + file + " to " + dest_dir
                shutil.move(file, dest_file)
            else:
                print "copying from " + file + " to " + dest_dir
                shutil.copy2(file, dest_dir)
        else:
            print file + " already exists! skipping"

def main(argv=None):
    if argv is None:
        argv = sys.argv
    usage = "usage: %prog [options] src-dir dest-dir"
    parser = OptionParser(usage, version="%prog version {0}".format(__version__))
    parser.add_option("-m", "--move", action="store_true", dest="move")
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("incorrect number of arguments")
    sort_dir(args[0], args[1], move=options.move)

if __name__ == "__main__":
    sys.exit(main())
