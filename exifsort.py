#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""exifsort.py

Copy or move digital pictures or movies using EXIF or filesystem
timestamps in a way that was idiosyncratic to the author.

See LICENSE.txt for licensing."""

__version__ = '0.1'

import sys
from glob import iglob
from optparse import OptionParser
import os
import os.path
import datetime
import shutil
import logging as log
import pyexiv2

allowed_extentions = set(['jpg', 'nef', 'mov', 'avi'])

def load_metadata(filename):
    """Return the EXIF metadata for filename.

    This exists as a wrapper around changes in pyexiv2.

    """
    try:
        metadata = pyexiv2.Image(filename)
        metadata.readMetadata()
    except AttributeError:
        metadata = pyexiv2.ImageMetadata(filename)
        metadata.read()
    return metadata

def get_datetime(metadata):
    """Return the datetime object associated with the metadata.

    This exists mostly as a compatilbity layer for different versions of
    pyexiv2--later ones moved it into a .value attribute.

    """
    return getattr(
        metadata['Exif.Image.DateTime'],
        'value',
        metadata['Exif.Image.DateTime']
    )


def sort_dir(src, dest, move=False):
    for filename in iglob(os.path.join(src, "*.[jJnNmMaA][pPeEoOvV][gGfFvViI]")):
        if filename[-3:].lower() not in allowed_extentions:
            continue
        try:
            image = load_metadata(filename)
            when = get_datetime(image)
        except (IOError, KeyError):
            s = os.stat(filename)
            when = datetime.datetime.fromtimestamp(s.st_mtime)
        dest_dir = os.path.join(dest, when.strftime('%Y_%m_%d'))
        dest_file = os.path.join(dest_dir, os.path.basename(filename))
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        if not os.path.exists(dest_file):
            if move:
                log.info("moving from {filename} to {dest_dir}".format(
                    filename=filename, dest_dir=dest_dir
                ))
                shutil.move(filename, dest_file)
            else:
                log.info("copying from {filename} to {dest_dir}".format(
                    filename=filename, dest_dir=dest_dir
                ))
                shutil.copy2(filename, dest_dir)
        else:
            log.warn("{filename} already exists! skipping".format(filename=filename))

def main(argv=None):
    argv = argv or sys.argv
    usage = "usage: %prog [options] src-dir dest-dir"
    parser = OptionParser(usage, version="%prog version {0}".format(__version__),
                          description=(
                              "Copy or move digital pictures or movies using "
                              "EXIF or filesystem timestamps in a way that was "
                              "idiosyncratic to the author."
                          ),
                          )
    parser.add_option("-m", "--move", action="store_true", dest="move",
                      help="move instead of copying")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      help="verbose mode")
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("incorrect number of arguments")

    log_level = log.DEBUG if options.verbose else log.WARNING
    log.basicConfig(format="%(message)s", level=log_level)

    sort_dir(args[0], args[1], move=options.move)

if __name__ == "__main__":
    sys.exit(main())
