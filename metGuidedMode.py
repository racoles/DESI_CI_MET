'''
@title metGuidedMode
@author: Rebecca Coles
Updated on Jan 10, 2018
Created on Dec 13, 2017

metGuidedMode
Guided mode for DESI CI FIF metrology.

Classes and Modules:

'''

# Import #######################################################################################
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Separator
import os
from focusCurve import focusCurve
from fileAndArrayHandling import fileAndArrayHandling
from centroidFIF import centroidFIF
import numpy as np
from CCDOpsPlanetMode import CCDOpsPlanetMode
################################################################################################

class metGuidedMode(tk.Tk):
    consoleLog = []
    logFile = []
    fifCentroidedLocationDict = {
                        "RefFIF" : [0,0,0], 
                        "NFIF" : [0,0,0], 
                        "WFIF" : [0,0,0],
                        "SFIF" : [0,0,0], 
                        "EFIF" : [0,0,0],
                        "CFIF" : [0,0,0],
                        "A1" : [0,0,0],
                        "A2" : [0,0,0], 
                        "A3" : [0,0,0],
                        "A4" : [0,0,0],
                        "B1" : [0,0,0],
                        "B2" : [0,0,0], 
                        "B3" : [0,0,0],
                        "B4" : [0,0,0],
                        "C1" : [0,0,0],
                        "C2" : [0,0,0], 
                        "C3" : [0,0,0],
                        "C4" : [0,0,0],
                        "D1" : [0,0,0],
                        "D2" : [0,0,0], 
                        "D3" : [0,0,0],
                        "D4" : [0,0,0]}
        
    def __init__(self, master):
        '''
        Constructor
        '''
        super(metGuidedMode, self).__init__()
        self.master = master
        master.title("DESI CI Meterology Guided Mode")
        
    def guidedModeFrames(self):
        '''
        Guide the user through measuring all of the FIFs.
        '''
        ###########################################################################
        ###Create pages
        ###########################################################################
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        pages = (fifPage, conclusion, helpPage)
    
        for page in pages:
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(pages[0]) #start on the start page

    def show_frame(self, cont):
        '''
        Show page to user.
        '''
        frame = self.frames[cont]
        frame.tkraise()
        
    def areYouSureExit(self):
        if messagebox.askyesno("Exit Guided Mode", "You are about to exit Guided Mode.\nAre You Sure?", icon='warning'):
            self.destroy()
        
class helpPage(tk.Frame):

    def __init__(self, container, metGuidedModeSelf):
        tk.Frame.__init__(self,container)
        label = tk.Label(self,
                          text="Guided Metrology will lead you through taking\n" +
                           "metrology measurements of the FIFs for the DESI CI.\n" +
                           "The button table will show the suggested order of \n" +
                           "measurements.\n",
                           font=('consolas', '10'))
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Exit to Guided Mode page",
                            command=lambda: self.destroy())
        button1.pack()

