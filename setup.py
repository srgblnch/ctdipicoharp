# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>
#
# ##### END GPL LICENSE BLOCK #####

__author__ = "Sergi Blanch-Torne"
__copyright__ = "Copyright 2014, CELLS / ALBA Synchrotron"
__license__ = "GPLv3+"

# The version is updated automatically with bumpversion
# Do not update manually
__version = '1.1.0-alpha'

from setuptools import setup, find_packages

setup(
    name="ctdipicoharp300",
    license=__license__, 
    version=__version, 
    author="Sergi Blanch-Torn\'e",
    author_email="sblanch@cells.es",
    packages=find_packages(),
    entry_points={
        'console_scripts': [],
        'gui_scripts': [
            'ctdipicoharp = picoharp.PicoHarpGui:main',
            ]
        },
    options={
        'build_scripts': {
                'executable': '/usr/bin/env python',
                    },
        },
    include_package_data=True,
    description="Graphical User Interface for the Alba's synchrotron "
    "PicoHarp300's Control",
    classifiers=['Development Status :: 5 - Production',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: '
                 'GNU General Public License v3 or later (GPLv3+)',
                 'Programming Language :: Python',
                 'Topic :: Scientific/Engineering :: '
                 ''],
    url="https://github.com/srgblnch/ctdipicoharp",
)
