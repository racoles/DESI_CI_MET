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
from tkinter import Button, PhotoImage, Label, Entry, END
################################################################################################

class metGuidedMode(object):
    '''
    Guided mode for DESI CI FIF metrology.
    '''

    def __init__(self, master):
        '''
        Constructor
        '''