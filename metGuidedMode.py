'''
@title metGuidedMode
@author: Rebecca Coles
Updated on Dec 13, 2017
Created on Dec 13, 2017

metGuidedMode
Guided mode for DESI CI FIF metrology.

Modules:
_log_entry_field:
    Manually enter text into log.

'''

# Import #######################################################################################
from tkinter import Frame
################################################################################################

class metGuidedMode(object):
    '''
    Guided mode for DESI CI FIF metrology.
    '''

    def __init__(self, master):
        '''
        Constructor
        '''
        
    def runGuidedMode(self):
        '''
        Guide the user through measuring all of the FIFs.
        '''
        #Create pages for all 22 FIFs
        container = Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        pages = list(range(0, 23)) #start page + FIF pages + conclusion page
        for page in (pages):
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