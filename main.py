'''
@title DESI_CI_MET
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
    Omatech Sheffield Cordax RS 70 DCC
'''

# Import #######################################################################################
from tkinter import Tk
from inputGUI import inputGUI
################################################################################################

if __name__ == '__main__':
    root = Tk()
    iGUI = inputGUI(root)
    root.mainloop()