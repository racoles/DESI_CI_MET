'''
@title tipTiltZCCD
@author: Rebecca Coles
Updated on Jan 19, 2018
Created on Jan 18, 2018

tipTiltZCCD
This module holds a series of functions that I use find the tip/tilt/Z of a CCD on the DESI CI.

Modules:
'''

# Import #######################################################################################
from focusCurve import focusCurve
from fileAndArrayHandling import fileAndArrayHandling
################################################################################################

class tipTiltZCCD(object):
    
    def __init__(self):
        '''
        Constructor
        '''
        
    def createEquilateralTriangle(self):
        '''
        Take focus curves at the points of an equilateral triangle
        to find the CCD center
        
        Return tip/tilt/z
        '''
        ###########################################################################
        ###Take A/B/C Focus Curves
        ########################################################################### 
        
    def tipCCD(self, Az, Bz, Cz, CCDLabel, consoleLog, logFile):
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
        ###Get Nominal Az/Bz/Cz 
        ###########################################################################
        fC = focusCurve() 
        Az_nominal = fC.trianglePonitCCDLocationsCS5[str(CCDLabel + 'A')]
        Bz_nominal = fC.trianglePonitCCDLocationsCS5[str(CCDLabel + 'B')]
        Cz_nominal = fC.trianglePonitCCDLocationsCS5[str(CCDLabel + 'C')]      
                
        faah = fileAndArrayHandling()
        
    def tiltCCD(self, Az, Bz, Cz, fifLabel, consoleLog, logFile):
        '''
        Calculate CCD tilt
        
        A(Z) _measured = A(Z) _nominal 
        B(Z)_measured = C(Z) _measured = B(Z)_nominal = C(Z) _nominal
        '''
        
    def ZCCD(self, Az, Bz, Cz, fifLabel, consoleLog, logFile):
        '''
        Return CCD Z
        
        Z(Center) _measured = Z(Center) _nominal 
        A(Z) _measured = A(Z) _nominal 
        B(Z)_measured = C(Z) _measured = B(Z)_nominal = C(Z) _nominal
        '''