'''
@title DESI_CI_MET
@author: Rebecca Coles
Updated on Dec 15, 2017
Created on Dec 11, 2017

astropy
matplotlib
opencv-python
'''

# Import #######################################################################################
from tkinter import Tk
from inputGUI import inputGUI
################################################################################################

if __name__ == '__main__':
    root = Tk()
    iGUI = inputGUI(root)
    root.mainloop()