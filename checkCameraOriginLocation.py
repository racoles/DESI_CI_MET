'''
@title checkCameraOriginLocation
@author: Rebecca Coles
Updated on June 06, 2018
Created on Mar 22, 2018

checkCameraOriginLocation
This module holds a series of functions that are used to find the origin of a CCD on the DESI CI in CS5.

'''

# Import #######################################################################################
import tkinter as tk
from fileAndArrayHandling import fileAndArrayHandling
from CCDOpsPlanetMode import CCDOpsPlanetMode
from centroidFIF import centroidFIF
from focusCurve import focusCurve
from alternateCentroidMethods import gmsCentroid
from cs5Offsets import cs5Offsets
from tipTiltZCCD import tipTiltZCCD
import numpy as np
import math
################################################################################################

class checkCameraOriginLocation(object):
    
    CCDSelection = ""
    
    #Pixel distance to origin check point
    pixelDistanceToCheckPointX = 25 #pixel location X
    pixelDistanceToCheckPointY = 25 #pixel location Y  
    
    #Pixel distance to sensor center
    pixelDistanceToCenterX = 3072/2 #pixel location X
    pixelDistanceToCenterY = 2048/2 #pixel location Y      
    
    #STi Pixel Size
    stipixel = 7.4
    
    #logfile
    logFile = ""
    
    #Calibration Offsets
    calOffX = "Not yet set"
    calOffY = "Not yet set"
    
    def __init__(self):
        '''
        Constructor
        '''
        
    def checkCameraOriginLocation(self, consoleLog, logFile):
        '''
        Find the location of the CI camera's sensor origin in CS5 and instruct the user to view 
        the origin with the DMM to ensure that the tip/tilt/focus pinhole triangle was placed properly
        on the SBIG STXL sensor.
        '''
        ###########################################################################
        ###Offset Calibration
        ###########################################################################
        
