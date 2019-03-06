#!/usr/bin/env python                                                          #
#                                                                              #
# Autor: Michela Negro, University of Torino.                                  #
#                                                                              #
# This program is free software; you can redistribute it and/or modify         #
# it under the terms of the GNU GengReral Public License as published by       #
# the Free Software Foundation; either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
#------------------------------------------------------------------------------#

"""GammaDipole: Framework for Gamma-ray Dipole Analysis
"""

import os

PACKAGE_NAME = 'GammaDipole'

"""Basic folder structure of the package.
"""
GD_ROOT = os.path.abspath(os.path.dirname(__file__))
GD_BIN = os.path.join(GD_ROOT, 'bin')
GD_CONFIG = os.path.join(GD_ROOT, 'config')
GD_UTILS = os.path.join(GD_ROOT, 'utils')


""" This is where we put the actual (FT1 and FT2) data sets.  
"""

from GammaDipole.utils.logging_ import logger
try:
    FT_DATA_FOLDER = os.environ['P8_DATA']
    logger.info('Base data folder set to $P8_DATA = %s...' % FT_DATA_FOLDER)
except KeyError:
    FT_DATA_FOLDER = '/data1/data/P8R3'
    logger.info('$P8_DATA not set, base data folder set to %s...' %\
                FT_DATA_FOLDER)

""" This is the output directory.
"""
try:
    GD_OUT = os.environ['GD_OUT']
    GD_OUT_FIG = os.environ['GD_OUT_FIG']
except:
    GD_OUT = os.path.join(GD_ROOT, 'output')
    GD_OUT_FIG = os.path.join(GD_ROOT, 'output/figures')

if __name__ == '__main__':
    print('GD_ROOT: %s' % GD_ROOT)
