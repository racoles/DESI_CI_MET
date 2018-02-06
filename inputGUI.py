'''
@title inputGUI
@author: Rebecca Coles
Updated on Dec 14, 2017
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
        #Guided Mode Label
        tk.Label(master, text="Guided Mode", font="bold").grid(row=0, column=0, columnspan=2, sticky='W')
        #Guided Mode Description
        tk.Label(master, text="Be guided through measuring the CI FIFs.").grid(row=1, column=0, columnspan=2, sticky='W')
        #Guided Mode Button        
        tk.Button(master, text="Begin FIF Guided Mode",bg = "white", command=lambda:self._beginGuidedMode(master, self.consoleLog, self.logFile)).grid(row=2, column=0, columnspan=2, sticky='W')
        
        #FIF Map
        self.fifMAP = tk.PhotoImage(file="FPA.png", width=350, height=350)
        tk.Label(image=self.fifMAP).grid(row=0, column=4, rowspan=11, sticky='W')  
        
        #Grid Separator
        Separator(master, orient="horizontal").grid(row=3, column=0, columnspan=4, sticky='ew')
        Style(master).configure("TSeparator", background="black")
        
        #Manual Mode Labels
        tk.Label(master, text="Manual Mode", font="bold").grid(row=4, column=0, columnspan=2, sticky='W')
        #Manual Mode Description
        tk.Label(master, text="Perform manual measurements").grid(row=5, column=0, columnspan=2, sticky='W')
        #Manual Mode FIF Focus Curve
        tk.Button(master, text="FIF Focus Curve",bg = "white", command=lambda:self._beginManualMode(master, self.consoleLog, self.logFile, "manualFIFFocusCurve")).grid(row=6, column=0, columnspan=1, sticky='W')
        #Manual Mode CCD Focus Curve
        tk.Button(master, text="CCD Focus Curve",bg = "white", command=lambda:self._beginManualMode(master, self.consoleLog, self.logFile, "manualCCDFocusCurve")).grid(row=6, column=1, columnspan=1, sticky='W')
        #Manual Mode CCD Tip/Tilt/Z
        tk.Button(master, text="CCD Tip/Tilt/Z",bg = "white", command=lambda:self._beginManualMode(master, self.consoleLog, self.logFile, "CCDTipTiltZ")).grid(row=7, column=0, columnspan=2, sticky='W')

        #Grid Separator
        Separator(master, orient="horizontal").grid(row=8, column=0, columnspan=4, sticky='ew')
        #Style(master).configure("TSeparator", background="black")   
 
        #Note Text Box Label
        tk.Label(master, text="Add Note to Log", font="bold").grid(row=9, column=0, columnspan=2, sticky='W')
        #Note Text Box
        noteBox = tk.Entry(master, width=40)
        noteBox.grid(row=10, column=0, columnspan=5, sticky='W')
        #Note Text Submit Button
        tk.Button(master, text='Submit', bg = "white", command=lambda:self._log_entry_field(noteBox, self.consoleLog, self.logFile)).grid(row=10, column=2, columnspan=2)
        
        #Grid Separator
        Separator(master, orient="horizontal").grid(row=11, column=0, columnspan=4, sticky='ew')
        #Style(master).configure("TSeparator", background="black")   

        ###########################################################################
        ###Log Console
        ###########################################################################         
        # create a Text widget with a Scrollbar attached
        self.consoleLog = ScrolledText.ScrolledText(self.master, undo=True)
        self.consoleLog['font'] = ('consolas', '10')
        self.consoleLog.grid(row=12, column=0, columnspan=5, sticky='ew') 
        # start log
        startTime = time.strftime("%Y-%m-%dT%H%M%SZ")
        self.logFile = open("DESI_CI_MET_" + startTime + "_log.txt", "w")
        self.logFile.write("Log started: " + startTime + '\n')
        self.consoleLog.insert(tk.END, "Log started: " + startTime + '\n')
        self.consoleLog.configure(state="disable")
        
        ###########################################################################
        ###Print focusCurve Dictionary of Nominal Values to Log/Console
        ###########################################################################
        faah = fileAndArrayHandling()
        fc = focusCurve()
               
        
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