class fifPage(tk.Frame):
        #"RefFIF", 
        #"NFIF", "WFIF", "SFIF", "EFIF", 
        #"A1", "A2", "A3", "A4", 
        #"B1", "B2", "B3", "B4", 
        #"C1", "C2", "C3", "C4", 
        #"D1", "D2", "D3", "D4",
        #"CFIF
    
    def __init__(self, container, metGuidedModeSelf):
        tk.Frame.__init__(self, container)

        ###########################################################################
        ###Buttons
        ###########################################################################
        tk.Label(self, text="DESI CI FIFs      FIF thread: 0.5mm per turn", font=('consolas', '10')).grid(row=0, column=0, columnspan=2, sticky='W')
        tk.Button(self, text="Help",
                            command=lambda: metGuidedModeSelf.show_frame(helpPage)).grid(row=0, column=3, sticky='E')
        Separator(self, orient="horizontal").grid(row=1, column=0, columnspan=4, sticky='ew') 
                           
        #Measurement grid
        # RefFIF
        tk.Label(self, text="RefFIF: (199.28,-345.15)", font=('consolas', '10')).grid(row=2, column=0, columnspan=1, sticky='W')
        refFIFF = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(refFIFF, "RefFIF", metGuidedModeSelf)))
        refFIFF.grid(row=3, column=0, sticky='W')
        refFIFC = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(refFIFC, "RefFIF", metGuidedModeSelf)))
        refFIFC.grid(row=4, column=0, sticky='W')
        Separator(self, orient="vertical").grid(row=1, column=0, rowspan=5, sticky='ens')
        Separator(self, orient="horizontal").grid(row=5, column=0, columnspan=4, sticky='ew')
        
        #NFIF
        tk.Label(self, text="NFIF: (-108.31,-383.55)", font=('consolas', '10')).grid(row=6, column=0, sticky='W')
        NFIFF = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(NFIFF, "NFIF", metGuidedModeSelf)))
        NFIFF.grid(row=7, column=0, sticky='W')
        NFIFC = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(NFIFC, "NFIF", metGuidedModeSelf)))
        NFIFC.grid(row=8, column=0, sticky='W')
        Separator(self, orient="vertical").grid(row=5, column=0, rowspan=5, sticky='ens')
        
        #WFIF
        tk.Label(self, text="WFIF: (-383.55,108.31)", font=('consolas', '10')).grid(row=6, column=1, sticky='W')
        WFIFF = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(WFIFF, "WFIF", metGuidedModeSelf)))
        WFIFF.grid(row=7, column=1, sticky='W')
        WFIFC = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(WFIFC, "WFIF", metGuidedModeSelf)))
        WFIFC.grid(row=8, column=1, sticky='W')
        Separator(self, orient="vertical").grid(row=5, column=1, rowspan=5, sticky='ens')   
        
        #SFIF
        tk.Label(self, text="SFIF: (108.31,383.55)", font=('consolas', '10')).grid(row=6, column=2, sticky='W')
        SFIFF = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(SFIFF, "SFIF", metGuidedModeSelf)))
        SFIFF.grid(row=7, column=2, sticky='W')
        SFIFC = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(SFIFC, "SFIF", metGuidedModeSelf)))
        SFIFC.grid(row=8, column=2, sticky='W')
        Separator(self, orient="vertical").grid(row=5, column=2, rowspan=5, sticky='ens')  
        
        #EFIF
        tk.Label(self, text="EFIF: (383.55,-108.31)", font=('consolas', '10')).grid(row=6, column=3, sticky='W')
        SFIFF = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(SFIFF, "SFIF", metGuidedModeSelf)))
        SFIFF.grid(row=7, column=3, sticky='W')
        SFIFC = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(SFIFC, "SFIF", metGuidedModeSelf)))
        SFIFC.grid(row=8, column=3, sticky='W')
        Separator(self, orient="horizontal").grid(row=9, column=0, columnspan=4, sticky='ew')
        Separator(self, orient="vertical").grid(row=5, column=3, rowspan=5, sticky='ens') 
        
        #A1
        tk.Label(self, text="A1: (281.82,-281.82)", font=('consolas', '10')).grid(row=10, column=0, sticky='W')
        A1F = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(A1F, "A1", metGuidedModeSelf)))
        A1F.grid(row=11, column=0, sticky='W')
        A1C = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(A1C, "A1", metGuidedModeSelf)))
        A1C.grid(row=12, column=0, sticky='W')
        Separator(self, orient="vertical").grid(row=9, column=0, rowspan=5, sticky='ens')  
        
        #A2
        tk.Label(self, text="A2: (-281.82,-281.82)", font=('consolas', '10')).grid(row=10, column=1, sticky='W')
        A2F = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(A2F, "A2", metGuidedModeSelf)))
        A2F.grid(row=11, column=1, sticky='W')
        A2C = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(A2C, "A2", metGuidedModeSelf)))
        A2C.grid(row=12, column=1, sticky='W')
        Separator(self, orient="vertical").grid(row=9, column=1, rowspan=5, sticky='ens')  
        
        #A3
        tk.Label(self, text="A3: (-281.82,281.82)", font=('consolas', '10')).grid(row=10, column=2, sticky='W')
        A3F = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(A3F, "A3", metGuidedModeSelf)))
        A3F.grid(row=11, column=2, sticky='W')
        A3C = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(A3C, "A3", metGuidedModeSelf)))
        A3C.grid(row=12, column=2, sticky='W')
        Separator(self, orient="vertical").grid(row=9, column=2, rowspan=5, sticky='ens')  
        
        #A4
        tk.Label(self, text="A4: (281.82,281.82)", font=('consolas', '10')).grid(row=10, column=3, sticky='W')
        A4F = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(A4F, "A4", metGuidedModeSelf)))
        A4F.grid(row=11, column=3, sticky='W')
        A4C = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(A4C, "A4", metGuidedModeSelf)))
        A4C.grid(row=12, column=3, sticky='W') 
        Separator(self, orient="horizontal").grid(row=13, column=0, columnspan=4, sticky='ew')
        Separator(self, orient="vertical").grid(row=9, column=3, rowspan=5, sticky='ens') 
        
        #B1
        tk.Label(self, text="B1: (293.64,136.93)", font=('consolas', '10')).grid(row=14, column=0, sticky='W')
        B1F = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(B1F, "B1", metGuidedModeSelf)))
        B1F.grid(row=15, column=0, sticky='W')
        B1C = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(B1C, "B1", metGuidedModeSelf)))
        B1C.grid(row=16, column=0, sticky='W')
        Separator(self, orient="vertical").grid(row=13, column=0, rowspan=5, sticky='ens') 
        
        #B2
        tk.Label(self, text="B2: (-293.64,136.93)", font=('consolas', '10')).grid(row=14, column=1, sticky='W')
        B2F = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(B2F, "B2", metGuidedModeSelf)))
        B2F.grid(row=15, column=1, sticky='W')
        B2C = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(B2C, "B2", metGuidedModeSelf)))
        B2C.grid(row=16, column=1, sticky='W')
        Separator(self, orient="vertical").grid(row=13, column=1, rowspan=5, sticky='ens') 
        
        #B3
        tk.Label(self, text="B3: (-293.64,-136.93)", font=('consolas', '10')).grid(row=14, column=2, sticky='W')
        B3F = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(B3F, "B3", metGuidedModeSelf)))
        B3F.grid(row=15, column=2, sticky='W')
        B3C = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(B3C, "B3", metGuidedModeSelf)))
        B3C.grid(row=16, column=2, sticky='W')
        Separator(self, orient="vertical").grid(row=13, column=2, rowspan=5, sticky='ens') 
        
        #B4
        tk.Label(self, text="B4: (-136.93,293.64)", font=('consolas', '10')).grid(row=14, column=3, sticky='W')
        B4F = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(B4F, "B4", metGuidedModeSelf)))
        B4F.grid(row=15, column=3, sticky='W')
        B4C = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(B4C, "B4", metGuidedModeSelf)))
        B4C.grid(row=16, column=3, sticky='W')
        Separator(self, orient="horizontal").grid(row=17, column=0, columnspan=4, sticky='ew') 
        Separator(self, orient="vertical").grid(row=13, column=3, rowspan=5, sticky='ens')     
        
        #C1
        tk.Label(self, text="C1: (96.44,232.82)", font=('consolas', '10')).grid(row=18, column=0, sticky='W')
        C1F = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(C1F, "C1", metGuidedModeSelf)))
        C1F.grid(row=19, column=0, sticky='W')
        C1C = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(C1C, "C1", metGuidedModeSelf)))
        C1C.grid(row=20, column=0, sticky='W')
        Separator(self, orient="vertical").grid(row=17, column=0, rowspan=5, sticky='ens')    
        
        #C2
        tk.Label(self, text="C2: (232.82,-96.44)", font=('consolas', '10')).grid(row=18, column=1, sticky='W')
        C2F = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(C2F, "C2", metGuidedModeSelf)))
        C2F.grid(row=19, column=1, sticky='W')
        C2C = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(C2C, "C2", metGuidedModeSelf)))
        C2C.grid(row=20, column=1, sticky='W')
        Separator(self, orient="vertical").grid(row=17, column=1, rowspan=5, sticky='ens')  
        
        #C3
        tk.Label(self, text="C3: (-96.44,-232.82)", font=('consolas', '10')).grid(row=18, column=2, sticky='W')
        C3F = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(C3F, "C3", metGuidedModeSelf)))
        C3F.grid(row=19, column=2, sticky='W')
        C3C = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(C3C, "C3", metGuidedModeSelf)))
        C3C.grid(row=20, column=2, sticky='W')
        Separator(self, orient="vertical").grid(row=17, column=2, rowspan=5, sticky='ens')  
        
        #C4
        tk.Label(self, text="C4: (-232.82,96.44)", font=('consolas', '10')).grid(row=18, column=3, sticky='W')
        C4F = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(C4F, "C4", metGuidedModeSelf)))
        C4F.grid(row=19, column=3, sticky='W')
        C4C = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(C4C, "C4", metGuidedModeSelf)))
        C4C.grid(row=20, column=3, sticky='W')  
        Separator(self, orient="horizontal").grid(row=21, column=0, columnspan=4, sticky='ew')
        Separator(self, orient="vertical").grid(row=17, column=3, rowspan=5, sticky='ens')  
        
        #D1
        tk.Label(self, text="D1: (0,185.00)", font=('consolas', '10')).grid(row=22, column=0, sticky='W')
        D1F = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(D1F, "D1", metGuidedModeSelf)))
        D1F.grid(row=23, column=0, sticky='W')
        D1C = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(D1C, "D1", metGuidedModeSelf)))
        D1C.grid(row=24, column=0, sticky='W')
        Separator(self, orient="vertical").grid(row=21, column=0, rowspan=5, sticky='ens')
        
        #D2
        tk.Label(self, text="D2: (185.00,0)", font=('consolas', '10')).grid(row=22, column=1, sticky='W')
        D2F = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(D2F, "D2", metGuidedModeSelf)))
        D2F.grid(row=23, column=1, sticky='W')
        D2C = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(D2C, "D2", metGuidedModeSelf)))
        D2C.grid(row=24, column=1, sticky='W')
        Separator(self, orient="vertical").grid(row=21, column=1, rowspan=5, sticky='ens')
        
        #D3
        tk.Label(self, text="D3: (0,-185.00)", font=('consolas', '10')).grid(row=22, column=2, sticky='W')
        D3F = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(D3F, "D3", metGuidedModeSelf)))
        D3F.grid(row=23, column=2, sticky='W')
        D3C = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(D3C, "D3", metGuidedModeSelf)))
        D3C.grid(row=24, column=2, sticky='W')
        Separator(self, orient="vertical").grid(row=21, column=2, rowspan=5, sticky='ens')  
        
        #D4
        tk.Label(self, text="D4: (-185.00,0)", font=('consolas', '10')).grid(row=22, column=3, sticky='W')
        D4F = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(D4F, "D4", metGuidedModeSelf)))
        D4F.grid(row=23, column=3, sticky='W')
        D4C = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(D4C, "D4", metGuidedModeSelf)))
        D4C.grid(row=24, column=3, sticky='W') 
        Separator(self, orient="horizontal").grid(row=25, column=0, columnspan=4, sticky='ew') 
        Separator(self, orient="vertical").grid(row=21, column=3, rowspan=5, sticky='ens') 
        
        #CFIF
        tk.Label(self, text="CFIF: (108.31,15.00)", font=('consolas', '10')).grid(row=26, column=0, sticky='W')
        CFIFF = tk.Button(self, text="Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(CFIFF, "CFIF", metGuidedModeSelf)))
        CFIFF.grid(row=27, column=0, sticky='W')
        CFIFC = tk.Button(self, text="Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(CFIFC, "CFIF", metGuidedModeSelf)))
        CFIFC.grid(row=28, column=0, sticky='W') 
        Separator(self, orient="vertical").grid(row=25, column=0, rowspan=4, sticky='ens') 
        
        #Exit Buttons
        Separator(self, orient="horizontal").grid(row=29, column=0, columnspan=4, sticky='ew') 
        tk.Label(self, text=" ", font=('consolas', '10')).grid(row=30, column=0, columnspan=1, sticky='W')
        
        ExitButton1 = tk.Button(self, text="Conclude Measurements",
                            command=lambda: metGuidedModeSelf.show_frame(conclusion)) #are you sure?
        ExitButton1.grid(row=31, column=2, columnspan=2, sticky='W')
        
        ExitButton2 = tk.Button(self, text="Exit to Map Screen", 
                            command=lambda: metGuidedModeSelf.areYouSureExit()) #are you sure?
        ExitButton2.grid(row=31, column=0, columnspan=2, sticky='W')
        
        #FIF orientation diagram
        fifOrMap = tk.Toplevel()
        tk.Label(fifOrMap, text="FIF Pinhole Orientation Relative to CI Perimeter").grid(row=0, column=0, columnspan=2, sticky='W')
        self.fifOrient = tk.PhotoImage(file="FIF-orientation.png", width=500, height=558)
        tk.Label(fifOrMap, image=self.fifOrient).grid(row=1, column=0, rowspan=10, sticky='W')
        
    def focusCurve(self, sensorButton, fiflabel, metGuidedModeSelf):
        ###########################################################################
        ###Create Dir
        ###########################################################################
        faah = fileAndArrayHandling()
        dirName = faah.createDir(fiflabel, metGuidedModeSelf, 'Focus_Curve')
        
        ###########################################################################
        ###Message user to fill dir (mention label names)
        ###########################################################################
        faah.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      "Suggested " +  str(fiflabel) + " focus curve directory: \n" + str(os.getcwd()) + '\\' + dirName + 
                                      "\nNOTE: the file names will be used to create the Z axis values (distance)\n" +
                                        " so please label the FITS files appropriately\n" +
                                        "(example: 350.fit for the image taken at 350um).")
        
        ###########################################################################
        ###Get images
        ###########################################################################
        imageArray4D, filelist = faah.openAllFITSImagesInDirectory()
        
        ###########################################################################
        ###Create focus curve
        ########################################################################### 
        fC = focusCurve()       
        xInter = fC.stdFocusCurve(fiflabel, imageArray4D, filelist)
        faah.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      "Measured Best focus for " + str(fiflabel) + " is: " + str(xInter) + "um")
        
        ###########################################################################
        ###Nominal best focus
        ###########################################################################
        nominalZ = fC.asphericFocalCurve(fC.fifLocationsCS5[fiflabel][0], fC.fifLocationsCS5[fiflabel][1])
        faah.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      "Nominal Z for " + str(fiflabel) + " is: " + str(nominalZ) + "um in CS5 coordinates.")
        faah.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      "Absolute value of (Nominal Z - Measured Best Focus) = " +  str(np.absolute(nominalZ-xInter)) + 'um')
        
        ###########################################################################
        ###Add Z data to fifCentroidedLocationDict
        ###########################################################################
        metGuidedModeSelf.fifCentroidedLocationDict[fiflabel][2] = xInter
        
        ###########################################################################
        ###Change button text and color
        ###########################################################################
        sensorButton.config(text = "Focus Curve Complete", bg = 'green')
        
        
    def centroidFIF(self, sensorButton, fiflabel, metGuidedModeSelf):
        ###########################################################################
        ###Create Dir
        ###########################################################################
        faah = fileAndArrayHandling()
        dirName = faah.createDir(fiflabel, metGuidedModeSelf, 'Centroid')
        
        ###########################################################################
        ###Message user to fill dir (mention label names)
        ###########################################################################
        faah.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      "Suggested " +  str(fiflabel) + " centroid directory: \n" + str(os.getcwd()) + '\\' + dirName)
        
        ###########################################################################
        ###Get images
        ###########################################################################
        imageArray4D, filelist = faah.openAllFITSImagesInDirectory()
        aa = round(len(filelist)/2) #select a focused image from array a
        
        ###########################################################################
        ###Find fif in image and create subarray
        ###########################################################################
        faah.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      "Centroiding " + str(fiflabel) + " using FITs file:\n" + str(filelist[aa]).replace('/', '\\'))
        fifSubArray, subArrayBoxSize, maxLoc  = centroidFIF.findFIFInImage(self, imageArray4D[aa])
        faah.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      str(fiflabel) + " FIF found at pixel location: (" + str(maxLoc[1]) + "," + str(maxLoc[0]) + "). Will now centroid using that location.")
        
        ###########################################################################
        ###Centroid
        ###########################################################################
        cF = centroidFIF()
        xcen, ycen = cF.findCentroid(fifSubArray, int(subArrayBoxSize/2), int(subArrayBoxSize/2), extendbox = 3)
        
        ###########################################################################
        ###Add offsets to account for subarray
        ###########################################################################
        xcen = xcen + maxLoc[0]-subArrayBoxSize/2
        ycen = ycen + maxLoc[1]-subArrayBoxSize/2
        
        ###########################################################################
        ###Add X and Y data to fifCentroidedLocationDict
        ###########################################################################
        #Account for planet mode
        pM = CCDOpsPlanetMode()
        xOffset, yOffset, _ = pM.readFitsHeader(imageArray4D, filelist, metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile)
        
        #Distance from center of FIF to origin of sensor (x=0, y=0)
        xDistToSensorOrigin = ycen + xOffset 
        yDistToSensorOrigin = xcen + yOffset
        
        #Add X and Y to fifCentroidedLocationDict
        metGuidedModeSelf.fifCentroidedLocationDict[fiflabel][0] = xDistToSensorOrigin
        metGuidedModeSelf.fifCentroidedLocationDict[fiflabel][1] = yDistToSensorOrigin
        
        ###########################################################################
        ###Print Location of FIF Centroid
        ###########################################################################
        faah.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                str(fiflabel) + " center found at location: (" + str(xDistToSensorOrigin) + "," + str(yDistToSensorOrigin) + ")")
        
        ###########################################################################
        ###Change button text and color
        ###########################################################################
        sensorButton.config(text = "Centroid Complete", bg = 'green')
        
        return xDistToSensorOrigin, yDistToSensorOrigin

class conclusion(tk.Frame):
    
    #warning, did not create focus curve or met for X, go back?

    def __init__(self, container, metGuidedModeSelf):
        tk.Frame.__init__(self, container)
        label = tk.Label(self, text="You are on Conclusion", font=('consolas', '10'))
        label.pack(pady=10,padx=10)

        button2 = tk.Button(self, text="Fif page",
                            command=lambda: metGuidedModeSelf.show_frame(fifPage))
        button2.pack()