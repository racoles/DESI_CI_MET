'''
@title metManualMode
@author: Rebecca Coles
Updated on Jan 18, 2018
Created on Jan 18, 2018

metManualMode
Guided mode for DESI CI metrology.

Classes and Modules:

'''

# Import #######################################################################################
import tkinter as tk
from focusCurve import focusCurve
from fileAndArrayHandling import fileAndArrayHandling
from centroidFIF import centroidFIF
import os
import numpy as np
################################################################################################

class metManualMode(tk.Tk):
    consoleLog = []
    logFile = []
        
    def __init__(self, master):
        '''
        Constructor
        '''
        super(metManualMode, self).__init__()
        self.master = master
        master.title("DESI CI Meterology Manual Mode")
        
    def manualFocusCurve(self):
        ###########################################################################
        ###Get FIF Seletion from User
        ###########################################################################
        self._fifSelectionWindow()        
        
        ###########################################################################
        ###Create Dir Using self.fifSection
        ###########################################################################
        faah = fileAndArrayHandling()
        dirName = faah.createDir(self.fifSection, metManualMode, 'Manual_Mode_Focus_Curve')
        
        ###########################################################################
        ###Message user to fill dir (mention label names)
        ###########################################################################
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "Suggested " +  str(self.fifSection) + " manual mode focus curve directory: \n" + str(os.getcwd()) + '\\' + dirName + 
                                      "\nNOTE: the file names will be used to create the Z axis values (distance)\n" +
                                        " so please label the FITS files appropriately\n" +
                                        "(example: 350.fit for the image taken at 350um).")     
        
        ###########################################################################
        ###Get images
        ###########################################################################
        imageArray4D, filelist = faah.openAllFITSImagesInDirectory()
        
        ###########################################################################
        ###Create focus curve
        ########################################################################### 
        fC = focusCurve()       
        xInter = fC.stdFocusCurve(self.fifSection, imageArray4D, filelist)
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "Manual Mode Measured Best focus for " + str(self.fifSection) + " is: " + str(xInter) + "um")
        
        ###########################################################################
        ###Nominal best focus
        ###########################################################################
        nominalZ = self.asphericFocalCurve(fC.fifLocationsCS5[self.fifSection][0], fC.fifLocationsCS5[self.fifSection][1])
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "Nominal Z for " + str(self.fifSection) + " is: " + str(nominalZ) + "um in CS5 coordinates.")
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "Manual Mode Absolute value of (Nominal Z - Measured Best Focus) = " +  str(np.absolute(nominalZ-xInter)) + 'um')
        
    def _setTrueAndExit(self, windowVariable, fifLabel=" ", CCDLabel=" "):
        self.fifSection = fifLabel
        self.CCDSection = CCDLabel
        windowVariable.destroy
        
    def _CCDSelectionWindow(self):
        ###########################################################################
        ###FIF Button Option Window
        ###########################################################################   
        top = tk.Toplevel()
        top.title("CCD Manual Mode")        
        
        #Manual Mode Description
        tk.Label(top, text="Which CCD would you like to measure?").grid(row=0, column=0, columnspan=2, sticky='W')
        
        # NCCD
        NCCD = tk.Button(self, text="NCCD", command=lambda: self._setTrueAndExit(top, CCDLabel="NCCD"))
        NCCD.grid(row=1, column=0)
        
        # WCCD
        WCCD = tk.Button(self, text="WCCD", command=lambda: self._setTrueAndExit(top, CCDLabel="WCCD"))
        WCCD.grid(row=2, column=0)
        
        # SCCD
        SCCD = tk.Button(self, text="SCCD", command=lambda: self._setTrueAndExit(top, CCDLabel="SCCD"))
        SCCD.grid(row=3, column=0)
        
        # ECCD
        ECCD = tk.Button(self, text="ECCD", command=lambda: self._setTrueAndExit(top, CCDLabel="ECCD"))
        ECCD.grid(row=4, column=0)
        
        # CCCD
        CCCD = tk.Button(self, text="CCCD", command=lambda: self._setTrueAndExit(top, CCDLabel="CCCD"))
        CCCD.grid(row=5, column=0)
        
        # Other (will set x=0 y=0)
        other = tk.Button(self, text="Other", command=lambda: self._setTrueAndExit(top, CCDLabel="Other"))
        other.grid(row=6, column=0)  
    
    def _fifSelectionWindow(self):
        ###########################################################################
        ###FIF Button Option Window
        ###########################################################################   
        top = tk.Toplevel()
        top.title("FIF Manual Mode")
        
        #Manual Mode Description
        tk.Label(top, text="Which FIF would you like to measure?").grid(row=0, column=0, columnspan=2, sticky='W')
        
        # RefFIF
        refFIF = tk.Button(self, text="RefFIF", command=lambda: self._setTrueAndExit(top, fifLabel="RefFIF"))
        refFIF.grid(row=1, column=0)
        
        # NFIF
        NFIF = tk.Button(self, text="NFIF", command=lambda: self._setTrueAndExit(top, fifLabel="NFIF"))
        NFIF.grid(row=2, column=0)
        
        # WFIF
        WFIF = tk.Button(self, text="WFIF", command=lambda: self._setTrueAndExit(top, fifLabel="WFIF"))
        WFIF.grid(row=2, column=1)
        
        # SFIF
        SFIF = tk.Button(self, text="SFIF", command=lambda: self._setTrueAndExit(top, fifLabel="SFIF"))
        SFIF.grid(row=2, column=2)
        
        # EFIF
        EFIF = tk.Button(self, text="EFIF", command=lambda: self._setTrueAndExit(top, fifLabel="EFIF"))
        EFIF.grid(row=2, column=3)
        
        # A1
        A1 = tk.Button(self, text="A1", command=lambda: self._setTrueAndExit(top, fifLabel="A1"))
        A1.grid(row=3, column=0)
        
        # A2
        A2 = tk.Button(self, text="A2", command=lambda: self._setTrueAndExit(top, fifLabel="A2"))
        A2.grid(row=3, column=1)
        
        # A3
        A3 = tk.Button(self, text="A3", command=lambda: self._setTrueAndExit(top, fifLabel="A3"))
        A3.grid(row=3, column=2)
        
        # A4
        A4 = tk.Button(self, text="A4", command=lambda: self._setTrueAndExit(top, fifLabel="A4"))
        A4.grid(row=3, column=3)
        
        # B1
        B1 = tk.Button(self, text="B1", command=lambda: self._setTrueAndExit(top, fifLabel="B1"))
        B1.grid(row=4, column=0)
        
        # B2
        B2 = tk.Button(self, text="B2", command=lambda: self._setTrueAndExit(top, fifLabel="B2"))
        B2.grid(row=4, column=1)
        
        # B3
        B3 = tk.Button(self, text="B3", command=lambda: self._setTrueAndExit(top, fifLabel="B3"))
        B3.grid(row=4, column=2)
        
        # B4
        B4 = tk.Button(self, text="B4", command=lambda: self._setTrueAndExit(top, fifLabel="B4"))
        B4.grid(row=4, column=3)
        
        # C1
        C1 = tk.Button(self, text="C1", command=lambda: self._setTrueAndExit(top, fifLabel="C1"))
        C1.grid(row=5, column=0)
        
        # C2
        C2 = tk.Button(self, text="C2", command=lambda: self._setTrueAndExit(top, fifLabel="C2"))
        C2.grid(row=5, column=1)
        
        # C3
        C3 = tk.Button(self, text="C3", command=lambda: self._setTrueAndExit(top, fifLabel="C3"))
        C3.grid(row=5, column=2)
        
        # C4
        C4 = tk.Button(self, text="C4", command=lambda: self._setTrueAndExit(top, fifLabel="C4"))
        C4.grid(row=5, column=3)
        
        # D1
        D1 = tk.Button(self, text="D1", command=lambda: self._setTrueAndExit(top, fifLabel="D1"))
        D1.grid(row=6, column=0)
        
        # D2
        D2 = tk.Button(self, text="D2", command=lambda: self._setTrueAndExit(top, fifLabel="D2"))
        D2.grid(row=6, column=1)
        
        # D3
        D3 = tk.Button(self, text="D3", command=lambda: self._setTrueAndExit(top, fifLabel="D3"))
        D3.grid(row=6, column=2)
        
        # D4
        D4 = tk.Button(self, text="D4", command=lambda: self._setTrueAndExit(top, fifLabel="D4"))
        D4.grid(row=6, column=3)
        
        # CFIF
        CFIF = tk.Button(self, text="CFIF", command=lambda: self._setTrueAndExit(top, fifLabel="CFIF"))
        CFIF.grid(row=7, column=0)
        
        # Other
        other = tk.Button(self, text="Other (will set x=0 y=0)", command=lambda: self._setTrueAndExit(top, fifLabel="Other"))
        other.grid(row=8, column=0)