'''
@title metManualMode
@author: Rebecca Coles
Updated on Jan 22, 2018
Created on Jan 18, 2018

metManualMode
Guided mode for DESI CI metrology.

Classes and Modules:

'''

# Import #######################################################################################
import tkinter as tk
from focusCurve import focusCurve
from fileAndArrayHandling import fileAndArrayHandling
import os
import numpy as np
################################################################################################

class metManualMode(tk.Tk):
    consoleLog = []
    logFile = []
    CCDSelection = " "
    fifSelection = " "
    trianglePointSelection = " "
        
    def __init__(self, master):
        '''
        Constructor
        '''
        super(metManualMode, self).__init__()
        self.master = master
        master.title("DESI CI Meterology Manual Mode")
        
    def manualFIFFocusCurve(self):
        ###########################################################################
        ###Get FIF Seletion from User
        ###########################################################################
        self._fifSelectionWindow()        
        
        ###########################################################################
        ###Create Dir Using self.fifSelection
        ###########################################################################
        faah = fileAndArrayHandling()
        dirName = faah.createDir(self.fifSelection, self, 'Manual_Mode_FIF_Focus_Curve')
        
        ###########################################################################
        ###Message user to fill dir (mention label names)
        ###########################################################################
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "Suggested " +  str(self.fifSelection) + " manual mode focus curve directory: \n" + str(os.getcwd()) + '\\' + dirName + 
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
        xInter = fC.stdFocusCurve(self.fifSelection, imageArray4D, filelist)
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "FIF Manual Mode Measured Best focus for " + str(self.fifSelection) + " is: " + str(xInter) + "um")
        
        ###########################################################################
        ###Nominal best focus
        ###########################################################################
        nominalZ = fC.asphericFocalCurve(fC.fifLocationsCS5[self.fifSelection][0], fC.fifLocationsCS5[self.fifSelection][1])
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "Nominal Z for " + str(self.fifSelection) + " is: " + str(nominalZ) + "um in CS5 coordinates.")
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "FIF Manual Mode Absolute value of (Nominal Z - Measured Best Focus) = " +  str(np.absolute(nominalZ-xInter)) + 'um')
        
    def manualCCDFocusCurve(self):
        ###########################################################################
        ###Get CCD Seletion from User
        ###########################################################################
        self._CCDSelectionWindow() 
        self._trianglePointSelectionWindow()
        
        ###########################################################################
        ###Create Dir Using self.CCDSelection
        ###########################################################################
        faah = fileAndArrayHandling()
        dirName = faah.createDir(str(self.CCDSelection + '_' + self.trianglePointSelection), self, 'Manual_Mode_CCD_Focus_Curve')
        
        ###########################################################################
        ###Message user to fill dir (mention label names)
        ###########################################################################
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "Suggested " +  str(self.CCDSelection + ' ' + self.trianglePointSelection) + 
                                      " manual mode focus curve directory: \n" + str(os.getcwd()) + '\\' + dirName + 
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
        xInter = fC.stdFocusCurve(self.CCDSelection, imageArray4D, filelist)
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "CCD Manual Mode Measured Best focus for " + str(self.CCDSelection + ' ' + self.trianglePointSelection) + " is: " + str(xInter) + "um")
        
        ###########################################################################
        ###Nominal best focus
        ###########################################################################
        nominalZ = fC.asphericFocalCurve(fC.CCDLocationsCS5[self.CCDSelection][0], fC.CCDLocationsCS5[self.CCDSelection][1])
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "Nominal Z for " + str(self.CCDSelection + ' ' + self.trianglePointSelection) + " is: " + str(nominalZ) + "um in CS5 coordinates.")
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "CCD Manual Mode Absolute value of (Nominal Z - Measured Best Focus) = " +  str(np.absolute(nominalZ-xInter)) + 'um')
        
    def CCDTipTiltZ(self):
        ###########################################################################
        ###Get CCD Seletion from User
        ###########################################################################
        self._CCDSelectionWindow()
        
        ###########################################################################
        ###Create Dir Using self.CCDSelection
        ###########################################################################
        faah = fileAndArrayHandling()
        dirNameA = faah.createDir(str(self.CCDSelection + '_A'), self, 'Manual_Mode_CCD_Focus_Curve')
        dirNameB = faah.createDir(str(self.CCDSelection + '_B'), self, 'Manual_Mode_CCD_Focus_Curve')
        dirNameC = faah.createDir(str(self.CCDSelection + '_C'), self, 'Manual_Mode_CCD_Focus_Curve')
        
        ###########################################################################
        ###Message user to fill dir (mention label names)
        ###########################################################################
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "Suggested " +  str(self.CCDSelection) + 
                                      " manual mode focus curve directories for points A, B, and C: \n" + str(os.getcwd()) + '\\' + dirNameA + "\n" +
                                      str(os.getcwd()) + '\\' + dirNameB + "\n" +
                                      str(os.getcwd()) + '\\' + dirNameC + "\n" +
                                      "\nNOTE: the file names will be used to create the Z axis values (distance)\n" +
                                        " so please label the FITS files appropriately\n" +
                                        "(example: 350.fit for the image taken at 350um).")
        
        ###########################################################################
        ###Windows to Prompt Focus Curve Image Loading
        ###########################################################################        
        top = Toplevel()
        top.title("About this application...")

        msg = Message(top, text=about_message)
        msg.pack()

        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack()
        
    def _setTrueAndExit(self, windowVariable, fifLabel=" ", CCDLabel=" ", trianglePointLabel=" "):
        if fifLabel != " ":
            self.fifSelection = fifLabel
        if CCDLabel != " ":
            self.CCDSelection = CCDLabel
        if trianglePointLabel != " ":
            self.trianglePointSelection = trianglePointLabel
        windowVariable.destroy()
        
    def _CCDSelectionWindow(self):
        ###########################################################################
        ###CCD Button Option Window
        ###########################################################################   
        top = tk.Toplevel()
        top.title("CCD Manual Mode")
        self.wm_withdraw()
        
        #Manual Mode Description
        tk.Label(top, text="Which CCD would you like to measure?").grid(row=0, column=0, columnspan=2, sticky='W')
        
        # NCCD
        NCCD = tk.Button(top, text="NCCD: (0,-387.26)", command=lambda: self._setTrueAndExit(top, CCDLabel="NCCD"))
        NCCD.grid(row=1, column=0)
        
        # WCCD
        WCCD = tk.Button(top, text="WCCD: (-387.26,0)", command=lambda: self._setTrueAndExit(top, CCDLabel="WCCD"))
        WCCD.grid(row=2, column=0)
        
        # SCCD
        SCCD = tk.Button(top, text="SCCD: (0,387.26)", command=lambda: self._setTrueAndExit(top, CCDLabel="SCCD"))
        SCCD.grid(row=3, column=0)
        
        # ECCD
        ECCD = tk.Button(top, text="ECCD: (387.26,0)", command=lambda: self._setTrueAndExit(top, CCDLabel="ECCD"))
        ECCD.grid(row=4, column=0)
        
        # CCCD
        CCCD = tk.Button(top, text="CCCD: (0,0)", command=lambda: self._setTrueAndExit(top, CCDLabel="CCCD"))
        CCCD.grid(row=5, column=0)
        
        # Other (will set x=0 y=0)
        other = tk.Button(top, text="Other", command=lambda: self._setTrueAndExit(top, CCDLabel="Other"))
        other.grid(row=6, column=0)  
        
        top.wait_window()
        
    def _trianglePointSelectionWindow(self):
        ###########################################################################
        ###Triangle Point Button Option Window
        ###########################################################################   
        top = tk.Toplevel()
        top.title("CCD Manual Mode")
        self.wm_withdraw()
        
        #Manual Mode Description
        tk.Label(top, text="Which triangle point would you like to measure?").grid(row=0, column=0, columnspan=2, sticky='W')
        
        #A
        A = tk.Button(top, text="A", command=lambda: self._setTrueAndExit(top, trianglePointLabel="A"))
        A.grid(row=1, column=0, sticky='W')
        
        #B
        B = tk.Button(top, text="B", command=lambda: self._setTrueAndExit(top, trianglePointLabel="B"))
        B.grid(row=2, column=0, sticky='W')
        
        #C
        C = tk.Button(top, text="C", command=lambda: self._setTrueAndExit(top, trianglePointLabel="C"))
        C.grid(row=3, column=0, sticky='W')
        
        #Other (will set x=0 y=0)
        other = tk.Button(top, text="Other (will set x=0 y=0)", command=lambda: self._setTrueAndExit(top, trianglePointLabel="Other"))
        other.grid(row=6, column=0, sticky='W')  
        
        #Map
        tk.Label(top, text=" ").grid(row=7, column=0, columnspan=2, sticky='W')
        top.triangleMAP = tk.PhotoImage(file="FPA_triangles-300x300.png", width=300, height=300)
        tk.Label(top, image=top.triangleMAP).grid(row=8, column=0, rowspan=3, sticky='W')
        
        top.wait_window()
    
    def _fifSelectionWindow(self):
        ###########################################################################
        ###FIF Button Option Window
        ###########################################################################   
        top = tk.Toplevel()
        top.title("FIF Manual Mode")
        self.wm_withdraw()
        
        #Manual Mode Description
        tk.Label(top, text="Which FIF would you like to measure?").grid(row=0, column=0, columnspan=2, sticky='W')
        
        # RefFIF
        refFIF = tk.Button(top, text="RefFIF: (199.28,-345.15)", command=lambda: self._setTrueAndExit(top, fifLabel="RefFIF"))
        refFIF.grid(row=1, column=0, sticky='W')
        
        # NFIF
        NFIF = tk.Button(top, text="NFIF: (-108.31,-383.55)", command=lambda: self._setTrueAndExit(top, fifLabel="NFIF"))
        NFIF.grid(row=2, column=0, sticky='W')
        
        # WFIF
        WFIF = tk.Button(top, text="WFIF: (-383.55,108.31)", command=lambda: self._setTrueAndExit(top, fifLabel="WFIF"))
        WFIF.grid(row=2, column=1, sticky='W')
        
        # SFIF
        SFIF = tk.Button(top, text="SFIF: (108.31,383.55)", command=lambda: self._setTrueAndExit(top, fifLabel="SFIF"))
        SFIF.grid(row=2, column=2, sticky='W')
        
        # EFIF
        EFIF = tk.Button(top, text="EFIF: (383.55,-108.31)", command=lambda: self._setTrueAndExit(top, fifLabel="EFIF"))
        EFIF.grid(row=2, column=3, sticky='W')
        
        # A1
        A1 = tk.Button(top, text="A1: (281.82,-281.82)", command=lambda: self._setTrueAndExit(top, fifLabel="A1"))
        A1.grid(row=3, column=0, sticky='W')
        
        # A2
        A2 = tk.Button(top, text="A2: (-281.82,-281.82)", command=lambda: self._setTrueAndExit(top, fifLabel="A2"))
        A2.grid(row=3, column=1, sticky='W')
        
        # A3
        A3 = tk.Button(top, text="A3: (-281.82,281.82)", command=lambda: self._setTrueAndExit(top, fifLabel="A3"))
        A3.grid(row=3, column=2, sticky='W')
        
        # A4
        A4 = tk.Button(top, text="A4: (281.82,281.82)", command=lambda: self._setTrueAndExit(top, fifLabel="A4"))
        A4.grid(row=3, column=3, sticky='W')
        
        # B1
        B1 = tk.Button(top, text="B1: (293.64,136.93)", command=lambda: self._setTrueAndExit(top, fifLabel="B1"))
        B1.grid(row=4, column=0, sticky='W')
        
        # B2
        B2 = tk.Button(top, text="B2: (-293.64,136.93)", command=lambda: self._setTrueAndExit(top, fifLabel="B2"))
        B2.grid(row=4, column=1, sticky='W')
        
        # B3
        B3 = tk.Button(top, text="B3: (-293.64,-136.93)", command=lambda: self._setTrueAndExit(top, fifLabel="B3"))
        B3.grid(row=4, column=2, sticky='W')
        
        # B4
        B4 = tk.Button(top, text="B4: (-136.93,293.64)", command=lambda: self._setTrueAndExit(top, fifLabel="B4"))
        B4.grid(row=4, column=3, sticky='W')
        
        # C1
        C1 = tk.Button(top, text="C1: (96.44,232.82)", command=lambda: self._setTrueAndExit(top, fifLabel="C1"))
        C1.grid(row=5, column=0, sticky='W')
        
        # C2
        C2 = tk.Button(top, text="C2: (232.82,-96.44)", command=lambda: self._setTrueAndExit(top, fifLabel="C2"))
        C2.grid(row=5, column=1, sticky='W')
        
        # C3
        C3 = tk.Button(top, text="C3: (-96.44,-232.82)", command=lambda: self._setTrueAndExit(top, fifLabel="C3"))
        C3.grid(row=5, column=2, sticky='W')
        
        # C4
        C4 = tk.Button(top, text="C4: (-232.82,96.44)", command=lambda: self._setTrueAndExit(top, fifLabel="C4"))
        C4.grid(row=5, column=3, sticky='W')
        
        # D1
        D1 = tk.Button(top, text="D1: (0,185.00)", command=lambda: self._setTrueAndExit(top, fifLabel="D1"))
        D1.grid(row=6, column=0, sticky='W')
        
        # D2
        D2 = tk.Button(top, text="D2: (185.00,0)", command=lambda: self._setTrueAndExit(top, fifLabel="D2"))
        D2.grid(row=6, column=1, sticky='W')
        
        # D3
        D3 = tk.Button(top, text="D3: (0,-185.00)", command=lambda: self._setTrueAndExit(top, fifLabel="D3"))
        D3.grid(row=6, column=2, sticky='W')
        
        # D4
        D4 = tk.Button(top, text="D4: (-185.00,0)", command=lambda: self._setTrueAndExit(top, fifLabel="D4"))
        D4.grid(row=6, column=3, sticky='W')
        
        # CFIF
        CFIF = tk.Button(top, text="CFIF: (108.31,15.00)", command=lambda: self._setTrueAndExit(top, fifLabel="CFIF"))
        CFIF.grid(row=7, column=0, sticky='W')
        
        # Other
        other = tk.Button(top, text="Other (will set x=0 y=0)", command=lambda: self._setTrueAndExit(top, fifLabel="Other"))
        other.grid(row=8, column=0, columnspan=3, sticky='W')
        
        top.wait_window()