'''
@title metGuidedMode
@author: Rebecca Coles
Updated on Dec 19, 2017
Created on Dec 13, 2017

metGuidedMode
Guided mode for DESI CI FIF metrology.

Classes and Modules:

'''

# Import #######################################################################################
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Separator
import os, errno, re
from focusCurve import focusCurve
from fileAndArrayHandling import fileAndArrayHandling
from centroidFIF import centroidFIF
################################################################################################

class metGuidedMode(tk.Tk):
    consoleLog = []
    logFile = []
    fifCentroidedLocationDict = {}
        
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
        
    def pageLogging(self, cLog, lFile, logText):
        '''
        Send text to console and log file.
        '''
        ###########################################################################
        ###Send text to console
        ###########################################################################
        cLog.configure(state="normal")
        cLog.insert(tk.END, str(logText) + '\n')
        cLog.configure(state="disable")
        
        ###########################################################################
        ###Send text to log file
        ###########################################################################
        lFile.write(str(logText) + '\n')
        
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
        tk.Label(self, text="FIFs can be measured in the order shown below for maximum efficiency.             ", font=('consolas', '10')).grid(row=0, column=0, columnspan=5, sticky='W')
        tk.Button(self, text="Help",
                            command=lambda: metGuidedModeSelf.show_frame(helpPage)).grid(row=0, column=6, sticky='E')
        Separator(self, orient="horizontal").grid(row=1, column=0, columnspan=6, sticky='ew') 
                           
        #Measurement grid
        # RefFIFLabel
        tk.Label(self, text="RefFIF", font=('consolas', '10')).grid(row=2, column=0, columnspan=1, sticky='W')
        RefFIFF = tk.Button(self, text="RefFIF Focus Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve(RefFIFF, "RefFIF", metGuidedModeSelf))).grid(row=3, column=0, sticky='W')
        RefFIFC = tk.Button(self, text="RefFIF Centroid",
                            command=lambda: metGuidedModeSelf.show_frame(self.centroidFIF(RefFIFC, "RefFIF", metGuidedModeSelf))).grid(row=4, column=0, sticky='W')

        #Exit Buttons
        Separator(self, orient="horizontal").grid(row=5, column=0, columnspan=6, sticky='ew') 
        ExitButton1 = tk.Button(self, text="Conclude Measurements",
                            command=lambda: metGuidedModeSelf.show_frame(conclusion)) #are you sure?
        ExitButton1.grid(row=6, column=1, columnspan=1, sticky='W')
        
        ExitButton2 = tk.Button(self, text="Exit to Map Screen", 
                            command=lambda: metGuidedModeSelf.areYouSureExit()) #are you sure?
        ExitButton2.grid(row=6, column=0, columnspan=1, sticky='W')
        
    def focusCurve(self, RefFIFF, fiflabel, metGuidedModeSelf):
        ###########################################################################
        ###Create Dir
        ###########################################################################
        dirName = self.createDir(fiflabel, metGuidedModeSelf)
        
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
        fC = focusCurve()
        imageArray4D, filelist = fH.openAllFITSImagesInDirectory()
        
        ###########################################################################
        ###Create focus curve
        ###########################################################################        
        xInter = fC.stdFocusCurve(imageArray4D, filelist)
        metGuidedModeSelf.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      "Measured Best focus for " + str(fiflabel) + " is: " + str(xInter) + "um")
        
        ###########################################################################
        ###Nominal best focus
        ########################################################################### 
        
    def centroidFIF(self, sensorButton, fiflabel, metGuidedModeSelf):
        ###########################################################################
        ###Create Dir
        ###########################################################################
        dirName = self.createDir(fiflabel, metGuidedModeSelf)
        
        ###########################################################################
        ###Message user to fill dir (mention label names)
        ###########################################################################
        metGuidedModeSelf.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      "Suggested " +  str(fiflabel) + " centroid directory: \n" + str(os.getcwd()) + '\\' + dirName)
        
        ###########################################################################
        ###Get images
        ###########################################################################
        fH = fileAndArrayHandling()
        imageArray4D, filelist = fH.openAllFITSImagesInDirectory()
        
        ###########################################################################
        ###Find fif in image and create subarray
        ###########################################################################
        metGuidedModeSelf.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      "Centroiding " + str(fiflabel) + " using FITs file:\n" + str(filelist[0]).replace('/', '\\'))
        fifSubArray, subArrayBoxSize, maxLoc  = centroidFIF.findFIFInImage(self, imageArray4D[0])
        metGuidedModeSelf.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      str(fiflabel) + "FIF found at pixel location: (" + str(maxLoc[0]) + "," + str(maxLoc[1]) + "). Will now centroid using that location.")
        
        ###########################################################################
        ###Centroid
        ###########################################################################
        xcen, ycen = centroidFIF.findCentroid(fifSubArray, int(subArrayBoxSize/2), int(subArrayBoxSize/2), extendbox = 3)
        
        ###########################################################################
        ###Add offsets to account for subarray
        ###########################################################################
        xcen = xcen + maxLoc[0]-subArrayBoxSize/2
        ycen = ycen + maxLoc[1]-subArrayBoxSize/2
        metGuidedModeSelf.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      str(fiflabel) + " center found at location: (" + str(xcen) + "," + str(ycen) + ")")
        
        ###########################################################################
        ###Save values to metGuidedMode dictionary: fifCentroidedLocationDict
        ###########################################################################
        metGuidedModeSelf.fifCentroidedLocationDict[fiflabel] = (xcen, ycen)
        
        ###########################################################################
        ###Change button text and color
        ###########################################################################
        sensorButton.config(text = "Centroid Complete", bg = 'green')

    
    def createDir(self, fiflabel, metGuidedModeSelf):
        ###########################################################################
        ###Get log start time
        ###########################################################################
        logTime = re.findall(r'\d+', metGuidedModeSelf.logFile.name)
        logTime = '-'.join(logTime[:])
        
        ###########################################################################
        ###Create Dir
        ###########################################################################
        try:
            os.makedirs(str(fiflabel + "_" + logTime))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        return str(fiflabel + "_" +  logTime)
    
    def asphericFocalCurve(self, x, y):
        '''
        Use ZEMAX Image surface definition, of 10th order even 
        polynomial, to find best focus nominal Z (mm) for a FIF
        that has its center pinhole at location (x, y).
        
        r = sqrt(x^2 + y^2) (mm)
        1/c = -4977.99mm
        k = 0
        
        Aspheric terms
        a2 = ((r^2)/(1/c))/(1+SQRT(1-(r^2/(1/c)^2)))
        a4 = (-0.00000000029648)r^4
        a6 = (0.0000000000000034523)r^6
        a8 = (-1.8042E-20)r^8
        a10 = (3.2571E-26)r^10
        
        nominalZ = a2 + a4 + a6 + a8 + a10
        '''
        #r = sqrt(x^2 + y^2)
        #inv_c = -4977.99
        #return nominalZ

class conclusion(tk.Frame):
    
    #warning, did not create focus curve or met for X, go back?

    def __init__(self, container, metGuidedModeSelf):
        tk.Frame.__init__(self, container)
        label = tk.Label(self, text="You are on Conclusion", font=('consolas', '10'))
        label.pack(pady=10,padx=10)

        button2 = tk.Button(self, text="Fif page",
                            command=lambda: metGuidedModeSelf.show_frame(fifPage))
        button2.pack()