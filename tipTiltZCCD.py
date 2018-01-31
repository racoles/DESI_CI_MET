'''
@title tipTiltZCCD
@author: Rebecca Coles
Updated on Jan 31, 2018
Created on Jan 18, 2018

tipTiltZCCD
This module holds a series of functions that I use find the tip/tilt/Z of a CCD on the DESI CI.

Modules:
'''

# Import #######################################################################################
from fileAndArrayHandling import fileAndArrayHandling
################################################################################################

class tipTiltZCCD(object):
    
    def __init__(self):
        '''
        Constructor
        '''
        
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

    def ZCCD(self, Az, Bz, Cz, Az_nominal, Bz_nominal, Cz_nominal, CCDLabel, consoleLog, logFile):
        '''
        Return CCD Z
        
        Z(Center) _measured = Z(Center) _nominal 
        A(Z) _measured = A(Z) _nominal 
        B(Z)_measured = C(Z) _measured = B(Z)_nominal = C(Z) _nominal
        '''                 
        ###########################################################################
        ###Boundry Condition Check 
        ###########################################################################
        faah = fileAndArrayHandling()
        faah.pageLogging(self.consoleLog, self.logFile, 
                                      "Checking " + str(CCDLabel) + " Z:")
        #N,W,S,E
        #C
        #Other
