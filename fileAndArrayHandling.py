'''
@title fileAndArrayHandling
@author: Rebecca Coles
Updated on Dec 12, 2017
Created on Dec 12, 2017

fileAndArrayHandling
This module holds a series of functions that I use to convert
images to arrays, and converts images to arrays.

Modules:
openAllFITSImagesInDirectory
    This function convertsFITs type images to a 4D array.
openDir
    This function creates an open directory dialogue box and returns the name of the user selected directory.
'''

# Import #######################################################################################
from numpy import array
from glob import glob
from astropy.io import fits
from tkinter import filedialog
import os, errno, re
################################################################################################

class fileAndArrayHandling(object):
    
    def __init__(self):
        '''
        Constructor
        '''
        
    def openAllFITSImagesInDirectory(self):
        '''
        Open multiple images and save them to a numpy array
        '''
        ###########################################################################
        ###Open image file
        ###########################################################################
        try:
            dirLocation = self._openDir()
        except IOError:
            print('The directory could not be opened, or no directory was selected.')
        filelist = glob(dirLocation + '/*.*')
        fitsImages = [fits.getdata(image) for image in filelist]
        
        ###########################################################################
        ###Convert images to 4D numpy array
        ###########################################################################
        return array(fitsImages), filelist
    
    def _openDir(self):
        '''
        Create open directory dialogue box
        '''
        return filedialog.askdirectory()
    
    def createDir(self, fiflabel, metGuidedModeSelf, dirType):
        ###########################################################################
        ###Get log start time
        ###########################################################################
        logTime = re.findall(r'\d+', metGuidedModeSelf.logFile.name)
        logTime = '-'.join(logTime[:])
        
        ###########################################################################
        ###Create Dir
        ###########################################################################
        try:
            os.makedirs(str(fiflabel + "_" + dirType + '_' + logTime))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        return str(fiflabel + "_" + dirType + '_' + logTime)