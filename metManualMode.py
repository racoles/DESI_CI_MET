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
        ###FIF Button Option Window
        ###########################################################################   
        top = tk.Toplevel()
        top.title("FIF Manual Mode")
        
        #Manual Mode Description
        tk.Label(top, text="Which FIF would you like to measure?").grid(row=0, column=0, columnspan=2, sticky='W')
        
        # RefFIF
        refFIF = tk.Button(self, text="RefFIF", command=lambda: self._setTrueAndExit("RefFIF", top))
        refFIF.grid(row=1, column=0)
        # NFIF
        NFIF = tk.Button(self, text="NFIF", command=lambda: self._setTrueAndExit("NFIF", top))
        NFIF.grid(row=2, column=0)
        # WFIF
        WFIF = tk.Button(self, text="WFIF", command=lambda: self._setTrueAndExit("WFIF", top))
        WFIF.grid(row=2, column=1)
        # SFIF
        SFIF = tk.Button(self, text="SFIF", command=lambda: self._setTrueAndExit("SFIF", top))
        SFIF.grid(row=2, column=2)
        # EFIF
        EFIF = tk.Button(self, text="EFIF", command=lambda: self._setTrueAndExit("EFIF", top))
        EFIF.grid(row=2, column=3)
        # A1
        A1 = tk.Button(self, text="A1", command=lambda: self._setTrueAndExit("A1", top))
        A1.grid(row=3, column=0)
        # A2
        A2 = tk.Button(self, text="A2", command=lambda: self._setTrueAndExit("A2", top))
        A2.grid(row=3, column=1)
        # A3
        A3 = tk.Button(self, text="A3", command=lambda: self._setTrueAndExit("A3", top))
        A3.grid(row=3, column=2)
        # A4
        A4 = tk.Button(self, text="A4", command=lambda: self._setTrueAndExit("A4", top))
        A4.grid(row=3, column=3)
        # B1
        B1 = tk.Button(self, text="B1", command=lambda: self._setTrueAndExit("B1", top))
        B1.grid(row=4, column=0)
        # B2
        B2 = tk.Button(self, text="B2", command=lambda: self._setTrueAndExit("B2", top))
        B2.grid(row=4, column=1)
        # B3
        B3 = tk.Button(self, text="B3", command=lambda: self._setTrueAndExit("B3", top))
        B3.grid(row=4, column=2)
        # B4
        B4 = tk.Button(self, text="B4", command=lambda: self._setTrueAndExit("B4", top))
        B4.grid(row=4, column=3)
        # C1
        C1 = tk.Button(self, text="C1", command=lambda: self._setTrueAndExit("C1", top))
        C1.grid(row=5, column=0)
        # C2
        C2 = tk.Button(self, text="C2", command=lambda: self._setTrueAndExit("C2", top))
        C2.grid(row=5, column=1)
        # C3
        C3 = tk.Button(self, text="C3", command=lambda: self._setTrueAndExit("C3", top))
        C3.grid(row=5, column=2)
        # C4
        C4 = tk.Button(self, text="C4", command=lambda: self._setTrueAndExit("C4", top))
        C4.grid(row=5, column=3)
        # D1
        D1 = tk.Button(self, text="D1", command=lambda: self._setTrueAndExit("D1", top))
        D1.grid(row=6, column=0)
        # D2
        D2 = tk.Button(self, text="D2", command=lambda: self._setTrueAndExit("D2", top))
        D2.grid(row=6, column=1)
        # D3
        D3 = tk.Button(self, text="D3", command=lambda: self._setTrueAndExit("D3", top))
        D3.grid(row=6, column=2)
        # D4
        D4 = tk.Button(self, text="D4", command=lambda: self._setTrueAndExit("D4", top))
        D4.grid(row=6, column=3)
        # CFIF
        CFIF = tk.Button(self, text="CFIF", command=lambda: self._setTrueAndExit("CFIF", top))
        CFIF.grid(row=7, column=0)
        # Other
        other = tk.Button(self, text="Other (will set x=0 y=0)", command=lambda: self._setTrueAndExit("Other", top))
        other.grid(row=8, column=0)
        
        tk.Label(top, text=" ").grid(row=9, column=0, columnspan=2, sticky='W')
        dismissButton = tk.Button(top, text="Exit", command=top.destroy)
        dismissButton.grid(row=10, column=0)       
        
        ###########################################################################
        ###Create Dir Using self.fifSection
        ###########################################################################
        
        dirName = self.createDir(self.fifSection, metGuidedModeSelf, 'Manual_Mode_Focus_Curve')
        
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
        
    def _setTrueAndExit(self, fifLabel, windowVariable):
        self.fifSection = fifLabel
        windowVariable.destroy
        
    def _createManualDir(self, fiflabel, dirType, ):
        try:
            os.makedirs(str(fiflabel + "_" + dirType + '_' + logTime))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        return str(fiflabel + "_" + dirType + '_' + logTime)