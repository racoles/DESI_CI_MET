'''
@title focusCurve
@author: Rebecca Coles
Updated on Feb 01, 2017
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
import os, time, math
from os.path import basename
from operator import itemgetter
################################################################################################
        
class focusCurve(object):

    #Dict of (x,y) for FIF centers (mm)
    fifLocationsCS5 = {"RefFIF" : (199.28,-345.15,asphericFocalCurve(focusCurve.focusCurve.fifLocationsCS5["RefFIF"][0], focusCurve.fifLocationsCS5["RefFIF"][1])), 
                        "NFIF" : (-108.31,-383.55,asphericFocalCurve(focusCurve.fifLocationsCS5["NFIF"][0], focusCurve.fifLocationsCS5["NFIF"][1])), 
                        "WFIF" : (-383.55,108.31,asphericFocalCurve(focusCurve.fifLocationsCS5["WFIF"][0], focusCurve.fifLocationsCS5["WFIF"][1])),
                        "SFIF" : (108.31,383.55,asphericFocalCurve(focusCurve.fifLocationsCS5["SFIF"][0], focusCurve.fifLocationsCS5["SFIF"][1])), 
                        "EFIF" : (383.55,-108.31,asphericFocalCurve(focusCurve.fifLocationsCS5["EFIF"][0], focusCurve.fifLocationsCS5["EFIF"][1])),
                        "CFIF" : (108.31,15.00,asphericFocalCurve(focusCurve.fifLocationsCS5["CFIF"][0], focusCurve.fifLocationsCS5["CFIF"][1])),
                        "A1" : (281.82,-281.82,asphericFocalCurve(focusCurve.fifLocationsCS5["A1"][0], focusCurve.fifLocationsCS5["A1"][1])),
                        "A2" : (-281.82,-281.82,asphericFocalCurve(focusCurve.fifLocationsCS5["A2"][0], focusCurve.fifLocationsCS5["A2"][1])), 
                        "A3" : (-281.82,281.82,asphericFocalCurve(focusCurve.fifLocationsCS5["A3"][0], focusCurve.fifLocationsCS5["A3"][1])),
                        "A4" : (281.82,281.82,asphericFocalCurve(focusCurve.fifLocationsCS5["A4"][0], focusCurve.fifLocationsCS5["A4"][1])),
                        "B1" : (293.64,136.93,asphericFocalCurve(focusCurve.fifLocationsCS5["B1"][0], focusCurve.fifLocationsCS5["B1"][1])),
                        "B2" : (-293.64,136.93,asphericFocalCurve(focusCurve.fifLocationsCS5["B2"][0], focusCurve.fifLocationsCS5["B2"][1])), 
                        "B3" : (-293.64,-136.93,asphericFocalCurve(focusCurve.fifLocationsCS5["B3"][0], focusCurve.fifLocationsCS5["B3"][1])),
                        "B4" : (-136.93,293.64,asphericFocalCurve(focusCurve.fifLocationsCS5["B4"][0], focusCurve.fifLocationsCS5["B4"][1])),
                        "C1" : (96.44,232.82,asphericFocalCurve(focusCurve.fifLocationsCS5["C1"][0], focusCurve.fifLocationsCS5["C1"][1])),
                        "C2" : (232.82,-96.44,asphericFocalCurve(focusCurve.fifLocationsCS5["C2"][0], focusCurve.fifLocationsCS5["C2"][1])), 
                        "C3" : (-96.44,-232.82,asphericFocalCurve(focusCurve.fifLocationsCS5["C3"][0], focusCurve.fifLocationsCS5["C3"][1])),
                        "C4" : (-232.82,96.44,asphericFocalCurve(focusCurve.fifLocationsCS5["C4"][0], focusCurve.fifLocationsCS5["C4"][1])),
                        "D1" : (0,185.00,asphericFocalCurve(focusCurve.fifLocationsCS5["D1"][0], focusCurve.fifLocationsCS5["D1"][1])),
                        "D2" : (185.00,0,asphericFocalCurve(focusCurve.fifLocationsCS5["D2"][0], focusCurve.fifLocationsCS5["D2"][1])), 
                        "D3" : (0,-185.00,asphericFocalCurve(focusCurve.fifLocationsCS5["D3"][0], focusCurve.fifLocationsCS5["D3"][1])),
                        "D4" : (-185.00,0,asphericFocalCurve(focusCurve.fifLocationsCS5["D4"][0], focusCurve.fifLocationsCS5["D4"][1])),
                        "Other" : (0,0,asphericFocalCurve(focusCurve.fifLocationsCS5["Other"][0], focusCurve.fifLocationsCS5["Other"][1]))}
    
    #Dict of (x,y,z) for CCD centers(mm)
    focusCurve.CCDLocationsCS5 = {"NCCD" : (0,-396.48,focusCurve.CCDLocationsCS5["NCCD"][0], focusCurve.CCDLocationsCS5["NCCD"][1]),
                       "WCCD" : (-396.48,0,focusCurve.CCDLocationsCS5["WCCD"][0], focusCurve.CCDLocationsCS5["WCCD"][1]),
                       "SCCD" : (0,396.48,focusCurve.CCDLocationsCS5["SCCD"][0], focusCurve.CCDLocationsCS5["SCCD"][1]),
                       "ECCD" : (396.48,0,focusCurve.CCDLocationsCS5["ECCD"][0], focusCurve.CCDLocationsCS5["ECCD"][1]),
                       "CCCD" : (0,0,focusCurve.CCDLocationsCS5["CCCD"][0], focusCurve.CCDLocationsCS5["CCCD"][1]),
                       "Other" : (0,0,focusCurve.CCDLocationsCS5["Other"][0], focusCurve.CCDLocationsCS5["Other"][1])}
    
    #Dict of (x,y) for CCD triangles around center point (mm)
    focusCurve.trianglePonitfocusCurve = { 'NCCDA': (0,-388.48,focusCurve.trianglePonitfocusCurve['NCCDA'][0], focusCurve.trianglePonitfocusCurve['NCCDA'][1]),
                                     'NCCDB': (-8.4327,-399.1466,focusCurve.trianglePonitfocusCurve['NCCDB'][0], focusCurve.trianglePonitfocusCurve['NCCDB'][1]),
                                     'NCCDC': (8.4327,-399.1466,focusCurve.trianglePonitfocusCurve['NCCDC'][0], focusCurve.trianglePonitfocusCurve['NCCDC'][1]),
                                     'WCCDA': (-388.48,0,focusCurve.trianglePonitfocusCurve['WCCDA'][0], focusCurve.trianglePonitfocusCurve['WCCDA'][1]),
                                     'WCCDB': (-399.1466,8.4327,focusCurve.trianglePonitfocusCurve['WCCDB'][0], focusCurve.trianglePonitfocusCurve['WCCDB'][1]),
                                     'WCCDC': (-399.1466,-8.4327,focusCurve.trianglePonitfocusCurve['WCCDC'][0], focusCurve.trianglePonitfocusCurve['WCCDC'][1]),
                                     'SCCDA': (0,388.48,focusCurve.trianglePonitfocusCurve['SCCDA'][0], focusCurve.trianglePonitfocusCurve['SCCDA'][1]),
                                     'SCCDB': (8.4327,399.1466,focusCurve.trianglePonitfocusCurve['SCCDB'][0], focusCurve.trianglePonitfocusCurve['SCCDB'][1]),
                                     'SCCDC': (-8.4327,399.1466,focusCurve.trianglePonitfocusCurve['SCCDC'][0], focusCurve.trianglePonitfocusCurve['SCCDC'][1]),
                                     'ECCDA': (388.48,0,focusCurve.trianglePonitfocusCurve['ECCDA'][0], focusCurve.trianglePonitfocusCurve['ECCDA'][1]),
                                     'ECCDB': (399.1466,-8.4327,focusCurve.trianglePonitfocusCurve['ECCDB'][0], focusCurve.trianglePonitfocusCurve['ECCDB'][1]),
                                     'ECCDC': (399.1466,8.4327,focusCurve.trianglePonitfocusCurve['ECCDC'][0], focusCurve.trianglePonitfocusCurve['ECCDC'][1]),
                                     'CCCDA': (0,-8,focusCurve.trianglePonitfocusCurve['CCCDA'][0], focusCurve.trianglePonitfocusCurve['CCCDA'][1]),
                                     'CCCDB': (8.4327,2.6666,focusCurve.trianglePonitfocusCurve['CCCDB'][0], focusCurve.trianglePonitfocusCurve['CCCDB'][1]),
                                     'CCCDC': (-8.4327,2.6666,focusCurve.trianglePonitfocusCurve['CCCDC'][0], focusCurve.trianglePonitfocusCurve['CCCDC'][1]),
                                     'OtherA': (0,0,focusCurve.trianglePonitfocusCurve['OtherA'][0], focusCurve.trianglePonitfocusCurve['OtherA'][1]),
                                     'OtherB': (0,0,focusCurve.trianglePonitfocusCurve['OtherB'][0], focusCurve.trianglePonitfocusCurve['OtherB'][1]),
                                     'OtherC': (0,0,focusCurve.trianglePonitfocusCurve['OtherC'][0], focusCurve.trianglePonitfocusCurve['OtherC'][1])}
    
    def __init__(self):
        '''
        Constructor
        '''

    def stdFocusCurve(self, fiflabel, imageArray4D, filelist, pointLabel = ""):
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
        fig2.savefig(str(fiflabel) + '_' + str(pointLabel) + '_Focus_Curve_' +  time.strftime("%Y%m%d-%H%M%S") + '.png') 
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

    def asphericFocalCurve(self, x, y):
        '''
        Use ZEMAX Image surface definition, of 10th order even 
        polynomial, to find best focus nominal Z (mm) for a FIF
        that has its center pinhole at location (x, y).
        
        r = sqrt(x^2 + y^2) (mm)
        1/c = -4977.99mm
        k = 0
        
        Aspheric terms
        a2 = ((r^2)/(1/c))/(1+SQRT(1-(r^2/(1/c)^2)))
        a4 = (-0.00000000029648)r^4
        a6 = (0.0000000000000034523)r^6
        a8 = (-1.8042E-20)r^8
        a10 = (3.2571E-26)r^10
        
        nominalZ = a2 + a4 + a6 + a8 + a10
        '''
        r = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        inv_c = -4977.99
        
        ###########################################################################
        ###Aspheric terms
        ###########################################################################
        a2 = (math.pow(r, 2)/inv_c)/(1+math.sqrt(1-(math.pow(r, 2)/math.pow(inv_c, 2))))
        a4 = -0.00000000029648*math.pow(r, 4)
        a6 = 0.0000000000000034523*math.pow(r, 6)
        a8 = -1.8042E-20*math.pow(r, 8)
        a10 = 3.2571E-26*math.pow(r, 10)
        
        ###########################################################################
        ###Nominal Z in (um)
        ###########################################################################
        return (a2 + a4 + a6 + a8 + a10) #*1000 #converted from mm to microns