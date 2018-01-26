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
import numpy as np
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
        
    def tipCCD(self, Az, Bz, Cz, fifLabel, consoleLog, logFile):
        '''
        Calculate CCD tip
        
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