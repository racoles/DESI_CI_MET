'''
@title metManualMode
@author: Rebecca Coles
Updated on Feb 01, 2018
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
from tipTiltZCCD import tipTiltZCCD
from CCDOpsPlanetMode import CCDOpsPlanetMode
from centroidFIF import centroidFIF
from fractions import Fraction
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
        
    def manualFIFFocusCurve(self, fifThread = 0.5, fifThreadOD = 6):
        '''
        Creates a focus curve for FIFs using FITs images.
        
        Default FIF threading: fifThread = 0.5mm Z increase/decrease per turn.
        '''
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
        
        ###########################################################################
        ###Nominal best focus
        ###########################################################################
        nominalZ = fC.asphericFocalCurve(fC.fifLocationsCS5[self.fifSelection][0], fC.fifLocationsCS5[self.fifSelection][1])
        faah.pageLogging(self.consoleLog, self.logFile, 
                                    "FIF Manual Mode Measured Best focus for " + str(self.fifSelection) + " is: " + str(xInter) + "um.\n"
                                    "Nominal Z for " + str(self.fifSelection) + " is: " + str(nominalZ) + "um (in CS5 coordinates).")
        
        ###########################################################################
        ###Make FIF Height Adjustment
        ###########################################################################
        #If the FIF height isn't equal to the nominal height
        if xInter != nominalZ:
            #is the FIF too low or too high (clockwise = down, counter-clockwise = up)
            if xInter < 0: 
                turn = 'counter-clockwise' 
            else: 
                turn = 'clockwise'
            #How many turns will it take to reach nominal height?
            turnDistance_um = np.absolute(xInter)/(fifThread*1000) #X turns = needed height / fif pitch (height per one full turn). Convert mm to microns.
            turnDistanceDegrees = faah.decNonZeroRound(np.absolute(turnDistance_um/((fifThreadOD*1000)/360))) #to get number of degrees. 1 degree = fifThreadODMicrons/360 um. Convert mm to microns.
            turnFraction = np.absolute(Fraction(turnDistance_um).limit_denominator()) #turnFraction-th of a turn
            #Issue warning
            faah.pageLogging(self.consoleLog, self.logFile, 
                                      "WARNING: the FIF Z height is " + str(xInter)[0:5] + "um away from nominal.\n The current FIF thread pitch is " +
                                      str(fifThread) + "mm (" + str(fifThread*1000) + "um), with a OD of " + str(fifThreadOD) + "mm (" +  str(fifThreadOD*1000) + "um)." + 
                                      "\n To adjust this FIF to the nominal height, you will need to turn the FIF\n " + 
                                       str(turnDistanceDegrees) + " degrees " + turn +" (" + 
                                       str(turnFraction).replace('(', '').replace(')', '') + 
                                       "th of a turn).")
        
        
        
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
        
    def manualCentroidFIF(self, fiflabel):
        ###########################################################################
        ###Create Dir
        ###########################################################################
        faah = fileAndArrayHandling()
        dirName = faah.createDir(fiflabel, self, 'Centroid')
        
        ###########################################################################
        ###Message user to fill dir (mention label names)
        ###########################################################################
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "Suggested " +  str(fiflabel) + " centroid directory: \n" + str(os.getcwd()) + '\\' + dirName)
        
        ###########################################################################
        ###Get images
        ###########################################################################
        imageArray4D, filelist = faah.openAllFITSImagesInDirectory()
        
        ###########################################################################
        ###Find fif in image and create subarray
        ###########################################################################
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "Centroiding " + str(fiflabel) + " using FITs file:\n" + str(filelist[0]).replace('/', '\\'))
        fifSubArray, subArrayBoxSize, maxLoc  = centroidFIF.findFIFInImage(self, imageArray4D[0])
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      str(fiflabel) + " FIF found at pixel location: (" + str(maxLoc[0]) + "," + str(maxLoc[1]) + "). Will now centroid using that location.")
        
        ###########################################################################
        ###Centroid
        ###########################################################################
        cF = centroidFIF()
        xcen, ycen = cF.findCentroid(fifSubArray, int(subArrayBoxSize/2), int(subArrayBoxSize/2), extendbox = 3)
        
        ###########################################################################
        ###Add offsets to account for subarray
        ###########################################################################
        xcen = xcen + maxLoc[0]-subArrayBoxSize/2
        ycen = ycen + maxLoc[1]-subArrayBoxSize/2
        
        ###########################################################################
        ###Add X and Y data to fifCentroidedLocationDict
        ###########################################################################
        #Account for planet mode
        pM = CCDOpsPlanetMode()
        xOffset, yOffset, pixelSize = pM.readFitsHeader(imageArray4D, filelist, self.consoleLog, self.logFile)
        
        #Distance from center of FIF to origin of sensor (x=0, y=0)
        xDistToSensorOrigin = xcen + xOffset
        yDistToSensorOrigin = ycen + yOffset
        
        #Add X and Y to fifCentroidedLocationDict
        self.fifCentroidedLocationDict[fiflabel][0] = xDistToSensorOrigin
        self.fifCentroidedLocationDict[fiflabel][1] = yDistToSensorOrigin
        
        ###########################################################################
        ###Print Location of FIF Centroid
        ###########################################################################
        faah.pageLogging(self.consoleLog, self.logFile, 
                str(fiflabel) + " center found at location: (" + str(xDistToSensorOrigin) + "," + str(yDistToSensorOrigin) + ")")
        
        return xDistToSensorOrigin, yDistToSensorOrigin
        
    def CCDTipTiltZ(self):
        '''
        Take focus curves at the points of an equilateral triangle
        to find the CCD center
        '''
        ###########################################################################
        ###Get CCD Seletion from User
        ###########################################################################
        self._CCDSelectionWindow()
        fC = focusCurve()
        
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
        #Point A      
        topA = tk.Toplevel()
        topA.title("CCD tip/tilt/Z Triangle Point A")
        aboutMessageA = 'Fill directory with focus curve images for point A' + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + 'A'])
        msgA = tk.Message(topA, text=aboutMessageA)
        msgA.pack()
        buttonA = tk.Button(topA, text="Ready", command=topA.destroy)
        buttonA.pack()
        topA.wait_window()
        imageArray4DA, filelistA = faah.openAllFITSImagesInDirectory()
        
        #Point B      
        topB = tk.Toplevel()
        topB.title("CCD tip/tilt/Z Triangle Point B")
        aboutMessageB = 'Fill directory with focus curve images for point B' + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + 'B'])
        msgB = tk.Message(topB, text=aboutMessageB)
        msgB.pack()
        buttonB = tk.Button(topB, text="Ready", command=topB.destroy)
        buttonB.pack()
        topB.wait_window()
        imageArray4DB, filelistB = faah.openAllFITSImagesInDirectory()
        
        #Point C      
        topC = tk.Toplevel()
        topC.title("CCD tip/tilt/Z Triangle Point C")
        aboutMessageC = 'Fill directory with focus curve images for point C' + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + 'C'])
        msgC = tk.Message(topC, text=aboutMessageC)
        msgC.pack()
        buttonC = tk.Button(topC, text="Ready", command=topC.destroy)
        buttonC.pack()
        topC.wait_window()
        imageArray4DC, filelistC = faah.openAllFITSImagesInDirectory()
        
        ###########################################################################
        ###Create focus curves
        ###########################################################################
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "Z VALUES FOR " + str(self.CCDSelection) + " POINTS A, B, and C:")
        #A    
        xInterA = fC.stdFocusCurve(self.CCDSelection, imageArray4DA, filelistA, pointLabel = "A")
        nominalZA = fC.asphericFocalCurve(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + 'A'][0], fC.trianglePonitCCDLocationsCS5[self.CCDSelection + 'A'][1])
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      str(self.CCDSelection) + " A (Best Focus):" + str(xInterA) + "um\n" + str(self.CCDSelection) + " A (Nominal Z):" + str(nominalZA) + "um")

        #B
        xInterB = fC.stdFocusCurve(self.CCDSelection, imageArray4DB, filelistB, pointLabel = "B")
        nominalZB = fC.asphericFocalCurve(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + 'B'][0], fC.trianglePonitCCDLocationsCS5[self.CCDSelection + 'B'][1])
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      str(self.CCDSelection) + " B (Best Focus):" + str(xInterB) + "um\n" + str(self.CCDSelection) + " B (Nominal Z):" + str(nominalZB) + "um") 
        #C
        xInterC = fC.stdFocusCurve(self.CCDSelection, imageArray4DC, filelistC, pointLabel = "C")
        nominalZC = fC.asphericFocalCurve(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + 'C'][0], fC.trianglePonitCCDLocationsCS5[self.CCDSelection + 'C'][1])
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      str(self.CCDSelection) + " C (Best Focus):" + str(xInterC) + "um\n" + str(self.CCDSelection) + " C (Nominal Z):" + str(nominalZC) + "um")
        
        ###########################################################################
        ###Check Tip and Tilt
        ###########################################################################
        ttz = tipTiltZCCD()
        #Tip
        ttz.tipCCD(xInterA, xInterB, xInterC, nominalZA, nominalZB, nominalZC, self.CCDSelection, self.consoleLog, self.logFile)
        #Tilt
        ttz.tiltCCD(xInterA, xInterB, xInterC, nominalZA, nominalZB, nominalZC, self.CCDSelection, self.consoleLog, self.logFile)
        #Z
        ttz.ZCCD(xInterA, xInterB, xInterC, self.CCDSelection, self.consoleLog, self.logFile)
        
        
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