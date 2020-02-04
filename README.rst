Pymeshio
========


`pymeshio` is a package for 3d model io.
create for blender import/expoert plugin backend.


Requirements
------------
* Python 3.4

Features
--------
* read       Metasequioa mqo format
* read/write MikuMikuDance pmd format
* read/write MikuMikuDance pmx format
* read       MikuMikuDance vmd format
* read       MikuMikuDance vpd format
* convert    MikuMikuDance pmd format to MikuMikuDance pmx format


Install as python module
------------------------
from internet
~~~~~~~~~~~~~
::

   $ pip install git+https://github.com/zhouhang95/pymeshio

from archive
~~~~~~~~~~~~
::

   $ unzip pymeshio-x.x.x.zip
   $ cd pymeshio-x.x.x
   $ python setup.py install

Usage as python module
~~~~~~~~~~~~~~~~~~~~~~

::

    >>> import pymeshio.pmd.reader
    >>> m=pymeshio.pmd.reader.read_from_file('resources/初音ミクVer2.pmd')
    >>> print(m)
    <pmd-1, "初音ミク" vertex: 12354, face: 68883, material: 17, bone: 140 ik: 7, skin: 31>
    >>> import pymeshio.converter
    >>> pmx_model=pymeshio.converter.pmd_to_pmx(m)
    >>> print(pmx_model)
    <pmx-2.0 "Miku Hatsune" 12354vertices>
    >>> import pymeshio.pmx.writer
    >>> pymeshio.pmx.writer.write_to_file(pmx_model, "out.pmx")
    True
    >>> import pymeshio.vmd.reader
    >>> pymeshio.vmd.reader.read_from_file('resources/motion.vmd')
    <VMDLoader model: "初音ミク", motion: 16897, shape: 997, camera: 0, light: 0>


