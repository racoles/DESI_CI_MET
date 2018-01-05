'''
@title focusCurve
@author: Rebecca Coles
Updated on Dec 12, 2017
Created on Dec 12, 2017

focusCurve
This module holds a series of functions that I use to plot images.

Modules:
stdFocusCurve
    Accepts a 4D numpy array and plots standard deviations of the images.
    Note: assumes filenames are distances (int)
fileNameToInt
    Create x values by remove extension from filenames and converting them to ints
zipAndSort
    Zip xx and yy values into array of tulups
    Sort list by distance (x) so xx (distances) are in the proper order in the plot
xyPolyFit
    Calculate polynomial fit (order given)
    Calculate new x's and y's for plotting
    Find slope = 0 for fit, this will be used to split the data to a left and right liner fit
    Find the first derivative of the poly1d
    Solve deriv =ax + b for deriv = 0 (point of best focus)
'''

# Import #######################################################################################
import numpy as np
import matplotlib.pyplot as py
import os, time
from os.path import basename
from operator import itemgetter

################################################################################################

class focusCurve(object):
    
    def __init__(self):
        '''
        Constructor
        '''

    def stdFocusCurve(self, fiflabel, imageArray4D, filelist):
        '''
        Accepts a 4D numpy array and plots standard deviations of the images.
        note: assumes filenames are distances (int)
        '''
        ###########################################################################
        ###Turn interactive plotting off
        ###########################################################################
        py.ioff()
        
        ###########################################################################
        ###Initialize std array
        ###########################################################################
        stdList = np.zeros(imageArray4D.shape[0])

        ###########################################################################
        ###Get stds
        ###########################################################################
        for image in range(imageArray4D.shape[0]):
            flattenedArray = imageArray4D[image].flatten()
            stdList[image] = np.std(flattenedArray)
        
        ###########################################################################
        ###Create x values by remove extension from filenames and converting them to ints
        ###########################################################################
        xx = self.fileNameToInt(filelist)
        
        ###########################################################################
        ###Best fit (poly order=2)
        ###########################################################################     
        #zip xx and yy = std values into array of tulups
        #sort list by distance (x) so xx (distances) are in the proper order in the plot
        sortedX, sortedY  = self.zipAndSort(xx, stdList)
        
        ###########################################################################
        ###Calculate new x's and y's, poly fuct, and best focus (xSplitPoint)
        ###########################################################################     
        xFit, yFit, f2, xSplitPoint = self.xyPolyFit(sortedX, sortedY, 2)
        
        ###########################################################################
        ###Find Best Focus
        ########################################################################### 
        #get separate X and Y lists from sorted data
        sortedXL = [kk for kk in sortedX if kk <= xSplitPoint]
        sortedYL = sortedY[:len(sortedXL)]
        sortedXR = sortedX[len(sortedXL):]
        sortedYR = sortedY[len(sortedXL):]
        
        #linear fit each side
        mL, bL = np.polyfit(sortedXL, sortedYL, 1) #left
        mR, bR = np.polyfit(sortedXR, sortedYR, 1) #right
        
        #find intercept of the linear fits
        # want position where XL = XR and YL = YR using y =mx +b:
        # mL*sortedXL + bL = mR*sortedXR + bR
        xInter = (bR-bL)/(mL-mR)
        yInter = mL*xInter +bL
        
        #add intercept point to x and y value sets
        sortedXL.append(xInter)
        sortedXR.append(xInter)
        
        ###########################################################################
        ###Plot stds
        ########################################################################### 
        fig2 = py.figure()
        ax2 = fig2.add_subplot(111)
        ax2.plot(sortedX, sortedY, 'ro', xFit, yFit, 
                 sortedXL, [mL*ll+bL for ll in sortedXL], 
                 sortedXR, [mR*mm+bR for mm in sortedXR])
        py.xlabel('Focal Position (microns)')
        py.ylabel('Standard Deviation')
        py.title('Standard Deviation versus Distance')
        py.text(0, 0, 'Left Linear Fit: y = ' + str(mL) + ' x + ' + str(bL) + 
             '\n\nRight Linear Fit: y = ' + str(mR) + ' x + ' + str(bR) + 
             '\n\nPolynomial Fit:\n        ' + str(f2) +
             '\n\nPolynomial Fit Max Distance= ' + str(xSplitPoint)[0:3] + ' um\n', fontsize = 7, transform=ax2.transAxes)
        py.grid(True)
        ax2.annotate('Best Focus = ' + str(xInter)[0:5] + ' um', xy=(xInter, yInter), 
                     xytext=(xInter+1, yInter+1), fontsize = 7,)
         
        ###########################################################################
        ###Save figure
        ###########################################################################        
        fig2.savefig(str(fiflabel) + '_focus_curve_' +  time.strftime("%Y%m%d-%H%M%S") + '.png') 
        #return best focus
        return xInter
    
    def fileNameToInt(self, filelist):
        '''
        Create x values by remove extension from filenames and converting them to ints
        '''
        xx = []
        [xx.append(os.path.splitext(filelist[image])[0]) for image in range(len(filelist))]
        for ii in range(len(xx)):#get basename of files
            xx[ii] = int(basename(xx[ii]))
        return xx
    
    def zipAndSort(self, xx, yy):
        '''
        Zip xx and yy values into array of tulups
        Sort list by distance (x) so xx (distances) are in the proper order in the plot
        '''
        ###########################################################################
        ###Zip xx and yy
        ###########################################################################    
        xy = []
        [xy.append(jj) for jj in zip(xx, yy)]
        
        ###########################################################################
        ###Sort list by distance (x)
        ###########################################################################  
        sortedXY = sorted(xy, key=itemgetter(0))
        
        ###########################################################################
        ###Separate into X and Y
        ########################################################################### 
        sortedX = [kk[0] for kk in sortedXY]
        sortedY = [ll[1] for ll in sortedXY]
        
        return sortedX, sortedY
    
    def xyPolyFit(self, xx, yy, order):
        '''
        Calculate polynomial fit (order given)
        Calculate new x's and y's for plotting
        Find slope = 0 for fit, this will be used to split the data to a left and right liner fit
        Find the first derivative of the poly1d
        Solve deriv =ax + b for deriv = 0 (point of best focus)
        '''
        ###########################################################################
        ###Calculate polynomial
        ########################################################################### 
        funct = np.poly1d(np.polyfit(xx, yy, order))
        
        ###########################################################################
        ###Calculate new x's and y's
        ########################################################################### 
        xFit = np.linspace(xx[0], xx[-1])
        yFit = funct(xFit)
        
        ###########################################################################
        ###Find slope = 0 for fit, this will be used to split the data to a left and right liner fit
        ########################################################################### 
        #find the first derivative of the poly1d
        deriv = np.polyder(funct)
        #solve deriv =ax + b for deriv = 0 (used to split data into left and right sides of the curve)
        bestFocus = (0-deriv.c[1])/(deriv.c[0])
        
        return xFit, yFit, funct, bestFocus
