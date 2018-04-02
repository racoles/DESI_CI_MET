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
from alternateCentroidMethods import gmsCentroid
from CCDOpsPlanetMode import CCDOpsPlanetMode
import math
################################################################################################

class tipTiltZCCD(object):
    
    def __init__(self):
        '''
        Constructor
        '''
    
    def findTipTiltZ(self, imageArray4DA, filelistA, imageArray4DB, filelistB, imageArray4DC, filelistC, 
                     Az, Bz, Cz, Az_nominal, Bz_nominal, Cz_nominal, CCDLabel, triangleSideLength, micrometerDistance, consoleLog, logFile, TTFThread = 0.3175, TTFThreadOD = 6.35):
        #TTFThread = 0.3175mm = 1/80 inch
        #TTFThreadOD = 6.35mm for a 1/4-80 screw
        
        ###########################################################################
        ###Get adjustment ratios
        ###########################################################################     
        #Since the triangle of micrometers is much larger than the small ABC
        #imaginary triangle that we create on the sensor surface, we need to
        #calculate how an adjustment to the micrometers affect the ABC heights. 
        triangleAdjustmentRatio = (micrometerDistance/triangleSideLength) #mm/mm
        
        ###########################################################################
        ###Get the tip/tilt/z deltas
        ###########################################################################   
        #Point B
        bb = round(len(filelistB)/2) #select a focused image from array 
        #Point B
        cc = round(len(filelistC)/2) #select a focused image from array 
        #Tip
        AzDeltaTip, BzDeltaTip, CzDeltaTip = self.tipCCD(Az, Bz, Cz, Az_nominal, Bz_nominal, Cz_nominal, CCDLabel, consoleLog, logFile)
        #Tilt
        AzDeltaTilt, BzDeltaTilt, CzDeltaTilt = self.tiltCCD(Az, Bz, Cz, Az_nominal, Bz_nominal, Cz_nominal, CCDLabel, consoleLog, logFile)
        #Z
        CenterDeltaZ = self.ZCCD(Az, Bz, Cz, CCDLabel, consoleLog, logFile)
        #Rz
        angleRz = self.rz(imageArray4DB[bb], imageArray4DC[cc], CCDLabel, triangleSideLength, consoleLog, logFile)

        ###########################################################################
        ###Find Needed Micrometer Adjustments 
        ###########################################################################
        AturnDistanceDegrees = 999999999999
        BturnDistanceDegrees = 999999999999
        CturnDistanceDegrees = 999999999999
        turnA = "None"
        turnB = "None"
        turnC = "None"
        faah = fileAndArrayHandling()
        
        #If the A height isn't equal to the nominal height
        if AzDeltaTip or AzDeltaTilt != 0:
            #is A too low or too high (clockwise = down, counter-clockwise = up relative to CS5 +Z)
            if AzDeltaTip < 0: 
                turnA = 'counter-clockwise' 
            else: 
                turnA = 'clockwise'
            #How many turns will it take to reach nominal height?
            AturnDistance_rev = np.absolute(AzDeltaTip*triangleAdjustmentRatio)/(TTFThread*1000) #X turns = needed height / micrometer pitch (height per one full turn). Convert mm to microns.
            #AturnDistanceDegrees = faah.decNonZeroRound(np.absolute(AturnDistance_um/((TTFThreadOD*1000)/360))) #to get number of degrees. 1 degree = fifThreadODMicrons/360 um. Convert mm to microns.
            AturnDistanceDegrees = np.absolute(AturnDistance_rev*360)
            
        #If the B height isn't equal to the nominal height
        if BzDeltaTip or BzDeltaTilt != 0:
            #is B too low or too high (clockwise = down, counter-clockwise = up)
            if BzDeltaTip < 0: 
                turnB = 'counter-clockwise' 
            else: 
                turnB = 'clockwise'
            #How many turns will it take to reach nominal height?
            BturnDistance_rev = np.absolute(BzDeltaTip*triangleAdjustmentRatio)/(TTFThread*1000) #X turns = needed height / fif pitch (height per one full turn). Convert mm to microns.
            BturnDistanceDegrees = np.absolute(BturnDistance_rev*360) #to get number of degrees. 1 degree = fifThreadODMicrons/360 um. Convert mm to microns.
        
        #If the C height isn't equal to the nominal height
        if CzDeltaTip or CzDeltaTilt or CenterDeltaZ != 0:
            #is A too low or too high (clockwise = down, counter-clockwise = up)
            if CzDeltaTip < 0: 
                turnC = 'counter-clockwise' 
            else: 
                turnC = 'clockwise'
            #How many turns will it take to reach nominal height?
            CturnDistance_rev = np.absolute(CzDeltaTip*triangleAdjustmentRatio)/(TTFThread*1000) #X turns = needed height / fif pitch (height per one full turn). Convert mm to microns.
            CturnDistanceDegrees =  np.absolute(CturnDistance_rev*360) #to get number of degrees. 1 degree = fifThreadODMicrons/360 um. Convert mm to microns.
            
        ###########################################################################
        ###Send Warning Message
        ###########################################################################
        #micrometer ticks to turn: 360 degrees / 50 ticks on TTF micrometers = 7.2 degrees per tick
        
        self.distanceBetweenTrianglePoints(imageArray4DA, filelistA, imageArray4DB, filelistB, imageArray4DC, filelistC, consoleLog, logFile)
        
        faah.pageLogging(consoleLog, logFile, "The ratio between the virtual triangle on the sensor (A, B, C), and the\n large triangle (micrometer A, micrometer B, micrometer C):\n\n" +
                         "Triangle Adjustment Ratio=(Distance between micrometers)/(Sensor triangle side length)*1000um\n Triangle Adjustment Ratio = " + format(micrometerDistance, '.3f') + 
                         "mm / " + format(triangleSideLength, '.3f') + "mm = " + format(triangleAdjustmentRatio, '.3f') + "\n")
        
        faah.pageLogging(consoleLog, logFile, 
                "WARNING: the " + str(CCDLabel) +" camera Z heights are not equal to the nominal height.\n\n" + "The current micrometer thread pitch is " + str(TTFThread) + "mm (= " + str(TTFThread*1000) + "um = 1/80 in).\n" + 
                "\nTo adjust the camera to the nominal height, adjust the micrometers as:\n\n" + 
                "Micrometer A:\n " + 
                " A(micrometer revolutions) = (AzDelta um * triangleAdjustmentRatio)/(TTFThread mm *1000)\n" +
                "    = " + "(" + format(AzDeltaTip, '.2f') + "um * " + format(triangleAdjustmentRatio, '.2f') + "um) / (" +  format(TTFThread, '.4f') + " * 1000) = " + format(AturnDistance_rev, '.2f') + " rev\n" +
                " A(degrees) = A(revolutions)*360 = " + format(AturnDistanceDegrees, '.2f') + " degrees " + turnA + "\n"
                " A(ticks) = A(revolutions)*ticks_per_revolution = " + format(AturnDistance_rev, '.2f') + "*50 = " + format(AturnDistance_rev*50, '.2f') + " ticks"
                "\n\nMicrometer B:\n " + 
                " B(micrometer revolutions) = (BzDelta um * triangleAdjustmentRatio)/(TTFThread mm *1000)\n" +
                "    = " + "(" + format(BzDeltaTip, '.2f') + "um * " + format(triangleAdjustmentRatio, '.2f') + "um) / (" +  format(TTFThread, '.4f') + " * 1000) = " + format(BturnDistance_rev, '.2f') + " rev\n" +
                " B(degrees) = B(revolutions)*360 = " + format(BturnDistanceDegrees, '.2f') + " degrees " + turnB + "\n"
                " B(ticks) = B(revolutions)*ticks_per_revolution = " + format(BturnDistance_rev, '.2f') + "*50 = " + format(BturnDistance_rev*50, '.2f') + " ticks"                
                "\n\nMicrometer C: \n" + 
                " C(micrometer revolutions) = (CzDelta um * triangleAdjustmentRatio)/(TTFThread mm *1000)\n" +
                "    = " + "(" + format(CzDeltaTip, '.2f') + "um * " + format(triangleAdjustmentRatio, '.2f') + "um) / (" +  format(TTFThread, '.4f') + " * 1000) = " + format(CturnDistance_rev, '.2f') + " rev\n" +
                " C(degrees) = C(revolutions)*360 = " + format(CturnDistanceDegrees, '.2f') + " degrees " + turnC + "\n"
                " C(ticks) = C(revolutions)*ticks_per_revolution = " + format(CturnDistance_rev, '.2f') + "*50 = " + format(CturnDistance_rev*50, '.2f') + " ticks",
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
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        A(Z)_nominal = " + format(Az_nominal, '.3f') + "um\n" )
        faah.pageLogging(consoleLog, logFile, 
                                        "    Condition #2: B(Z)_measured = C(Z)_measured = B(Z)_nominal = C(Z)_nominal\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        B(Z)_nominal = " + format(Bz_nominal, '.3f') + "um\n" +
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n" +     
                                        "        C(Z)_nominal = " + format(Cz_nominal, '.3f') + "um\n")  
        #N,W,S,E
        if CCDLabel == "NCCD" or CCDLabel == "WCCD" or CCDLabel == "SCCD" or CCDLabel == "ECCD": 
            faah.pageLogging(consoleLog, logFile, 
                                        "    Condition #3: A(Z)_measured > B(Z)_measured && C(Z)_measured\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n")
        #C
        if CCDLabel == "CCCD":
            faah.pageLogging(consoleLog, logFile, 
                                        "    Condition #3: [A(Z) = B(Z) = C(Z)]_measured  = [A(Z) = B(Z) = C(Z)]_nominal\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n")
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
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        A(Z)_nominal = " + format(Az_nominal, '.3f') + "um\n" )
                faah.pageLogging(consoleLog, logFile, 
                                        "    Condition #2: B(Z)_measured = C(Z)_measured = B(Z)_nominal = C(Z)_nominal\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        B(Z)_nominal = " + format(Bz_nominal, '.3f') + "um\n" +
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n" +     
                                        "        C(Z)_nominal = " + format(Cz_nominal, '.3f') + "um\n") 
        #C
        if CCDLabel == "CCCD":
            faah.pageLogging(consoleLog, logFile, 
                                        "    Condition #3: [A(Z) = B(Z) = C(Z)]_measured  = [A(Z) = B(Z) = C(Z)]_nominal\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n")
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
                                        "        Center(Z)_measured = " + format(zCenter_measured, '.3f') + "um\n" + 
                                        "        Center(Z)_nominal = " + format(zCenter_nominal, '.3f') + "um\n" )

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
             
        #If B and C aren't aligned (in either X or Y depending on the camera location)
        if CCDLabel == "NCCD":
            _, ycenB = cF.findCentroid(fifSubArrayB, int(subArrayBoxSizeB/2), int(subArrayBoxSizeB/2), extendbox = 3) 
            _, ycenC = cF.findCentroid(fifSubArrayC, int(subArrayBoxSizeC/2), int(subArrayBoxSizeC/2), extendbox = 3)
            if ycenB != ycenC:
                if ycenB > ycenC:     
                #calculate angle between B and C. Report in CS5 relative to +X: 180 degrees - BC angle
                #BC Should be parallel to CS5X. CCDLabel sensor origin is [180 degrees - BC angle] degrees Rz about CS5X.                
                    angleRz = math.degrees(np.arcsin((ycenB-ycenC)/triangleSideLength))
                    faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(180-angleRz, '.3f') + " degrees about CS5X." ) 
                if ycenB < ycenC:
                #calculate angle between B and C. Report in CS5 relative to +X: 180 degrees + BC angle
                #BC Should be parallel to CS5X. CCDLabel sensor origin is [180 degrees + BC angle] degrees Rz about CS5X.
                    angleRz = math.degrees(np.arcsin((ycenC-ycenB)/triangleSideLength))
                    faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(180+angleRz, '.3f') + " degrees about CS5X." )
            else:
                angleRz = 180
                faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(angleRz, '.3f') + " degrees about CS5X.\n        Sensor is properly aligned in Rz" ) 
                    
        if CCDLabel == "SCCD" or CCDLabel == "CCCD":
            _, ycenB = cF.findCentroid(fifSubArrayB, int(subArrayBoxSizeB/2), int(subArrayBoxSizeB/2), extendbox = 3) 
            _, ycenC = cF.findCentroid(fifSubArrayC, int(subArrayBoxSizeC/2), int(subArrayBoxSizeC/2), extendbox = 3)
            if ycenB != ycenC:
                if ycenB > ycenC:                
                #calculate angle between B and C. Report in CS5 relative to +X: 360 degrees - BC angle.
                #BC Should be parallel to CS5X. CCDLabel sensor origin is [360 degrees - BC angle] degrees Rz about CS5X.                 
                    angleRz = math.degrees(np.arcsin((ycenB-ycenC)/triangleSideLength))
                    faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(360-angleRz, '.3f') + " degrees about CS5X." ) 
                if ycenB < ycenC:
                #calculate angle between B and C. Report in CS5 relative to +X: 0 degrees + BC angle.
                #BC Should be parallel to CS5X. CCDLabel sensor origin is [0 degrees + BC angle] degrees Rz about CS5X.  
                    angleRz = math.degrees(np.arcsin((ycenC-ycenB)/triangleSideLength))
                    faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(angleRz, '.3f') + " degrees about CS5X." ) 
            else:
                angleRz = 0
                faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(angleRz, '.3f') + " degrees about CS5X.\n        Sensor is properly aligned in Rz" ) 
                
        if CCDLabel == "ECCD":
            _, ycenB = cF.findCentroid(fifSubArrayB, int(subArrayBoxSizeB/2), int(subArrayBoxSizeB/2), extendbox = 3) 
            _, ycenC = cF.findCentroid(fifSubArrayC, int(subArrayBoxSizeC/2), int(subArrayBoxSizeC/2), extendbox = 3)  
            if ycenB != ycenC:
                if ycenB > ycenC: 
                #calculate angle between B and C. Report in CS5 relative to +X: 270 degrees - BC angle 
                #BC Should be parallel to CS5Y. CCDLabel sensor origin is [270 degrees - BC angle] degrees Rz about CS5X.                 
                    angleRz = math.degrees(np.arcsin((ycenB-ycenC)/triangleSideLength))
                    faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(270-angleRz, '.3f') + " degrees about CS5X." ) 
                if ycenB < ycenC:               
                #calculate angle between B and C. Report in CS5 relative to +X: 270 degrees + BC angle
                #BC Should be parallel to CS5Y. CCDLabel sensor origin is [270 degrees + BC angle] degrees Rz about CS5X.           
                    angleRz = math.degrees(np.arcsin((ycenC-ycenB)/triangleSideLength)) 
                    faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(270+angleRz, '.3f') + " degrees about CS5X." )   
            else:
                angleRz = 270
                faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(angleRz, '.3f') + " degrees about CS5X.\n        Sensor is properly aligned in Rz" )     
                    
        if CCDLabel == "WCCD":        
            _, ycenB = cF.findCentroid(fifSubArrayB, int(subArrayBoxSizeB/2), int(subArrayBoxSizeB/2), extendbox = 3) 
            _, ycenC = cF.findCentroid(fifSubArrayC, int(subArrayBoxSizeC/2), int(subArrayBoxSizeC/2), extendbox = 3)  
            if ycenB != ycenC:
                if ycenB > ycenC: 
                #calculate angle between B and C. Report in CS5 relative to +X: 90 degrees - BC angle
                #BC Should be parallel to CS5Y. CCDLabel sensor origin is [90 degrees - BC angle] degrees Rz about CS5X. 
                    angleRz = math.degrees(np.arcsin((ycenB-ycenC)/triangleSideLength))
                    faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + "Sensor origin is " + format(90-angleRz, '.3f') + " degrees about CS5X." ) 
                if ycenB < ycenC:              
                #calculate angle between B and C. Report in CS5 relative to +X: 90 degrees + BC angle  
                #BC Should be parallel to CS5Y. CCDLabel sensor origin is [90 degrees + BC angle] degrees Rz about CS5X.           
                    angleRz = math.degrees(np.arcsin((ycenC-ycenB)/triangleSideLength)) 
                    faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + "Sensor origin is " + format(90+angleRz, '.3f') + " degrees about CS5X." ) 
            else:
                angleRz = 90
                faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + "Sensor origin is " + format(angleRz, '.3f') + " degrees about CS5X.\n        Sensor is properly aligned in Rz" )    
        
        if CCDLabel == "Other":
                faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + "Sensor Other selected. Can't find Rz." )    
        
        return angleRz
       
    def distanceBetweenTrianglePoints(self, imageArray4DA, filelistA, imageArray4DB, filelistB, imageArray4DC, filelistC, consoleLog, logFile):             
        '''
        Find the measured distance between triangle points on the sensor.
        '''
        ###########################################################################
        ###Get images
        ###########################################################################   
        #Point A
        aa = round(len(filelistA)/2) #select a focused image from array
        #Point B
        bb = round(len(filelistB)/2) #select a focused image from array 
        #Point B
        cc = round(len(filelistC)/2) #select a focused image from array 
        
        #Log image that will be used for centroiding
        faah = fileAndArrayHandling()
        faah.pageLogging(consoleLog, logFile, 
                         "\nCentroiding image for point A: " +  str(filelistA[aa]).replace('/', '\\') +
                         "\nCentroiding image for point B: " +  str(filelistA[bb]).replace('/', '\\') +
                         "\nCentroiding image for point C: " +  str(filelistA[cc]).replace('/', '\\') + "\n")
        
        ###########################################################################
        ###Centroid images
        ###########################################################################         
        cF = centroidFIF()
        
        _ , subArrayBoxSizeA, maxLocA = cF.findFIFInImage(imageArray4DA[aa])
        _ , subArrayBoxSizeB, maxLocB = cF.findFIFInImage(imageArray4DB[bb])
        _ , subArrayBoxSizeC, maxLocC = cF.findFIFInImage(imageArray4DC[cc])
        
        #Account for planet mode
        pM = CCDOpsPlanetMode()
        xOffsetA, yOffsetA, pixelSizeA = pM.readFitsHeader(imageArray4DA, filelistA, consoleLog, logFile)
        xOffsetB, yOffsetB, pixelSizeB = pM.readFitsHeader(imageArray4DB, filelistB, consoleLog, logFile)
        xOffsetC, yOffsetC, pixelSizeC = pM.readFitsHeader(imageArray4DC, filelistC, consoleLog, logFile)

        #GMS Bisector       
        Ax, Ay, _, _ = gmsCentroid(imageArray4DA[aa], maxLocA[1], maxLocA[0], 
                                                         int(round(subArrayBoxSizeA/2)), int(round(subArrayBoxSizeA/2)), axis='both', verbose=False)
        Bx, By, _, _ = gmsCentroid(imageArray4DB[bb], maxLocB[1], maxLocB[0], 
                                                         int(round(subArrayBoxSizeB/2)), int(round(subArrayBoxSizeB/2)), axis='both', verbose=False)
        Cx, Cy, _, _ = gmsCentroid(imageArray4DC[cc], maxLocC[1], maxLocC[0], 
                                                         int(round(subArrayBoxSizeC/2)), int(round(subArrayBoxSizeC/2)), axis='both', verbose=False)
        
        ###########################################################################
        ###Calculate Delta Distance (measured size of sides)
        ########################################################################### 
        #Get Nominal triangle side length
        fC = focusCurve() 
        nominalSideLength = fC.tccs * 1000 #um

        #Delta Distance (measured - nominal)
        #A->B
        dab = (np.sqrt(math.pow(((Bx+xOffsetB)-(Ax+xOffsetA)), 2) + math.pow(((By+yOffsetB)-(Ay+yOffsetA)), 2))*pixelSizeA)#um
        #B->C
        dbc = (np.sqrt(math.pow(((Cx+xOffsetC)-(Bx+xOffsetB)), 2) + math.pow(((Cy+yOffsetC)-(By+yOffsetB)), 2))*pixelSizeB)#um
        #C->A
        dca = (np.sqrt(math.pow(((Ax+xOffsetA)-(Cx+xOffsetC)), 2) + math.pow(((Ay+yOffsetA)-(Cy+yOffsetC)), 2))*pixelSizeC)#um
        
        #Report Delta Distances
        faah.pageLogging(consoleLog, logFile, 
                         "\nTriangle A-B-C Delta Distances (measured - nominal):"
                         "\nA->B: " +  format(dab, '.3f') + " - " + format(nominalSideLength, '.3f') + " = " + format(dab-nominalSideLength, '.3f') + "um" +
                         "\nB->C: " +  format(dbc, '.3f') + " - " + format(nominalSideLength, '.3f') + " = " + format(dbc-nominalSideLength, '.3f') + "um" +
                         "\nC->A: " +  format(dca, '.3f') + " - " + format(nominalSideLength, '.3f') + " = " + format(dca-nominalSideLength, '.3f') + "um" + "\n")
