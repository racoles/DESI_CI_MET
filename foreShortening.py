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
