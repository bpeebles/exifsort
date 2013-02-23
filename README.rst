========
exifsort
========

exifsort.py provides an interface to the core functionality of sorting
(copying by default but move supported) a limited subset of digital picture
and movie files from a single "incoming" directory into multiple dated ones. It
uses the EXIF data for any format supported by pyexiv2 as the date, otherwise
it falls-back to the mtime of the file.

Requirements
============

Not in PyPi
-----------

- `pyexiv2 <http://tilloy.net/dev/pyexiv2/>`_

Supported file formats
======================

- JPG
- NEF
- MOV
- AVI

Example usage
=============

Run::

    $ exifsort.py /media/Nikon/DCIM /media/WD/2013

it will copy all of the files not already in the destination into folders such
as:

- /media/WD/2013/2013-01-20
- /media/WD/2013/2013-01-25

etc.

TODO
====

- Make target directories configurable.

- Support muiltple targets with a single pass (use case: multiple external
  harddrives for backup).

- Switch to `Gexiv2 <http://redmine.yorba.org/projects/gexiv2/wiki>`_ for
  EXIF parsing (or some Pypi supported tool).
