'''
@title foreShortening
@author: Rebecca Coles
Updated on June 18, 2018
Created on Mar 18, 2018

foreShortening
This module holds a series of functions that are used to find the magnitude of this fore-shortening:

1.    The 6303 Cameras (N,E,S,W) are tilted by 5.4 degrees from the Z axis. Therefore when the CCDs are viewed from above, 
        and measurements are made in the CS5 X,Y plane, the 6303 CCDs will appear to be fore-shortened across their width for all four  cameras. 
2.    Magnitude of this fore-shortening is ~ (1- COS(5.4deg)) *(2048*9um) = 82 um  (too large to ignore)


'''

# Import #######################################################################################
################################################################################################

class foreShortening(object):
    
    def __init__(self):
        '''
        Constructor
        '''
        
    def foreShortening(self, consoleLog, logFile, CCDSelection):
        '''
        Find the magnitude of this fore-shortening for the 6303 Cameras (N,E,S,W)
        '''
        
        ###########################################################################
        ###Offset Calibration
        ###########################################################################

