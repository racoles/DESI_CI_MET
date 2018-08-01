'''
@title inputGUI
@author: Rebecca Coles
Updated on Jun 21, 2017
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
import time, os, re
from metGuidedMode import metGuidedMode
from metManualMode import metManualMode
from focusCurve import focusCurve
from fileAndArrayHandling import fileAndArrayHandling
from centroidFIF import centroidFIF
from checkCameraOriginLocation import checkCameraOriginLocation
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
        # |"Description"                  |         Console        |
        # |*Focus Curve*                  |           Log          |
        # |*Centroid FIF*                 |                        |
        # |-------------------------------|                        |
        # |Add Note to Log                |                        |
        # |[text box] *Submit*            |                        |
        # |-------------------------------|                        |
        # |                               |                        |
        # |                               |                        |
        # |                               |                        |
        # |          CI Map               |                        |
        # |                               |                        |
        # |                               |                        |
        # |                               |                        |
        # |_______________________________|________________________|
        
        ###########################################################################
        ###Buttons
        ########################################################################### 
        #CS5 Calibration
        ccol = checkCameraOriginLocation()
        #cs5off = cs5Offsets()
        #tk.Label(master, text="CS5 Calibration", font="bold").grid(row=0, column=0, columnspan=2, sticky='W')
        #calibrationScreenButton = tk.Button(master, text="Calibration Offsets",bg = "white",command=lambda:cs5off.calibrationScreen(calibrationScreenButton, self.consoleLog, self.logFile))
        #calibrationScreenButton.grid(row=1, column=0, columnspan=2, sticky='W')

        #Title Label
        tk.Label(master, text="DESI CI Meterology", font="bold").grid(row=0, column=0, columnspan=2, sticky='W')
        
        #Grid Separator
        Separator(master, orient="horizontal").grid(row=2, column=0, columnspan=4, sticky='ew')
        
        #Guided Mode Label
        tk.Label(master, text="Guided Mode", font="bold").grid(row=3, column=0, columnspan=2, sticky='W')
        #Guided Mode Description
        tk.Label(master, text="Be guided through measuring the CI FIFs.").grid(row=4, column=0, columnspan=2, sticky='W')
        #Guided Mode Button        
        tk.Button(master, text="Begin FIF Guided Mode",bg = "white", command=lambda:self._beginGuidedMode(master, self.consoleLog, self.logFile)).grid(row=5, column=0, columnspan=2, sticky='W')
        
        #Grid Separator
        Separator(master, orient="horizontal").grid(row=6, column=0, columnspan=4, sticky='ew')
        Style(master).configure("TSeparator", background="black")
        
        #Manual Mode Labels
        tk.Label(master, text="Manual Mode", font="bold").grid(row=7, column=0, columnspan=2, sticky='W')
        #Manual Mode Centroid Pinhole
        cF = centroidFIF()
        tk.Button(master, text="Centroid Pinhole",bg = "white",command=lambda:cF.alternateCentroid(self.consoleLog, self.logFile)).grid(row=8, column=0, columnspan=2, sticky='W')
        #Manual Mode Check Camera Origin
        tk.Button(master, text="Check Camera Origin",bg = "white",command=lambda:ccol.checkCameraOriginLocation(self.consoleLog, self.logFile)).grid(row=8, column=1, columnspan=2, sticky='W')
        #Manual Mode Temperature Check
        self.recordTempButton = tk.Button(master, text="Record Temperatures",bg = "white",command=lambda:self._recordTemperatures(self.recordTempButton, self.consoleLog, self.logFile))
        self.recordTempButton.grid(row=8, column=2, columnspan=2, sticky='W')
        self._updateLabel()
        #Manual Mode FIF Focus Curve
        tk.Button(master, text="FIF Focus Curve",bg = "white", command=lambda:self._beginManualMode(master, self.consoleLog, self.logFile, "manualFIFFocusCurve")).grid(row=9, column=0, columnspan=1, sticky='W')
        #Manual Mode CCD Focus Curve
        tk.Button(master, text="CCD Focus Curve",bg = "white", command=lambda:self._beginManualMode(master, self.consoleLog, self.logFile, "manualCCDFocusCurve")).grid(row=9, column=1, columnspan=1, sticky='W')
        #Manual Mode CCD Tip/Tilt/Z
        tk.Button(master, text="CCD Tip/Tilt/Z",bg = "white", command=lambda:self._beginManualMode(master, self.consoleLog, self.logFile, "CCDTipTiltZ")).grid(row=10, column=0, columnspan=2, sticky='W')
        #Print focusCurve Dictionary of Nominal Values to Log/Console
        tk.Button(master, text="Print Nominal Values",bg = "white", command=lambda:self._printDictOfNominalCIValues(self.consoleLog, self.logFile, ccol.calOffX, ccol.calOffY)).grid(row=10, column=1, columnspan=2, sticky='W')

        #Grid Separator
        Separator(master, orient="horizontal").grid(row=11, column=0, columnspan=4, sticky='ew')
        #Style(master).configure("TSeparator", background="black")   
 
        #Note Text Box Label
        tk.Label(master, text="Add Note to Log", font="bold").grid(row=12, column=0, columnspan=2, sticky='W')
        #Note Text Box
        noteBox = tk.Entry(master, width=55)
        noteBox.grid(row=13, column=0, columnspan=4, sticky='W')
        #Note Text Submit Button
        tk.Button(master, text='Submit', bg = "white", command=lambda:self._log_entry_field(noteBox, self.consoleLog, self.logFile)).grid(row=13, column=2, columnspan=2, sticky='E')
        
        #Grid Separator
        Separator(master, orient="horizontal").grid(row=14, column=0, columnspan=4, sticky='ew')
        #Style(master).configure("TSeparator", background="black")   
        
        #FIF Map
        self.fifMAP = tk.PhotoImage(file="FPA.png", width=400, height=400)
        tk.Label(image=self.fifMAP).grid(row=15, column=0, rowspan=15, columnspan=4, sticky='W')  
        
        ###########################################################################
        ###Log Console
        ###########################################################################         
        # create a Text widget with a Scrollbar attached
        self.consoleLog = ScrolledText.ScrolledText(self.master, undo=True, height=45)
        self.consoleLog['font'] = ('consolas', '10')
        self.consoleLog.grid(row=0, column=4, rowspan=30, sticky='ew') 
        
        # start log
        startTime = time.strftime("%Y-%m-%dT%H%M%SZ")
        self.logFile = open("DESI_CI_MET_" + startTime + "_log.txt", "w")
        self.logFile.write("Log started: " + startTime + '\n')
        self.consoleLog.insert(tk.END, "Log started: " + startTime + '\n')
        self.consoleLog.configure(state="disable")
        
        ###########################################################################
        ###Create Calibration Directory
        ###########################################################################
        self._createCalibrationDir()     
               
    def _log_entry_field(self, noteBox, consoleLog, logFile):
        '''
        Manually enter text into log.
        '''
        currentTime = time.strftime("%Y-%m-%dT%H%M%SZ")
        # console
        consoleLog.configure(state="normal")
        consoleLog.insert(tk.END,  currentTime + ': ' + str(noteBox.get()) + '\n')
        consoleLog.configure(state="disable")
        # log file
        logFile.write(str(currentTime + ': ' + noteBox.get()) + '\n')
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
            
    def _printDictOfNominalCIValues(self, consoleLog, logFile, calOffX, calOffY):
        '''
        Print focusCurve Dictionary of Nominal Values to Log/Console
        '''
        faah = fileAndArrayHandling()
        fC = focusCurve()
        faah.printDictToFile(fC.fifLocationsCS5, "Nominal FIF Locations in CS5 (X mm, Y mm, Z um)" , self.consoleLog, self.logFile, printNominalDicts = True)
        faah.printDictToFile(fC.CCDLocationsCS5, "Nominal CCD Center Locations in CS5 (X mm, Y mm, Z um)" , self.consoleLog, self.logFile, printNominalDicts = True)       
        faah.printDictToFile(fC.trianglePonitCCDLocationsCS5, "Nominal CCD tip/tilt/Z Measurement Triangle Locations in CS5 (X mm, Y mm, Z um)" , self.consoleLog, self.logFile, printNominalDicts = True)
        
        if calOffX == "Not yet set" or calOffY == "Not yet set":
            faah.pageLogging(consoleLog, logFile, "CS5 Calibration Offsets (mm) (X = " + calOffX + ", Y = " + calOffY + ")\n")
        else:
            faah.pageLogging(consoleLog, logFile, "CS5 Calibration Offsets (mm) (X = " + format(calOffX/1000, '.3f')+ ", Y = " + format(calOffY/1000, '.3f') + ")\n")
            
    def _recordTemperatures(self, button, consoleLog, logFile):
        '''
        Allow the user in enter CI temperatures from the sensors on the CI
        '''
        faah = fileAndArrayHandling()     
        top = tk.Toplevel()
        top.title("Record Temperatures")
        aboutMessage = str("Enter CI temperatures:")
        faah.pageLogging(consoleLog, logFile, aboutMessage)
        
        #Temp1
        tk.Label(top, text="Temp #1 (degrees C) = ").grid(row=1, column=0, sticky='W')
        temp1 = tk.Entry(top, width=20)
        temp1.grid(row=1, column=1, sticky='W')
        temp1Button = tk.Button(top, text='Submit', bg = "white", command=lambda:self._submitTempValue(temp1Button, temp1, "1", consoleLog, logFile))
        temp1Button.grid(row=1, column=2)
        
        #Temp2
        tk.Label(top, text="Temp #2 (degrees C) = ").grid(row=2, column=0, sticky='W')
        temp2 = tk.Entry(top, width=20)
        temp2.grid(row=2, column=1, sticky='W')
        temp2Button = tk.Button(top, text='Submit', bg = "white", command=lambda:self._submitTempValue(temp2Button, temp2, "2", consoleLog, logFile))
        temp2Button.grid(row=2, column=2)
        
        #Temp3
        tk.Label(top, text="Temp #3 (degrees C) = ").grid(row=3, column=0, sticky='W')
        temp3 = tk.Entry(top, width=20)
        temp3.grid(row=3, column=1, sticky='W')
        temp3Button = tk.Button(top, text='Submit', bg = "white", command=lambda:self._submitTempValue(temp3Button, temp3, "3", consoleLog, logFile))
        temp3Button.grid(row=3, column=2)
        
        #Temp4
        tk.Label(top, text="Temp #4 (degrees C) = ").grid(row=4, column=0, sticky='W')
        temp4 = tk.Entry(top, width=20)
        temp4.grid(row=4, column=1, sticky='W')
        temp4Button = tk.Button(top, text='Submit', bg = "white", command=lambda:self._submitTempValue(temp4Button, temp4, "4", consoleLog, logFile))
        temp4Button.grid(row=4, column=2)
        
        #Temp4
        tk.Label(top, text="Temp #5 (degrees C) = ").grid(row=5, column=0, sticky='W')
        temp5 = tk.Entry(top, width=20)
        temp5.grid(row=5, column=1, sticky='W')
        temp5Button = tk.Button(top, text='Submit', bg = "white", command=lambda:self._submitTempValue(temp5Button, temp5, "5", consoleLog, logFile))
        temp5Button.grid(row=5, column=2)
        
        tk.Label(top, text=" ").grid(row=6, column=0, sticky='W')
        exitButton = tk.Button(top, text="Exit Temperature Screen", command=top.destroy)
        exitButton.grid(row=7, column=0)
        
        button.config(bg = 'white')  
        top.wait_window()
            
    def _submitTempValue(self, tempButton, temp, tempSensor, consoleLog, logFile):
        tempButton.config(text = "Entered", bg = 'green') 
        faah = fileAndArrayHandling()
        faah.pageLogging(consoleLog, logFile, "Temp #" + tempSensor + ": " + str(temp.get()) + "C", tempLog = True)
        
    def _updateLabel(self):
        self.recordTempButton.config(bg = 'red') 
        self.master.after(60000*30, self._updateLabel)
        
    def _createCalibrationDir(self):
        ###########################################################################
        ###Get log start time
        ###########################################################################
        logTime = re.findall(r'\d+', self.logFile.name)
        logTime = '-'.join(logTime[:])
        
        ###########################################################################
        ###Create Dir
        ###########################################################################
        file_exists_condition = True
        ittr = 0
        while file_exists_condition:
            if os.path.isdir("Calibration_" + str(logTime) + "_" + str(ittr)):
                ittr += 1
            else:
                os.makedirs("Calibration_" + str(logTime) + "_" + str(ittr))
                file_exists_condition = False
            