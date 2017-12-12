'''
@title focusCurve
@author: Rebecca Coles
Updated on Dec 12, 2017
Created on Dec 12, 2017

cropAndResize
This module holds a series of functions that I use to plot images.

Modules:
stdFocusCurve
    Accepts a 4D numpy array and plots standard deviations of the images.
    Note: assumes filenames are distances (int)
'''

# Import #######################################################################################
from numpy import std, zeros, polyfit
from matplotlib.pyplot import ioff, xlabel, ylabel, title, grid, figure, text
################################################################################################

class focusCurve(object):
    
    def __init__(self):
        '''
        Constructor
        '''

    def stdFocusCurve(self, imageArray4D, filelist):
        '''
        Accepts a 4D numpy array and plots standard deviations of the images.
        note: assumes filenames are distances (int)
        '''
        # Turn interactive plotting off
        ioff()
        
        #initialize std array
        stdList = zeros(imageArray4D.shape[0])
        
        #get stds
        for image in range(imageArray4D.shape[0]):
            flattenedArray = imageArray4D[image].flatten()
            stdList[image] = std(flattenedArray)
        
        #create x values by remove extension from filenames and converting them to ints
        xx = self.fileNameToInt(filelist)
        
        ################### best fit (poly order=2) ###################
        
        #zip xx and yy = std values into array of tulups
        #sort list by distance (x) so xx (distances) are in the proper order in the plot
        sortedX, sortedY  = self.zipAndSort(xx, stdList)
        
        #calculate new x's and y's, poly fuct, and best focus (xSplitPoint)
        xFit, yFit, f2, xSplitPoint = self.xyPolyFit(sortedX, sortedY, 2)
        
        ################### find best focus ###################
        
        #get separate X and Y lists from sorted data
        sortedXL = [kk for kk in sortedX if kk <= xSplitPoint]
        sortedYL = sortedY[:len(sortedXL)]
        sortedXR = sortedX[len(sortedXL):]
        sortedYR = sortedY[len(sortedXL):]
        
        #linear fit each side
        mL, bL = polyfit(sortedXL, sortedYL, 1) #left
        mR, bR = polyfit(sortedXR, sortedYR, 1) #right
        
        #find intercept of the linear fits
        # want position where XL = XR and YL = YR using y =mx +b:
        # mL*sortedXL + bL = mR*sortedXR + bR
        xInter = (bR-bL)/(mL-mR)
        yInter = mL*xInter +bL
        
        #add intercept point to x and y value sets
        sortedXL.append(xInter)
        sortedXR.append(xInter)
        
        ################## plot stds ##################
        fig2 = figure()
        ax2 = fig2.add_subplot(111)
        ax2.plot(sortedX, sortedY, 'ro', xFit, yFit, 
                 sortedXL, [mL*ll+bL for ll in sortedXL], 
                 sortedXR, [mR*mm+bR for mm in sortedXR])
        xlabel('Focal Position (microns)')
        ylabel('Standard Deviation')
        title('Standard Deviation versus Distance')
        text(0, 0, 'Left Linear Fit: y = ' + str(mL) + ' x + ' + str(bL) + 
             '\n\nRight Linear Fit: y = ' + str(mR) + ' x + ' + str(bR) + 
             '\n\nPolynomial Fit:\n        ' + str(f2) +
             '\n\nPolynomial Fit Max Distance= ' + str(xSplitPoint)[0:3] + ' um\n', fontsize = 7, transform=ax2.transAxes)
        grid(True)
        ax2.annotate('Best Focus = ' + str(xInter)[0:5] + ' um', xy=(xInter, yInter), 
                     xytext=(xInter+1, yInter+1), fontsize = 7,)
         
        #save figure
        fig2.savefig('std_vs_position-fitted.png') 
        #return best focus
        return xInter
