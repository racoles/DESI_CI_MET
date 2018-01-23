'''
@title CCDOpsPlanetMode
@author: Rebecca Coles
Updated on Jan 22, 2018
Created on Jan 22, 2018

CCDOpsPlanetMode
This module holds a series of functions that I use find offsets when using the
CCDOps software in "planet" imaging mode.

Modules:
'''

# Import #######################################################################################
import numpy as np
from astropy.io import fits
from binhex import hexbin
################################################################################################

class CCDOpsPlanetMode(object):
    
    def __init__(self):
        '''
        Constructor
        '''
    def readFitsHeader(self, imageArray4D, filelist, planetModeBool):
        '''
        Return offsets (in pixels) if an image is taken in CCDOps
        software Planet Mode.
        
        Note from SBFITSEXT Version 1.0:
        XORGSUBF: Sub frame X position of upper-left pixel relative to whole frame in binned pixel units
        YORGSUBF: Sub frame Y position of upper-left pixel relative to whole frame in binned pixel units
        '''
        ###########################################################################
        ###planetModeBool == True Indicates Subframe
        ###########################################################################
        if planetModeBool == True:
            #Message about using planet mode
            #image sizes check and warning
                #imageArray4D[0]
            #Read header of first image
            hdul = fits.open(filelist[0])
            #Find X and Y bin sizes
            xBin = hdul[0].header['XBINNING']
            yBin = hdul[0].header['YBINNING']
            #Find X and Y offsets
            xOffset = hdul[0].header['XORGSUBF']
            yOffset = hdul[0].header['YORGSUBF']
        else:
            #Message about using planet mode
            #image sizes check and warning
                #imageArray4D[0]