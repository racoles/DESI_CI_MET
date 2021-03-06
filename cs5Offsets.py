'''
@title cs5Offsets
@author: Rebecca Coles
Updated on Dec 04, 2018
Created on Feb 14, 2018

cs5Offsets
This module is used to find the CS5 location of an illuminated object that is imaged using the 
SBIG ST-I and STXL-6303 cameras that is attached to the DMM, while the DMM is attached to a CMM.

'''

# Import #######################################################################################
import tkinter as tk
from tkinter.ttk import Separator
from fileAndArrayHandling import fileAndArrayHandling
from centroidFIF import centroidFIF
from CCDOpsPlanetMode import CCDOpsPlanetMode
from alternateCentroidMethods import gmsCentroid
################################################################################################

class cs5Offsets(object):
    
    #Pinhole Image Distnce To Sensor Origin (0,0) Defaults (tested in lab to find the location of the 100um pinhole in an STi image)
    #PIDTSO_x = 293.48
    #PIDTSO_y = 205.93
    
    PIDTSO_x = 324.1
    PIDTSO_y = 295.7
    
    #CS5 Point on CI Dowel from probe
    CPOCID_X = 0
    CPOCID_Y = 0
    
    #CS5 Point from centroided image
    CPOCID_cent_x = 0
    CPOCID_cent_y = 0
    
    #DMM Magnification
    dmmMag = 4.417
    
    def __init__(self):
        '''
        Constructor
        '''
    
    def calibrationScreen(self, consoleLog, logFile):
        '''
        To find the CS5 location of an illuminated object that is imaged using the
        SBIG ST-I and STXL-6303 cameras that is attached to the DMM, while the DMM 
        is attached to a CMM.
        '''
        ###########################################################################
        ###Calibration Window
        ###########################################################################   
        top = tk.Toplevel()
        top.title("DESI CI Metrology Software Calibration")
        
        #Manual Mode Description
        tk.Label(top, text="Goal", justify="left", font = '-weight bold').grid(row=1, column=0, sticky='W', columnspan=2)
        tk.Label(top, text="To find the CS5 location of an illuminated object that is imaged using the SBIG ST-I and STXL-6303 cameras" + 
                 "that is attached to the DMM, while the DMM is attached to a CMM.\n", wraplength=700, justify="left").grid(row=2, column=0, sticky='W', columnspan=2)
        Separator(top, orient="horizontal").grid(row=3, column=0, sticky='ew', columnspan=2)
        
        #Offset 1: Light from 100um DMM Pinhole in ST-I Image (Needed for CCD Metrology Measurements)
        tk.Label(top, text="Light from 100um DMM Pinhole in ST-I Image (Needed for CCD Metrology Measurements)", font = '-weight bold', justify="left").grid(row=4, column=0, sticky='W', columnspan=2)
        tk.Label(top, text="When we project light from the DMM’s 100um pinhole onto a surface (usually a CCD), and image it" + 
                 " using the DMM’s ST-I camera, we need to know the distance from where the projected pinhole shows up on a ST-I" + 
                 " full frame image (in units of rows and columns) to the corner of that image (rows = 0, column = 0). The image" + 
                 " used to find this off set is created by focusing the light from the 100um pinhole on the DMM onto a diffuse" + 
                 " surface and analyzing the resulting ST-I image. This measurement is completed before the DMM is attached to the" + 
                 " CMM, and the resulting distance is a static variable in the DESI CI Metrology Software.\n\n" +
                 "The current predetermined offsets show that the center the 100um pinhole on the DMM, when imaged with the ST-i" + 
                 " is located at:\n\n (row = " + str(self.PIDTSO_x) + ", column = " + str(self.PIDTSO_y) + ")\n", 
                 wraplength=700, justify="left").grid(row=5, column=0, sticky='W', columnspan=2)
                 
        faah = fileAndArrayHandling()
        faah.pageLogging(consoleLog, logFile, "\n\nBeginning Calibration Routine", calibration = True)
        faah.pageLogging(consoleLog, logFile, "The current predetermined offset for the DMM's 100um pinhole as imaged with the ST-i" + 
                 " is: (row = " + str(self.PIDTSO_x) + ", column = " + str(self.PIDTSO_y) + ")", calibration = True)
                       
        #Offset 2: CS5 Point on CI Dowel as shown in ST-I Image (Needed for FIF and CCD Metrology Measurements)
        Separator(top, orient="horizontal").grid(row=6, column=0, sticky='ew', columnspan=2)
        tk.Label(top, text="CS5 Point on CI Dowel as shown in ST-I Image (Needed for FIF and CCD Metrology Measurements)", font = '-weight bold', justify="left").grid(row=7, column=0, sticky='W', columnspan=2) 
        tk.Label(top, text="When we tell the CS5 calibrated CMM to move to a given CS5 location, we will need to know where the" +
                 " specified point will show up in the associated ST-I image taken with the DMM for that point. To find this offset" + 
                 " in units of (rows, columns), perform the following  measurements prior to mounting the DMM on the CMM:\n\n" +
                 "\t1. The CI will have a dowel placed at a know location. The dowel will have an illuminated divot on top.\n" + 
                 "\t\x20\x20\x20\x20Prior to mounting the DMM on the CS5 calibrated CMM, use the CMM's touch probe to find the exact\n" +
                 "\t\x20\x20\x20\x20location of the illuminated divot in CS5 coordinates.\n\n" +
                 "\t2. After attaching the DMM to the CMM, tell the CMM to move to the CS5 location of the illuminated divot.\n\n" +
                 "\t3. Take an image of the illuminated divot using the ST-I camera on the DMM.\n\n" +
                 "\t4. Input the image into the DESI CI Metrology software using the input button below. The software will\n" +
                 "\t\x20\x20\x20\x20locate the location of the illuminated divot in units of (rows, columns).\n", wraplength=700, justify="left").grid(row=8, column=0, sticky='W', columnspan=2)
        offset2aButton = tk.Button(top, text="Enter CS5 coordinates of Illuminated Dowel Center", command=lambda: self._offset2a_moveToIlluminatedDowelAndProbe(offset2aButton, consoleLog, logFile))
        offset2aButton.grid(row=9, column=0, sticky='W', columnspan=2)        
        offset2bButton = tk.Button(top, text="Load Image of Illuminated Divot", command=lambda: self._offset2b_moveToIlluminatedDowelAndImage(offset2bButton, consoleLog, logFile))
        offset2bButton.grid(row=9, column=1, sticky='W', columnspan=2)
        top.wait_window()
        
        return self.PIDTSO_x, self.PIDTSO_y, self.CPOCID_X, self.CPOCID_Y, self.CPOCID_cent_x, self.CPOCID_cent_y, self.dmmMag
        
    #def _offset1_PinholeImageDistnceToSensorOrigin(self):
        
    def _offset2a_moveToIlluminatedDowelAndProbe(self, offset2aButton, consoleLog, logFile): 
        '''
        AKA: The Dowel Measurement Part 1
        
        When we tell the CS5 calibrated CMM to move to a given CS5 location, we will need to know
        where the specified point will show up in the associated ST-I image taken with the DMM for 
        that point. To find this offset in units of (rows, columns), we perform the following 
        measurements prior to mounting the DMM on the CMM:
        
        1.    The CI will have two dowels placed at know locations. Each dowel will have an 
                illuminated divot on top. Prior to mounting the DMM on the CS5 calibrated CMM, 
                we use the CMM's touch probe to find the exact location of the divots in CS5 
                coordinates.
        '''      
        ###########################################################################
        ###Dowel Probe Center Input Screen
        ###########################################################################
        top = tk.Toplevel()
        top.title("Dowel Probe Center Input Screen")
        
        #Manual Mode Description
        tk.Label(top, text="Enter CS5 coordinates of the center of the illuminated \ndowel obtained from the CMM probe measurement.").grid(row=0, column=0, columnspan=2, sticky='W')
        
        #Rows
        tk.Label(top, text="CS5 X (mm) = ").grid(row=1, column=0, sticky='W')
        CPOCID_X = tk.Entry(top, width=20)
        CPOCID_X.grid(row=1, column=1, sticky='W')
        XButton = tk.Button(top, text='Submit', bg = "white", command=lambda:self._submitValueX(XButton, CPOCID_X, consoleLog, logFile))
        XButton.grid(row=1, column=2)
        
        #Columns
        tk.Label(top, text="CS5 Y (mm) = ").grid(row=2, column=0, sticky='W')
        CPOCID_Y = tk.Entry(top, width=20)
        CPOCID_Y.grid(row=2, column=1, sticky='W')
        YButton = tk.Button(top, text='Submit', bg = "white", command=lambda:self._submitValueY(YButton, CPOCID_Y, consoleLog, logFile))
        YButton.grid(row=2, column=2)
        
        ###########################################################################
        ###Change button text and color
        ###########################################################################
        offset2aButton.config(text = "CS5 coordinates for Illuminated Dowel Complete", bg = 'green')  
    
    def _submitValueX(self, XButton, CPOCID_X, consoleLog, logFile):
        self.CPOCID_X = CPOCID_X.get()
        XButton.config(text = "CS5 X Entered", bg = 'green') 
        faah = fileAndArrayHandling()
        faah.pageLogging(consoleLog, logFile, "Illuminated Dowel Probed CS5 X = " + str(self.CPOCID_X) + "mm", calibration = True)
        
    def _submitValueY(self, YButton, CPOCID_Y, consoleLog, logFile):
        self.CPOCID_Y = CPOCID_Y.get()
        YButton.config(text = "CS5 Y Entered", bg = 'green') 
        faah = fileAndArrayHandling()
        faah.pageLogging(consoleLog, logFile, "Illuminated Dowel Probed CS5 Y = " + str(self.CPOCID_Y) + "mm", calibration = True)
         
    
    def _offset2b_moveToIlluminatedDowelAndImage(self, offset2bButton, consoleLog, logFile):
        '''
        AKA: The Dowel Measurement Part 2
        
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
        ###########################################################################
        ###Load Calibration Image
        ###########################################################################
        faah = fileAndArrayHandling()
        imageArray4D, filelist = faah.openAllFITSImagesInDirectory()
        
        #Log image that will be used for centroiding
        faah = fileAndArrayHandling()
        faah.pageLogging(consoleLog, logFile, 
                         "Centroiding image: " +  str(filelist[0]).replace('/', '\\'), calibration = True)
        
        #Get location of pinhole image in (rows, columns)
        cF = centroidFIF()
        _ , _ , maxLoc = cF.findFIFInImage(imageArray4D[0])
        
        #Account for planet mode
        pM = CCDOpsPlanetMode()
        xOffset, yOffset, _ = pM.readFitsHeader(imageArray4D, filelist, consoleLog, logFile, calibration = True)
             
        ###########################################################################
        ###Centroid Pinhole
        ###########################################################################
        #Use alternate methods to centroid pinhole image
        #    gmsCentroid: Gaussian Marginal Sum (GMS) Centroid Method.
        xCenGMS, yCenGMS, xErrGMS, yErrGMS = gmsCentroid(imageArray4D[0], maxLoc[1], maxLoc[0], 
                                                         int(round(cF.widthOfSubimage/2)), int(round(cF.widthOfSubimage/2)), axis='both', verbose=False)
        
        ###########################################################################
        ###Change button text and color
        ###########################################################################
        offset2bButton.config(text = "Illuminated Dowel Calibration Complete", bg = 'green')
        
        ###########################################################################
        ###Return Offset2
        ###########################################################################
        faah.pageLogging(consoleLog, logFile, "Calibration Pinhole image found at (rows, columns): (" + str(maxLoc[1] + xOffset) + ', ' + str(maxLoc[0] + yOffset)+ ')\n' +
                        "Calibration GMS Centroid (rows, columns): (" +  format(xCenGMS + xOffset, '.2f') + ' +/- ' + format(xErrGMS, '.2f') + 
                        ', ' + format(yCenGMS + yOffset, '.2f') + ' +/- ' + format(yErrGMS, '.2f') + ')\n' + "Illuminated point on CI illuminated dowel, as shown in ST-I image," +
                        " offset will be set to: ("+  format(xCenGMS + xOffset, '.2f') + ', ' + format(yCenGMS + yOffset, '.2f') + ")", calibration = True)
                        
        ###########################################################################
        ###Set Offset2
        ###########################################################################
        self.CPOCID_cent_x = xCenGMS + xOffset
        self.CPOCID_cent_y = yCenGMS + yOffset