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
import tkinter as tk
import time
from focusCurve import focusCurve
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
    
    def createDir(self, fiflabel, metModeSelf, dirType):
        ###########################################################################
        ###Get log start time
        ###########################################################################
        logTime = re.findall(r'\d+', metModeSelf.logFile.name)
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
    
    def pageLogging(self, cLog, lFile, logText, doubleSpaceWithTime = True):
        '''
        Send text to console and log file.
        
        Using ISO 8601 for date-time
        '''
        ###########################################################################
        ###Current Time
        ###########################################################################
        currentTime = time.strftime("%Y-%m-%dT%H%M%SZ")
        
        ###########################################################################
        ###Send text to console
        ###########################################################################
        if doubleSpaceWithTime == True:
            cLog.configure(state="normal")
            cLog.insert(tk.END, currentTime + ': ' + str(logText) + '\n\n')
            cLog.configure(state="disable")
        else:
            cLog.configure(state="normal")
            cLog.insert(tk.END, str(logText) + '\n')
            cLog.configure(state="disable")
        
        ###########################################################################
        ###Send text to log file
        ###########################################################################
        lFile.write(currentTime + ': ' + str(logText) + '\n')
        lFile.flush()
        
    def printDictToFile(self, dict, title ,consoleLog, logFile, printNominalDicts = False):
        '''
        Output dictionary data to file.
        '''
        ###########################################################################
        ###If printNominalDicts == True print Nominal Dict
        ########################################################################### 
        self.pageLogging(consoleLog, logFile, '\n' + str(title), doubleSpaceWithTime = False)
        if printNominalDicts == True:
            fC = focusCurve()
            for key,value in dict.items():
                self.pageLogging(consoleLog, logFile, str(key) + ": " + str(value).strip('()') + ', ' +
                                  str(fC.asphericFocalCurve(dict[str(key)][0], dict[str(key)][1])), doubleSpaceWithTime = False)