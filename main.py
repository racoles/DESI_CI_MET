'''
@title DESI_CI_MET 1.2
@author: Rebecca Coles
Updated on Feb 21, 2017
Created on Dec 11, 2017

Using external packages:
    astropy
    matplotlib
    opencv-python
    
Testing:
    DESI_CI_MET_1.0: Haas Probe test (02/26/2018)
    DESI_CI_MET_1.1: Haas Software test (03/07/2018)
Pending Testing:
    Ometech
        Sheffield Cordax RS70 DCC CMM – 40” x 50” x 40” with Renishaw AR1probe changer, PH10 head, PH7 probe. 
        CMM manager software with reverse engineering capabilities as well as automated scanning.
        
        
Notes:

BackFocus
    Precision measurements of each camera's back focus is not necessary. Back focus measurements were only done to check that al 5 cameras are close to each other.

    We will measure the Z position of three points on each CCD as accurately as possible. 
    The 3 primary sources of error are:
    CMM (or HAAS) Z axis scale error ~ 2-3 micron CMM, (10 - 15 micron Haas)
    "best focus" determination error from the focus curves  of 100 micron pinhole onto CCD ~ 10 - 15 microns
    Ability to adjust the TTF to the desired value  with the micrometers  ~ 5 microns (not demonstrated yet)

    Therefore we should be able to meet the 50 micron Z spec for the CCDs

'''

# Import #######################################################################################
from tkinter import Tk
from inputGUI import inputGUI
################################################################################################

if __name__ == '__main__':
    root = Tk()
    iGUI = inputGUI(root)
    root.mainloop()