'''
@title RSA_Metrology
@author: Rebecca Coles
Updated on Dec 11, 2017
Created on Dec 11, 2017
'''

# Import #######################################################################################
from tkinter import Tk
from inputGUI import inputGUI
################################################################################################

if __name__ == '__main__':
    root = Tk()
    iGUI = inputGUI(root)
    root.mainloop()
    
    
    #im = imageToArray()
    #fH = fileHandling()
    #pl = plots()
    
    
    #STD focus curve for a 4D array of FITs images
    #imageArray, fileList = im.openAllFITSImagesInDirectory()
    #pl.stdPlotAll(imageArray, fileList)
