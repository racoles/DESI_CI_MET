'''
@title foreShortening
@author: Rebecca Coles
Updated on June 18, 2018
Created on Mar 18, 2018

foreShortening
This module holds a series of functions that are used to find the magnitude of this fore-shortening:

1.    The 6303 Cameras (N,E,S,W) are tilted by 5.4 degrees from the Z axis. Therefore when the CCDs are viewed from above, 
        and measurements are made in the CS5 X,Y plane, the 6303 CCDs will appear to be fore-shortened across their width for all four cameras. 
2.    Magnitude of this fore-shortening is ~ (1- COS(5.4deg)) *(2048*9um) = 82 um  (too large to ignore)
'''

# Import #######################################################################################
import numpy as np
from focusCurve import focusCurve
from fileAndArrayHandling import fileAndArrayHandling
################################################################################################

class foreShortening(object):
    
    CCDAngle = 5.4 #degrees
    
    def __init__(self):
        '''
        Constructor
        '''
        
    def foreShortening(self, consoleLog, logFile, CCDLabel, pixelSize):
        '''
        Find the magnitude of this fore-shortening for the 6303 Cameras (N,E,S,W)
        '''
        ###########################################################################
        ###Select Camera
        ###########################################################################
        faah = fileAndArrayHandling()
        fC = focusCurve()
                
        if CCDLabel == "NCCD": #(fore-shortened in Y)
            #trinaglePoint A
            distA = fC.trianglePonitCCDLocationsCS5["NCCDA"][1] - fC.CCDLocationsCS5["NCCD"][1] 
                #X
            foreShortenedCS5Location_AX = fC.trianglePonitCCDLocationsCS5["NCCDA"][0]
                #Y
            foreShortenedDistanceFromCenter_AY = (1 - np.cos(self.CCDAngle)) * (distA * (pixelSize/1000)) #mm
            foreShortenedCS5Location_AY = fC.CCDLocationsCS5["NCCD"][1] + foreShortenedDistanceFromCenter_AY #mm
            
            #trinaglePoint B
            distB = fC.CCDLocationsCS5["NCCD"][1] - fC.trianglePonitCCDLocationsCS5["NCCDB"][1]
                #X
            foreShortenedCS5Location_BX = fC.trianglePonitCCDLocationsCS5["NCCDB"][0]
                #Y
            foreShortenedDistanceFromCenter_BY = (1 - np.cos(self.CCDAngle)) * (distB * (pixelSize/1000)) #mm
            foreShortenedCS5Location_BY = fC.CCDLocationsCS5["NCCD"][1] - foreShortenedDistanceFromCenter_BY #mm
            
            #trinaglePoint C
            distC = fC.CCDLocationsCS5["NCCD"][1] - fC.trianglePonitCCDLocationsCS5["NCCDC"][1]
                #X            
            foreShortenedCS5Location_CX = fC.trianglePonitCCDLocationsCS5["NCCDC"][0]
                #Y
            foreShortenedDistanceFromCenter_CY = (1 - np.cos(self.CCDAngle)) * (distC * (pixelSize/1000)) #mm
            foreShortenedCS5Location_CY = fC.CCDLocationsCS5["NCCD"][1] - foreShortenedDistanceFromCenter_CY #mm   

        elif CCDLabel == "WCCD": #(fore-shortened in X)
            #trinaglePoint A
            distA = fC.trianglePonitCCDLocationsCS5["WCCDA"][0] - fC.CCDLocationsCS5["WCCD"][0] 
                #X
            foreShortenedDistanceFromCenter_AX = (1 - np.cos(self.CCDAngle)) * (distA * (pixelSize/1000)) #mm
            foreShortenedCS5Location_AX = fC.CCDLocationsCS5["WCCD"][0] + foreShortenedDistanceFromCenter_AX #mm
                #Y
            foreShortenedCS5Location_AY = fC.trianglePonitCCDLocationsCS5["WCCDA"][1]
                
            #trinaglePoint B
            distB = fC.CCDLocationsCS5["WCCD"][0] - fC.trianglePonitCCDLocationsCS5["WCCDB"][0]
                #X  
            foreShortenedDistanceFromCenter_BX = (1 - np.cos(self.CCDAngle)) * (distB * (pixelSize/1000)) #mm
            foreShortenedCS5Location_BX = fC.CCDLocationsCS5["WCCD"][0] - foreShortenedDistanceFromCenter_BX #mm
                #Y
            foreShortenedCS5Location_BY = fC.trianglePonitCCDLocationsCS5["WCCDB"][1]
                
            #trinaglePoint C
            distC = fC.CCDLocationsCS5["WCCD"][0] - fC.trianglePonitCCDLocationsCS5["WCCDC"][0]
                #X  
            foreShortenedDistanceFromCenter_CX = (1 - np.cos(self.CCDAngle)) * (distC * (pixelSize/1000)) #mm
            foreShortenedCS5Location_CX = fC.CCDLocationsCS5["WCCD"][0] - foreShortenedDistanceFromCenter_CX #mm
                #Y
            foreShortenedCS5Location_CY = fC.trianglePonitCCDLocationsCS5["WCCDC"][1]
            
        elif CCDLabel == "SCCD": #(fore-shortened in Y)
            #trinaglePoint A
            distA = fC.CCDLocationsCS5["SCCD"][1] - fC.trianglePonitCCDLocationsCS5["SCCDA"][1]
                #X            
            foreShortenedCS5Location_AX = fC.trianglePonitCCDLocationsCS5["SCCDA"][0]  
                #Y  
            foreShortenedDistanceFromCenter_AY = (1 - np.cos(self.CCDAngle)) * (distA * (pixelSize/1000)) #mm
            foreShortenedCS5Location_AY = fC.CCDLocationsCS5["SCCD"][1] - foreShortenedDistanceFromCenter_AY #mm
            
            #trinaglePoint B
            distB = fC.trianglePonitCCDLocationsCS5["SCCDB"][1] - fC.CCDLocationsCS5["SCCD"][1] 
                #X  
            foreShortenedCS5Location_BX = fC.trianglePonitCCDLocationsCS5["SCCDB"][0]
                #Y 
            foreShortenedDistanceFromCenter_BY = (1 - np.cos(self.CCDAngle)) * (distB * (pixelSize/1000)) #mm
            foreShortenedCS5Location_BY = fC.CCDLocationsCS5["SCCD"][1] + foreShortenedDistanceFromCenter_BY #mm
            
            #trinaglePoint C
            distC = fC.trianglePonitCCDLocationsCS5["SCCDC"][1] - fC.CCDLocationsCS5["SCCD"][1] 
                #X  
            foreShortenedCS5Location_CX = fC.trianglePonitCCDLocationsCS5["SCCDC"][0]
                #Y 
            foreShortenedDistanceFromCenter_CY = (1 - np.cos(self.CCDAngle)) * (distC * (pixelSize/1000)) #mm
            foreShortenedCS5Location_CY = fC.CCDLocationsCS5["SCCD"][1] + foreShortenedDistanceFromCenter_CY #mm
            
        elif CCDLabel == "ECCD": #(fore-shortened in X)
            #trinaglePoint A
            distA = fC.CCDLocationsCS5["ECCD"][0] - fC.trianglePonitCCDLocationsCS5["ECCDA"][0]
            foreShortenedDistanceFromCenter_A = (1 - np.cos(self.CCDAngle)) * (distA * (pixelSize/1000)) #mm
            foreShortenedCS5Location_A = fC.CCDLocationsCS5["ECCD"][0] - foreShortenedDistanceFromCenter_A #mm
            #trinaglePoint B
            distB = fC.trianglePonitCCDLocationsCS5["ECCDB"][0] - fC.CCDLocationsCS5["ECCD"][0]
            foreShortenedDistanceFromCenter_B = (1 - np.cos(self.CCDAngle)) * (distB * (pixelSize/1000)) #mm
            foreShortenedCS5Location_B = fC.CCDLocationsCS5["ECCD"][0] + foreShortenedDistanceFromCenter_B #mm
            #trinaglePoint C
            distC = fC.trianglePonitCCDLocationsCS5["ECCDC"][0] - fC.CCDLocationsCS5["ECCD"][0]
            foreShortenedDistanceFromCenter_C = (1 - np.cos(self.CCDAngle)) * (distC * (pixelSize/1000)) #mm
            foreShortenedCS5Location_C = fC.CCDLocationsCS5["ECCD"][0] + foreShortenedDistanceFromCenter_C #mm
                
        elif CCDLabel == "CCCD":
            #trinaglePoint A
            distA = fC.CCDLocationsCS5["CCCD"][1] - fC.trianglePonitCCDLocationsCS5["CCCDA"][1]
            foreShortenedDistanceFromCenter_A = (1 - np.cos(self.CCDAngle)) * (distA * (pixelSize/1000)) #mm
            foreShortenedCS5Location_A = fC.CCDLocationsCS5["CCCD"][1] - foreShortenedDistanceFromCenter_A #mm
            #trinaglePoint B
            distB = fC.trianglePonitCCDLocationsCS5["CCCDB"][1] - fC.CCDLocationsCS5["CCCD"][1] 
            foreShortenedDistanceFromCenter_B = (1 - np.cos(self.CCDAngle)) * (distB * (pixelSize/1000)) #mm
            foreShortenedCS5Location_B = fC.CCDLocationsCS5["CCCD"][1] + foreShortenedDistanceFromCenter_B #mm
            #trinaglePoint C
            distC = fC.trianglePonitCCDLocationsCS5["CCCDC"][1] - fC.CCDLocationsCS5["CCCD"][1] 
            foreShortenedDistanceFromCenter_C = (1 - np.cos(self.CCDAngle)) * (distC * (pixelSize/1000)) #mm
            foreShortenedCS5Location_C = fC.CCDLocationsCS5["CCCD"][1] + foreShortenedDistanceFromCenter_C #mm
                
        else:
            faah.pageLogging(consoleLog, logFile, "\n\nWarning: was unable to fore-shorten value.\n\n", warning = True)
                
        return foreShortenedCS5Location_AX, foreShortenedCS5Location_AY, foreShortenedCS5Location_BX, foreShortenedCS5Location_BY, foreShortenedCS5Location_CX, foreShortenedCS5Location_CY