#Note: in future, row versus columns equal to x and y will be different for NESW cameras

        #Print fif loactions
        faah = fileAndArrayHandling()
        fC = focusCurve()
        faah.printDictToFile(fC.fifLocationsCS5, "Nominal FIF Locations in CS5 (X mm, Y mm, Z mm)" , consoleLog, logFile, printNominalDicts = True)
        
        #Get calibration values 
        cs5off = cs5Offsets()
        PIDTSO_x, PIDTSO_y, CPOCID_X, CPOCID_Y, CPOCID_cent_x, CPOCID_cent_y, dmmMag = cs5off.calibrationScreen(consoleLog, logFile)
        
        #print(PIDTSO_x)
        #print(PIDTSO_y)
        #print(CPOCID_X)
        #print(CPOCID_Y)
        #print(CPOCID_cent_x)
        #print(CPOCID_cent_y)
        #print(dmmMag)
        #Calculate offset
        
        calOffX = ((PIDTSO_x - CPOCID_cent_x)*self.stipixel)/dmmMag
        calOffY = ((PIDTSO_y - CPOCID_cent_y)*self.stipixel)/dmmMag
        
        #Print offset
        faah.pageLogging(consoleLog, logFile, "Using: \n[((100um pinhole mapping STi (pixels)) - (optical CS5 origin (FIF centroid) (pixels))) * (STi Pixel size (um))] / (DMM magnification)\n" +
                         "Calibration Offset X (um) = [(" + str(PIDTSO_x) + " - " + format(CPOCID_cent_x, '.3f') + ") * " + str(self.stipixel) + "] / " + str(dmmMag) + " = " + format(calOffX, '.3f') + "\n" +
                         "Calibration Offset Y (um) = [(" + str(PIDTSO_y) + " - " + format(CPOCID_cent_y, '.3f') + ") * " + str(self.stipixel) + "] / " + str(dmmMag) + " = " + format(calOffY, '.3f') + "\n" +
                         "Calibration Offset (um): (" + format(calOffX, '.3f') + ", " + format(calOffY, '.3f') + ")\n", calibration = True)
        faah.pageLogging(consoleLog, logFile, "Calibration Routine Complete\n", calibration = True)
        
        ###########################################################################
        ###Sensor Location menu
        ###########################################################################
        self._checkCameraOriginLocationSelectionWindow()
        
        ###########################################################################
        ###Get images
        ###########################################################################
        #Point A      
        topA = tk.Toplevel()
        topA.title("CCD Origin Test: Triangle Point A")
        aboutMessageA = str('Fill directory with images for point A (' + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + 'A'][0], '.3f') + 
                            " ," + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + 'A'][1], '.3f') + ")")
        faah.pageLogging(consoleLog, logFile, aboutMessageA)
        msgA = tk.Message(topA, text=aboutMessageA)
        msgA.pack()
        buttonA = tk.Button(topA, text="Ready", command=topA.destroy)
        buttonA.pack()
        topA.wait_window()
        imageArray4DA, filelistA = faah.openAllFITSImagesInDirectory()
        
        #Point B      
        topB = tk.Toplevel()
        topB.title("CCD Origin Test: Triangle Point B")
        aboutMessageB = str('Fill directory with images for point B (' + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + 'B'][0], '.3f') + 
                            " ," + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + 'B'][1], '.3f') + ")")
        faah.pageLogging(consoleLog, logFile, aboutMessageB)
        msgB = tk.Message(topB, text=aboutMessageB)
        msgB.pack()
        buttonB = tk.Button(topB, text="Ready", command=topB.destroy)
        buttonB.pack()
        topB.wait_window()
        imageArray4DB, filelistB = faah.openAllFITSImagesInDirectory()
        
        #Point C      
        topC = tk.Toplevel()
        topC.title("CCD Origin Test: Triangle Point C")
        aboutMessageC = str('Fill directory with images for point C (' + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + 'C'][0], '.3f') + 
                            " ," + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + 'C'][1], '.3f') + ")\n")
        faah.pageLogging(consoleLog, logFile, aboutMessageC)
        msgC = tk.Message(topC, text=aboutMessageC)
        msgC.pack()
        buttonC = tk.Button(topC, text="Ready", command=topC.destroy)
        buttonC.pack()
        topC.wait_window()
        imageArray4DC, filelistC = faah.openAllFITSImagesInDirectory()        
               
        aa = round(len(filelistA)/2) #select a focused image from array a
        bb = round(len(filelistB)/2) #select b focused image from array b
        cc = round(len(filelistC)/2) #select c focused image from array c
                
        ###########################################################################
        ###Centroid Images
        ########################################################################### 
        #Get location of pinhole image in (rows, columns)
        cF = centroidFIF()
        _ , subArrayBoxSizeA, maxLocA = cF.findFIFInImage(imageArray4DA[aa])
        _ , subArrayBoxSizeB, maxLocB = cF.findFIFInImage(imageArray4DA[bb])
        _ , subArrayBoxSizeC, maxLocC = cF.findFIFInImage(imageArray4DA[cc])
        
        #Account for planet mode
        pM = CCDOpsPlanetMode()
        xOffsetA, yOffsetA, _ = pM.readFitsHeader(imageArray4DA, filelistA, consoleLog, logFile)
        xOffsetB, yOffsetB, _ = pM.readFitsHeader(imageArray4DB, filelistB, consoleLog, logFile)
        xOffsetC, yOffsetC, pixelSize = pM.readFitsHeader(imageArray4DC, filelistC, consoleLog, logFile)
        
        #Use alternate methods to centroid pinhole image
        #    gmsCentroid: Gaussian Marginal Sum (GMS) Centroid Method.
        xCenGMSA, yCenGMSA, _, _ = gmsCentroid(imageArray4DA[aa], maxLocA[1], maxLocA[0], 
                                                         int(round(subArrayBoxSizeA/2)), int(round(subArrayBoxSizeA/2)), axis='both', verbose=False)
        xCenGMSB, yCenGMSB, _, _ = gmsCentroid(imageArray4DB[bb], maxLocB[1], maxLocB[0], 
                                                         int(round(subArrayBoxSizeB/2)), int(round(subArrayBoxSizeB/2)), axis='both', verbose=False)
        xCenGMSC, yCenGMSC, _, _ = gmsCentroid(imageArray4DC[cc], maxLocC[1], maxLocC[0], 
                                                         int(round(subArrayBoxSizeC/2)), int(round(subArrayBoxSizeC/2)), axis='both', verbose=False)
        
        
        
        ###########################################################################
        ###Get Rz
        ###########################################################################
        ttzCCD = tipTiltZCCD()
        angleRz = ttzCCD.rz(imageArray4DB[bb], filelistB, imageArray4DC[cc], filelistC, self.CCDSelection, consoleLog, logFile)
        faah.pageLogging(consoleLog, logFile, "\nRz Local (degrees): " + format(angleRz, '.3f'))   

        ###########################################################################
        ###Calculate the distance to pixelDistanceToCheckPoint pixelDistanceToCenter and using centroided image.
        ###########################################################################  
        #Find distance in um to CCD pixelDistanceToCheckPoint
        DeltaX_SBIGXL_A = ((xCenGMSA + xOffsetA) - self.pixelDistanceToCheckPointX) * pixelSize
        DeltaY_SBIGXL_A = ((yCenGMSA + yOffsetA) - self.pixelDistanceToCheckPointY) * pixelSize
        
        DeltaX_SBIGXL_B = ((xCenGMSB + xOffsetB) - self.pixelDistanceToCheckPointX) * pixelSize
        DeltaY_SBIGXL_B = ((yCenGMSB + yOffsetB) - self.pixelDistanceToCheckPointY) * pixelSize
        
        DeltaX_SBIGXL_C = ((xCenGMSC + xOffsetC) - self.pixelDistanceToCheckPointX) * pixelSize
        DeltaY_SBIGXL_C = ((yCenGMSC + yOffsetC) - self.pixelDistanceToCheckPointY) * pixelSize
        
        #Find distance in um to CCD pixelDistanceToCenter
        DeltaX_SBIGXL_A_Sensor_Center = ((xCenGMSA + xOffsetA) - self.pixelDistanceToCenterX) * pixelSize
        DeltaY_SBIGXL_A_Sensor_Center = ((yCenGMSA + yOffsetA) - self.pixelDistanceToCenterY) * pixelSize
        
        DeltaX_SBIGXL_B_Sensor_Center = (self.pixelDistanceToCenterX - (xCenGMSB + xOffsetB) ) * pixelSize
        DeltaY_SBIGXL_B_Sensor_Center = (self.pixelDistanceToCenterY - (yCenGMSB + yOffsetB)) * pixelSize
        
        DeltaX_SBIGXL_C_Sensor_Center = ((xCenGMSC + xOffsetC) - self.pixelDistanceToCenterX) * pixelSize
        DeltaY_SBIGXL_C_Sensor_Center = ((yCenGMSC + yOffsetC) - self.pixelDistanceToCenterY) * pixelSize
        
        #X(A)
        #if (xCenGMSA + xOffsetA) <= self.pixelDistanceToCenterX:
        #    DeltaX_SBIGXL_A_Sensor_Center = (self.pixelDistanceToCenterX - (xCenGMSA + xOffsetA)) * pixelSize
        #else:
        #    DeltaX_SBIGXL_A_Sensor_Center = ((xCenGMSA + xOffsetA) - self.pixelDistanceToCenterX) * pixelSize
        #Y(A)
        #if (yCenGMSA + yOffsetA) <= self.pixelDistanceToCenterY:
        #    DeltaY_SBIGXL_A_Sensor_Center = (self.pixelDistanceToCenterY - (yCenGMSA + yOffsetA)) * pixelSize
        #else:
        #    DeltaY_SBIGXL_A_Sensor_Center = ((yCenGMSA + yOffsetA) - self.pixelDistanceToCenterY) * pixelSize
            
        #X(B)
        #if (xCenGMSB + xOffsetB) <= self.pixelDistanceToCenterX:
        #    DeltaX_SBIGXL_B_Sensor_Center = (self.pixelDistanceToCenterX - (xCenGMSB + xOffsetB)) * pixelSize
        #else:
        #    DeltaX_SBIGXL_B_Sensor_Center = ((xCenGMSB + xOffsetB) - self.pixelDistanceToCenterX) * pixelSize
        #Y(B)
        #if (yCenGMSB + yOffsetB) <= self.pixelDistanceToCenterY:
        #    DeltaY_SBIGXL_B_Sensor_Center = (self.pixelDistanceToCenterY - (yCenGMSB + yOffsetB)) * pixelSize
        #else:
        #    DeltaY_SBIGXL_B_Sensor_Center = ((yCenGMSB + yOffsetB) - self.pixelDistanceToCenterY) * pixelSize
            
        #X(C)
        #if (xCenGMSC + xOffsetC) <= self.pixelDistanceToCenterX:
        #    DeltaX_SBIGXL_C_Sensor_Center = (self.pixelDistanceToCenterX - (xCenGMSC + xOffsetC)) * pixelSize
        #else:
        #   DeltaX_SBIGXL_C_Sensor_Center = ((xCenGMSC + xOffsetC) - self.pixelDistanceToCenterX) * pixelSize
        #Y(C)
        #if (yCenGMSC + yOffsetC) <= self.pixelDistanceToCenterY:
        #    DeltaY_SBIGXL_C_Sensor_Center = (self.pixelDistanceToCenterY - (yCenGMSC + yOffsetC)) * pixelSize
        #else:
        #    DeltaY_SBIGXL_C_Sensor_Center = ((yCenGMSC + yOffsetC) - self.pixelDistanceToCenterY) * pixelSize      
        
        ###########################################################################
        ###Rotation Coordinate Transform from SBIG Coordinates to CS5 Coordinates
        ###Go to (pixelDistanceToCheckPointX, pixelDistanceToCheckPointY)
        ########################################################################### 

        if angleRz < 0: #c(y)>b(y) = +Rz = Counter-Clockwise
            DeltaX_CS5_A = (DeltaX_SBIGXL_A * np.cos(math.radians(angleRz))) - (DeltaY_SBIGXL_A * np.sin(math.radians(angleRz)))
            DeltaY_CS5_A = (DeltaX_SBIGXL_A * np.sin(math.radians(angleRz))) + (DeltaY_SBIGXL_A * np.cos(math.radians(angleRz)))
            
            DeltaX_CS5_B = (DeltaX_SBIGXL_B * np.cos(math.radians(angleRz))) - (DeltaY_SBIGXL_B * np.sin(math.radians(angleRz)))
            DeltaY_CS5_B = (DeltaX_SBIGXL_B * np.sin(math.radians(angleRz))) + (DeltaY_SBIGXL_B * np.cos(math.radians(angleRz)))   
            
            DeltaX_CS5_C = (DeltaX_SBIGXL_C * np.cos(math.radians(angleRz))) - (DeltaY_SBIGXL_C * np.sin(math.radians(angleRz)))
            DeltaY_CS5_C = (DeltaX_SBIGXL_C * np.sin(math.radians(angleRz))) + (DeltaY_SBIGXL_C * np.cos(math.radians(angleRz))) 
            
            DeltaX_CS5_A_Sensor_Center = (DeltaX_SBIGXL_A_Sensor_Center * np.cos(math.radians(angleRz))) - (DeltaY_SBIGXL_A_Sensor_Center * np.sin(math.radians(angleRz)))
            DeltaY_CS5_A_Sensor_Center = (DeltaX_SBIGXL_A_Sensor_Center * np.sin(math.radians(angleRz))) + (DeltaY_SBIGXL_A_Sensor_Center * np.cos(math.radians(angleRz)))
        
            DeltaX_CS5_B_Sensor_Center = (DeltaX_SBIGXL_B_Sensor_Center * np.cos(math.radians(angleRz))) - (DeltaY_SBIGXL_B_Sensor_Center * np.sin(math.radians(angleRz)))
            DeltaY_CS5_B_Sensor_Center = (DeltaX_SBIGXL_B_Sensor_Center * np.sin(math.radians(angleRz))) + (DeltaY_SBIGXL_B_Sensor_Center * np.cos(math.radians(angleRz)))
        
            DeltaX_CS5_C_Sensor_Center = (DeltaX_SBIGXL_C_Sensor_Center * np.cos(math.radians(angleRz))) - (DeltaY_SBIGXL_C_Sensor_Center * np.sin(math.radians(angleRz)))
            DeltaY_CS5_C_Sensor_Center = (DeltaX_SBIGXL_C_Sensor_Center * np.sin(math.radians(angleRz))) + (DeltaY_SBIGXL_C_Sensor_Center * np.cos(math.radians(angleRz)))
            
            CS5XA = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][0] + DeltaX_CS5_A/1000
            CS5YA = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][1] + DeltaY_CS5_A/1000
            
            CS5XB = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][0] + DeltaX_CS5_B/1000
            CS5YB = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][1] + DeltaY_CS5_B/1000
            
            CS5XC = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][0] + DeltaX_CS5_C/1000
            CS5YC = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][1] + DeltaY_CS5_C/1000
            
            faah.pageLogging(consoleLog, logFile, "\nMove to pixel (" + str(self.pixelDistanceToCheckPointX) + ", " + str(self.pixelDistanceToCheckPointY) + ")\n\n" +
                         "Using: ((centroid(pixel) + planetModeOffset) +/- targetPixel(pixel)) * pixelSize\n" +
                         "Distance in SBIGXL frame (mm):\n" +
                         "    DeltaX_SBIGXL_A = (" + format(xCenGMSA , '.3f') +  " + " + format(xOffsetA, '.3f') + ") - " + str(self.pixelDistanceToCheckPointX) + ") * " + str(pixelSize/1000) + " = " + format(DeltaX_SBIGXL_A/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_A = (" + format(yCenGMSA , '.3f') +  " + " + format(yOffsetA, '.3f') + ") - " + str(self.pixelDistanceToCheckPointY) + ") * " + str(pixelSize/1000) + " = " + format(DeltaY_SBIGXL_A/1000, '.3f') + "\n\n" +
                         "    DeltaX_SBIGXL_B = (" + format(xCenGMSB , '.3f') +  " + " + format(xOffsetB, '.3f') + ") - " + str(self.pixelDistanceToCheckPointX) + ") * " + str(pixelSize/1000) + " = " + format(DeltaX_SBIGXL_B/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_B = (" + format(yCenGMSB , '.3f') +  " + " + format(yOffsetB, '.3f') + ") - " + str(self.pixelDistanceToCheckPointY) + ") * " + str(pixelSize/1000) + " = " + format(DeltaY_SBIGXL_B/1000, '.3f') + "\n\n" +
                         "    DeltaX_SBIGXL_C = (" + format(xCenGMSC , '.3f') +  " + " + format(xOffsetC, '.3f') + ") - " + str(self.pixelDistanceToCheckPointX) + ") * " + str(pixelSize/1000) + " = " + format(DeltaX_SBIGXL_C/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_C = (" + format(yCenGMSC , '.3f') +  " + " + format(yOffsetC, '.3f') + ") - " + str(self.pixelDistanceToCheckPointY) + ") * " + str(pixelSize/1000) + " = " + format(DeltaY_SBIGXL_C/1000, '.3f') + "\n\n" +
                         
                         "Using: Rotational Coordinate Transform\n" + "       DeltaX_CS5 = (DeltaX_SBIGXL * cos(Rz)) - (DeltaY_SBIGXL * sin(Rz))\n       DeltaY_CS5 = (DeltaX_SBIGXL * sin(Rz)) + (DeltaY_SBIGXL * cos(Rz))\n\n" +
                         "Distance in CS5 frame (mm):\n" +
                         "    DeltaX_CS5_A = (" + format(DeltaX_SBIGXL_A/1000, '.3f') + " * " + format(np.cos(math.radians(angleRz)), '.3f') + ") - (" + format(DeltaY_SBIGXL_A/1000, '.3f') + " * " + format(np.sin(math.radians(angleRz)), '.3f') + ") = "+ format(DeltaX_CS5_A/1000, '.3f') +"\n" +
                         "    DeltaY_CS5_A = (" + format(DeltaX_SBIGXL_A/1000, '.3f') + " * " + format(np.sin(math.radians(angleRz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_A/1000, '.3f') + " * " + format(np.cos(math.radians(angleRz)), '.3f') + ") = "+ format(DeltaY_CS5_A/1000, '.3f') +"\n\n" +
                         "    DeltaX_CS5_B = (" + format(DeltaX_SBIGXL_B/1000, '.3f') + " * " + format(np.cos(math.radians(angleRz)), '.3f') + ") - (" + format(DeltaY_SBIGXL_B/1000, '.3f') + " * " + format(np.sin(math.radians(angleRz)), '.3f') + ") = "+ format(DeltaX_CS5_B/1000, '.3f') +"\n" +
                         "    DeltaY_CS5_B = (" + format(DeltaX_SBIGXL_B/1000, '.3f') + " * " + format(np.sin(math.radians(angleRz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_B/1000, '.3f') + " * " + format(np.cos(math.radians(angleRz)), '.3f') + ") = "+ format(DeltaY_CS5_B/1000, '.3f') +"\n\n" +
                         "    DeltaX_CS5_C = (" + format(DeltaX_SBIGXL_C/1000, '.3f') + " * " + format(np.cos(math.radians(angleRz)), '.3f') + ") - (" + format(DeltaY_SBIGXL_C/1000, '.3f') + " * " + format(np.sin(math.radians(angleRz)), '.3f') + ") = "+ format(DeltaX_CS5_C/1000, '.3f') +"\n" +
                         "    DeltaY_CS5_C = (" + format(DeltaX_SBIGXL_C/1000, '.3f') + " * " + format(np.sin(math.radians(angleRz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_C/1000, '.3f') + " * " + format(np.cos(math.radians(angleRz)), '.3f') + ") = "+ format(DeltaY_CS5_C/1000, '.3f') +"\n\n" +
                         
                         "Using: Target Pixel CS5 Location (mm) = Nominal CS5 + DeltaCS5\n" +
                         "Calculated using triangle point A:\n" +
                         "    CS5X(A) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][0]) + " + " + format(DeltaX_CS5_A/1000, '.3f') + " = " + 
                         format(CS5XA, '.3f') + "\n" +
                         "    CS5Y(A) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][1]) + " + " + format(DeltaY_CS5_A/1000, '.3f') + " = " + 
                         format(CS5YA, '.3f') + "\n\n" +
                         "Calculated using triangle point B:\n" +
                         "    CS5X(B) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][0]) + " + " + format(DeltaX_CS5_B/1000, '.3f') + " = " + 
                         format(CS5XB, '.3f') + "\n" +
                         "    CS5Y(B) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][1]) + " + " + format(DeltaY_CS5_B/1000, '.3f') + " = " + 
                         format(CS5YB, '.3f') + "\n\n" +
                         "Calculated using triangle point C:\n" +
                         "    CS5X(C) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][0]) + " + " + format(DeltaX_CS5_C/1000, '.3f') + " = " + 
                         format(CS5XC, '.3f') + "\n" +
                         "    CS5Y(C) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][1]) + " + " + format(DeltaY_CS5_C/1000, '.3f') + " = " + 
                         format(CS5YC, '.3f')) 
            
        elif angleRz > 0: #b(y)>c(y) = -Rz = Clockwise
            DeltaX_CS5_A = (DeltaX_SBIGXL_A * np.cos(math.radians(angleRz))) + (DeltaY_SBIGXL_A * np.sin(math.radians(angleRz)))
            DeltaY_CS5_A = (-DeltaX_SBIGXL_A * np.sin(math.radians(angleRz))) + (DeltaY_SBIGXL_A * np.cos(math.radians(angleRz)))
            
            DeltaX_CS5_B = (DeltaX_SBIGXL_B * np.cos(math.radians(angleRz))) + (DeltaY_SBIGXL_B * np.sin(math.radians(angleRz)))
            DeltaY_CS5_B = (-DeltaX_SBIGXL_B * np.sin(math.radians(angleRz))) + (DeltaY_SBIGXL_B * np.cos(math.radians(angleRz)))   
            
            DeltaX_CS5_C = (DeltaX_SBIGXL_C * np.cos(math.radians(angleRz))) + (DeltaY_SBIGXL_C * np.sin(math.radians(angleRz)))
            DeltaY_CS5_C = (-DeltaX_SBIGXL_C * np.sin(math.radians(angleRz))) + (DeltaY_SBIGXL_C * np.cos(math.radians(angleRz))) 
            
            DeltaX_CS5_A_Sensor_Center = (DeltaX_SBIGXL_A_Sensor_Center * np.cos(math.radians(angleRz))) + (DeltaY_SBIGXL_A_Sensor_Center * np.sin(math.radians(angleRz)))
            DeltaY_CS5_A_Sensor_Center = (-DeltaX_SBIGXL_A_Sensor_Center * np.sin(math.radians(angleRz))) + (DeltaY_SBIGXL_A_Sensor_Center * np.cos(math.radians(angleRz)))
        
            DeltaX_CS5_B_Sensor_Center = (DeltaX_SBIGXL_B_Sensor_Center * np.cos(math.radians(angleRz))) + (DeltaY_SBIGXL_B_Sensor_Center * np.sin(math.radians(angleRz)))
            DeltaY_CS5_B_Sensor_Center = (-DeltaX_SBIGXL_B_Sensor_Center * np.sin(math.radians(angleRz))) + (DeltaY_SBIGXL_B_Sensor_Center * np.cos(math.radians(angleRz))) 
        
            DeltaX_CS5_C_Sensor_Center = (DeltaX_SBIGXL_C_Sensor_Center * np.cos(math.radians(angleRz))) + (DeltaY_SBIGXL_C_Sensor_Center * np.sin(math.radians(angleRz)))
            DeltaY_CS5_C_Sensor_Center = (-DeltaX_SBIGXL_C_Sensor_Center * np.sin(math.radians(angleRz))) + (DeltaY_SBIGXL_C_Sensor_Center * np.cos(math.radians(angleRz))) 
            
            CS5XA = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][0] + DeltaX_CS5_A/1000
            CS5YA = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][1] + DeltaY_CS5_A/1000
            
            CS5XB = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][0] + DeltaX_CS5_B/1000
            CS5YB = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][1] + DeltaY_CS5_B/1000
            
            CS5XC = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][0] + DeltaX_CS5_C/1000
            CS5YC = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][1] + DeltaY_CS5_C/1000
            
            faah.pageLogging(consoleLog, logFile, "\nMove to pixel (" + str(self.pixelDistanceToCheckPointX) + ", " + str(self.pixelDistanceToCheckPointY) + ")\n\n" +
                         "Using: ((centroid(pixel)) + planetModeOffset) +/- targetPixel(pixel)) * pixelSize\n" +
                         "Distance in SBIGXL frame (mm):\n" +
                         "    DeltaX_SBIGXL_A = (" + format(xCenGMSA , '.3f') +  " + " + format(xOffsetA, '.3f') + ") - " + str(self.pixelDistanceToCheckPointX) + ") * " + str(pixelSize/1000) + " = " + format(DeltaX_SBIGXL_A/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_A = (" + format(yCenGMSA , '.3f') +  " + " + format(yOffsetA, '.3f') + ") - " + str(self.pixelDistanceToCheckPointY) + ") * " + str(pixelSize/1000) + " = " + format(DeltaY_SBIGXL_A/1000, '.3f') + "\n\n" +
                         "    DeltaX_SBIGXL_B = (" + format(xCenGMSB , '.3f') +  " + " + format(xOffsetB, '.3f') + ") - " + str(self.pixelDistanceToCheckPointX) + ") * " + str(pixelSize/1000) + " = " + format(DeltaX_SBIGXL_B/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_B = (" + format(yCenGMSB , '.3f') +  " + " + format(yOffsetB, '.3f') + ") - " + str(self.pixelDistanceToCheckPointY) + ") * " + str(pixelSize/1000) + " = " + format(DeltaY_SBIGXL_B/1000, '.3f') + "\n\n" +
                         "    DeltaX_SBIGXL_C = (" + format(xCenGMSC , '.3f') +  " + " + format(xOffsetC, '.3f') + ") - " + str(self.pixelDistanceToCheckPointX) + ") * " + str(pixelSize/1000) + " = " + format(DeltaX_SBIGXL_C/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_C = (" + format(yCenGMSC , '.3f') +  " + " + format(yOffsetC, '.3f') + ") - " + str(self.pixelDistanceToCheckPointY) + ") * " + str(pixelSize/1000) + " = " + format(DeltaY_SBIGXL_C/1000, '.3f') + "\n\n" +
                         
                         "Using: Rotational Coordinate Transform\n" + "       DeltaX_CS5 = (DeltaX_SBIGXL * cos(Rz)) + (DeltaY_SBIGXL * sin(Rz))\n       DeltaY_CS5 = (DeltaX_SBIGXL * -sin(Rz)) + (DeltaY_SBIGXL * cos(Rz))\n\n" +
                         "Distance in CS5 frame (mm):\n" +
                         "    DeltaX_CS5_A = (" + format(DeltaX_SBIGXL_A/1000, '.3f') + " * " + format(np.cos(math.radians(angleRz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_A/1000, '.3f') + " * " + format(np.sin(math.radians(angleRz)), '.3f') + ") = " + format(DeltaX_CS5_A/1000, '.3f') + "\n" +
                         "    DeltaY_CS5_A = (" + format(-DeltaX_SBIGXL_A/1000, '.3f') + " * " + format(np.sin(math.radians(angleRz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_A/1000, '.3f') + " * " + format(np.cos(math.radians(angleRz)), '.3f') + ") = " + format(DeltaY_CS5_A/1000, '.3f') + "\n\n" +
                         "    DeltaX_CS5_B = (" + format(DeltaX_SBIGXL_B/1000, '.3f') + " * " + format(np.cos(math.radians(angleRz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_B/1000, '.3f') + " * " + format(np.sin(math.radians(angleRz)), '.3f') + ") = " + format(DeltaX_CS5_B/1000, '.3f') +"\n" +
                         "    DeltaY_CS5_B = (" + format(-DeltaX_SBIGXL_B/1000, '.3f') + " * " + format(np.sin(math.radians(angleRz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_B/1000, '.3f') + " * " + format(np.cos(math.radians(angleRz)), '.3f') + ") = " + format(DeltaY_CS5_B/1000, '.3f') +"\n\n" +
                         "    DeltaX_CS5_C = (" + format(DeltaX_SBIGXL_C/1000, '.3f') + " * " + format(np.cos(math.radians(angleRz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_C/1000, '.3f') + " * " + format(np.sin(math.radians(angleRz)), '.3f') + ") = " +  format(DeltaX_CS5_C/1000, '.3f') +"\n" +
                         "    DeltaY_CS5_C = (" + format(-DeltaX_SBIGXL_C/1000, '.3f') + " * " + format(np.sin(math.radians(angleRz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_C/1000, '.3f') + " * " + format(np.cos(math.radians(angleRz)), '.3f') + ") = " + format(DeltaY_CS5_C/1000, '.3f') +"\n\n" +
                         
                         "Using: Target Pixel CS5 Location (mm) = Nominal CS5 + DeltaCS5\n" +
                         "Calculated using triangle point A:\n" +
                         "    CS5X(A) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][0]) + " + " + format(DeltaX_CS5_A/1000, '.3f') + " = " + 
                         format(CS5XA, '.3f') + "\n" +
                         "    CS5Y(A) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][1]) + " + " + format(DeltaY_CS5_A/1000, '.3f') + " = " + 
                         format(CS5YA, '.3f') + "\n\n" +
                         "Calculated using triangle point B:\n" +
                         "    CS5X(B) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][0]) + " + " + format(DeltaX_CS5_B/1000, '.3f') + " = " + 
                         format(CS5XB, '.3f') + "\n" +
                         "    CS5Y(B) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][1]) + " + " + format(DeltaY_CS5_B/1000, '.3f') + " = " + 
                         format(CS5YB, '.3f') + "\n\n" +
                         "Calculated using triangle point C:\n" +
                         "    CS5X(C) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][0]) + " + " + format(DeltaX_CS5_C/1000, '.3f') + " = " + 
                         format(CS5XC, '.3f') + "\n" +
                         "    CS5Y(C) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][1]) + " + " + format(DeltaY_CS5_C/1000, '.3f') + " = " + 
                         format(CS5YC, '.3f')) 
               
        else:
            faah.pageLogging(consoleLog, logFile, "Rz = 0: no rotational transform needed.")
            
            DeltaX_CS5_A = DeltaX_SBIGXL_A
            DeltaY_CS5_A = DeltaY_SBIGXL_A
            
            DeltaX_CS5_B = DeltaX_SBIGXL_B
            DeltaY_CS5_B = DeltaY_SBIGXL_B   
            
            DeltaX_CS5_C = DeltaX_SBIGXL_C
            DeltaY_CS5_C = DeltaY_SBIGXL_C 
            
            DeltaX_CS5_A_Sensor_Center = DeltaX_SBIGXL_A_Sensor_Center
            DeltaY_CS5_A_Sensor_Center = DeltaY_SBIGXL_A_Sensor_Center
        
            DeltaX_CS5_B_Sensor_Center = DeltaX_SBIGXL_B_Sensor_Center
            DeltaY_CS5_B_Sensor_Center = DeltaY_SBIGXL_B_Sensor_Center
        
            DeltaX_CS5_C_Sensor_Center = DeltaX_SBIGXL_C_Sensor_Center
            DeltaY_CS5_C_Sensor_Center = DeltaY_SBIGXL_C_Sensor_Center
 ################           
            CS5XA = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][0] + DeltaX_CS5_A/1000
            CS5YA = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][1] + DeltaY_CS5_A/1000
            
            CS5XB = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][0] + DeltaX_CS5_B/1000
            CS5YB = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][1] + DeltaY_CS5_B/1000
            
            CS5XC = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][0] + DeltaX_CS5_C/1000
            CS5YC = fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][1] + DeltaY_CS5_C/1000
            
            
            faah.pageLogging(consoleLog, logFile, "\nMove to pixel (" + str(self.pixelDistanceToCheckPointX) + ", " + str(self.pixelDistanceToCheckPointY) + ")\n\n" +
                         "Using: ((centroid(pixel)) + planetModeOffset) +/- targetPixel(pixel)) * pixelSize\n" +
                         "Distance in SBIGXL frame (mm):\n" +
                         "    DeltaX_SBIGXL_A = (" + format(xCenGMSA , '.3f') +  " + " + format(xOffsetA, '.3f') + ") - " + str(self.pixelDistanceToCheckPointX) + ") * " + str(pixelSize/1000) + " = " + format(DeltaX_SBIGXL_A/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_A = (" + format(yCenGMSA , '.3f') +  " + " + format(yOffsetA, '.3f') + ") - " + str(self.pixelDistanceToCheckPointY) + ") * " + str(pixelSize/1000) + " = " + format(DeltaY_SBIGXL_A/1000, '.3f') + "\n\n" +
                         "    DeltaX_SBIGXL_B = (" + format(xCenGMSB , '.3f') +  " + " + format(xOffsetB, '.3f') + ") - " + str(self.pixelDistanceToCheckPointX) + ") * " + str(pixelSize/1000) + " = " + format(DeltaX_SBIGXL_B/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_B = (" + format(yCenGMSB , '.3f') +  " + " + format(yOffsetB, '.3f') + ") - " + str(self.pixelDistanceToCheckPointY) + ") * " + str(pixelSize/1000) + " = " + format(DeltaY_SBIGXL_B/1000, '.3f') + "\n\n" +
                         "    DeltaX_SBIGXL_C = (" + format(xCenGMSC , '.3f') +  " + " + format(xOffsetC, '.3f') + ") - " + str(self.pixelDistanceToCheckPointX) + ") * " + str(pixelSize/1000) + " = " + format(DeltaX_SBIGXL_C/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_C = (" + format(yCenGMSC , '.3f') +  " + " + format(yOffsetC, '.3f') + ") - " + str(self.pixelDistanceToCheckPointY) + ") * " + str(pixelSize/1000) + " = " + format(DeltaY_SBIGXL_C/1000, '.3f') + "\n\n" +
                         
                         "Using: No Rotational Coordinate Transform\n" + "DeltaX_CS5 = DeltaX_SBIGXL\nDeltaY_CS5 = DeltaX_SBIGXL\n" +
                         "Distance in CS5 frame (mm):\n" +
                         "    DeltaX_CS5_A = DeltaX_SBIGXL_A = " + format(DeltaX_CS5_A/1000 , '.3f') + "\n" +
                         "    DeltaY_CS5_A = DeltaY_SBIGXL_A = " + format(DeltaY_CS5_A/1000 , '.3f') + "\n\n" +
                         "    DeltaX_CS5_B = DeltaX_SBIGXL_B = " + format(DeltaX_CS5_B/1000 , '.3f') + "\n" +
                         "    DeltaY_CS5_B = DeltaY_SBIGXL_B = " + format(DeltaY_CS5_B/1000 , '.3f') + "\n\n" +
                         "    DeltaX_CS5_C = DeltaX_SBIGXL_C = " + format(DeltaX_CS5_C/1000 , '.3f') + "\n" +
                         "    DeltaY_CS5_C = DeltaY_SBIGXL_C = " + format(DeltaY_CS5_C/1000 , '.3f') + "\n\n" +
                         
                         "Using: Target Pixel CS5 Location (mm) = Nominal CS5 + DeltaCS5\n" +
                         "Calculated using triangle point A:\n" +
                         "    CS5X(A) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][0]) + " + " + format(DeltaX_CS5_A/1000, '.3f') + " = " + 
                         format(CS5XA, '.3f') + "\n" +
                         "    CS5Y(A) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][1]) + " + " + format(DeltaY_CS5_A/1000, '.3f') + " = " + 
                         format(CS5YA, '.3f') + "\n\n" +
                         "Calculated using triangle point B:\n" +
                         "    CS5X(B) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][0]) + " + " + format(DeltaX_CS5_B/1000, '.3f') + " = " + 
                         format(CS5XB, '.3f') + "\n" +
                         "    CS5Y(B) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][1]) + " + " + format(DeltaY_CS5_B/1000, '.3f') + " = " + 
                         format(CS5YB, '.3f') + "\n\n" +
                         "Calculated using triangle point C:\n" +
                         "    CS5X(C) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][0]) + " + " + format(DeltaX_CS5_C/1000, '.3f') + " = " + 
                         format(CS5XC, '.3f') + "\n" +
                         "    CS5Y(C) (mm) = " + str(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][1]) + " + " + format(DeltaY_CS5_C/1000, '.3f') + " = " + 
                         format(CS5YC, '.3f')) 
        
        ###########################################################################
        ###Image (pixelDistanceToCheckPointX, pixelDistanceToCheckPointY) with SBIGXL
        ###########################################################################                 
        top = tk.Toplevel()
        top.title("\nImage pixel (" + str(self.pixelDistanceToCheckPointX) + ", " + str(self.pixelDistanceToCheckPointY) + ")?")
        aboutMessage = str("\nAre you ready to image pixel (" + str(self.pixelDistanceToCheckPointX) + ", " + str(self.pixelDistanceToCheckPointY) + ")?")
        faah.pageLogging(consoleLog, logFile, aboutMessage)
        msg = tk.Message(top, text=aboutMessage)
        msg.pack()
        button = tk.Button(top, text="Ready", command=top.destroy)
        button.pack()
        top.wait_window()
        
        #Get images for target pixel
        self.logFile = logFile #because faah.createDir get the logfile name from metModeSelf.logFile.name
        faah.createDir(self.CCDSelection, self, "(" + str(self.pixelDistanceToCheckPointX) + ", " + str(self.pixelDistanceToCheckPointY) + ")")
        imageArray4DTarget, filelistTarget = faah.openAllFITSImagesInDirectory()
        
        #Centroid
        tar = round(len(filelistTarget)/2) #select c focused image from array c
        _ , subArrayBoxSizeTarget, maxLocTarget = cF.findFIFInImage(imageArray4DTarget[tar])
        
        #Planet Mode
        xOffsetTarget, yOffsetTarget, _ = pM.readFitsHeader(imageArray4DTarget, filelistTarget, consoleLog, logFile)
        
        #Use alternate methods to centroid pinhole image
        #    gmsCentroid: Gaussian Marginal Sum (GMS) Centroid Method.
        xCenGMSTarget, yCenGMSTarget, _, _ = gmsCentroid(imageArray4DTarget[tar], maxLocTarget[1], maxLocTarget[0], 
                                                         int(round(subArrayBoxSizeTarget/2)), int(round(subArrayBoxSizeTarget/2)), axis='both', verbose=False)
        
        #Find distance in um to CCD Origin  
        DeltaX_SBIGXL_Target = (xCenGMSTarget + xOffsetTarget) * pixelSize
        DeltaY_SBIGXL_Target = (yCenGMSTarget + yOffsetTarget) * pixelSize
        
        #Rotation Matrix
        if angleRz < 0:
            DeltaX_CS5_Target = (DeltaX_SBIGXL_Target * np.cos(math.radians(angleRz))) - (DeltaY_SBIGXL_Target * np.sin(math.radians(angleRz)))
            DeltaY_CS5_Target = (DeltaX_SBIGXL_Target * np.sin(math.radians(angleRz))) + (DeltaY_SBIGXL_Target * np.cos(math.radians(angleRz)))
        elif angleRz > 0:
            DeltaX_CS5_Target = (DeltaX_SBIGXL_Target * np.cos(math.radians(angleRz))) + (DeltaY_SBIGXL_Target * np.sin(math.radians(angleRz)))
            DeltaY_CS5_Target = (-DeltaX_SBIGXL_Target * np.sin(math.radians(angleRz))) + (DeltaY_SBIGXL_Target * np.cos(math.radians(angleRz)))
        else:
            DeltaX_CS5_Target = DeltaX_SBIGXL_Target
            DeltaY_CS5_Target = DeltaY_SBIGXL_Target    
        
        ###########################################################################
        ###Apply Calibration Offset
        ###########################################################################   
       
        faah.pageLogging(consoleLog, logFile,
                        "CALIBRATION OFFSET APPLIED\n" + "For target pixel (" + str(self.pixelDistanceToCheckPointX) + ", " + str(self.pixelDistanceToCheckPointY) + ")\n" +
                        "Using: CS5 CCD Origin (mm) = CS5 CCD target pixel with no offset (mm) + calibration Offset (mm)\n" +
                        "Calibration Offset (mm): (" + format(calOffX/1000, '.3f') + ", " + format(calOffY/1000, '.3f') + ")\n\n"
                        "    CS5 CCD target pixel X(A) = " + format(CS5XA, '.3f') + " + " + format(calOffX/1000, '.3f') + " = " + format(CS5XA + calOffX/1000, '.3f') + "\n" +
                        "    CS5 CCD target pixel Y(A) = " + format(CS5YA, '.3f') + " + " + format(calOffY/1000, '.3f') + " = " + format(CS5YA + calOffY/1000, '.3f') + "\n\n" +
                        "    CS5 CCD target pixel X(B) = " + format(CS5XB, '.3f') + " + " + format(calOffX/1000, '.3f') + " = " + format(CS5XB + calOffX/1000, '.3f') + "\n" +
                        "    CS5 CCD target pixel Y(B) = " + format(CS5YB, '.3f') + " + " + format(calOffY/1000, '.3f') + " = " + format(CS5YB + calOffY/1000, '.3f') + "\n\n" +
                        "    CS5 CCD target pixel X(C) = " + format(CS5XC, '.3f') + " + " + format(calOffX/1000, '.3f') + " = " + format(CS5XC + calOffX/1000, '.3f') + "\n" +
                        "    CS5 CCD target pixel Y(C) = " + format(CS5YC, '.3f') + " + " + format(calOffY/1000, '.3f') + " = " + format(CS5YC + calOffY/1000, '.3f') + "\n\n")
        
        ###########################################################################
        ###CCD Origin (pixel (0,0) in CS5 with offset)
        ###########################################################################          
        #Distance from target pixel to origin (um)
        faah.pageLogging(consoleLog, logFile,
                        "CALIBRATION OFFSET APPLIED\n" + "For pixel point (" + str(0) + ", " + str(0) + ")\n" +
                        "Using: CS5 CCD Origin (mm) = CS5 CCD target pixel with no offset (mm) + calibration Offset (mm) + (target point (pixel) * pixelSize (mm))\n" +
                        "Calibration Offset (mm): (" + format(calOffX/1000, '.3f') + ", " + format(calOffY/1000, '.3f') + ")\n\n" +
                        "    CS5 CCD Origin X(A) = " + format(CS5XA, '.3f') + " + " + format(calOffX/1000, '.3f') +  " + " + format((self.pixelDistanceToCheckPointX * pixelSize)/1000, '.3f') +
                         " = " + format(CS5XA + calOffX/1000 + ((self.pixelDistanceToCheckPointX * pixelSize)/1000), '.3f') + "\n" +
                        "    CS5 CCD Origin Y(A) = " + format(CS5YA, '.3f') + " + " + format(calOffY/1000, '.3f') +  " + " + format((self.pixelDistanceToCheckPointX * pixelSize)/1000, '.3f') +
                         " = " + format(CS5YA + calOffY/1000 + ((self.pixelDistanceToCheckPointX * pixelSize)/1000), '.3f') + "\n\n" +
                        "    CS5 CCD Origin X(B) = " + format(CS5XB, '.3f') + " + " + format(calOffX/1000, '.3f') +  " + " + format((self.pixelDistanceToCheckPointX * pixelSize)/1000, '.3f') +
                          " = " + format(CS5XB + calOffX/1000 + ((self.pixelDistanceToCheckPointX * pixelSize)/1000), '.3f') + "\n" +
                        "    CS5 CCD Origin Y(B) = " + format(CS5YB, '.3f') + " + " + format(calOffY/1000, '.3f') +  " + " + format((self.pixelDistanceToCheckPointX * pixelSize)/1000, '.3f') +
                          " = " + format(CS5YB + calOffY/1000 + ((self.pixelDistanceToCheckPointX * pixelSize)/1000), '.3f') + "\n\n" +
                        "    CS5 CCD Origin X(C) = " + format(CS5XC, '.3f') + " + " + format(calOffX/1000, '.3f') +  " + " + format((self.pixelDistanceToCheckPointX * pixelSize)/1000, '.3f') +
                          " = " + format(CS5XC + calOffX/1000 + ((self.pixelDistanceToCheckPointX * pixelSize)/1000), '.3f') + "\n" +
                        "    CS5 CCD Origin Y(C) = " + format(CS5YC, '.3f') + " + " + format(calOffY/1000, '.3f') +  " + " + format((self.pixelDistanceToCheckPointX * pixelSize)/1000, '.3f') +
                          " = " + format(CS5YC + calOffY/1000 + ((self.pixelDistanceToCheckPointX * pixelSize)/1000), '.3f') + "\n\n" +
                        "    CS5 CCD Origin X(" + str(self.pixelDistanceToCheckPointX) + ") = " + format(((CS5XA + CS5XB + CS5XC)/3), '.3f') + " + " + format(DeltaX_CS5_Target/1000, '.3f') + " + " + format(calOffX/1000, '.3f') +  " = " + format(((CS5XA + CS5XB + CS5XC)/3) + DeltaX_CS5_Target/1000 + calOffX/1000, '.3f') + "\n" +
                        "    CS5 CCD Origin Y(" + str(self.pixelDistanceToCheckPointY) + ") = " + format(((CS5YA + CS5YB + CS5YC)/3), '.3f') + " + " + format(DeltaY_CS5_Target/1000, '.3f') + " + " + format(calOffY/1000, '.3f') + " = " + format(((CS5YA + CS5YB + CS5YC)/3) + DeltaY_CS5_Target/1000 + calOffY/1000, '.3f') + "\n\n" +
                        "CS5 CCD Origin Average X (mm) = " + format(((CS5XA + CS5XB + CS5XC)/3) + calOffX/1000 + ((self.pixelDistanceToCheckPointX * pixelSize)/1000), '.3f') + "\n"
                        "CS5 CCD Origin Average Y (mm) = " + format(((CS5YA + CS5YB + CS5YC)/3) + calOffY/1000 + ((self.pixelDistanceToCheckPointY * pixelSize)/1000), '.3f') + "\n\n")
        
        ###########################################################################
        ###Set Calibration Offsets for class
        ########################################################################### 
        self.calOffX = calOffX
        self.calOffY = calOffY

        
    def _checkCameraOriginLocationSelectionWindow(self):
        '''
        Find the location of the CI camera's sensor origin in CS5 and instruct the user to view 
        the origin with the DMM to ensure that the tip/tilt/focus pinhole triangle was placed properly
        on the SBIG STXL sensor.
        '''
        ###########################################################################
        ###Construct menu
        ###########################################################################   
        top = tk.Toplevel()
        top.title("Check Camera Origin")
        
        #CCD Location Description
        tk.Label(top, text="Which CCD location\n would you like to\n measure?").grid(row=0, column=0, sticky='W')
        
        # NCCD
        NCCD = tk.Button(top, text="NCCD", command=lambda: self._setTrueAndExit(top, CCDLabel="NCCD"))
        NCCD.grid(row=1, column=0, sticky='W')
        
        # WCCD
        WCCD = tk.Button(top, text="WCCD", command=lambda: self._setTrueAndExit(top, CCDLabel="WCCD"))
        WCCD.grid(row=2, column=0, sticky='W')
        
        # SCCD
        SCCD = tk.Button(top, text="SCCD", command=lambda: self._setTrueAndExit(top, CCDLabel="SCCD"))
        SCCD.grid(row=3, column=0, sticky='W')
        
        # ECCD
        ECCD = tk.Button(top, text="ECCD", command=lambda: self._setTrueAndExit(top, CCDLabel="ECCD"))
        ECCD.grid(row=4, column=0, sticky='W')
        
        # CCCD
        CCCD = tk.Button(top, text="CCCD", command=lambda: self._setTrueAndExit(top, CCDLabel="CCCD"))
        CCCD.grid(row=5, column=0, sticky='W')
        
        top.wait_window()
           
    def _setTrueAndExit(self, windowVariable, CCDLabel):
        self.CCDSelection = CCDLabel
        windowVariable.destroy()
        
