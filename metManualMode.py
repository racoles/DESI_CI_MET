'''
@title metManualMode
@author: Rebecca Coles
Updated on Jan 18, 2018
Created on Jan 18, 2018

metManualMode
Guided mode for DESI CI metrology.

Classes and Modules:

'''

# Import #######################################################################################
import tkinter as tk
################################################################################################

class metManualMode():
        
    def __init__(self, master):
        '''
        Constructor
        '''
        super(metManualMode, self).__init__()
        self.master = master
        master.title("DESI CI Meterology Manual Mode")
        
    def manualFocusCurve(self):
        ###########################################################################
        ###FIF Location Button Dictionary
        ########################################################################### 
        fifSelectionDict = {"RefFIF" : False, "NFIF" : False, "WFIF" : False,
                           "SFIF" : False, "EFIF" : False, "CFIF" : False,
                           "A1" : False, "A2" : False, "A3" : False,
                           "A4" : False, "B1" : False, "B2" : False, 
                           "B3" : False, "B4" : False, "C1" : False,
                           "C2" : False, "C3" : False, "C4" : False,
                           "D1" : False, "D2" : False, "D3" : False, 
                           "D4" : False, "Other" : False}
        ###########################################################################
        ###FIF Button Option Window
        ###########################################################################   
        top = tk.Toplevel()
        top.title("FIF Manual Mode")
        
        #Manual Mode Description
        tk.Label(top, text="Which FIF would you like to measure?").grid(row=0, column=0, columnspan=2, sticky='W')
        
        # RefFIF
        refFIF = False
        refFIF = tk.Button(self, text="RefFIF", command=lambda:)

        button = tk.Button(top, text="Dismiss", command=top.destroy)
        button.pack()
        
        # RefFIF
        refFIF = tk.Button(self, text="RefFIF", command=lambda:)
        
        ###########################################################################
        ###Create Dir
        ###########################################################################
        dirName = self.createDir(fiflabel, metGuidedModeSelf, 'Focus_Curve')
        
        ###########################################################################
        ###Message user to fill dir (mention label names)
        ###########################################################################
        metGuidedModeSelf.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      "Suggested " +  str(fiflabel) + " focus curve directory: \n" + str(os.getcwd()) + '\\' + dirName + 
                                      "\nNOTE: the file names will be used to create the Z axis values (distance)\n" +
                                        " so please label the FITS files appropriately\n" +
                                        "(example: 350.fit for the image taken at 350um).")
        
        ###########################################################################
        ###Get images
        ###########################################################################
        fH = fileAndArrayHandling()
        imageArray4D, filelist = fH.openAllFITSImagesInDirectory()
        
        ###########################################################################
        ###Create focus curve
        ########################################################################### 
        fC = focusCurve()       
        xInter = fC.stdFocusCurve(fiflabel, imageArray4D, filelist)
        metGuidedModeSelf.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      "Measured Best focus for " + str(fiflabel) + " is: " + str(xInter) + "um")
        
        ###########################################################################
        ###Nominal best focus
        ###########################################################################
        #Dict of (x,y) for FIFs
        fifLocationsCS5 = {"RefFIF" : (199.28,-345.15), 
                           "NFIF" : (-108.31,-383.55), 
                           "WFIF" : (-383.55,108.31),
                           "SFIF" : (108.31,383.55), 
                           "EFIF" : (383.55,-108.31),
                           "CFIF" : (108.31,15.00),
                           "A1" : (281.82,-281.82),
                           "A2" : (-281.82,-281.82), 
                           "A3" : (-281.82,281.82),
                           "A4" : (281.82,281.82),
                           "B1" : (293.64,136.93),
                           "B2" : (-293.64,136.93), 
                           "B3" : (-293.64,-136.93),
                           "B4" : (-136.93,293.64),
                           "C1" : (96.44,232.82),
                           "C2" : (232.82,-96.44), 
                           "C3" : (-96.44,-232.82),
                           "C4" : (-232.82,96.44),
                           "D1" : (0,185.00),
                           "D2" : (185.00,0), 
                           "D3" : (0,-185.00),
                           "D4" : (-185.00,0)}

        nominalZ = self.asphericFocalCurve(fifLocationsCS5[fiflabel][0], fifLocationsCS5[fiflabel][1])
        metGuidedModeSelf.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      "Nominal Z for " + str(fiflabel) + " is: " + str(nominalZ) + "um in CS5 coordinates.")
        metGuidedModeSelf.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      "Absolute value of (Nominal Z - Measured Best Focus) = " +  str(np.absolute(nominalZ-xInter)) + 'um')
        
    