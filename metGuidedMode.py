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
import os, errno
################################################################################################

class metGuidedMode(tk.Tk):
    consoleLog = []
    logFile = []
        
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
        #Create pages
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
        # console
        cLog.configure(state="normal")
        cLog.insert(tk.END, str(logText) + '\n')
        cLog.configure(state="disable")
        # log file
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
        
        tk.Label(self, text="FIFs can be measured in the order shown below for maximum efficiency.             ", font=('consolas', '10')).grid(row=0, column=0, columnspan=5, sticky='W')
        tk.Button(self, text="Help",
                            command=lambda: metGuidedModeSelf.show_frame(helpPage)).grid(row=0, column=6, sticky='E')
        Separator(self, orient="horizontal").grid(row=1, column=0, columnspan=6, sticky='ew') 
                           
        #Measurement grid
        # RefFIFLabel
        tk.Label(self, text="RefFIF", font=('consolas', '10')).grid(row=2, column=0, columnspan=5, sticky='W')
        tk.Button(self, text="RefFIF Focal Curve",
                            command=lambda: metGuidedModeSelf.show_frame(self.focusCurve("RefFIF", metGuidedModeSelf))).grid(row=3, column=0, sticky='E')


        #Exit Buttons
        ExitButton1 = tk.Button(self, text="Conclude Measurements",
                            command=lambda: metGuidedModeSelf.show_frame(conclusion)) #are you sure?
        ExitButton1.grid(row=3, column=0, columnspan=5, sticky='W')
        
        ExitButton2 = tk.Button(self, text="Exit to Map Screen", 
                            command=lambda: metGuidedModeSelf.areYouSureExit()) #are you sure?
        ExitButton2.grid(row=4, column=0, columnspan=5, sticky='W')
        
    def focusCurve(self, fiflabel, metGuidedModeSelf):
        #Create dir
        dirName = self.createDir(fiflabel, metGuidedModeSelf)
        #Message user to fill dir (mention label names)
        #    Log the message
        metGuidedModeSelf.pageLogging(metGuidedModeSelf.consoleLog, metGuidedModeSelf.logFile, 
                                      fiflabel + " focus curve directory: " + dirName)
        #    Dialogue window
        #create curve
        pass
    
    def centroidFIF(self, fiflabel, metGuidedModeSelf):
        #Create folder
        #message user to fill folder (mention label names) + log the message using metGuidedModeSelf funct
        #find fif in image
        #create subarray (note location offsets)
        #centroid
        #return locations + offsets
        pass
    
    def createDir(self, fiflabel, metGuidedModeSelf):
        #Get log start time
        logTime = [int(s) for s in metGuidedModeSelf.logFile.name.split() if s.isdigit()]
        logTime = '-'.join(logTime[:])
        #Create dir
        try:
            os.makedirs(str(fiflabel + logTime))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        return str(fiflabel + logTime)

class conclusion(tk.Frame):
    
    #warning, did not create focus curve or met for X, go back?

    def __init__(self, container, metGuidedModeSelf):
        tk.Frame.__init__(self, container)
        label = tk.Label(self, text="You are on Conclusion", font=('consolas', '10'))
        label.pack(pady=10,padx=10)

        button2 = tk.Button(self, text="Fif page",
                            command=lambda: metGuidedModeSelf.show_frame(fifPage))
        button2.pack()