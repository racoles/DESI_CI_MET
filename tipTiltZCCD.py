'''
@title tipTiltZCCD
@author: Rebecca Coles
Updated on Mar 06, 2018
Created on Jan 18, 2018

tipTiltZCCD
This module holds a series of functions that I use find the tip/tilt/Z of a CCD on the DESI CI.

Modules:
'''

# Import #######################################################################################
from fileAndArrayHandling import fileAndArrayHandling
from focusCurve import focusCurve
from fractions import Fraction
import numpy as np
################################################################################################

class tipTiltZCCD(object):
    
    def __init__(self):
        '''
        Constructor
        '''
    
    def findTipTiltZ(self, Az, Bz, Cz, Az_nominal, Bz_nominal, Cz_nominal, CCDLabel, triangleSideLength, micrometerDistance, consoleLog, logFile, TTFThread = 0.5, TTFThreadOD = 6):
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

        ###########################################################################
        ###Find Needed Micrometer Adjustments 
        ###########################################################################
        faah = fileAndArrayHandling()
        fC = focusCurve()
        
        #If the A height isn't equal to the nominal height
        if AzDeltaTip or AzDeltaTilt != 0:
            #is A too low or too high (clockwise = down, counter-clockwise = up)
            if AzDeltaTip < 0: 
                turnA = 'counter-clockwise' 
            else: 
                turnA = 'clockwise'
            #How many turns will it take to reach nominal height?
            AturnDistance_um = np.absolute(AzDeltaTip*triangleAdjustmentRatio)/(TTFThread*1000) #X turns = needed height / micrometer pitch (height per one full turn). Convert mm to microns.
            AturnDistanceDegrees = faah.decNonZeroRound(np.absolute(AturnDistance_um/((TTFThreadOD*1000)/360))) #to get number of degrees. 1 degree = fifThreadODMicrons/360 um. Convert mm to microns.
            AturnFraction = np.absolute(Fraction(AturnDistance_um).limit_denominator()) #turnFraction-th of a turn
            
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
            BturnFraction = np.absolute(Fraction(BturnDistance_um).limit_denominator()) #turnFraction-th of a turn
        
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
            CturnFraction = np.absolute(Fraction(CturnDistance_um).limit_denominator()) #turnFraction-th of a turn
            
        ###########################################################################
        ###Send Warning Message
        ###########################################################################
        
        ####ADD Rz
        
        ####ADD B-C distance
        
        #######ADD MICROMETER TICK DISTANCE
        
        faah.pageLogging(consoleLog, logFile, 
                "WARNING: the" + str(CCDLabel) +" camera Z height is not equal to the nominal height.\n" + "The current micrometer thread pitch is " +
                str(TTFThread) + "mm (" + str(TTFThread*1000) + "um), with a OD of " + str(TTFThreadOD) + "mm (" +  str(TTFThreadOD*1000) + "um)." + 
                "\n To adjust this camera to the nominal height, you will need to adjust the micrometers as:\n " + 
                "Micrometer A: " + str(AturnDistanceDegrees) + " degrees " + turnA +" (" + str(AturnFraction).replace('(', '').replace(')', '') + "th of a turn).\n" +
                "Micrometer B: " + str(BturnDistanceDegrees) + " degrees " + turnB +" (" + str(BturnFraction).replace('(', '').replace(')', '') + "th of a turn).\n" +
                "Micrometer C: " + str(CturnDistanceDegrees) + " degrees " + turnC +" (" + str(CturnFraction).replace('(', '').replace(')', '') + "th of a turn).\n", 
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
    
    def Rz(self):
        '''
        Camera Rz (angle) 
        
        For North, Center, Or South Cameras
        For East and West Cameras
        '''             
        #If B and C aren't aligned (in either X or Y depending on the camera location)
        if CCDLabel == "NCCD" or CCDLabel == "CCCD" or CCDLabel == "SCCD":
            #If North camera
            if CCDLabel == "NCCD":
                if fC.CCDLocationsCS5["NCCD"][0] 
            #If Center camera
            if CCDLabel == "CCCD":   
            #If South camera
            if CCDLabel == "SCCD":   
                

         if CCDLabel == "ECCD" or CCDLabel == "WCCD":
            #If East camera
            if CCDLabel == "ECCD":    
            #If West camera
            if CCDLabel == "WCCD":                 
       
    def distanceBetweenTrianglePointsBandC(self):             
        #Distance between B and C (using centroiding and pixel size) versus nominal