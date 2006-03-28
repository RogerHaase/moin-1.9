# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Fullsearch Index Script Package

    @copyright: 2006 by Thomas Waldmann
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.util import pysupport

# create a list of extension scripts from the subpackage directory
index_scripts = pysupport.getPackageModules(__file__)
modules = index_scripts
