#!/usr/bin/env python                                                          #
#                                                                              #
# Autor: Michela Negro, University of Torino.                                  #
# On behalf of the Fermi-LAT Collaboration.                                    #
#                                                                              #
# This program is free software; you can redistribute it and/or modify         #
# it under the terms of the GNU General Public License as published by         #
# the Free Software Foundation; either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
#------------------------------------------------------------------------------#

"""Configuration file for bin/mkfuxmaps.py app.
   Instructions:
   ------------
       >>> python bin/mkfluxmaps.py -c config/config_fluxmaps.py
"""

OUTFILES_LIST = ['1yr_data_outfiles.txt', '2yr_data_outfiles.txt',
                 '3yr_data_outfiles.txt', '4yr_data_outfiles.txt',
                 '5yr_data_outfiles.txt', '6yr_data_outfiles.txt',
                 '7yr_data_outfiles.txt', '8yr_data_outfiles.txt',
                 '9yr_data_outfiles.txt'
                ]

MICRO_EBINS_FILE = 'output/ebinning.txt'
OUTLABEL = 'Allyrs_SV_FB'
