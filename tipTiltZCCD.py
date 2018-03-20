'''
@title tipTiltZCCD
@author: Rebecca Coles
Updated on Mar 06, 2018
Created on Jan 18, 2018

tipTiltZCCD
This module holds a series of functions that are used to find the tip/tilt/Z of a CCD on the DESI CI.

Modules:
'''

# Import #######################################################################################
from fileAndArrayHandling import fileAndArrayHandling
from focusCurve import focusCurve
import numpy as np
from centroidFIF import centroidFIF
import math
################################################################################################

class tipTiltZCCD(object):
    
    def __init__(self):
        '''
        Constructor
        '''
    
    def findTipTiltZ(self, imageA, imageB, imageC, Az, Bz, Cz, Az_nominal, Bz_nominal, Cz_nominal, CCDLabel, triangleSideLength, micrometerDistance, consoleLog, logFile, TTFThread = 0.5, TTFThreadOD = 6):
        ###########################################################################
        ###Get adjustment ratios
        ###########################################################################     
        #Since the triangle of micrometers is much larger than the small ABC
        #imaginary triangle that we create on the sensor surface, we need to
        #calculate how an adjustment to the micrometers affect the ABC heights. 
        triangleAdjustmentRatio = micrometerDistance/triangleSideLength
        
        ###########################################################################
        ###Get the tip/tilt/z deltas
        ###########################################################################   
        #Tip
        AzDeltaTip, BzDeltaTip, CzDeltaTip = self.tipCCD(Az, Bz, Cz, Az_nominal, Bz_nominal, Cz_nominal, CCDLabel, consoleLog, logFile)
        #Tilt
        AzDeltaTilt, BzDeltaTilt, CzDeltaTilt = self.tiltCCD(Az, Bz, Cz, Az_nominal, Bz_nominal, Cz_nominal, CCDLabel, consoleLog, logFile)
        #Z
        CenterDeltaZ = self.ZCCD(Az, Bz, Cz, CCDLabel, consoleLog, logFile)
        #Rz
        angleRz = self.rz(imageB, imageC, CCDLabel, triangleSideLength, consoleLog, logFile)

        ###########################################################################
        ###Find Needed Micrometer Adjustments 
        ###########################################################################
        AturnDistanceDegrees = 99999999
        BturnDistanceDegrees = 99999999
        CturnDistanceDegrees = 99999999
        turnA = "None"
        turnB = "None"
        turnC = "None"
        
        faah = fileAndArrayHandling()
        fC = focusCurve()
        
        #If the A height isn't equal to the nominal height
        if AzDeltaTip or AzDeltaTilt != 0:
            #is A too low or too high (clockwise = down, counter-clockwise = up relative to CS5 +Z)
            if AzDeltaTip < 0: 
                turnA = 'counter-clockwise' 
            else: 
                turnA = 'clockwise'
            #How many turns will it take to reach nominal height?
            AturnDistance_um = np.absolute(AzDeltaTip*triangleAdjustmentRatio)/(TTFThread*1000) #X turns = needed height / micrometer pitch (height per one full turn). Convert mm to microns.
            AturnDistanceDegrees = faah.decNonZeroRound(np.absolute(AturnDistance_um/((TTFThreadOD*1000)/360))) #to get number of degrees. 1 degree = fifThreadODMicrons/360 um. Convert mm to microns.
            
        #If the B height isn't equal to the nominal height
        if BzDeltaTip or BzDeltaTilt != 0:
            #is B too low or too high (clockwise = down, counter-clockwise = up)
            if BzDeltaTip < 0: 
                turnB = 'counter-clockwise' 
            else: 
                turnB = 'clockwise'
            #How many turns will it take to reach nominal height?
            BturnDistance_um = np.absolute(BzDeltaTip*triangleAdjustmentRatio)/(TTFThread*1000) #X turns = needed height / fif pitch (height per one full turn). Convert mm to microns.
            BturnDistanceDegrees = faah.decNonZeroRound(np.absolute(BturnDistance_um/((TTFThreadOD*1000)/360))) #to get number of degrees. 1 degree = fifThreadODMicrons/360 um. Convert mm to microns.
        
        #If the C height isn't equal to the nominal height
        if CzDeltaTip or CzDeltaTilt or CenterDeltaZ != 0:
            #is A too low or too high (clockwise = down, counter-clockwise = up)
            if CzDeltaTip < 0: 
                turnC = 'counter-clockwise' 
            else: 
                turnC = 'clockwise'
            #How many turns will it take to reach nominal height?
            CturnDistance_um = np.absolute(CzDeltaTip*triangleAdjustmentRatio)/(TTFThread*1000) #X turns = needed height / fif pitch (height per one full turn). Convert mm to microns.
            CturnDistanceDegrees = faah.decNonZeroRound(np.absolute(CturnDistance_um/((TTFThreadOD*1000)/360))) #to get number of degrees. 1 degree = fifThreadODMicrons/360 um. Convert mm to microns.
            
        ###########################################################################
        ###Send Warning Message
        ###########################################################################
        #micrometer ticks to turn: 360 degrees / 50 ticks on TTF micrometers = 7.2 degrees per tick
        
