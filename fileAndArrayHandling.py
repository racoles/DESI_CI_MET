'''
@title fileAndArrayHandling
@author: Rebecca Coles
Updated on Feb 7, 2017
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
import os, errno, re, math
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
        if doubleSpaceWithTime == True:
            lFile.write(str(logText) + '\n')
            lFile.flush()            
        else:
            lFile.write(currentTime + ': ' + str(logText) + '\n')
            lFile.flush()
        
    def printDictToFile(self, dict, title ,consoleLog, logFile, printNominalDicts = False):
        '''
        Output dictionary data to file.
        '''
        ###########################################################################
        ###If printNominalDicts == True print Nominal Dict .strip('()')
        ########################################################################### 
        self.pageLogging(consoleLog, logFile, '\n' + str(title), doubleSpaceWithTime = False)
        if printNominalDicts == True:
            fC = focusCurve()
            for key,value in dict.items():
                self.pageLogging(consoleLog, logFile, str(key) + ": " + str(self.to_precision(value[0], 6)) + ' ' + str(self.to_precision(value[1], 6)) + ', ' +
                                  str(self.to_precision(fC.asphericFocalCurve(dict[str(key)][0], dict[str(key)][1]), 6)), doubleSpaceWithTime = False)
                
    def to_precision(self, x, p):
        '''
        returns a string representation of x formatted with a precision of p
    
        Based on the webkit javascript implementation taken from here:
        https://code.google.com/p/webkit-mirror/source/browse/JavaScriptCore/kjs/number_object.cpp
        
        Converted by Randle Taylor
        http://randlet.com/blog/python-significant-figures-format/
        '''
        x = float(x)
        if x == 0.:
            return "0." + "0"*(p-1)
        out = []
    
        if x < 0:
            out.append("-")
            x = -x
    
        e = int(math.log10(x))
        tens = math.pow(10, e - p + 1)
        n = math.floor(x/tens)
    
        if n < math.pow(10, p - 1):
            e = e -1
            tens = math.pow(10, e - p+1)
            n = math.floor(x / tens)
    
        if abs((n + 1.) * tens - x) <= abs(n * tens -x):
            n = n + 1
    
        if n >= math.pow(10,p):
            n = n / 10.
            e = e + 1
    
        m = "%.*g" % (p, n)
    
        if e < -2 or e >= p:
            out.append(m[0])
            if p > 1:
                out.append(".")
                out.extend(m[1:p])
            out.append('e')
            if e > 0:
                out.append("+")
            out.append(str(e))
        elif e == (p -1):
            out.append(m)
        elif e >= 0:
            out.append(m[:e+1])
            if e+1 < len(m):
                out.append(".")
                out.extend(m[e+1:])
        else:
            out.append("0.")
            out.extend(["0"]*-(e+1))
            out.append(m)
    
        return "".join(out)
    
    def decNonZeroRound(self, n):
        '''
        Round a decimal to the first non-zero value
        '''
        if n == 0:
            return 0
        sgn = -1 if n < 0 else 1
        scale = int(-math.floor(math.log10(abs(n))))
        if scale <= 0:
            scale = 1
            factor = 10**scale
        return sgn*math.floor(abs(n)*factor)/factor