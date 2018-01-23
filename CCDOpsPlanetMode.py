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
from astropy.io import fits
from fileAndArrayHandling import fileAndArrayHandling
################################################################################################

class CCDOpsPlanetMode(object):
    
    def __init__(self):
        '''
        Constructor
        '''
    def readFitsHeader(self, imageArray4D, filelist, planetModeBool, consoleLog, logFile):
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
            faah = fileAndArrayHandling()
            faah.pageLogging(consoleLog, logFile, 
                        "You have indicated that you WILL be using CCDOps Planet Mode")
            
            #image sizes check and warning
            for ii in range(imageArray4D.shape[0]):
                if imageArray4D[ii].shape != imageArray4D[ii-1].shape:
                    faah.pageLogging(consoleLog, logFile, 
                        "Image " + str(filelist[ii]) + " is not the same dimensions as the other images."
                         + ' are you sure that all images in the directory were taken in planet mode?'
                         + 'Not having all images be the same dimension WILL provoke centroid inaccuracies.')
            #Read header of first image
            hdul = fits.open(filelist[0])
            
            #Find X and Y bin sizes
            xBin = hdul[0].header['XBINNING']
            yBin = hdul[0].header['YBINNING']
            
            #Find X and Y offsets
            xOffset = hdul[0].header['XORGSUBF']
            yOffset = hdul[0].header['YORGSUBF']
            
            #Convert from units of "bins" to pixels
            xOffset = int(xOffset)/int(xBin)
            yOffset = int(yOffset)/int(yBin)
            
            #log offsets
            faah.pageLogging(consoleLog, logFile, 
                        "CCDOps Planet Mode Offsets; (x,y) position of upper-left pixel relative to whole frame: (" 
                        + str(xOffset) + "," + str(yOffset) + ")")
            
        else:
            #Message about using planet mode
            faah.pageLogging(consoleLog, logFile, 
                        "You have indicated that you will NOT be using CCDOps Planet Mode")