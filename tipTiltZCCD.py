'''
@title tipTiltZCCD
@author: Rebecca Coles
Updated on Apr 16, 2018
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
                     Az, Bz, Cz, Az_nominal, Bz_nominal, Cz_nominal, CCDLabel, consoleLog, logFile, TTFThread = 0.3175):
        #TTFThread = 0.3175mm = 1/80 inch
        #TTFThreadOD = 6.35mm for a 1/4-80 screw
        
        ###########################################################################
        ###Get the tip/tilt/z deltas
        ###########################################################################   
        #Tip
        self.tipCCD(Az, Bz, Cz, Az_nominal, Bz_nominal, Cz_nominal,  CCDLabel, consoleLog, logFile)
        #Tilt
        self.tiltCCD(Az, Bz, Cz, Az_nominal, Bz_nominal, Cz_nominal,  CCDLabel, consoleLog, logFile)
        #Z
        self.ZCCD(Az, Bz, Cz, CCDLabel, consoleLog, logFile)
        
        ###########################################################################
        ###Get adjustment ratio
        ###########################################################################     
        #Since the triangle of micrometers is much larger than the small ABC
        #imaginary triangle that we create on the sensor surface, we need to
        #calculate how an adjustment to the micrometers affect the ABC heights.
        fC = focusCurve()
        triangleAdjustmentRatio = fC.micrometerDistance/fC.tccs
        
        #Rz
        bb = round(len(filelistB)/2) #select a focused image from array b
        cc = round(len(filelistC)/2) #select a focused image from array c
        angleRz = self.rz(imageArray4DB[bb], filelistB, imageArray4DC[cc], filelistC, CCDLabel, consoleLog, logFile)

        ###########################################################################
        ###Find Needed Micrometer Adjustments 
        ###########################################################################
        turnA = "None"
        turnB = "None"
        turnC = "None"
        
        ###########################################################################
        ###Calculate acutator moves
        ###########################################################################
        focusedMeasured = -((Az-Az_nominal) + (Bz-Bz_nominal) + (Cz-Cz_nominal))/3
        focusPara = -(triangleAdjustmentRatio*(Az_nominal - Az) + triangleAdjustmentRatio*(Bz_nominal - Bz) + triangleAdjustmentRatio*(Cz_nominal - Cz))/3

        Az_move = focusedMeasured + focusPara + (triangleAdjustmentRatio*(Az_nominal - Az))
        Bz_move = focusedMeasured + focusPara + (triangleAdjustmentRatio*(Bz_nominal - Bz))
        Cz_move = focusedMeasured + focusPara + (triangleAdjustmentRatio*(Cz_nominal - Cz))
        
        #If the A height isn't equal to the nominal height
        if Az != Az_nominal:
            #is A too low or too high (clockwise = down, counter-clockwise = up relative to CS5 +Z)
            if Az < 0: 
                turnA = 'counter-clockwise' 
            else: 
                turnA = 'clockwise'
            #How many turns will it take to reach nominal height?
            AturnDistanceDegrees = np.absolute((Az_move/(TTFThread*1000))*360) #in um
            #In ticks
            AturnDistanceTicks = np.absolute(AturnDistanceDegrees/(360/50))
            
        #If the B height isn't equal to the nominal height
        if Bz != Bz_nominal:
            #is A too low or too high (clockwise = down, counter-clockwise = up relative to CS5 +Z)
            if Bz < 0: 
                turnB = 'counter-clockwise' 
            else: 
                turnB = 'clockwise'
            #How many turns will it take to reach nominal height?
            BturnDistanceDegrees = np.absolute((Bz_move/(TTFThread*1000))*360) #in um
            #In ticks
            BturnDistanceTicks = np.absolute(BturnDistanceDegrees/(360/50))
        
        #If the C height isn't equal to the nominal height
        if Cz != Cz_nominal:
            #is A too low or too high (clockwise = down, counter-clockwise = up relative to CS5 +Z)
            if Cz < 0: 
                turnC = 'counter-clockwise' 
            else: 
                turnC = 'clockwise'
            #How many turns will it take to reach nominal height?
            CturnDistanceDegrees = np.absolute((Cz_move/(TTFThread*1000))*360) #in um
            #In ticks
            CturnDistanceTicks = np.absolute(CturnDistanceDegrees/(360/50))
        
        ###########################################################################
        ###Send Warning Message
        ###########################################################################
        #micrometer ticks to turn: 360 degrees / 50 ticks on TTF micrometers = 7.2 degrees per tick
        faah = fileAndArrayHandling()
        self.distanceBetweenTrianglePoints(imageArray4DA, filelistA, imageArray4DB, filelistB, imageArray4DC, filelistC, consoleLog, logFile)
        
        faah.pageLogging(consoleLog, logFile,"The ratio between the virtual triangle on the sensor (A, B, C), and the\n large triangle (micrometer A, micrometer B, micrometer C):\n" +
                         " Triangle Adjustment Ratio=(Distance between micrometers)/(Sensor triangle side length)\n Triangle Adjustment Ratio = " + format(fC.micrometerDistance, '.3f') + 
                         "mm / " + format(fC.tccs, '.3f') + "mm = " + format(triangleAdjustmentRatio, '.3f') + "\n")
        
        faah.pageLogging(consoleLog, logFile, "WARNING: the " + str(CCDLabel) +" camera Z heights are not equal to the nominal height.\n" + "The current micrometer thread pitch is " + str(TTFThread) + "mm (= " + str(TTFThread*1000) + "um = 1/80 in)." + 
                "\nTo adjust the camera to the nominal height, adjust the micrometers as:\n\n" + 
                "Micrometer A:\n " + 
                "A(micrometer um) = " + format(Az_move, '.3f') + "um" +
                "\nA(degrees) = " + format(AturnDistanceDegrees, '.2f') + " degrees " + turnA + "\n" +
                "A(ticks) = " + format(AturnDistanceTicks, '.2f') + " ticks " + turnA + 
                "\n\nMicrometer B:\n " + 
                "B(micrometer um) = " + format(Bz_move, '.3f') + "um" +
                "\nB(degrees) = " + format(BturnDistanceDegrees, '.2f') + " degrees " + turnB + "\n" +
                "B(ticks) = " + format(BturnDistanceTicks, '.2f') + " ticks " + turnB +              
                "\n\nMicrometer C: \n" + 
                "C(micrometer um) = " + format(Cz_move, '.3f') + "um" +
                "\nC(degrees) = " + format(CturnDistanceDegrees, '.2f') + " degrees " + turnC + "\n" +
                "C(ticks) = " + format(CturnDistanceTicks, '.2f') + " ticks " + turnC, warning = True)
        
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
        faah.pageLogging(consoleLog, logFile,"Checking " + str(CCDLabel) + " TIP:")

        if round(Az,3) != round(Az_nominal,3):
            faah.pageLogging(consoleLog, logFile,"    Condition #1: A(Z)_measured = A(Z)_nominal\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        A(Z)_nominal = " + format(Az_nominal, '.3f') + "um\n" +
                                        "        A(Z)_measured != A(Z)_nominal\n")
        else:
            faah.pageLogging(consoleLog, logFile,"    Condition #1: A(Z)_measured = A(Z)_nominal\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        A(Z)_nominal = " + format(Az_nominal, '.3f') + "um\n" +
                                        "A(Z)_measured = A(Z)_nominal\n")
        if round(Bz,3) != round(Bz_nominal,3) or round(Cz,3) != round(Cz_nominal,3):
            if round(Bz,3) != round(Bz_nominal,3) and round(Cz,3) == round(Cz_nominal,3):
                faah.pageLogging(consoleLog, logFile,"    Condition #2: B(Z)_measured = C(Z)_measured = B(Z)_nominal = C(Z)_nominal\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        B(Z)_nominal = " + format(Bz_nominal, '.3f') + "um\n" +
                                        "        B(Z)_measured != B(Z)_nominal\n" +
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n" +     
                                        "        C(Z)_nominal = " + format(Cz_nominal, '.3f') + "um\n" +
                                        "        C(Z)_measured = C(Z)_nominal\n") 
            elif round(Bz,3) == round(Bz_nominal,3) and round(Cz,3) != round(Cz_nominal,3):
                faah.pageLogging(consoleLog, logFile,"    Condition #2: B(Z)_measured = C(Z)_measured = B(Z)_nominal = C(Z)_nominal\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        B(Z)_nominal = " + format(Bz_nominal, '.3f') + "um\n" +
                                        "        B(Z)_measured = B(Z)_nominal\n" +
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n" +     
                                        "        C(Z)_nominal = " + format(Cz_nominal, '.3f') + "um\n" +
                                        "        C(Z)_measured != C(Z)_nominal\n") 
            else:
                faah.pageLogging(consoleLog, logFile,"    Condition #2: B(Z)_measured = C(Z)_measured = B(Z)_nominal = C(Z)_nominal\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        B(Z)_nominal = " + format(Bz_nominal, '.3f') + "um\n" +
                                        "        B(Z)_measured != B(Z)_nominal\n" +
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n" +     
                                        "        C(Z)_nominal = " + format(Cz_nominal, '.3f') + "um\n" +
                                        "        C(Z)_measured != C(Z)_nominal\n")  
        #N,W,S,E
        if CCDLabel == "NCCD" or CCDLabel == "WCCD" or CCDLabel == "SCCD" or CCDLabel == "ECCD": 
            if round(Az,3) >= round(Bz,3) and round(Az,3) <= round(Cz,3):
                faah.pageLogging(consoleLog, logFile,"    Condition #3: A(Z)_measured > B(Z)_measured && C(Z)_measured\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n\n" +
                                        "        A(Z)_measured >= B(Z)_measured\n" +
                                        "        A(Z)_measured <= C(Z)_measured\n")
            elif round(Az,3) >= round(Cz,3) and round(Az,3) <= round(Bz,3):
                faah.pageLogging(consoleLog, logFile,"    Condition #3: A(Z)_measured > B(Z)_measured && C(Z)_measured\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n\n" +
                                        "        A(Z)_measured <= B(Z)_measured\n" +
                                        "        A(Z)_measured >= C(Z)_measured\n")
            else:
                faah.pageLogging(consoleLog, logFile,"    Condition #3: A(Z)_measured > B(Z)_measured && C(Z)_measured\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n\n" +
                                        "        A(Z)_measured >= B(Z)_measured\n" +
                                        "        A(Z)_measured >= C(Z)_measured\n")
        #C
        if CCDLabel == "CCCD":
            if round(Az,3) != round(Bz,3) and round(Az,3) == round(Cz,3) and round(Bz,3) == round(Cz,3):
                faah.pageLogging(consoleLog, logFile,"    Condition #3: [A(Z) = B(Z) = C(Z)]_measured  = [A(Z) = B(Z) = C(Z)]_nominal\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n\n" +
                                        "        A(Z)_measured != B(Z)_measured\n" +
                                        "        A(Z)_measured = C(Z)_measured\n" +
                                        "        B(Z)_measured = C(Z)_measured\n")                
            if round(Az,3) != round(Cz,3) and round(Az,3) == round(Bz,3) and round(Bz,3) == round(Cz,3):
                faah.pageLogging(consoleLog, logFile,"    Condition #3: [A(Z) = B(Z) = C(Z)]_measured  = [A(Z) = B(Z) = C(Z)]_nominal\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n\n" +
                                        "        A(Z)_measured = B(Z)_measured\n" +
                                        "        A(Z)_measured != C(Z)_measured\n" +
                                        "        B(Z)_measured = C(Z)_measured\n")     
            if round(Bz,3) != round(Cz,3) and round(Az,3) == round(Bz,3) and round(Az,3) == round(Cz,3):
                faah.pageLogging(consoleLog, logFile,"    Condition #3: [A(Z) = B(Z) = C(Z)]_measured  = [A(Z) = B(Z) = C(Z)]_nominal\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n\n" +
                                        "        A(Z)_measured = B(Z)_measured\n" +
                                        "        A(Z)_measured = C(Z)_measured\n" +
                                        "        B(Z)_measured != C(Z)_measured\n")     
            else:
                faah.pageLogging(consoleLog, logFile,"    Condition #3: [A(Z) = B(Z) = C(Z)]_measured  = [A(Z) = B(Z) = C(Z)]_nominal\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n\n" +
                                        "        A(Z)_measured != B(Z)_measured\n" +
                                        "        A(Z)_measured != C(Z)_measured\n" +
                                        "        B(Z)_measured != C(Z)_measured\n") 
        #Other
        if CCDLabel == "Other":
            faah.pageLogging(consoleLog, logFile,"CCD selection: Other. Not able to calculate Tip.")
        
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
        faah.pageLogging(consoleLog, logFile,"Checking " + str(CCDLabel) + " TILT:")
        #N,W,S,E
        if CCDLabel == "NCCD" or CCDLabel == "WCCD" or CCDLabel == "SCCD" or CCDLabel == "ECCD":
            if round(Az,3) != round(Az_nominal,3):
                faah.pageLogging(consoleLog, logFile,"    Condition #1: A(Z)_measured = A(Z)_nominal\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        A(Z)_nominal = " + format(Az_nominal, '.3f') + "um\n\n" +
                                        "        A(Z)_measured != A(Z)_nominal\n" )
            else:
                faah.pageLogging(consoleLog, logFile,"    Condition #1: A(Z)_measured = A(Z)_nominal\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        A(Z)_nominal = " + format(Az_nominal, '.3f') + "um\n\n" +
                                        "        A(Z)_measured = A(Z)_nominal\n" )
                
            if round(Bz,3) != round(Cz,3):
                faah.pageLogging(consoleLog, logFile,"    Condition #2: B(Z)_measured = C(Z)_measured = B(Z)_nominal = C(Z)_nominal\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        B(Z)_nominal = " + format(Bz_nominal, '.3f') + "um\n" +
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n" +     
                                        "        C(Z)_nominal = " + format(Cz_nominal, '.3f') + "um\n\n" +
                                        "        B(Z)_measured != C(Z)_measured\n") 
            elif round(Bz,3) == round(Cz,3) and round(Cz,3) != round(Cz_nominal,3) or round(Bz,3) != round(Bz_nominal,3):
                if round(Cz,3) != round(Cz_nominal,3):
                    faah.pageLogging(consoleLog, logFile,"    Condition #2: B(Z)_measured = C(Z)_measured = B(Z)_nominal = C(Z)_nominal\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        B(Z)_nominal = " + format(Bz_nominal, '.3f') + "um\n" +
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n" +     
                                        "        C(Z)_nominal = " + format(Cz_nominal, '.3f') + "um\n\n" +
                                        "        C(Z)_measured != C(Z)_nominal\n") 
                if round(Bz,3) != round(Bz_nominal,3):
                    faah.pageLogging(consoleLog, logFile,"    Condition #2: B(Z)_measured = C(Z)_measured = B(Z)_nominal = C(Z)_nominal\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        B(Z)_nominal = " + format(Bz_nominal, '.3f') + "um\n" +
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n" +     
                                        "        C(Z)_nominal = " + format(Cz_nominal, '.3f') + "um\n\n" +
                                        "        B(Z)_measured != B(Z)_nominal\n") 
            elif round(Bz,3) == round(Cz,3) and round(Cz,3) == round(Cz_nominal,3) and round(Bz,3) == round(Bz_nominal,3): 
                faah.pageLogging(consoleLog, logFile,"    Condition #2: B(Z)_measured = C(Z)_measured = B(Z)_nominal = C(Z)_nominal\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        B(Z)_nominal = " + format(Bz_nominal, '.3f') + "um\n" +
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n" +     
                                        "        C(Z)_nominal = " + format(Cz_nominal, '.3f') + "um\n\n" +
                                        "        B(Z)_measured = C(Z)_measured = B(Z)_nominal = C(Z)_nominal\n")            
        #C
        if CCDLabel == "CCCD":
            if round(Az,3) != round(Bz,3) and round(Bz,3) == round(Cz,3):
                faah.pageLogging(consoleLog, logFile,"    Condition #1: [A(Z) = B(Z) = C(Z)]_measured  = [A(Z) = B(Z) = C(Z)]_nominal\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n\n" +
                                        "        A(Z)_measured != B(Z)_measured\n" +
                                        "        B(Z)_measured = C(Z)_measured\n\n")
            elif round(Az,3) == round(Bz,3) and round(Bz,3) != round(Cz,3):
                faah.pageLogging(consoleLog, logFile,"    Condition #1: [A(Z) = B(Z) = C(Z)]_measured  = [A(Z) = B(Z) = C(Z)]_nominal\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n\n" +
                                        "        A(Z)_measured = B(Z)_measured\n" +
                                        "        B(Z)_measured != C(Z)_measured\n\n")
            elif round(Az,3) != round(Bz,3) and round(Bz,3) != round(Cz,3):
                faah.pageLogging(consoleLog, logFile,"    Condition #1: [A(Z) = B(Z) = C(Z)]_measured  = [A(Z) = B(Z) = C(Z)]_nominal\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n\n" +
                                        "        A(Z)_measured != B(Z)_measured\n" +
                                        "        B(Z)_measured != C(Z)_measured\n\n")
            elif round(Az,3) == round(Bz,3) and round(Bz,3) == round(Cz,3) and round(Az,3) != round(Az_nominal,3):
                faah.pageLogging(consoleLog, logFile,"    Condition #1: [A(Z) = B(Z) = C(Z)]_measured  = [A(Z) = B(Z) = C(Z)]_nominal\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n\n" +
                                        "        A(Z)_measured = B(Z)_measured\n" +
                                        "        B(Z)_measured = C(Z)_measured\n" +
                                        "        [A(Z) = B(Z) = C(Z)]_measured  != [A(Z) = B(Z) = C(Z)]_nominal\n\n")
            elif round(Az,3) == round(Bz,3) and round(Bz,3) == round(Cz,3) and round(Az,3) == round(Az_nominal,3):
                faah.pageLogging(consoleLog, logFile,"    Condition #1: [A(Z) = B(Z) = C(Z)]_measured  = [A(Z) = B(Z) = C(Z)]_nominal\n" + 
                                        "        A(Z)_measured = " + format(Az, '.3f') + "um\n" + 
                                        "        B(Z)_measured = " + format(Bz, '.3f') + "um\n" + 
                                        "        C(Z)_measured = " + format(Cz, '.3f') + "um\n\n" +
                                        "        A(Z)_measured = B(Z)_measured\n" +
                                        "        B(Z)_measured = C(Z)_measured\n" +
                                        "        [A(Z) = B(Z) = C(Z)]_measured  = [A(Z) = B(Z) = C(Z)]_nominal\n\n")
        #Other
        if CCDLabel == "Other":
                faah.pageLogging(consoleLog, logFile,"CCD selection: Other. Not able to calculate Tilt.")

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
        faah.pageLogging(consoleLog, logFile,"Checking " + str(CCDLabel) + " CCD Center Z:")
        #N,W,S,E,C,Other
        if round(zCenter_measured,3) != round(zCenter_nominal,3):
            faah.pageLogging(consoleLog, logFile,"Condition: Center(Z)_measured = Center(Z)_nominal\n" + 
                                        "        Center(Z)_measured = [Az + Bz + Cz]_measured/3 = " + format(zCenter_measured, '.3f') + "um\n" + 
                                        "        Center(Z)_nominal = " + format(zCenter_nominal, '.3f') + "um\n" +
                                        "        Center(Z)_measured != Center(Z)_nominal\n\n")
        if round(zCenter_measured,3) == round(zCenter_nominal,3):
            faah.pageLogging(consoleLog, logFile,"Condition: Center(Z)_measured = Center(Z)_nominal\n" + 
                                        "        Center(Z)_measured = [Az + Bz + Cz]_measured/3 = " + format(zCenter_measured, '.3f') + "um\n" + 
                                        "        Center(Z)_nominal = " + format(zCenter_nominal, '.3f') + "um\n" +
                                        "        Center(Z)_measured == Center(Z)_nominal\n\n")
    
    def rz(self, imageB, filelistB, imageC, filelistC, CCDLabel, consoleLog, logFile):
        '''
        Camera Rz (angle) 
        
        For North, Center, Or South Cameras:
            B(x) = C(x)
        For East and West Cameras:
            B(y) = C(y)
        '''             
        
        #Centroid images
        cF = centroidFIF()
        fifSubArrayB, subArrayBoxSizeB, maxLocB  = cF.findFIFInImage(imageB)
        fifSubArrayC, subArrayBoxSizeC, maxLocC  = cF.findFIFInImage(imageC)
        
        ###########################################################################
        ###Report Rz 
        ###########################################################################
        angleRz = 9999999999999999999999999
        
        faah = fileAndArrayHandling()
        
        pM = CCDOpsPlanetMode()
        xOffsetB, yOffsetB, _ = pM.readFitsHeader(imageB, filelistB, consoleLog, logFile)
        xOffsetC, yOffsetC, _ = pM.readFitsHeader(imageC, filelistC, consoleLog, logFile)
        
        xcenB, ycenB, _, _ = gmsCentroid(imageB, maxLocB[1], maxLocB[0], 
                                                         int(round(subArrayBoxSizeB/2)), int(round(subArrayBoxSizeB/2)), axis='both', verbose=False)
        xcenC, ycenC, _, _ = gmsCentroid(imageC, maxLocC[1], maxLocC[0], 
                                                         int(round(subArrayBoxSizeC/2)), int(round(subArrayBoxSizeC/2)), axis='both', verbose=False)
        
        #xcenB, ycenB = cF.findCentroid(fifSubArrayB, int(subArrayBoxSizeB/2), int(subArrayBoxSizeB/2), extendbox = 3) 
        #xcenC, ycenC = cF.findCentroid(fifSubArrayC, int(subArrayBoxSizeC/2), int(subArrayBoxSizeC/2), extendbox = 3)
        angleRz = math.degrees(np.arctan(((ycenC + yOffsetC)- (ycenB + yOffsetB))/((xcenC + xOffsetC) - (xcenB + xOffsetB))))
        
        
        
        
        
        print("angleRz = math.degrees(np.arctan(((ycenC + yOffsetC) - (ycenB + yOffsetB))/((xcenC + xOffsetC) - (xcenB + xOffsetB))))")
        print("math.degrees(np.arctan(((" + format(ycenC, '.3f') + " + " + format(yOffsetC, '.3f') + ") - (" + format(ycenB, '.3f') + " + " + format(yOffsetB, '.3f') + 
              "))/((" + format(xcenC, '.3f') + " + " + format(xOffsetC, '.3f') + ") - (" + format(xcenB, '.3f') + " + " + format(xOffsetB, '.3f') + ") = " + format(angleRz, '.3f') )
        
        '''     
        #If B and C aren't aligned (in either X or Y depending on the camera location)
        if CCDLabel == "NCCD":
            xcenB, ycenB = cF.findCentroid(fifSubArrayB, int(subArrayBoxSizeB/2), int(subArrayBoxSizeB/2), extendbox = 3) 
            xcenC, ycenC = cF.findCentroid(fifSubArrayC, int(subArrayBoxSizeC/2), int(subArrayBoxSizeC/2), extendbox = 3)
            if ycenB != ycenC:
                if ycenB > ycenC:     
                #calculate angle between B and C. Report in CS5 relative to +X: 180 degrees - BC angle
                #BC Should be parallel to CS5X. CCDLabel sensor origin is [180 degrees - BC angle] degrees Rz about CS5X.                
                    angleRz = math.degrees(np.arctan((ycenC-ycenB)/(xcenC-xcenB)))
                    faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(180-angleRz, '.3f') + " degrees about CS5X." ) 
                if ycenB < ycenC:
                #calculate angle between B and C. Report in CS5 relative to +X: 180 degrees + BC angle
                #BC Should be parallel to CS5X. CCDLabel sensor origin is [180 degrees + BC angle] degrees Rz about CS5X.
                    angleRz = math.degrees(np.arctan((ycenC-ycenB)/(xcenC-xcenB)))
                    faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(180+angleRz, '.3f') + " degrees about CS5X." )
            else:
                angleRz = 180
                faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(angleRz, '.3f') + " degrees about CS5X.\n        Sensor is properly aligned in Rz" ) 
                    
        if CCDLabel == "SCCD" or CCDLabel == "CCCD":
            xcenB, ycenB = cF.findCentroid(fifSubArrayB, int(subArrayBoxSizeB/2), int(subArrayBoxSizeB/2), extendbox = 3) 
            xcenC, ycenC = cF.findCentroid(fifSubArrayC, int(subArrayBoxSizeC/2), int(subArrayBoxSizeC/2), extendbox = 3)
            if ycenB != ycenC:
                if ycenB > ycenC:                
                #calculate angle between B and C. Report in CS5 relative to +X: 360 degrees - BC angle.
                #BC Should be parallel to CS5X. CCDLabel sensor origin is [360 degrees - BC angle] degrees Rz about CS5X.                 
                    angleRz = math.degrees(np.arctan((ycenC-ycenB)/(xcenC-xcenB)))
                    faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(360-angleRz, '.3f') + " degrees about CS5X." ) 
                if ycenB < ycenC:
                #calculate angle between B and C. Report in CS5 relative to +X: 0 degrees + BC angle.
                #BC Should be parallel to CS5X. CCDLabel sensor origin is [0 degrees + BC angle] degrees Rz about CS5X.  
                    angleRz = math.degrees(np.arctan((ycenC-ycenB)/(xcenC-xcenB)))
                    faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(angleRz, '.3f') + " degrees about CS5X." ) 
            else:
                angleRz = 0
                faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5X.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(angleRz, '.3f') + " degrees about CS5X.\n        Sensor is properly aligned in Rz" ) 
                
        if CCDLabel == "ECCD":
            xcenB, ycenB = cF.findCentroid(fifSubArrayB, int(subArrayBoxSizeB/2), int(subArrayBoxSizeB/2), extendbox = 3) 
            xcenC, ycenC = cF.findCentroid(fifSubArrayC, int(subArrayBoxSizeC/2), int(subArrayBoxSizeC/2), extendbox = 3)  
            if ycenB != ycenC:
                if ycenB > ycenC: 
                #calculate angle between B and C. Report in CS5 relative to +X: 270 degrees - BC angle 
                #BC Should be parallel to CS5Y. CCDLabel sensor origin is [270 degrees - BC angle] degrees Rz about CS5X.                 
                    angleRz = math.degrees(np.arctan((ycenC-ycenB)/(xcenC-xcenB)))
                    faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(270-angleRz, '.3f') + " degrees about CS5X." ) 
                if ycenB < ycenC:               
                #calculate angle between B and C. Report in CS5 relative to +X: 270 degrees + BC angle
                #BC Should be parallel to CS5Y. CCDLabel sensor origin is [270 degrees + BC angle] degrees Rz about CS5X.           
                    angleRz = math.degrees(np.arctan((ycenC-ycenB)/(xcenC-xcenB)))
                    faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(270+angleRz, '.3f') + " degrees about CS5X." )   
            else:
                angleRz = 270
                faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + " Sensor origin is " + format(angleRz, '.3f') + " degrees about CS5X.\n        Sensor is properly aligned in Rz" )     
                    
        if CCDLabel == "WCCD":        
            xcenB, ycenB = cF.findCentroid(fifSubArrayB, int(subArrayBoxSizeB/2), int(subArrayBoxSizeB/2), extendbox = 3) 
            xcenC, ycenC = cF.findCentroid(fifSubArrayC, int(subArrayBoxSizeC/2), int(subArrayBoxSizeC/2), extendbox = 3)  
            if ycenB != ycenC:
                if ycenB > ycenC: 
                #calculate angle between B and C. Report in CS5 relative to +X: 90 degrees - BC angle
                #BC Should be parallel to CS5Y. CCDLabel sensor origin is [90 degrees - BC angle] degrees Rz about CS5X. 
                    angleRz = math.degrees(np.arctan((ycenC-ycenB)/(xcenC-xcenB)))
                    faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + "Sensor origin is " + format(90-angleRz, '.3f') + " degrees about CS5X." ) 
                if ycenB < ycenC:              
                #calculate angle between B and C. Report in CS5 relative to +X: 90 degrees + BC angle  
                #BC Should be parallel to CS5Y. CCDLabel sensor origin is [90 degrees + BC angle] degrees Rz about CS5X.           
                    angleRz = math.degrees(np.arctan((ycenC-ycenB)/(xcenC-xcenB)))
                    faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + "Sensor origin is " + format(90+angleRz, '.3f') + " degrees about CS5X." ) 
            else:
                angleRz = 90
                faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + "Sensor origin is " + format(angleRz, '.3f') + " degrees about CS5X.\n        Sensor is properly aligned in Rz" )    
        
        if CCDLabel == "Other":
                faah.pageLogging(consoleLog, logFile, "Checking " + str(CCDLabel) + " Rz about CS5X:" + "Side BC Should be parallel to CS5Y.\n" + 
                                     "        " + CCDLabel + "Sensor Other selected. Can't find Rz." )  
                
        '''        
        faah.pageLogging(consoleLog, logFile, "Rz Local (degrees): " + format(angleRz, '.3f'))   
        
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
