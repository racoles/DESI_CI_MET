'''
@title cs5Offsets
@author: Rebecca Coles
Updated on Mar 06, 2018
Created on Feb 14, 2018

cs5Offsets
This module is used to find the CS5 location of an illuminated object that is imaged using the 
SBIG ST-I and STXL-6303 cameras that is attached to the DMM, while the DMM is attached to a CMM.

'''

# Import #######################################################################################
import tkinter as tk
################################################################################################

class cs5Offsets(object):
    
    def __init__(self):
        '''
        Constructor
        '''
    def offsetCS5LocationInImage(self):
        '''
        AKA: The Dowel Measurement
        
        When we tell the CS5 calibrated CMM to move to a given CS5 location, we will need to know
        where the specified point will show up in the associated ST-I image taken with the DMM for 
        that point. To find this offset in units of (rows, columns), we perform the following 
        measurements prior to mounting the DMM on the CMM:
        1.    The CI will have two dowels placed at know locations. Each dowel will have an 
                illuminated divot on top. Prior to mounting the DMM on the CS5 calibrated CMM, 
                we use the CMM's touch probe to find the exact location of the divots in CS5 
                coordinates.
        2.    After attaching the DMM to the CMM, we tell the CMM to move to the CS5 
                location of the divot.
        3.    We take an image of the divot using the ST-I camera on the DMM.
        4.    We input the image into the DESI CI Metrology software, and it located the 
                location of the divot in units of (rows, column).

        How we use this offset: 
        this offset tells us where an object that we image with the ST-I (usually a FIF pinhole
        or light from the 100um pinhole on the DMM), at a given CS5 location, will appear in the 
        image. Put simply, the ST-I is not mounted on the DMM such that an imaged object appears 
        directly in the center of the image, and this offset tells us where the imaged-object 
        origin is in ST-I images.
        '''
    
    def _moveToIlluminatedDowelAndImage(self):
        '''
        '''
        ###########################################################################
        ###FIF Button Option Window
        ###########################################################################   
        top = tk.Toplevel()
        top.title("DESI CI Metrology Software Calibration")
        self.wm_withdraw()
        
        #Manual Mode Description
        tk.Label(top, text="Which FIF would you like to measure?").grid(row=0, column=0, columnspan=2, sticky='W')
        
        # RefFIF
        refFIF = tk.Button(top, text="RefFIF: (199.28,-345.15)", command=lambda: self._setTrueAndExit(top, fifLabel="RefFIF"))
        refFIF.grid(row=1, column=0, sticky='W')
        