####ADD B-C distance
        
        faah.pageLogging(consoleLog, logFile, 
                "WARNING: the" + str(CCDLabel) +" camera Z height is not equal to the nominal height.\n" + "        The current micrometer thread pitch is " +
                str(TTFThread) + "mm (" + str(TTFThread*1000) + "um), with a OD of " + str(TTFThreadOD) + "mm (" +  str(TTFThreadOD*1000) + "um)." + 
                "\n        To adjust the camera to the nominal height, adjust the micrometers as:\n" + 
                "        Micrometer A: " + format(AturnDistanceDegrees, '.1f') + " degrees " + turnA + ", or " + format(AturnDistanceDegrees/7.2, '.1f') + " micrometer ticks.\n" +
                "        Micrometer B: " + format(BturnDistanceDegrees, '.1f') + " degrees " + turnB + ", or " + format(BturnDistanceDegrees/7.2, '.1f') + " micrometer ticks.\n" +
                "        Micrometer C: " + format(CturnDistanceDegrees, '.1f') + " degrees " + turnC +  ", or " + format(CturnDistanceDegrees/7.2, '.1f') + " micrometer ticks.\n",
                warning = True)
        
    def tipCCD(self, Az, Bz, Cz, Az_nominal, Bz_nominal, Cz_nominal, CCDLabel, consoleLog, logFile):
        '''
        Calculate CCD tip
        
        CCDLabel = N,W,S,E,C,Other
        
        A(Z) _measured = A(Z) _nominal 
        B(Z)_measured = C(Z) _measured = B(Z)_nominal = C(Z) _nominal
        North, West, South, and East CCDs:
            A(Z) _measured > B(Z) _measured && C(Z) _measured (by a known distance)
        Center CCD:
            A(Z) _measured = B(Z) _measured = C(Z) _measured = A(Z) _nominal = B(Z) _nominal = C(Z) _nominal
        '''                    
        ###########################################################################
        ###Boundary Condition Check 
        ###########################################################################
        faah = fileAndArrayHandling()
        faah.pageLogging(consoleLog, logFile, 
                                      "Checking " + str(CCDLabel) + " TIP:")

        faah.pageLogging(consoleLog, logFile, 
                                        "    Condition #1: A(Z)_measured = A(Z)_nominal\n" + 
                                        "        A(Z)_measured = " + str(Az) + "um\n" + 
                                        "        A(Z)_nominal = " + str(Az_nominal) + "um\n" )
        faah.pageLogging(consoleLog, logFile, 
                                        "    Condition #2: B(Z)_measured = C(Z)_measured = B(Z)_nominal = C(Z)_nominal\n" + 
                                        "        B(Z)_measured = " + str(Bz) + "um\n" + 
                                        "        B(Z)_nominal = " + str(Bz_nominal) + "um\n" +
                                        "        C(Z)_measured = " + str(Cz) + "um\n" +     
                                        "        C(Z)_nominal = " + str(Cz_nominal) + "um\n")  
        #N,W,S,E
        if CCDLabel == "NCCD" or CCDLabel == "WCCD" or CCDLabel == "SCCD" or CCDLabel == "ECCD": 
            faah.pageLogging(consoleLog, logFile, 
                                        "    Condition #3: A(Z)_measured > B(Z)_measured && C(Z)_measured\n" + 
                                        "        A(Z)_measured = " + str(Az) + "um\n" + 
                                        "        B(Z)_measured = " + str(Bz) + "um\n" + 
                                        "        C(Z)_measured = " + str(Cz) + "um\n")
        #C
        if CCDLabel == "CCCD":
            faah.pageLogging(consoleLog, logFile, 
                                        "    Condition #3: [A(Z) = B(Z) = C(Z)]_measured  = [A(Z) = B(Z) = C(Z)]_nominal\n" + 
                                        "        A(Z)_measured = " + str(Az) + "um\n" + 
                                        "        B(Z)_measured = " + str(Bz) + "um\n" + 
                                        "        C(Z)_measured = " + str(Cz) + "um\n")
        #Other
        if CCDLabel == "Other":
            faah.pageLogging(consoleLog, logFile, 
                                        "CCD selection: Other. Not able to calculate Tip.")

        #Return deltas
        return Az_nominal-Az, Bz_nominal-Bz, Cz_nominal-Cz
        
    def tiltCCD(self, Az, Bz, Cz, Az_nominal, Bz_nominal, Cz_nominal, CCDLabel, consoleLog, logFile):
        '''
        Calculate CCD tilt
        
        A(Z) _measured = A(Z) _nominal 
        B(Z)_measured = C(Z) _measured = B(Z)_nominal = C(Z) _nominal
        '''          
        ###########################################################################
        ###Boundry Condition Check 
        ###########################################################################
        faah = fileAndArrayHandling()
        faah.pageLogging(consoleLog, logFile, 
                                      "Checking " + str(CCDLabel) + " TILT:")
        #N,W,S,E
        if CCDLabel == "NCCD" or CCDLabel == "WCCD" or CCDLabel == "SCCD" or CCDLabel == "ECCD": 
                faah.pageLogging(consoleLog, logFile, 
                                        "    Condition #1: A(Z)_measured = A(Z)_nominal\n" + 
                                        "        A(Z)_measured = " + str(Az) + "um\n" + 
                                        "        A(Z)_nominal = " + str(Az_nominal) + "um\n" )
                faah.pageLogging(consoleLog, logFile, 
                                        "    Condition #2: B(Z)_measured = C(Z)_measured = B(Z)_nominal = C(Z)_nominal\n" + 
                                        "        B(Z)_measured = " + str(Bz) + "um\n" + 
                                        "        B(Z)_nominal = " + str(Bz_nominal) + "um\n" +
                                        "        C(Z)_measured = " + str(Cz) + "um\n" +     
                                        "        C(Z)_nominal = " + str(Cz_nominal) + "um\n") 
        #C
        if CCDLabel == "CCCD":
            faah.pageLogging(consoleLog, logFile, 
                                        "    Condition #3: [A(Z) = B(Z) = C(Z)]_measured  = [A(Z) = B(Z) = C(Z)]_nominal\n" + 
                                        "        A(Z)_measured = " + str(Az) + "um\n" + 
                                        "        B(Z)_measured = " + str(Bz) + "um\n" + 
                                        "        C(Z)_measured = " + str(Cz) + "um\n")
        #Other
        if CCDLabel == "Other":
            faah.pageLogging(consoleLog, logFile, 
                                        "CCD selection: Other. Not able to calculate Tilt.")

        #Return deltas
        return Az_nominal-Az, Bz_nominal-Bz, Cz_nominal-Cz

    def ZCCD(self, Az, Bz, Cz, CCDLabel, consoleLog, logFile):
        '''
        Return CCD Z
        
        Z(Center) _measured = Z(Center) _nominal 
        A(Z) _measured = A(Z) _nominal 
        B(Z)_measured = C(Z) _measured = B(Z)_nominal = C(Z) _nominal
        '''            
        ###########################################################################
        ###Get nominal  and measured Z for CCD center
        ###########################################################################               
        fC = focusCurve()
        zCenter_measured = (Az + Bz + Cz)/3
        zCenter_nominal = fC.asphericFocalCurve(fC.CCDLocationsCS5[CCDLabel][0], fC.CCDLocationsCS5[CCDLabel][1])
        
        ###########################################################################
        ###Boundry Condition Check 
        ###########################################################################
        faah = fileAndArrayHandling()
        faah.pageLogging(consoleLog, logFile, 
                                      "Checking " + str(CCDLabel) + " CCD Center Z:")
        #N,W,S,E,C,Other
        faah.pageLogging(consoleLog, logFile, 
                                        "Condition: Center(Z)_measured = Center(Z)_nominal\n" + 
                                        "        Center(Z)_measured = " + str(zCenter_measured) + "um\n" + 
                                        "        Center(Z)_nominal = " + str(zCenter_nominal) + "um\n" )

        #Return deltas
        return zCenter_nominal-zCenter_measured
    
    def rz(self, imageB, imageC, CCDLabel, triangleSideLength, consoleLog, logFile):
        '''
        Camera Rz (angle) 
        
        For North, Center, Or South Cameras:
            B(x) = C(x)
        For East and West Cameras:
            B(y) = C(y)
        '''             

        #Centroid images
        cF = centroidFIF()
        fifSubArrayB, subArrayBoxSizeB, _  = cF.findFIFInImage(imageB)
        fifSubArrayC, subArrayBoxSizeC, _  = cF.findFIFInImage(imageC)
        
        ###########################################################################
        ###Report Rz 
        ###########################################################################
        angleRz = 99999
        
        faah = fileAndArrayHandling()
        faah.pageLogging(consoleLog, logFile, 
                                      "Checking " + str(CCDLabel) + " Rz about CS5X:")
             
        #If B and C aren't aligned (in either X or Y depending on the camera location)
        if CCDLabel == "NCCD":
            _, ycenB = cF.findCentroid(fifSubArrayB, int(subArrayBoxSizeB/2), int(subArrayBoxSizeB/2), extendbox = 3) 
            _, ycenC = cF.findCentroid(fifSubArrayC, int(subArrayBoxSizeC/2), int(subArrayBoxSizeC/2), extendbox = 3)
            if ycenB != ycenC:
                if ycenB > ycenC:     
                #calculate angle between B and C. Report in CS5 relative to +X: 180 degrees - BC angle
                #BC Should be parallel to CS5X. CCDLabel sensor origin is [180 degrees - BC angle] degrees Rz about CS5X.                
                    angleRz = math.degrees(np.arcsin((ycenB-ycenC)/triangleSideLength))
                    faah.pageLogging(consoleLog, logFile, "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + str(180-angleRz) + " degrees about CS5X." ) 
                if ycenB < ycenC:
                #calculate angle between B and C. Report in CS5 relative to +X: 180 degrees + BC angle
                #BC Should be parallel to CS5X. CCDLabel sensor origin is [180 degrees + BC angle] degrees Rz about CS5X.
                    angleRz = math.degrees(np.arcsin((ycenC-ycenB)/triangleSideLength))
                    faah.pageLogging(consoleLog, logFile, "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + str(180+angleRz) + " degrees about CS5X." )
            else:
                angleRz = 180
                faah.pageLogging(consoleLog, logFile, "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + str(angleRz) + " degrees about CS5X.\n        Sensor is properly aligned in Rz" ) 
                    
        if CCDLabel == "SCCD" or CCDLabel == "CCCD":
            _, ycenB = cF.findCentroid(fifSubArrayB, int(subArrayBoxSizeB/2), int(subArrayBoxSizeB/2), extendbox = 3) 
            _, ycenC = cF.findCentroid(fifSubArrayC, int(subArrayBoxSizeC/2), int(subArrayBoxSizeC/2), extendbox = 3)
            if ycenB != ycenC:
                if ycenB > ycenC:                
                #calculate angle between B and C. Report in CS5 relative to +X: 360 degrees - BC angle.
                #BC Should be parallel to CS5X. CCDLabel sensor origin is [360 degrees - BC angle] degrees Rz about CS5X.                 
                    angleRz = math.degrees(np.arcsin((ycenB-ycenC)/triangleSideLength))
                    faah.pageLogging(consoleLog, logFile, "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + str(360-angleRz) + " degrees about CS5X." ) 
                if ycenB < ycenC:
                #calculate angle between B and C. Report in CS5 relative to +X: 0 degrees + BC angle.
                #BC Should be parallel to CS5X. CCDLabel sensor origin is [0 degrees + BC angle] degrees Rz about CS5X.  
                    angleRz = math.degrees(np.arcsin((ycenC-ycenB)/triangleSideLength))
                    faah.pageLogging(consoleLog, logFile, "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + str(angleRz) + " degrees about CS5X." ) 
            else:
                angleRz = 0
                faah.pageLogging(consoleLog, logFile, "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + str(angleRz) + " degrees about CS5X.\n        Sensor is properly aligned in Rz" ) 
                
        if CCDLabel == "ECCD":
            _, ycenB = cF.findCentroid(fifSubArrayB, int(subArrayBoxSizeB/2), int(subArrayBoxSizeB/2), extendbox = 3) 
            _, ycenC = cF.findCentroid(fifSubArrayC, int(subArrayBoxSizeC/2), int(subArrayBoxSizeC/2), extendbox = 3)  
            if ycenB != ycenC:
                if ycenB > ycenC: 
                #calculate angle between B and C. Report in CS5 relative to +X: 270 degrees - BC angle 
                #BC Should be parallel to CS5Y. CCDLabel sensor origin is [270 degrees - BC angle] degrees Rz about CS5X.                 
                    angleRz = math.degrees(np.arcsin((ycenB-ycenC)/triangleSideLength))
                    faah.pageLogging(consoleLog, logFile, "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + str(270-angleRz) + " degrees about CS5X." ) 
                if ycenB < ycenC:               
                #calculate angle between B and C. Report in CS5 relative to +X: 270 degrees + BC angle
                #BC Should be parallel to CS5Y. CCDLabel sensor origin is [270 degrees + BC angle] degrees Rz about CS5X.           
                    angleRz = math.degrees(np.arcsin((ycenC-ycenB)/triangleSideLength)) 
                    faah.pageLogging(consoleLog, logFile, "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + str(270+angleRz) + " degrees about CS5X." )   
            else:
                angleRz = 270
                faah.pageLogging(consoleLog, logFile, "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + str(angleRz) + " degrees about CS5X.\n        Sensor is properly aligned in Rz" )     
                    
        if CCDLabel == "WCCD":        
            _, ycenB = cF.findCentroid(fifSubArrayB, int(subArrayBoxSizeB/2), int(subArrayBoxSizeB/2), extendbox = 3) 
            _, ycenC = cF.findCentroid(fifSubArrayC, int(subArrayBoxSizeC/2), int(subArrayBoxSizeC/2), extendbox = 3)  
            if ycenB != ycenC:
                if ycenB > ycenC: 
                #calculate angle between B and C. Report in CS5 relative to +X: 90 degrees - BC angle
                #BC Should be parallel to CS5Y. CCDLabel sensor origin is [90 degrees - BC angle] degrees Rz about CS5X. 
                    angleRz = math.degrees(np.arcsin((ycenB-ycenC)/triangleSideLength))
                    faah.pageLogging(consoleLog, logFile, "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + "Sensor origin is " + str(90-angleRz) + " degrees about CS5X." ) 
                if ycenB < ycenC:              
                #calculate angle between B and C. Report in CS5 relative to +X: 90 degrees + BC angle  
                #BC Should be parallel to CS5Y. CCDLabel sensor origin is [90 degrees + BC angle] degrees Rz about CS5X.           
                    angleRz = math.degrees(np.arcsin((ycenC-ycenB)/triangleSideLength)) 
                    faah.pageLogging(consoleLog, logFile, "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + "Sensor origin is " + str(90+angleRz) + " degrees about CS5X." ) 
            else:
                angleRz = 90
                faah.pageLogging(consoleLog, logFile, "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + "Sensor origin is " + str(angleRz) + " degrees about CS5X.\n        Sensor is properly aligned in Rz" )    
        
        if CCDLabel == "Other":
                faah.pageLogging(consoleLog, logFile, "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + "Sensor Other selected. Can't find Rz." )    
        
        return angleRz
       
    def distanceBetweenTrianglePoints(self, imageA, imageB, imageC, CCDLabel, consoleLog, logFile):             
        '''
        Find the measured distance between triangle points on the sensor.
        '''
        ###########################################################################
        ###Get images
        ########################################################################### 
        faah = fileAndArrayHandling()
        
        #Point A
        imageArray4DA, filelistA = faah.openAllFITSImagesInDirectory()
        aa = round(len(filelistA)/2) #select a focused image from array
        #Point B
        imageArray4DB, filelistB = faah.openAllFITSImagesInDirectory()
        bb = round(len(filelistB)/2) #select a focused image from array 
        #Point B
        imageArray4DC, filelistC = faah.openAllFITSImagesInDirectory()
        cc = round(len(filelistC)/2) #select a focused image from array 
        
        #Log image that will be used for centroiding
        faah = fileAndArrayHandling()
        faah.pageLogging(consoleLog, logFile, 
                         "Centroiding image for point A: " +  str(filelistA[aa]).replace('/', '\\') +
                         "\nCentroiding image for point B: " +  str(filelistA[bb]).replace('/', '\\') +
                         "\nCentroiding image for point C: " +  str(filelistA[cc]).replace('/', '\\'))
        
        ###########################################################################
        ###Centroid images
        ###########################################################################         
        cF = centroidFIF()
        fifSubArrayA, subArrayBoxSizeA, maxLocA = cF.findFIFInImage(imageArray4DA[aa])
        fifSubArrayB, subArrayBoxSizeB, maxLocB = cF.findFIFInImage(imageArray4DB[bb])
        fifSubArrayC, subArrayBoxSizeC, maxLocC = cF.findFIFInImage(imageArray4DC[cc])
        
        ###########################################################################
        ###Calculate Delta Distance (measured size of sides)
        ########################################################################### 
        fC = focusCurve() 
        #fC.tccs * a number um

        '''
Centroid (rows, columns)
A:(29.34, 1579.43)
B:(1317.67, 734.87)
C:(1400.67, 2267.27)
Nominal side length = 8*sqrt(3) = 13.856mm = 13856.406um

In pixels
A->B:
d(ab) = sqrt[(Bx-Ax)^2+(By-Ay)^2] = sqrt[(1317.67-29.34)^2+(734.87-1579.43)^2] = sqrt[(1288.33)^2+(-844.56)^2] = sqrt[2.3730757825*^6] = 1540.479075645 pixels
B->C:
d(bc) = sqrt[(Cx-Bx)^2+(Cy-By)^2] = sqrt[(1400.67-1317.67)^2+(2267.27-734.87)^2] = sqrt[(83)^2+(1532.4)^2] = sqrt[2.35513876*^6] = 1534.646135107374 pixels
C->A:
d(ca) = sqrt[(Ax-Cx)^2+(Ay-Cy)^2] = sqrt[(29.34-1400.67)^2+(1579.43-2267.27)^2] = sqrt[(-1371.33)^2+(-687.84)^2] = sqrt[2.3536698345*^6] = 1534.1674727682112 pixels

In Microns
A->B: 1540.479075645 pixels * 9um/pixel = 13864.311680805um
B->C: 1534.646135107374 pixels * 9um/pixel = 13811.815215966366um
C->A: 1534.1674727682112 pixels * 9um/pixel = 13807.507254913899um

Delta Distance (measured - nominal)
A->B: 13864.311680805 - 13856.406 = 7.905680804999065um
B->C: 13811.815215966366 - 13856.406 = -44.59078403364um
C->A: 13807.507254913899 - 13856.406 = -48.898745086111376um
'''