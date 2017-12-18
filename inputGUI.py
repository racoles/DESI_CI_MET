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
        
        #Guided Mode Label
        tk.Label(master, text="Guided Mode", font="bold").grid(row=0, column=0, columnspan=2, sticky='W')
        #Guided Mode Description
        tk.Label(master, text="Be guided through measuring the CI FIFs.").grid(row=1, column=0, columnspan=2, sticky='W')
        #Guided Mode Button        
        tk.Button(master, text="Begin Guided Mode",bg = "white", command=lambda:self._beginGuidedMode(master, self.consoleLog, self.logFile)).grid(row=2, column=0, columnspan=2, sticky='W')
        
        #FIF Map
        self.fifMAP = tk.PhotoImage(file="FPA.png", width=350, height=350)
        tk.Label(image=self.fifMAP).grid(row=0, column=4, rowspan=11, sticky='W')  
        
        #Grid Separator
        Separator(master, orient="horizontal").grid(row=3, column=0, columnspan=4, sticky='ew')
        Style(master).configure("TSeparator", background="black")
        
        #Manual Mode Label
        tk.Label(master, text="Manual Mode", font="bold").grid(row=4, column=0, columnspan=2, sticky='W')
        #Manual Mode Description
        tk.Label(master, text="Perform manual measurements of the CI FIFs.").grid(row=5, column=0, columnspan=2, sticky='W')
        #Manual Mode Focus Curve
        tk.Button(master, text="Focus Curve",bg = "white", command=lambda:self._loadInputDataFile()).grid(row=6, column=0, columnspan=2, sticky='W')
        #Manual Mode Centroid FIF
        tk.Button(master, text="Centroid FIF",bg = "white", command=lambda:self._loadInputDataFile()).grid(row=7, column=0, columnspan=2, sticky='W')

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
        
        #Log Console
        # create a Text widget with a Scrollbar attached
        self.consoleLog = ScrolledText.ScrolledText(self.master, undo=True)
        self.consoleLog['font'] = ('consolas', '10')
        self.consoleLog.grid(row=12, column=0, columnspan=5, sticky='ew') 
        # start log
        startTime = time.strftime("%Y%m%d-%H%M%S")
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