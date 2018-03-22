'''
Created on Mar 22, 2018

@author: coles.81

@title tipTiltZCCD
@author: Rebecca Coles
Updated on Mar 06, 2018
Created on Jan 18, 2018

checkCameraOriginLocation
This module holds a series of functions that are used to find the origin of a CCD on the DESI CI in CS5.

'''

# Import #######################################################################################
import tkinter as tk
from tkinter.ttk import Separator
from fileAndArrayHandling import fileAndArrayHandling
from CCDOpsPlanetMode import CCDOpsPlanetMode
from centroidFIF import centroidFIF
import math
from focusCurve import focusCurve
import numpy as np
from alternateCentroidMethods import gmsCentroid
################################################################################################

class checkCameraOriginLocation(object):
    
    CCDSelection = ""
    trianglePointLabel = ""
    #Pixel distance to origin check point
    pixelDistanceToCheckPoint = 10 #pixel location (rows = pixelDistanceToCheckPoint, columns = pixelDistanceToCheckPoint)
    
    def __init__(self):
        '''
        Constructor
        '''
        
    def checkCameraOriginLocation(self, consoleLog, logFile):
        '''
        Find the location of the CI camera's sensor origin in CS5 and instruct the user to view 
        the origin with the DMM to ensure that the tip/tilt/focus pinhole triangle was placed properly
        on the SBIt STXL sensor.
        '''
        ###########################################################################
        ###Sensor Location menu
        ###########################################################################
        self._checkCameraOriginLocationSelectionWindow()
        print(self.CCDSelection)
        print(self.trianglePointLabel)
        
        ###########################################################################
        ###Get images
        ###########################################################################
        faah = fileAndArrayHandling()
        imageArray4D, filelist = faah.openAllFITSImagesInDirectory()
        aa = round(len(filelist)/2) #select a focused image from array a
                
        ###########################################################################
        ###Centroid Image
        ########################################################################### 
        #Get location of pinhole image in (rows, columns)
        cF = centroidFIF()
        _ , subArrayBoxSize, maxLoc = cF.findFIFInImage(imageArray4D[aa])
        
        #Account for planet mode
        pM = CCDOpsPlanetMode()
        xOffset, yOffset, pixelSize = pM.readFitsHeader(imageArray4D, filelist, consoleLog, logFile)
        
        #Use alternate methods to centroid pinhole image
        #    gmsCentroid: Gaussian Marginal Sum (GMS) Centroid Method.
        xCenGMS, yCenGMS, _, _ = gmsCentroid(imageArray4D[aa], maxLoc[1], maxLoc[0], 
                                                         int(round(subArrayBoxSize/2)), int(round(subArrayBoxSize/2)), axis='both', verbose=False)
        
        ###########################################################################
        ###Calculate the distance to the sensor origin using centroided image.
        ###########################################################################  
        #Find distance in um to CCD Origin  
        rows = xCenGMS + xOffset  
        columns = yCenGMS + yOffset
        
        hypotenuse = np.sqrt(math.pow((rows),2)+math.pow((columns),2))
        faah = fileAndArrayHandling()
        
        ##Find location of Origin in CS5    
        CS5OriginX = 0
        CS5OriginY = 0 
        fC = focusCurve()
        
        if self.trianglePointLabel != '':
            #pinhole is from 100um DMM (triangle)
            CS5OriginX = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + self.trianglePointLabel][0] + (rows*(pixelSize/1000))
            CS5OriginY = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + self.trianglePointLabel][1] + (columns*(pixelSize/1000))
            faah.pageLogging(consoleLog, logFile, 
                    "Distance from pinhole center to sensor origin: " + format(hypotenuse, '.3f') + "pixels or " + format(hypotenuse*pixelSize, '.3f') + 'um\n' +
                    "To check SBIG STXL sensor origin location, move to CCD pixel location (" + str(self.pixelDistanceToCheckPoint) + "," + str(self.pixelDistanceToCheckPoint) + ")" + 
                    ":\n CS5 (X = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + self.trianglePointLabel][0] + ((rows-self.pixelDistanceToCheckPoint)*(pixelSize/1000))) +
                     "mm, Y = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + self.trianglePointLabel][1] + ((columns-self.pixelDistanceToCheckPoint)*(pixelSize/1000))) + "mm)" + 
                    "At location CS5 (X = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + self.trianglePointLabel][0] + ((rows-self.pixelDistanceToCheckPoint)*(pixelSize/1000))) +
                     "mm, Y = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + self.trianglePointLabel][1] + ((columns-self.pixelDistanceToCheckPoint)*(pixelSize/1000))) + "mm) you should be able to see " + 
                    " the origin of the sensor using the SBIG ST-i. A pinhole projected onto the SBIG STXL at this point show show up in a SBIG STXL at pixel location " +
                    "( row = " + str(self.pixelDistanceToCheckPoint) + ", column = " + str(self.pixelDistanceToCheckPoint) + ")")
            
        elif self.CCDSelection != '' and self.trianglePointLabel == '':
            #pinhole is at CCD center
            CS5OriginX = fC.CCDLocationsCS5[self.CCDSelection][0] + (rows*(pixelSize/1000))
            CS5OriginY = fC.CCDLocationsCS5[self.CCDSelection][1] + (columns*(pixelSize/1000))
            faah.pageLogging(consoleLog, logFile, 
                    "Distance from pinhole center to sensor origin: " + format(hypotenuse, '.3f') + "pixels or " + format(hypotenuse*pixelSize, '.3f') + 'um\n'
                    "To check SBIG STXL sensor origin location, move to CCD pixel location (" + str(self.pixelDistanceToCheckPoint) + "," + str(self.pixelDistanceToCheckPoint) + ")" + 
                    ":\n CS5 (X = " + str(fC.CCDLocationsCS5[self.CCDSelection][0] + ((rows-self.pixelDistanceToCheckPoint)*(pixelSize/1000))) +
                     "mm, Y = " + str(fC.CCDLocationsCS5[self.CCDSelection][1] + ((columns-self.pixelDistanceToCheckPoint)*(pixelSize/1000))) + "mm)" + 
                    "At location CS5 (X = " + str(fC.CCDLocationsCS5[self.CCDSelection][0] + ((rows-self.pixelDistanceToCheckPoint)*(pixelSize/1000))) +
                     "mm, Y = " + str(fC.CCDLocationsCS5[self.CCDSelection][1] + ((columns-self.pixelDistanceToCheckPoint)*(pixelSize/1000))) + "mm) you should be able to see " + 
                    " the origin of the sensor using the SBIG ST-i. A pinhole projected onto the SBIG STXL at this point show show up in a SBIG STXL at pixel location " +
                    "( row = " + str(self.pixelDistanceToCheckPoint) + ", column = " + str(self.pixelDistanceToCheckPoint) + ")")
            
        else:
            #pinhole type not selected
            print('Pinhole type not selected. Will use CS5 (X = 0mm, Y = 0mm)')     
    
    def _checkCameraOriginLocationSelectionWindow(self):
        '''
        Find the location of the CI camera's sensor origin in CS5 and instruct the user to view 
        the origin with the DMM to ensure that the tip/tilt/focus pinhole triangle was placed properly
        on the SBIt STXL sensor.
        '''
        ###########################################################################
        ###Construct menu
        ###########################################################################   
        top = tk.Toplevel()
        top.title("Check Camera Origin")
        
        #CCD Location Description
        tk.Label(top, text="Which CCD location would you like to measure?").grid(row=0, column=0, columnspan=4, sticky='W')
        
        # NCCD
        Separator(top, orient="horizontal").grid(row=1, column=0, columnspan=4, sticky='ew')
        tk.Label(top, text="NCCD").grid(row=2, column=0, sticky='W')
        NCCD_A = tk.Button(top, text="NCCD: A", command=lambda: self._setTrueAndExit(top, CCDLabel="NCCD", trianglePointLabel="A"))
        NCCD_A.grid(row=3, column=0)
        NCCD_B = tk.Button(top, text="NCCD: B", command=lambda: self._setTrueAndExit(top, CCDLabel="NCCD", trianglePointLabel="B"))
        NCCD_B.grid(row=3, column=1)
        NCCD_C = tk.Button(top, text="NCCD: C", command=lambda: self._setTrueAndExit(top, CCDLabel="NCCD", trianglePointLabel="C"))
        NCCD_C.grid(row=3, column=2)
        NCCD_Center = tk.Button(top, text="NCCD: Center", command=lambda: self._setTrueAndExit(top, CCDLabel="NCCD"))
        NCCD_Center.grid(row=3, column=3)
        
        # WCCD
        Separator(top, orient="horizontal").grid(row=4, column=0, columnspan=4, sticky='ew')
        tk.Label(top, text="WCCD").grid(row=5, column=0, sticky='W')
        WCCD_A = tk.Button(top, text="WCCD: A", command=lambda: self._setTrueAndExit(top, CCDLabel="WCCD", trianglePointLabel="A"))
        WCCD_A.grid(row=6, column=0)
        WCCD_B = tk.Button(top, text="WCCD: B", command=lambda: self._setTrueAndExit(top, CCDLabel="WCCD", trianglePointLabel="B"))
        WCCD_B.grid(row=6, column=1)
        WCCD_C = tk.Button(top, text="WCCD: C", command=lambda: self._setTrueAndExit(top, CCDLabel="WCCD", trianglePointLabel="C"))
        WCCD_C.grid(row=6, column=2)
        WCCD_Center = tk.Button(top, text="WCCD: Center", command=lambda: self._setTrueAndExit(top, CCDLabel="WCCD"))
        WCCD_Center.grid(row=6, column=3)
        
        # SCCD
        Separator(top, orient="horizontal").grid(row=7, column=0, columnspan=4, sticky='ew')
        tk.Label(top, text="SCCD").grid(row=8, column=0, sticky='W')
        SCCD_A = tk.Button(top, text="SCCD: A", command=lambda: self._setTrueAndExit(top, CCDLabel="SCCD", trianglePointLabel="A"))
        SCCD_A.grid(row=9, column=0)
        SCCD_B = tk.Button(top, text="SCCD: B", command=lambda: self._setTrueAndExit(top, CCDLabel="SCCD", trianglePointLabel="B"))
        SCCD_B.grid(row=9, column=1)
        SCCD_C = tk.Button(top, text="SCCD: C", command=lambda: self._setTrueAndExit(top, CCDLabel="SCCD", trianglePointLabel="C"))
        SCCD_C.grid(row=9, column=2)
        SCCD_Center = tk.Button(top, text="SCCD: Center", command=lambda: self._setTrueAndExit(top, CCDLabel="SCCD"))
        SCCD_Center.grid(row=9, column=3)
        
        # ECCD
        Separator(top, orient="horizontal").grid(row=10, column=0, columnspan=4, sticky='ew')
        tk.Label(top, text="ECCD").grid(row=11, column=0, sticky='W')
        ECCD_A = tk.Button(top, text="ECCD: A", command=lambda: self._setTrueAndExit(top, CCDLabel="ECCD", trianglePointLabel="A"))
        ECCD_A.grid(row=12, column=0)
        ECCD_B = tk.Button(top, text="ECCD: B", command=lambda: self._setTrueAndExit(top, CCDLabel="ECCD", trianglePointLabel="B"))
        ECCD_B.grid(row=12, column=1)
        ECCD_C = tk.Button(top, text="ECCD: C", command=lambda: self._setTrueAndExit(top, CCDLabel="ECCD", trianglePointLabel="C"))
        ECCD_C.grid(row=12, column=2)
        ECCD_Center = tk.Button(top, text="ECCD: Center", command=lambda: self._setTrueAndExit(top, CCDLabel="ECCD"))
        ECCD_Center.grid(row=12, column=3)
        
        # CCCD
        Separator(top, orient="horizontal").grid(row=13, column=0, columnspan=4, sticky='ew')
        tk.Label(top, text="CCCD").grid(row=14, column=0, sticky='W')
        CCCD_A = tk.Button(top, text="CCCD: A", command=lambda: self._setTrueAndExit(top, CCDLabel="CCCD", trianglePointLabel="A"))
        CCCD_A.grid(row=15, column=0)
        CCCD_B = tk.Button(top, text="CCCD: B", command=lambda: self._setTrueAndExit(top, CCDLabel="CCCD", trianglePointLabel="B"))
        CCCD_B.grid(row=15, column=1)
        CCCD_C = tk.Button(top, text="CCCD: C", command=lambda: self._setTrueAndExit(top, CCDLabel="CCCD", trianglePointLabel="C"))
        CCCD_C.grid(row=15, column=2)
        CCCD_Center = tk.Button(top, text="CCCD: Center", command=lambda: self._setTrueAndExit(top, CCDLabel="CCCD"))
        CCCD_Center.grid(row=15, column=3)
        
        top.wait_window()
           
    def _setTrueAndExit(self, windowVariable, CCDLabel, trianglePointLabel=""):
        self.CCDSelection = CCDLabel
        if trianglePointLabel != "":
            self.trianglePointLabel = trianglePointLabel
        windowVariable.destroy()
        
