'''
@title inputGUI
@author: Rebecca Coles
Updated on Dec 8, 2017
Created on Dec 8, 2017

inputGUI
Software for the DESI CI metrology program.
'''

# Import #######################################################################################
from tkinter import Button, PhotoImage, Label, Entry
import tkinter.scrolledtext as ScrolledText
from tkinter.ttk import Separator, Style
################################################################################################

class inputGUI(object):
    '''
    GUI for DESI CI metrology software
    '''
    #Initialize empty data lists

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
        Label(master, text="Guided Mode", font="bold").grid(row=0, column=0, columnspan=2, sticky='W')
        #Guided Mode Description
        Label(master, text="Be guided through measuring the CI FIFs.").grid(row=1, column=0, columnspan=2, sticky='W')
        #Guided Mode Button        
        gmButton = Button(master, text="Begin Guided Mode",bg = "white", command=lambda:self._loadInputDataFile()).grid(row=2, column=0, columnspan=2, sticky='W')
        
        #FIF Map
        self.fifMAP = PhotoImage(file="tempmap.png", width=600, height=600)
        Label(image=self.fifMAP).grid(row=0, column=15, rowspan=3, sticky='W')  
        
        #Grid Separator
        Separator(master, orient="horizontal").grid(row=3, column=0, columnspan=5, sticky='ew')
        Style(master).configure("TSeparator", background="black")
        
        #Manual Mode Label
        Label(master, text="Manual Mode", font="bold").grid(row=4, column=0, columnspan=2, sticky='W')
        #Manual Mode Description
        Label(master, text="Perform manual measurements of the CI FIFs.").grid(row=5, column=0, columnspan=2, sticky='W')
        #Manual Mode Focus Curve
        mmFCButton = Button(master, text="Focus Curve",bg = "white", command=lambda:self._loadInputDataFile()).grid(row=6, column=0, columnspan=2, sticky='W')
        #Manual Mode Centroid FIF
        mmCButton = Button(master, text="Centroid FIF",bg = "white", command=lambda:self._loadInputDataFile()).grid(row=7, column=0, columnspan=2, sticky='W')

        #Grid Separator
        Separator(master, orient="horizontal").grid(row=8, column=0, columnspan=5, sticky='ew')
        #Style(master).configure("TSeparator", background="black")   
 
        #Note Text Box Label
        Label(master, text="Add Note to Log", font="bold").grid(row=9, column=0, columnspan=2, sticky='W')
        #Note Text Box
        noteBox = Entry(master, width=40).grid(row=10, column=0, columnspan=5, sticky='W')
        #Note Text Submit Button
        Button(master, text='Submit', bg = "white", command=lambda:self._log_entry_field(noteBox)).grid(row=10, column=1, columnspan=2, sticky='W')
        
        #Grid Separator
        Separator(master, orient="horizontal").grid(row=11, column=0, columnspan=5, sticky='ew')
        #Style(master).configure("TSeparator", background="black")   
        
        #Log Console
        # create a Text widget with a Scrollbar attached
        self.txt = ScrolledText.ScrolledText(self.master, undo=True)
        self.txt['font'] = ('consolas', '12')
        self.txt.grid(row=12, column=0, columnspan=5, sticky='ew')        
    
        
    def _log_entry_field(self, noteBox):
        print("First Name: %s\nLast Name: %s" % (noteBox.get()))
        noteBox.delete(0,'END')
