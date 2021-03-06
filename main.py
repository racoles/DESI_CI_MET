'''
@title DESI_CI_MET 1.5
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
    DESI_CI_MET_1.2: Haas Software test (03/27/2018-03/30/2018)
    DESI_CI_MET_1.2: Haas Software test (04/23/2018) 
    DESI_CI_MET_1.2: Haas Software test (04/27/2018)   
    DESI_CI_MET_1.3: Haas Software test (04/30/2018)   
    DESI_CI_MET_1.3: Haas Software test (05/02/2018)  
    DESI_CI_MET_1.3: Haas DMM Magnification Test (05/03/2018)     
    DESI_CI_MET_1.4: Haas Software test (05/31/2018-06/01/2018)
    DESI_CI_MET_1.5: Ometech Software test (06/27/2018)
    
      
Pending Testing:
    Ometech
        Sheffield Cordax RS70 DCC CMM – 40” x 50” x 40” with Renishaw AR1probe changer, PH10 head, PH7 probe. 
        CMM manager software with reverse engineering capabilities as well as automated scanning.
        
Notes:

BackFocus
    Precision measurements of each camera's back focus is not necessary. Back focus measurements were only done to check that all 5 cameras are close to each other.

    We will measure the Z position of three points on each CCD as accurately as possible. 
    The 3 primary sources of error are:
    CMM (or HAAS) Z axis scale error ~ 2-3 micron CMM, (10 - 15 micron Haas)
    "best focus" determination error from the focus curves  of 100 micron pinhole onto CCD ~ 10 - 15 microns
    Ability to adjust the TTF to the desired value  with the micrometers  ~ 5 microns (not demonstrated yet)

    Therefore we should be able to meet the 50 micron Z spec for the CCDs
    
Sensor -> TTF Baseplate Distance:
    The sensor to TTF baseplate distance (according to the SolidWorks model):
    C: 86.88mm
    N,E,S,W: 104.512mm

'''

# Import #######################################################################################
from tkinter import Tk
from inputGUI import inputGUI
################################################################################################

if __name__ == '__main__':
    root = Tk()
    iGUI = inputGUI(root)
    root.mainloop()