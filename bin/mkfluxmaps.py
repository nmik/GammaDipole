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

"""This app is amed to prepare the data sample to the dipole analysis.
   Several steps are computed:
       1) Sum in time: the data selection has been done in 1-year-wide time 
          ------------ bins, so now it is possible to merge those bins to get 
                       the total counts and exposures.
       2) Flux map Computation: the flux maps in each micro energy bin is 
          --------------------- obtained by dividing the counts maps for the 
                                relative exposure.
       3) Energy rebinning: at this point you have flux maps in fine energy 
          ----------------- bins. Prior to the anysotropy analysis we want 
                            wider energy bins.
    The output are counts and flux maps in the macro bins (will be located in 
    output/out_count_maps/ and output/out_flux_maps/ respectively).
    ######## ######## ######## ######## ########
      ATT: Foreground subtraction not included!
    ######## ######## ######## ######## ########
"""

import os
import imp
import argparse
import numpy as np
import healpy as hp

from GammaDipole import GD_OUT
from GammaDipole.utils.logging_ import logger, startmsg

__description__ = 'Computes flux maps'

formatter = argparse.ArgumentDefaultsHelpFormatter
PARSER = argparse.ArgumentParser(description=__description__,
                                 formatter_class=formatter)
PARSER.add_argument('-c', '--config', type=str, required=True,
                    help='the input configuration file')
PARSER.add_argument('--nmacroebins', type=int, required=False, default=None,
                    help='number of macro energy bins')

'''___________________________________________________________'''

def get_var_from_file(filename):
    f = open(filename)
    global data
    data = imp.load_source('data', '', f)
    f.close()

def mkfluxmaps(**kwargs): 
    """
    """
    assert(kwargs['config'].endswith('.py'))
    get_var_from_file(kwargs['config'])
    outfiles_ = data.OUTFILES_LIST 
    outlabel = data.OUTLABEL
    microebinfile = data.MICRO_EBINS_FILE
    if not os.path.exists(os.path.join(GD_OUT, 'out_fluxmaps/')):
        logger.info('Creating output folder "out_fluxmaps/"')
        os.makedirs(os.path.join(GD_OUT, 'out_fluxmaps/'))
    if not os.path.exists(os.path.join(GD_OUT, 'out_countmaps/')):
        logger.info('Creating output folder "out_countmaps/"')
        os.makedirs(os.path.join(GD_OUT, 'out_countmaps/'))    
    out_fluxmap_pathname =  os.path.join(GD_OUT, 'out_fluxmaps', 
                              outlabel+'_fluxmaps_microbins.fits')
    out_countmap_pathname =  os.path.join(GD_OUT, 'out_countmaps', 
                              outlabel+'_countmaps_microbins.fits')
    if os.path.exists(out_fluxmap_pathname):
        logger.info('Already existing %s'%out_fluxmap_pathname)
        logger.info('Retriving %s'%out_fluxmap_pathname)
        sum_in_time_flux_maps = hp.read_map(out_fluxmap_pathname, field=None)
    if os.path.exists(out_countmap_pathname):
        logger.info('Already existing %s'%out_countmap_pathname)
        logger.info('Retriving %s'%out_countmap_pathname)
        sum_in_time_counts_maps = hp.read_map(out_countmap_pathname, field=None)
    else:
        sum_in_time_counts_maps = []
        sum_in_time_flux_maps = []
        for i, f in enumerate(outfiles_[1:]):
            all_maps_file_ = open(os.path.join(GD_OUT, f)).readlines()
            counts_maps_file_ = all_maps_file_[2].replace('\n', '')
            exposure_maps_file_ = all_maps_file_[4].replace('\n', '')
            counts_maps = hp.read_map(counts_maps_file_, field=None)
            exposure_maps = hp.read_map(exposure_maps_file_, field=None)
            exposure_maps = hp.pixelfunc.ud_grade(exposure_maps, 
                                        hp.npix2nside(len(counts_maps[0])))
            mean_exp_maps = np.sqrt(exposure_maps[:-1]*exposure_maps[1:])
            if len(sum_in_time_counts_maps) == 0:
                sum_in_time_counts_maps = counts_maps
                sum_in_time_flux_maps = counts_maps/mean_exp_maps
            else:
                sum_in_time_counts_maps = sum_in_time_counts_maps + counts_maps
                sum_in_time_flux_maps = sum_in_time_flux_maps + \
                    counts_maps/mean_exp_maps
        hp.write_map(out_countmap_pathname, sum_in_time_counts_maps)
        logger.info('Creating %s'%(out_countmap_pathname))
        hp.write_map(out_fluxmap_pathname, sum_in_time_flux_maps)
        logger.info('Creating %s'%(out_fluxmap_pathname))

    if kwargs['nmacroebins'] is not None:
        micro_ebins = np.loadtxt(microebinfile)
        micro_emin = micro_ebins[:,0]
        micro_emax = micro_ebins[:,1]
        num_macrobins = kwargs['nmacroebins']
        logger.info('Creating %i maps for each macro energy bins'%num_macrobins)
        macro_ebinning_edges = np.logspace(np.log10(micro_emin[0]),
                                           np.log10(micro_emax[-1]), 
                                           num_macrobins+1)
        macro_indices_edges = np.linspace(0, len(sum_in_time_flux_maps), 
                                              num_macrobins+1).astype(int)
        for i, (emin, emax) in enumerate(zip(macro_ebinning_edges[:-1], 
                                             macro_ebinning_edges[1:])):
            logger.info('%.1f-%.1f GeV'%(emin/1000, emax/1000))
            macro_fluxmap = np.sum(sum_in_time_flux_maps[\
                    macro_indices_edges[i]:macro_indices_edges[i+1]], axis=0)
            macro_fluxmap_name = outlabel+\
                '_fluxmaps_macrobin_%i-%iMeV.fits'%(emin, emax)
            macro_countmap = np.sum(sum_in_time_counts_maps[\
                    macro_indices_edges[i]:macro_indices_edges[i+1]], axis=0)
            macro_countmap_name = outlabel+\
                '_countmaps_macrobin_%i-%iMeV.fits'%(emin, emax)
            hp.write_map(os.path.join(GD_OUT, 'out_fluxmaps', 
                                      macro_fluxmap_name), macro_fluxmap)
            hp.write_map(os.path.join(GD_OUT, 'out_countmaps', 
                                      macro_countmap_name), macro_countmap)
        logger.info('Done.')
            







'''___________________________________________________________'''

if __name__ == '__main__':
    startmsg()
    args = PARSER.parse_args()
    mkfluxmaps(**args.__dict__)
