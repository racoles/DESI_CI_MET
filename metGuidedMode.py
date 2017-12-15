'''
@title metGuidedMode
@author: Rebecca Coles
Updated on Dec 15, 2017
Created on Dec 13, 2017

metGuidedMode
Guided mode for DESI CI FIF metrology.

Modules:

'''

# Import #######################################################################################
import tkinter as tk
################################################################################################

class metGuidedMode(tk.Tk):

    def __init__(self, master):
        '''
        Constructor
        '''
        super(metGuidedMode, self).__init__()
        self.master = master
        master.title("DESI CI Meterology Guided Mode")
        
    def guidedModeFrames(self, consoleLog, logFile):
        '''
        Guide the user through measuring all of the FIFs.
        '''
        #load log and console files
        loadLogging(consoleLog, logFile)
        
        #Create pages for all 22 FIFs
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        
        pages = (startPage, fifPage, conclusion)
        #
        #"RefFIF", 
        #"NFIF", "EFIF", "SFIF", "WFIF", 
        #"A1", "A2", "A3", "A4", 
        #"B1", "B2", "B3", "B4", 
        #"C1", "C2", "C3", "C4", 
        #"D1", "D2", "D3", "D4",
        #"CFIF
        
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
        
class startPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=('consolas', '10'))
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(fifPage))
        button.pack()

        button2 = tk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(fifPage))
        button2.pack()

class fifPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=('consolas', '10'))
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(startPage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(conclusion))
        button2.pack()

class conclusion(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=('consolas', '10'))
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(startPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(fifPage))
        button2.pack()
        
class loadLogging(object):
    '''
    Load log and console files.
    '''
    def __init__(self, consoleLog, logFile):
        '''
        Constructor
        '''
        self.cLog = consoleLog
        self.lFile = logFile