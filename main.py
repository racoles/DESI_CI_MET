'''
@title DESI_CI_MET 1.1
@author: Rebecca Coles
Updated on Feb 21, 2017
Created on Dec 11, 2017

Using external packages:
    astropy
    matplotlib
    opencv-python
    
Testing:
    DESI_CI_MET_1.0: DESI CI Camera Back Focus Focus Curve Modules Test (02/22/2018)
Pending Testing:
    Ometech
        Sheffield Cordax RS70 DCC CMM – 40” x 50” x 40” with Renishaw AR1probe changer, PH10 head, PH7 probe. 
        CMM manager software with reverse engineering capabilities as well as automated scanning.
'''

# Import #######################################################################################
from tkinter import Tk
from inputGUI import inputGUI
################################################################################################

if __name__ == '__main__':
    root = Tk()
    iGUI = inputGUI(root)
    root.mainloop()