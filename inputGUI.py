'''
@title inputGUI
@author: Rebecca Coles
Updated on Feb 21, 2017
Created on Dec 8, 2017

inputGUI
Software for the DESI CI metrology program.

Modules:
_log_entry_field:
    Manually enter text into log.
_beginGuidedMode(self, master):
    Set up frames for guided mode

'''

# Import #######################################################################################
import tkinter as tk
import tkinter.scrolledtext as ScrolledText
from tkinter.ttk import Separator, Style
import time
from metGuidedMode import metGuidedMode
from metManualMode import metManualMode
from focusCurve import focusCurve
from fileAndArrayHandling import fileAndArrayHandling
from centroidFIF import centroidFIF
from alternateCentroidMethods import gmsCentroid, smsBisector, findCentroid
from CCDOpsPlanetMode import CCDOpsPlanetMode
from cs5Offsets import cs5Offsets
################################################################################################

class inputGUI(object):
    '''
    GUI for DESI CI metrology software
    '''

    def __init__(self, master):
        '''
        Constructor
        '''
        self.master = master
        master.title("DESI CI Meterology")
        
        #Construct GUI
        #  ________________________________________________________
        # |Guided Mode                    |                        |
        # |"Guided Mode Description"      |                        |
        # |*Guided Metrology Button*      |                        |
        # |-------------------------------|                        |
        # |Manual Mode                    |                        |
        # |"Description"                  |         CI Map         |
        # |*Focus Curve*                  |                        |
        # |*Centroid FIF*                 |                        |
        # |-------------------------------|                        |
        # |Add Note to Log                |                        |
        # |[text box] *Submit*            |                        |
        # |--------------------------------------------------------|
        # |                                                        |
        # |                                                        |
        # |                                                        |
        # |                      Log Console                       |
        # |                                                        |
        # |                                                        |
        # |                                                        |
        # |________________________________________________________|
        
        ###########################################################################
        ###Buttons
        ########################################################################### 
        #CS5 Calibration
        cs5off = cs5Offsets()
        tk.Label(master, text="CS5 Calibration", font="bold").grid(row=0, column=0, columnspan=2, sticky='W')
        calibrationScreenButton = tk.Button(master, text="Centroid Pinhole Image",bg = "white",command=lambda:cs5off.calibrationScreen(calibrationScreenButton, self.consoleLog, self.logFile))
        calibrationScreenButton.grid(row=1, column=0, columnspan=2, sticky='W')
        
        #Grid Separator
        Separator(master, orient="horizontal").grid(row=2, column=0, columnspan=4, sticky='ew')
        
        #Guided Mode Label
        tk.Label(master, text="Guided Mode", font="bold").grid(row=3, column=0, columnspan=2, sticky='W')
        #Guided Mode Description
        tk.Label(master, text="Be guided through measuring the CI FIFs.").grid(row=4, column=0, columnspan=2, sticky='W')
        #Guided Mode Button        
        tk.Button(master, text="Begin FIF Guided Mode",bg = "white", command=lambda:self._beginGuidedMode(master, self.consoleLog, self.logFile)).grid(row=5, column=0, columnspan=2, sticky='W')
        
        #FIF Map
        self.fifMAP = tk.PhotoImage(file="FPA.png", width=400, height=400)
        tk.Label(image=self.fifMAP).grid(row=0, column=4, rowspan=14, sticky='W')  
        
        #Grid Separator
        Separator(master, orient="horizontal").grid(row=6, column=0, columnspan=4, sticky='ew')
        Style(master).configure("TSeparator", background="black")
        
        #Manual Mode Labels
        tk.Label(master, text="Manual Mode", font="bold").grid(row=7, column=0, columnspan=2, sticky='W')
        #Manual Mode Description
        tk.Button(master, text="Centroid Pinhole Image",bg = "white",command=lambda:self._alternateCentroid(self.consoleLog, self.logFile)).grid(row=8, column=0, columnspan=2, sticky='W')
        #Manual Mode FIF Focus Curve
        tk.Button(master, text="FIF Focus Curve",bg = "white", command=lambda:self._beginManualMode(master, self.consoleLog, self.logFile, "manualFIFFocusCurve")).grid(row=9, column=0, columnspan=1, sticky='W')
        #Manual Mode CCD Focus Curve
        tk.Button(master, text="CCD Focus Curve",bg = "white", command=lambda:self._beginManualMode(master, self.consoleLog, self.logFile, "manualCCDFocusCurve")).grid(row=9, column=1, columnspan=1, sticky='W')
        #Manual Mode CCD Tip/Tilt/Z
        tk.Button(master, text="CCD Tip/Tilt/Z",bg = "white", command=lambda:self._beginManualMode(master, self.consoleLog, self.logFile, "CCDTipTiltZ")).grid(row=10, column=0, columnspan=2, sticky='W')
        #Print focusCurve Dictionary of Nominal Values to Log/Console
        tk.Button(master, text="Print Nominal Values",bg = "white", command=lambda:self._printDictOfNominalCIValues()).grid(row=10, column=1, columnspan=2, sticky='W')

        #Grid Separator
        Separator(master, orient="horizontal").grid(row=11, column=0, columnspan=4, sticky='ew')
        #Style(master).configure("TSeparator", background="black")   
 
        #Note Text Box Label
        tk.Label(master, text="Add Note to Log", font="bold").grid(row=12, column=0, columnspan=2, sticky='W')
        #Note Text Box
        noteBox = tk.Entry(master, width=40)
        noteBox.grid(row=13, column=0, columnspan=5, sticky='W')
        #Note Text Submit Button
        tk.Button(master, text='Submit', bg = "white", command=lambda:self._log_entry_field(noteBox, self.consoleLog, self.logFile)).grid(row=13, column=2, columnspan=2)
        
        #Grid Separator
        Separator(master, orient="horizontal").grid(row=14, column=0, columnspan=4, sticky='ew')
        #Style(master).configure("TSeparator", background="black")   

        ###########################################################################
        ###Log Console
        ###########################################################################         
        # create a Text widget with a Scrollbar attached
        self.consoleLog = ScrolledText.ScrolledText(self.master, undo=True, height=15)
        self.consoleLog['font'] = ('consolas', '10')
        self.consoleLog.grid(row=15, column=0, columnspan=5, sticky='ew') 
        # start log
        startTime = time.strftime("%Y-%m-%dT%H%M%SZ")
        self.logFile = open("DESI_CI_MET_" + startTime + "_log.txt", "w")
        self.logFile.write("Log started: " + startTime + '\n')
        self.consoleLog.insert(tk.END, "Log started: " + startTime + '\n')
        self.consoleLog.configure(state="disable")
               
    def _log_entry_field(self, noteBox, consoleLog, logFile):
        '''
        Manually enter text into log.
        '''
        # console
        consoleLog.configure(state="normal")
        consoleLog.insert(tk.END, str(noteBox.get()) + '\n')
        consoleLog.configure(state="disable")
        # log file
        logFile.write(str(noteBox.get()) + '\n')
        logFile.flush()
        noteBox.delete(0, tk.END)
        
    def _beginGuidedMode(self, master, consoleLog, logFile):
        '''
        Set up frames for guided mode
        '''
        #Setup Guided Mode
        gMode = metGuidedMode(master)
        gMode.consoleLog = consoleLog
        gMode.logFile = logFile
        gMode.guidedModeFrames()
        
    def _beginManualMode(self, master, consoleLog, logFile, manualFunction):
        '''
        Set up frames for guided mode
        '''
        #Setup Manual Mode
        mMode = metManualMode(master)
        mMode.consoleLog = consoleLog
        mMode.logFile = logFile

        #Manual Mode FIF Focus Curve
        if manualFunction == "manualFIFFocusCurve":
            mMode.manualFIFFocusCurve()
            
        #Manual Mode CCD Focus Curve
        if manualFunction == "manualCCDFocusCurve":
            mMode.manualCCDFocusCurve()
            
        #Manual Mode CCD Tip/Tilt/Z
        if manualFunction == "CCDTipTiltZ":
            mMode.CCDTipTiltZ()
            
    def _printDictOfNominalCIValues(self):
        '''
        Print focusCurve Dictionary of Nominal Values to Log/Console
        '''
        faah = fileAndArrayHandling()
        fC = focusCurve()
        faah.printDictToFile(fC.fifLocationsCS5, "Nominal FIF Locations in CS5 (X mm, Y mm, Z mm)" , self.consoleLog, self.logFile, printNominalDicts = True)
        faah.printDictToFile(fC.CCDLocationsCS5, "Nominal CCD Center Locations in CS5 (X mm, Y mm, Z mm)" , self.consoleLog, self.logFile, printNominalDicts = True)       
        faah.printDictToFile(fC.trianglePonitCCDLocationsCS5, "Nominal CCD tip/tilt/Z Measurement Triangle Locations in CS5 (X mm, Y mm, Z mm)" , self.consoleLog, self.logFile, printNominalDicts = True)
        
    def _alternateCentroid(self, consoleLog, logFile):
        '''
        Centroid pinhole image using alternate methods.
        '''
        
        #Get image
        faah = fileAndArrayHandling()
        imageArray4D, filelist = faah.openAllFITSImagesInDirectory()
        aa = round(len(filelist)/2) #select a focused image from array
        
        #Log image that will be used for centroiding
        faah = fileAndArrayHandling()
        faah.pageLogging(consoleLog, logFile, 
                         "Centroiding image: " +  str(filelist[aa]).replace('/', '\\'))
        
        #Get location of pinhole image in (rows, columns)
        cF = centroidFIF()
        fifSubArray, subArrayBoxSize, maxLoc = cF.findFIFInImage(imageArray4D[aa])
        
        #Account for planet mode
        pM = CCDOpsPlanetMode()
        xOffset, yOffset, _ = pM.readFitsHeader(imageArray4D, filelist, consoleLog, logFile)
        
        #Use alternate methods to centroid pinhole image
        #    gmsCentroid: Gaussian Marginal Sum (GMS) Centroid Method.
        xCenGMS, yCenGMS, xErrGMS, yErrGMS = gmsCentroid(imageArray4D[aa], maxLoc[1], maxLoc[0], 
                                                         int(round(subArrayBoxSize/2)), int(round(subArrayBoxSize/2)), axis='both', verbose=False)
        #    smsBisector: Sobel Marginal Sum (SMS) Bisector Method.
        xCenSMS, yCenSMS, _ = smsBisector(imageArray4D[aa], maxLoc[1], maxLoc[0], int(round(subArrayBoxSize/2)), 
                                          int(round(subArrayBoxSize/2)), axis='both', clipStars=False, wfac=1, verbose=False)
        #    alternateCentroidMethods.findCentroid: iterative GMS method centroid fitting.
        xCenFC, yCenFC, xErrFC, yErrFC = findCentroid(imageArray4D[aa], maxLoc[0], maxLoc[1], 
                                                      int(round(subArrayBoxSize/2)), maxiter=1000, tol=0.01, verbose=False)
        #    centroidFIF.findCentroid
        xCencF, yCencF = cF.findCentroid(fifSubArray, int(round(subArrayBoxSize/2)), int(round(subArrayBoxSize/2)), extendbox = 3)
        xCencF = xCencF + maxLoc[0]-subArrayBoxSize/2
        yCencF = yCencF + maxLoc[1]-subArrayBoxSize/2

        #Print Results
        faah.pageLogging(consoleLog, logFile,
                        "Pinhole image found at (rows, columns): (" + str(maxLoc[1] + xOffset) + ', ' + str(maxLoc[0] + yOffset)+ ')\n' +
                        "GMS Centroid (rows, columns): (" +  format(xCenGMS + xOffset, '.2f') + ' +/- ' + format(xErrGMS, '.2f') + 
                        ', ' + format(yCenGMS + yOffset, '.2f') + ' +/- ' + format(yErrGMS, '.2f') + ')\n' +
                        "SMS Bisector Centroid (rows, columns): (" +  format(xCenSMS + xOffset, '.2f') + ', ' + format(yCenSMS + yOffset, '.2f') + ')\n' +
                        "Iterative GMS Centroid (rows, columns): (" +  format(xCenFC + xOffset, '.2f') + ' +/- ' + format(xErrFC, '.2f') + ', ' +
                         format(yCenFC + yOffset, '.2f') + '+/-' + format(yErrFC, '.2f') + ')\n' +
                        "IDL DAOPHOT Centroid (rows, columns): (" + format(yCencF + xOffset, '.2f') + ', ' + format(xCencF + yOffset, '.2f')+ ')\n\n'
                         "In planet mode (xOffset = " + str(xOffset) + ", yOffset = " + str(yOffset) + ")\n"                   
                        "Pinhole image found at (rows, columns): (" + str(maxLoc[1]) + ', ' + str(maxLoc[0])+ ')\n' +
                        "GMS Centroid (rows, columns): (" +  format(xCenGMS, '.2f') + ' +/- ' + format(xErrGMS, '.2f') + 
                        ', ' + format(yCenGMS, '.2f') + ' +/- ' + format(yErrGMS, '.2f') + ')\n' +
                        "SMS Bisector Centroid (rows, columns): (" +  format(xCenSMS, '.2f') + ', ' + format(yCenSMS, '.2f') + ')\n' +
                        "Iterative GMS Centroid (rows, columns): (" +  format(xCenFC, '.2f') + ' +/- ' + format(xErrFC, '.2f') + ', ' +
                         format(yCenFC, '.2f') + '+/-' + format(yErrFC, '.2f') + ')\n' +
                        "IDL DAOPHOT Centroid (rows, columns): (" + format(yCencF, '.2f') + ', ' + format(xCencF, '.2f')+ ')\n\n', doubleSpaceWithTime = False)
