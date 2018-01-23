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
################################################################################################

class CCDOpsPlanetMode(object):
    
    def __init__(self):
        '''
        Constructor
        '''
    def readFitsHeader(self, imageArray4D, planetModeBool):
        '''
        Return offsets (in pixels) if an image is taken in CCDOps
        software Planet Mode.
        '''
        ###########################################################################
        ###planetModeBool == True Indicates Subframe
        ###########################################################################
        if planetModeBool == True:
            #read header of first image
            imageArray4D[0]