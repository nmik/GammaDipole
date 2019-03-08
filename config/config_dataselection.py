#!/usr/bin/env python                                                          #
#                                                                              #
# Autor: Michela Negro, University of Torino.                                  #
# On behalf of the Fermi-LAT Collaboration.                                    #
#                                                                              #
# This program is free software; you can redistribute it and/or modify         #
# it under the terms of the GNU GengReral Public License as published by       #
# the Free Software Foundation; either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
#------------------------------------------------------------------------------#


""" Example of configuration file for bin/mkdataselection.py.

    To run the analysis just do: 
    >>> python bin/mkdataselection.py -c config/config_dataselection.py
    To see the option availabe for bin/mkdataselection.py type:
    >>> python bin/mkdataselection.py -h
"""


import os
import numpy as np
from GRATools import FT_DATA_FOLDER
from GRATools.utils.ScienceTools_ import gtbindef


OUT_LABEL = '1yr_data'

#start and stop week number to be selected in FT1 and FT2 files
START_WEEK = 9 
STOP_WEEK = 60

# minumum and maximum energy and energy bin number to generate fits file
E_MIN = 100
E_MAX = 2000000
E_NBINS = 120
EBINNING_ARRAY = np.logspace(np.log10(E_MIN), np.log10(E_MAX), E_NBINS)
EBINNING_FILE = ebindef(EBINNING_ARRAY, file_name='ebinning.txt')

# other settings
ZMAX = 90
FILTER_CUT='DATA_QUAL==1&&LAT_CONFIG==1&&LAT_MODE==5&&IN_SAA!=T'+\
               '&&((ABS(ROCK_ANGLE)<52))'

GTSELECT_DICT = {'infile': 'DEFAULT',
                 'emin': 30,
                 'emax': 300000,
                 'zmax': ZMAX,
                 'evclass': 128,
                 'evtype': 3,
                 'outfile': 'DEFAULT',
                 'chatter': 4,
                 'clobber': 'no'}

GTMKTIME_DICT = {'evfile': 'DEFAULT',
                 'scfile': 'DEFAULT',
                 'filter': FILTER_CUT,
                 'roicut': 'no',
                 'outfile': 'DEFAULT',
                 'clobber': 'no'}

GTBIN_DICT = {'evfile': 'DEFAULT',
              'algorithm': 'HEALPIX',
              'scfile': 'DEFAULT',
              'hpx_ordering_scheme': 'RING',
              'hpx_order': 6,
              'coordsys': 'GAL',                                  
              'hpx_ebin': 'yes',
              'ebinalg': 'FILE',
              'ebinfile': EBINNING_FILE,
              'outfile': 'DEFAULT',
              'clobber': 'no'}

GTLTCUBE_DICT = {'evfile': 'DEFAULT',
                 'scfile': 'DEFAULT',
                 'zmax': ZMAX,                     
                 'dcostheta': 0.025,
                 'binsz': 1,
                 'outfile': os.path.join(FT_DATA_FOLDER,
                    'output/output_gtltcube/1yrP302S_filtered_gti_ltcube.fits'),
                 'chatter': 4,
                 'clobber': 'no'}

GTEXPCUBE2_DICT = {'infile': os.path.join(FT_DATA_FOLDER,
                    'output/output_gtltcube/1yrP302S_filtered_gti_ltcube.fits'),
                   'cmap': 'DEFAULT',
                   'irfs': 'CALDB',
                   'outfile': 'DEFAULT',
                   'clobber': 'no'}
