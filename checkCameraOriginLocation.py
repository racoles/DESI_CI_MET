'''
@title checkCameraOriginLocation
@author: Rebecca Coles
Updated on Apr 23, 2018
Created on Mar 22, 2018

checkCameraOriginLocation
This module holds a series of functions that are used to find the origin of a CCD on the DESI CI in CS5.

'''

# Import #######################################################################################
import tkinter as tk
from tkinter.ttk import Separator
from fileAndArrayHandling import fileAndArrayHandling
from CCDOpsPlanetMode import CCDOpsPlanetMode
from centroidFIF import centroidFIF
from focusCurve import focusCurve
from alternateCentroidMethods import gmsCentroid
from cs5Offsets import cs5Offsets
################################################################################################

class checkCameraOriginLocation(object):
    
    CCDSelection = ""
    trianglePointLabel = ""
    #Pixel distance to origin check point
    pixelDistanceToCheckPoint = 10 #pixel location (rows = pixelDistanceToCheckPoint, columns = pixelDistanceToCheckPoint)
    #STi Pixel Size
    stipixel = 7.4
    
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
        PIDTSO_rows, PIDTSO_columns, CPOCID_X, CPOCID_Y, CPOCID_rows, CPOCID_columns, dmmMag = cs5off.calibrationScreen(consoleLog, logFile)
        #Calculate offset
        calOffX = ((PIDTSO_rows - CPOCID_rows)*self.stipixel)/dmmMag
        calOffY = ((PIDTSO_columns - CPOCID_columns)*self.stipixel)/dmmMag
        #Print offset
        faah.pageLogging(consoleLog, logFile, "Calibration Offset (pixels): (rows = " + format(PIDTSO_rows - CPOCID_rows, '.3f') + ", columns = " + format(PIDTSO_columns - CPOCID_columns, '.3f') + ")\n" +
                         "Calibration Offset (um): (" + format(calOffX, '.3f') + ", " + format(calOffY, '.3f') + ")")
        
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
        faah.pageLogging(self.consoleLog, self.logFile, aboutMessageA)
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
        faah.pageLogging(self.consoleLog, self.logFile, aboutMessageB)
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
                            " ," + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + 'C'][1], '.3f') + ")")
        faah.pageLogging(self.consoleLog, self.logFile, aboutMessageC)
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
        ###Calculate the distance to the sensor origin using centroided image.
        ###########################################################################  
        #Find distance in um to CCD Origin  
        
        DeltaX_SBIGXL_A = ((self.xA) - self.pixelDistanceToCheckPoint) * self.pixelSize
        DeltaY_SBIGXL_A = ((self.yA) - self.pixelDistanceToCheckPoint) * self.pixelSize
        
        DeltaX_SBIGXL_B = ((self.xB) - self.pixelDistanceToCheckPoint) * self.pixelSize
        DeltaY_SBIGXL_B = ((self.yB) - self.pixelDistanceToCheckPoint) * self.pixelSize
        
        DeltaX_SBIGXL_C = ((self.xC) - self.pixelDistanceToCheckPoint) * self.pixelSize
        DeltaY_SBIGXL_C = ((self.yC) - self.pixelDistanceToCheckPoint) * self.pixelSize
        
        ###########################################################################
        ###Rotation Coordinate Transform from SBIG Coordinates to CS5 Coordinates
        ###Go to (pixelDistanceToCheckPoint, pixelDistanceToCheckPoint)
        ########################################################################### 
        #c(y)>b(y) = +Rz = Counter-Clockwise
        #b(y)>c(y) = -Rz = Clockwise

        if self.Rz > 0: #c(y)>b(y) = +Rz = Counter-Clockwise
            DeltaX_CS5_A = (DeltaX_SBIGXL_A * np.cos(math.radians(self.Rz))) - (DeltaY_SBIGXL_A * np.sin(math.radians(self.Rz)))
            DeltaY_CS5_A = (DeltaX_SBIGXL_A * np.sin(math.radians(self.Rz))) + (DeltaY_SBIGXL_A * np.cos(math.radians(self.Rz)))
            
            DeltaX_CS5_B = (DeltaX_SBIGXL_B * np.cos(math.radians(self.Rz))) - (DeltaY_SBIGXL_B * np.sin(math.radians(self.Rz)))
            DeltaY_CS5_B = (DeltaX_SBIGXL_B * np.sin(math.radians(self.Rz))) + (DeltaY_SBIGXL_B * np.cos(math.radians(self.Rz)))   
            
            DeltaX_CS5_C = (DeltaX_SBIGXL_C * np.cos(math.radians(self.Rz))) - (DeltaY_SBIGXL_C * np.sin(math.radians(self.Rz)))
            DeltaY_CS5_C = (DeltaX_SBIGXL_C * np.sin(math.radians(self.Rz))) + (DeltaY_SBIGXL_C * np.cos(math.radians(self.Rz)))       
            
            print("\nMove to pixel (" + str(self.pixelDistanceToCheckPoint) + ", " + str(self.pixelDistanceToCheckPoint) + ")\n\n" +
                         "Using: ((centroid(pixel)) - desiredPixel(pixel)) * pixelSize\n" +
                         "Distance in SBIGXL frame (mm):\n" +
                         "    DeltaX_SBIGXL_A = (" + format(self.xA , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaX_SBIGXL_A/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_A = (" + format(self.yA , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaY_SBIGXL_A/1000, '.3f') + "\n\n" +
                         "    DeltaX_SBIGXL_B = (" + format(self.xB , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaX_SBIGXL_B/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_B = (" + format(self.yB , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaY_SBIGXL_B/1000, '.3f') + "\n\n" +
                         "    DeltaX_SBIGXL_C = (" + format(self.xC , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaX_SBIGXL_C/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_C = (" + format(self.yC , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaY_SBIGXL_C/1000, '.3f') + "\n\n" +
                         
                         "Using: Counter-Clockwise Rotational Coordinate Transform\n" + "       DeltaX_CS5 = (DeltaX_SBIGXL * cos(Rz)) - (DeltaY_SBIGXL * sin(Rz))\n       DeltaY_CS5 = (DeltaX_SBIGXL * sin(Rz)) + (DeltaY_SBIGXL * cos(Rz))\n" +
                         "Distance in CS5 frame (mm):\n" +
                         "    DeltaX_CS5_A = (" + format(DeltaX_SBIGXL_A/1000, '.3f') + " * " + format(np.cos(math.radians(self.Rz)), '.3f') + ") - (" + format(DeltaY_SBIGXL_A/1000, '.3f') + " * " + format(np.sin(math.radians(self.Rz)), '.3f') + ") = "+ format(DeltaX_CS5_A/1000, '.3f') +"\n" +
                         "    DeltaY_CS5_A = (" + format(DeltaX_SBIGXL_A/1000, '.3f') + " * " + format(np.sin(math.radians(self.Rz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_A/1000, '.3f') + " * " + format(np.cos(math.radians(self.Rz)), '.3f') + ") = "+ format(DeltaY_CS5_A/1000, '.3f') +"\n\n" +
                         "    DeltaX_CS5_B = (" + format(DeltaX_SBIGXL_B/1000, '.3f') + " * " + format(np.cos(math.radians(self.Rz)), '.3f') + ") - (" + format(DeltaY_SBIGXL_B/1000, '.3f') + " * " + format(np.sin(math.radians(self.Rz)), '.3f') + ") = "+ format(DeltaX_CS5_B/1000, '.3f') +"\n" +
                         "    DeltaY_CS5_B = (" + format(DeltaX_SBIGXL_B/1000, '.3f') + " * " + format(np.sin(math.radians(self.Rz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_B/1000, '.3f') + " * " + format(np.cos(math.radians(self.Rz)), '.3f') + ") = "+ format(DeltaY_CS5_B/1000, '.3f') +"\n\n" +
                         "    DeltaX_CS5_C = (" + format(DeltaX_SBIGXL_C/1000, '.3f') + " * " + format(np.cos(math.radians(self.Rz)), '.3f') + ") - (" + format(DeltaY_SBIGXL_C/1000, '.3f') + " * " + format(np.sin(math.radians(self.Rz)), '.3f') + ") = "+ format(DeltaX_CS5_C/1000, '.3f') +"\n" +
                         "    DeltaY_CS5_C = (" + format(DeltaX_SBIGXL_C/1000, '.3f') + " * " + format(np.sin(math.radians(self.Rz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_C/1000, '.3f') + " * " + format(np.cos(math.radians(self.Rz)), '.3f') + ") = "+ format(DeltaY_CS5_C/1000, '.3f') +"\n\n" +
                         
                         "Using: Target Pixel CS5 Location (mm) = Nominal CS5 + DeltaCS5\n" +
                         "Calculated using triangle point A:\n" +
                         "    CS5X(A) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][0]) + " + " + format(DeltaX_CS5_A/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][0] + DeltaX_CS5_A/1000, '.3f') + "\n" +
                         "    CS5Y(A) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][1]) + " + " + format(DeltaY_CS5_A/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][1] + DeltaY_CS5_A/1000, '.3f') + "\n\n" +
                         "Calculated using triangle point B:\n" +
                         "    CS5X(B) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][0]) + " + " + format(DeltaX_CS5_B/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][0] + DeltaX_CS5_B/1000, '.3f') + "\n" +
                         "    CS5Y(B) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][1]) + " + " + format(DeltaY_CS5_B/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][1] + DeltaY_CS5_B/1000, '.3f') + "\n\n" +
                         "Calculated using triangle point C:\n" +
                         "    CS5X(C) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][0]) + " + " + format(DeltaX_CS5_C/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][0] + DeltaX_CS5_C/1000, '.3f') + "\n" +
                         "    CS5Y(C) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][1]) + " + " + format(DeltaY_CS5_C/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][1] + DeltaY_CS5_C/1000, '.3f')) 
            
        elif self.Rz < 0: #b(y)>c(y) = -Rz = Clockwise
            DeltaX_CS5_A = (DeltaX_SBIGXL_A * np.cos(math.radians(self.Rz))) + (DeltaY_SBIGXL_A * np.sin(math.radians(self.Rz)))
            DeltaY_CS5_A = (-DeltaX_SBIGXL_A * np.sin(math.radians(self.Rz))) + (DeltaY_SBIGXL_A * np.cos(math.radians(self.Rz)))
            
            DeltaX_CS5_B = (DeltaX_SBIGXL_B * np.cos(math.radians(self.Rz))) + (DeltaY_SBIGXL_B * np.sin(math.radians(self.Rz)))
            DeltaY_CS5_B = (-DeltaX_SBIGXL_B * np.sin(math.radians(self.Rz))) + (DeltaY_SBIGXL_B * np.cos(math.radians(self.Rz)))   
            
            DeltaX_CS5_C = (DeltaX_SBIGXL_C * np.cos(math.radians(self.Rz))) + (DeltaY_SBIGXL_C * np.sin(math.radians(self.Rz)))
            DeltaY_CS5_C = (-DeltaX_SBIGXL_C * np.sin(math.radians(self.Rz))) + (DeltaY_SBIGXL_C * np.cos(math.radians(self.Rz))) 
            
            print("\nMove to pixel (" + str(self.pixelDistanceToCheckPoint) + ", " + str(self.pixelDistanceToCheckPoint) + ")\n\n" +
                         "Using: ((centroid(pixel)) - desiredPixel(pixel)) * pixelSize\n" +
                         "Distance in SBIGXL frame (mm):\n" +
                         "    DeltaX_SBIGXL_A = (" + format(self.xA , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaX_SBIGXL_A/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_A = (" + format(self.yA , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaY_SBIGXL_A/1000, '.3f') + "\n\n" +
                         "    DeltaX_SBIGXL_B = (" + format(self.xB , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaX_SBIGXL_B/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_B = (" + format(self.yB , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaY_SBIGXL_B/1000, '.3f') + "\n\n" +
                         "    DeltaX_SBIGXL_C = (" + format(self.xC , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaX_SBIGXL_C/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_C = (" + format(self.yC , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaY_SBIGXL_C/1000, '.3f') + "\n\n" +
                         
                         "Using: Clockwise Rotational Coordinate Transform\n" + "       DeltaX_CS5 = (DeltaX_SBIGXL * cos(Rz)) + (DeltaY_SBIGXL * sin(Rz))\n       DeltaY_CS5 = (-DeltaX_SBIGXL * sin(Rz)) + (DeltaY_SBIGXL * cos(Rz))\n" +
                         "Distance in CS5 frame (mm):\n" +
                         "    DeltaX_CS5_A = (" + format(DeltaX_SBIGXL_A/1000, '.3f') + " * " + format(np.cos(math.radians(self.Rz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_A/1000, '.3f') + " * " + format(np.sin(math.radians(self.Rz)), '.3f') + ") = " + format(DeltaX_CS5_A/1000, '.3f') + "\n" +
                         "    DeltaY_CS5_A = (" + format(-DeltaX_SBIGXL_A/1000, '.3f') + " * " + format(np.sin(math.radians(self.Rz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_A/1000, '.3f') + " * " + format(np.cos(math.radians(self.Rz)), '.3f') + ") = " + format(DeltaY_CS5_A/1000, '.3f') + "\n\n" +
                         "    DeltaX_CS5_B = (" + format(DeltaX_SBIGXL_B/1000, '.3f') + " * " + format(np.cos(math.radians(self.Rz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_B/1000, '.3f') + " * " + format(np.sin(math.radians(self.Rz)), '.3f') + ") = " + format(DeltaX_CS5_B/1000, '.3f') +"\n" +
                         "    DeltaY_CS5_B = (" + format(-DeltaX_SBIGXL_B/1000, '.3f') + " * " + format(np.sin(math.radians(self.Rz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_B/1000, '.3f') + " * " + format(np.cos(math.radians(self.Rz)), '.3f') + ") = " + format(DeltaY_CS5_B/1000, '.3f') +"\n\n" +
                         "    DeltaX_CS5_C = (" + format(DeltaX_SBIGXL_C/1000, '.3f') + " * " + format(np.cos(math.radians(self.Rz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_C/1000, '.3f') + " * " + format(np.sin(math.radians(self.Rz)), '.3f') + ") = " +  format(DeltaX_CS5_C/1000, '.3f') +"\n" +
                         "    DeltaY_CS5_C = (" + format(-DeltaX_SBIGXL_C/1000, '.3f') + " * " + format(np.sin(math.radians(self.Rz)), '.3f') + ") + (" + format(DeltaY_SBIGXL_C/1000, '.3f') + " * " + format(np.cos(math.radians(self.Rz)), '.3f') + ") = " + format(DeltaY_CS5_C/1000, '.3f') +"\n\n" +
                         
                         "Using: Target Pixel CS5 Location (mm) = Nominal CS5 + DeltaCS5\n" +
                         "Calculated using triangle point A:\n" +
                         "    CS5X(A) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][0]) + " + " + format(DeltaX_CS5_A/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][0] + DeltaX_CS5_A/1000, '.3f') + "\n" +
                         "    CS5Y(A) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][1]) + " + " + format(DeltaY_CS5_A/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][1] + DeltaY_CS5_A/1000, '.3f') + "\n\n" +
                         "Calculated using triangle point B:\n" +
                         "    CS5X(B) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][0]) + " + " + format(DeltaX_CS5_B/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][0] + DeltaX_CS5_B/1000, '.3f') + "\n" +
                         "    CS5Y(B) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][1]) + " + " + format(DeltaY_CS5_B/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][1] + DeltaY_CS5_B/1000, '.3f') + "\n\n" +
                         "Calculated using triangle point C:\n" +
                         "    CS5X(C) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][0]) + " + " + format(DeltaX_CS5_C/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][0] + DeltaX_CS5_C/1000, '.3f') + "\n" +
                         "    CS5Y(C) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][1]) + " + " + format(DeltaY_CS5_C/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][1] + DeltaY_CS5_C/1000, '.3f')) 
               
        else:
            print("Rz = 0: no rotational transform needed.")
            
            DeltaX_CS5_A = DeltaX_SBIGXL_A
            DeltaY_CS5_A = DeltaY_SBIGXL_A
            
            DeltaX_CS5_B = DeltaX_SBIGXL_B
            DeltaY_CS5_B = DeltaY_SBIGXL_B   
            
            DeltaX_CS5_C = DeltaX_SBIGXL_C
            DeltaY_CS5_C = DeltaY_SBIGXL_C 
            
            print("\nMove to pixel (" + str(self.pixelDistanceToCheckPoint) + ", " + str(self.pixelDistanceToCheckPoint) + ")\n\n" +
                         "Using: ((centroid(pixel)) - desiredPixel(pixel)) * pixelSize\n" +
                         "Distance in SBIGXL frame (mm):\n" +
                         "    DeltaX_SBIGXL_A = (" + format(self.xA , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaX_SBIGXL_A/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_A = (" + format(self.yA , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaY_SBIGXL_A/1000, '.3f') + "\n\n" +
                         "    DeltaX_SBIGXL_B = (" + format(self.xB , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaX_SBIGXL_B/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_B = (" + format(self.yB , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaY_SBIGXL_B/1000, '.3f') + "\n\n" +
                         "    DeltaX_SBIGXL_C = (" + format(self.xC , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaX_SBIGXL_C/1000, '.3f') + "\n" +
                         "    DeltaY_SBIGXL_C = (" + format(self.yC , '.3f') + ") - " + str(self.pixelDistanceToCheckPoint) + " * " + str(self.pixelSize) + " = " + format(DeltaY_SBIGXL_C/1000, '.3f') + "\n\n" +
                         
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
                         "    CS5X(A) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][0]) + " + " + format(DeltaX_CS5_A/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][0] + DeltaX_CS5_A/1000, '.3f') + "\n" +
                         "    CS5Y(A) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][1]) + " + " + format(DeltaY_CS5_A/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][1] + DeltaY_CS5_A/1000, '.3f') + "\n\n" +
                         "Calculated using triangle point B:\n" +
                         "    CS5X(B) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][0]) + " + " + format(DeltaX_CS5_B/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][0] + DeltaX_CS5_B/1000, '.3f') + "\n" +
                         "    CS5Y(B) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][1]) + " + " + format(DeltaY_CS5_B/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][1] + DeltaY_CS5_B/1000, '.3f') + "\n\n" +
                         "Calculated using triangle point C:\n" +
                         "    CS5X(C) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][0]) + " + " + format(DeltaX_CS5_C/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][0] + DeltaX_CS5_C/1000, '.3f') + "\n" +
                         "    CS5Y(C) (mm) = " + str(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][1]) + " + " + format(DeltaY_CS5_C/1000, '.3f') + " = " + 
                         format(self.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][1] + DeltaY_CS5_C/1000, '.3f')) 
        
        ###########################################################################
        ###Image (pixelDistanceToCheckPoint, pixelDistanceToCheckPoint) with SBIGXL
        ###########################################################################                 
        top = tk.Toplevel()
        top.title("Image pixel (" + str(self.pixelDistanceToCheckPoint) + ", " + str(self.pixelDistanceToCheckPoint) + ")?")
        aboutMessage = str("Are you ready to image pixel (" + str(self.pixelDistanceToCheckPoint) + ", " + str(self.pixelDistanceToCheckPoint) + ")?")
        faah.pageLogging(consoleLog, logFile, aboutMessage)
        msg = tk.Message(top, text=aboutMessage)
        msg.pack()
        button = tk.Button(top, text="Ready", command=top.destroy)
        button.pack()
        top.wait_window()
        imageArray4DPIX, filelistPIX = faah.openAllFITSImagesInDirectory()
        
        #Centroid
        #Get location of pinhole image in (rows, columns)
        pixpix = round(len(filelistPIX)/2)
        _ , subArrayBoxSizePIX, maxLocPIX = cF.findFIFInImage(imageArray4DPIX[pixpix])
        
        #Account for planet mode
        xOffsetPIX, yOffsetPIX, _ = pM.readFitsHeader(imageArray4DA, filelistA, consoleLog, logFile)
        
        #Use alternate methods to centroid pinhole image
        #    gmsCentroid: Gaussian Marginal Sum (GMS) Centroid Method.
        xCenGMSPIX, yCenGMSPIX, _, _ = gmsCentroid(imageArray4DPIX[pixpix], maxLocPIX[1], maxLocPIX[0], 
                                                         int(round(subArrayBoxSizePIX/2)), int(round(subArrayBoxSizePIX/2)), axis='both', verbose=False)
        
        #report pixel centroid location
        faah.pageLogging(consoleLog, logFile, "Centroid for pixel (" + str(self.pixelDistanceToCheckPoint) + ", " + str(self.pixelDistanceToCheckPoint) + ") found at:" +
                         "row = " + format(xCenGMSPIX + xOffsetPIX, '.3f') + ", columns = " + format(yCenGMSPIX + yOffsetPIX, '.3f'))
        
        #calculate location of CCD (0,0) in CS5 using triangle a, b, c, and pixel  
        faah.pageLogging(consoleLog, logFile, "CS5 CCD ORIGIN\n\n" +
                         "Using: CS5 Nominal Triangle Point (um) - [centroided (pixel) * pixelSize]\n" +
                         "NO CALIBRATION OFFSET APPLIED\n" +
                         "    CS5 CCD Origin X(A) = " + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][0] - ((xCenGMSA + xOffsetA) * pixelSize), '.3f') + "\n" +
                         "    CS5 CCD Origin Y(A) = " + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][1] - ((yCenGMSA + yOffsetA) * pixelSize), '.3f') + "\n\n" +
                         "    CS5 CCD Origin X(B) = " + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][0] - ((xCenGMSB + xOffsetB) * pixelSize), '.3f') + "\n" +
                         "    CS5 CCD Origin Y(B) = " + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][1] - ((yCenGMSB + yOffsetB) * pixelSize), '.3f') + "\n\n" +
                         "    CS5 CCD Origin X(C) = " + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][0] - ((xCenGMSC + xOffsetC) * pixelSize), '.3f') + "\n" +
                         "    CS5 CCD Origin Y(C) = " + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][1] - ((yCenGMSC + yOffsetC) * pixelSize), '.3f') + "\n\n" +
                         "CALIBRATION OFFSET APPLIED\n" +
                         "Calibration Offset (um): (" + str(calOffX) + ", " + str(calOffY) + ")\n"
                         "    CS5 CCD Origin X(A) = " + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][0] - ((xCenGMSA + xOffsetA) * pixelSize) + calOffX, '.3f') + "\n" +
                         "    CS5 CCD Origin Y(A) = " + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "A"][1] - ((yCenGMSA + yOffsetA) * pixelSize) + calOffY, '.3f') + "\n\n" +
                         "    CS5 CCD Origin X(B) = " + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][0] - ((xCenGMSB + xOffsetB) * pixelSize) + calOffX, '.3f') + "\n" +
                         "    CS5 CCD Origin Y(B) = " + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "B"][1] - ((yCenGMSB + yOffsetB) * pixelSize) + calOffY, '.3f') + "\n\n" +
                         "    CS5 CCD Origin X(C) = " + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][0] - ((xCenGMSC + xOffsetC) * pixelSize) + calOffX, '.3f') + "\n" +
                         "    CS5 CCD Origin Y(C) = " + format(fC.trianglePonitCCDLocationsCS5[self.CCDSelection + "C"][1] - ((yCenGMSC + yOffsetC) * pixelSize) + calOffY, '.3f'))
        
        
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
        NCCD_Center = tk.Button(top, text="NCCD: pixel (" + str(self.pixelDistanceToCheckPoint) + ","  + str(self.pixelDistanceToCheckPoint) + ")", command=lambda: self._setTrueAndExit(top, CCDLabel="NCCD"))
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
        WCCD_Center = tk.Button(top, text="WCCD: pixel (" + str(self.pixelDistanceToCheckPoint) + ","  + str(self.pixelDistanceToCheckPoint) + ")", command=lambda: self._setTrueAndExit(top, CCDLabel="WCCD"))
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
        SCCD_Center = tk.Button(top, text="SCCD: pixel (" + str(self.pixelDistanceToCheckPoint) + ","  + str(self.pixelDistanceToCheckPoint) + ")", command=lambda: self._setTrueAndExit(top, CCDLabel="SCCD"))
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
        ECCD_Center = tk.Button(top, text="ECCD: pixel (" + str(self.pixelDistanceToCheckPoint) + ","  + str(self.pixelDistanceToCheckPoint) + ")", command=lambda: self._setTrueAndExit(top, CCDLabel="ECCD"))
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
        CCCD_Center = tk.Button(top, text="CCCD: pixel (" + str(self.pixelDistanceToCheckPoint) + ","  + str(self.pixelDistanceToCheckPoint) + ")", command=lambda: self._setTrueAndExit(top, CCDLabel="CCCD"))
        CCCD_Center.grid(row=15, column=3)
        
        top.wait_window()
           
    def _setTrueAndExit(self, windowVariable, CCDLabel, trianglePointLabel=""):
        self.CCDSelection = CCDLabel
        if trianglePointLabel != "":
            self.trianglePointLabel = trianglePointLabel
        windowVariable.destroy()
        
