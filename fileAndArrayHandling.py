'''
@title fileAndArrayHandling
@author: Rebecca Coles
Updated on Sep 18, 2017
Created on Sep 13, 2017

fileAndArrayHandling
This module holds a series of functions that I use to convert
images to arrays, and 

Modules:
openAllFITSImagesInDirectory
    This function convertsFITs type images to a 4D array.
'''

# Import #######################################################################################
from numpy import array
from glob import glob
from astropy.io import fits
from tkinter import filedialog
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
        #open image file
        try:
            dirLocation = self._openDir()
        except IOError:
            print('The directory could not be opened, or no directory was selected.')
        filelist = glob(dirLocation + '/*.*')
        fitsImages = [fits.getdata(image) for image in filelist]
        #convert to 4D numpy array
        return array(fitsImages), filelist
    
    def _openDir(self):
        '''
        Create open directory dialogue box
        '''
        return filedialog.askdirectory()
    
    