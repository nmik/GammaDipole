# GammaDipole
Framework for Gamma-ray Dipole Analysis

To use this package:
--------------------

0) - Install Fermi Science Tools
   - Install python 3
   - Install HEASARC FTools
   - Install matplotlib
   - Install healpy
   - Install PolSpice

1) Set the environment:
  
    - export PYTHONPATH=:/path/to/this/package/${PYTHONPATH}
    - export PATH=/path/to/this/package/GammaDipole/bin:${PATH}
    - export P8_DATA=/path/to/data_files

2) Change the directory where the data files are stored in __init__.py.

   - line 35:
   	FT_DATA_FOLDER = '/path/to/data_files'

   - In this directory should there be the following folders:
   
   	- photon/      -> where FT1 files are stored
	- spacecraft/  -> where FT2 files are stored
	- output/      -> where ST outputs will be stored


How to run the analysis:
------------------------
This will show all the possible settings of a given function in bin/ :

     python bin/ANYFUNCTION.py --h 
