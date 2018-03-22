'''
@title centroidFIF
@author: Rebecca Coles
Updated on Feb 14, 2018
Created on Dec 12, 2017

centroidPinHoleImage
This module holds a series of functions used to find the center of
an illuminated pin hole from an image using code that was adapted
from the IDL Astronomy Users Library. Original python conversion
by David Jones.

Compute the centroid of a star using a derivative search (adapted 
for IDL from DAOPHOT, then translated from IDL to Python).
Uses an early DAOPHOT "FIND" centroid algorithm by locating the 
position where the X and Y derivatives go to zero.

Modules:
findCentroid
    Take a numpy array of an image and centroid the pinholes within.
    Compute the centroid of a star using a derivative search 
    (adapted for IDL from DAOPHOT, then translated from IDL to Python).
    
    Maximum pixel within distance from input pixel X, Y  determined
    from FHWM is found and used as the center of a square, within
    which the centroid is computed as the value (XCEN,YCEN) at which
    the derivatives of the partial sums of the input image over (y,x)
    with respect to (x,y) = 0.  In order to minimize contamination from
    neighboring stars stars, a weighting factor W is defined as unity in
    center, 0.5 at end, and linear in between.
    
    Values for xcen and ycen will not be computed if the computed
    centroid falls outside of the box, or if the computed derivatives
    are non-decreasing.   If the centroid cannot be computed, then a 
    xcen and ycen are set to -1 and a message is displayed.
findFIFInImage
    Find FIF in image using intensity.

'''

# Import #######################################################################################
import numpy as np
np.set_printoptions(threshold=np.nan)
import cv2, math
from fileAndArrayHandling import fileAndArrayHandling
from focusCurve import focusCurve
################################################################################################

class centroidFIF(object):
    
    #Width of subimage for centroiding
    widthOfSubimage = 200 #pixels
    
    def __init__(self):
        '''
        Constructor
        '''
        
    def findCentroid(self, image, x, y, extendbox = False):
        '''
        Take a numpy array of an image and centroid the pinholes within
        Compute the centroid of a star (or FIF) using a derivative search 
        (adapted for IDL from DAOPHOT, then translated from IDL to Python).
        
        image  - 2D numpy array
        x,y  -  Integers giving approximate pin hole center
                The centroid is computed using a box of half width equal to 1.5 sigma = 0.637* fwhm.
        extendbox -  {non-negative positive integer}. findCentroid searches a box with
                       a half width equal to 1.5 sigma  = 0.637* FWHM to find the
                       maximum pixel. To search a larger area, set extendbox to
                       the number of pixels to enlarge the half-width of the box.
                       A list/array of [X,Y] coordinates defines a rectangle.
                       Default is 0; prior to June 2004, the default was extendbox = 3
        ''' 

        sz_image = np.shape(image)
        xsize = sz_image[1]
        ysize = sz_image[0]

        ###########################################################################
        ###Find fwhm
        ###########################################################################
        maxi = np.amax(image)
        floor = np.median(image.flatten())
        height = maxi - floor
        if height == 0.0: # if object is saturated it could be that median value is 32767 or 65535 --> height=0
            floor = np.mean(image.flatten())
            height = maxi - floor
        fwhm = np.sqrt(sum((image>floor+height/2.).flatten()))        

        ###########################################################################
        ###Compute size of box needed to compute centroid
        ###########################################################################
        if not extendbox: extendbox = 0
        nhalf =  int(0.637*fwhm)  
        if nhalf < 2: nhalf = 2
        nbox = 2*nhalf+1             # Width of box to be used to compute centroid
        if not hasattr(extendbox,'__len__'):
            Xextendbox,Yextendbox = extendbox,extendbox
        elif hasattr(extendbox,'__len__'):
            Xextendbox,Yextendbox = extendbox
        nhalfbigx = nhalf + Xextendbox; nhalfbigy = nhalf + Yextendbox
        nbigx = nbox + Xextendbox*2; nbigy = nbox + Yextendbox*2 #Extend box 3 pixels on each side to search for max pixel value

        if isinstance(x,float) or isinstance(x,int): npts = 1
        else: npts = len(x) 
        if npts == 1: xcen = float(x) ; ycen = float(y)
        else: xcen = x.astype(float) ; ycen = y.astype(float)
        ix = np.round( x )          # Central X pixel
        iy = np.round( y )          # Central Y pixel
    
        if npts == 1:
            x, y, ix, iy, xcen, ycen = [x], [y], [ix], [iy], [xcen], [ycen]
        for i in range(npts):        # Loop over X,Y vector
            pos = str(x[i]) + ' ' + str(y[i])

            if ((ix[i] < nhalfbigx) or ((ix[i] + nhalfbigx) > xsize-1) or
                (iy[i] < nhalfbigy) or ((iy[i] + nhalfbigy) > ysize-1)):
                xcen[i] = -1
                ycen[i] = -1
                print('Position '+ pos + ' too near edge of image')
                continue
            
            bigbox = image[int(iy[i]-nhalfbigy) : int(iy[i]+nhalfbigy+1),
                int(ix[i]-nhalfbigx) : int(ix[i]+nhalfbigx+1)]

            # Locate maximum pixel in 'NBIG' sized subimage
            goodrow = np.where(bigbox == bigbox)
            mx = np.max( bigbox[goodrow])     #Maximum pixel value in BIGBOX
            mx_pos = np.where(bigbox == mx) #How many pixels have maximum value?
            Nmax = len(mx_pos[0])
            idx = mx_pos[1] #% nbig          # X coordinate of Max pixel
            idy = mx_pos[0] #/ nbig          # Y coordinate of Max pixel

            if Nmax > 1:                 # More than 1 pixel at maximum?
                idx = np.round(np.sum(idx)/Nmax)
                idy = np.round(np.sum(idy)/Nmax)
            else:
                idx = idx[0]
                idy = idy[0]

            xmax = ix[i] - (nhalf+Xextendbox) + idx  #X coordinate in original image array
            ymax = iy[i] - (nhalf+Yextendbox) + idy  #Y coordinate in original image array
        else:
            xmax = ix[i]
            ymax = iy[i]

        ###########################################################################
        ###Check *new* center location for range (added by David Hogg)
        ###########################################################################
        if ((xmax < nhalf) or ((xmax + nhalf) > xsize-1) or
           (ymax < nhalf) or ((ymax + nhalf) > ysize-1)):
            xcen[i] = -1
            ycen[i] = -1
            print('Position '+ pos + ' moved too near edge of image')

        ###########################################################################
        ###Extract smaller 'STRBOX' sized subimage centered on maximum pixel
        ###########################################################################
        strbox = image[int(ymax-nhalf) : int(ymax+nhalf+1), int(xmax-nhalf) : int(xmax+nhalf+1)]

        ir = (nhalf-1)
        if ir < 1: ir = 1
        dd = np.arange(nbox-1).astype(int) + 0.5 - nhalf

        ###########################################################################
        ###Weighting factor W unity in center, 0.5 at end, and linear in between
        ###########################################################################
        w = 1. - 0.5*(np.abs(dd)-0.5)/(nhalf-0.5)
        sumc   = np.sum(w)

        ###########################################################################
        ###Find X centroid
        ###########################################################################
        deriv = np.roll(strbox,-1,axis=1) - strbox.astype(float)    #;Shift in X & subtract to get derivative
        deriv = deriv[nhalf-ir:nhalf+ir+1,0:nbox-1] #;Don't want edges of the array
        deriv = np.sum( deriv, 0 )                    #    ;Sum X derivatives over Y direction
        sumd   = np.sum( w*deriv )
        sumxd  = np.sum( w*dd*deriv )
        sumxsq = np.sum( w*dd**2 )
        if sumxd >= 0:    # ;Reject if X derivative not decreasing
            xcen[i]=-1
            ycen[i]=-1
            print('Unable to compute X centroid around position '+ pos)
        dx = sumxsq*sumd/(sumc*sumxd)
        if np.abs(dx) > nhalf:    # Reject if centroid outside box
            xcen[i]=-1
            ycen[i]=-1
            print('Computed X centroid for position '+ pos + ' out of range')
        xcen[i] = xmax - dx    # X centroid in original array

        ###########################################################################
        ###Find Y Centroid
        ###########################################################################
        deriv = np.roll(strbox,-1,axis=0) - strbox.astype(float)    # Shift in X & subtract to get derivative
        deriv = deriv[0:nbox-1,nhalf-ir:nhalf+ir+1]
        deriv = np.sum( deriv,1 )
        sumd =   np.sum( w*deriv )
        sumxd =  np.sum( w*deriv*dd )
        sumxsq = np.sum( w*dd**2 )
        if sumxd >= 0:  # Reject if Y derivative not decreasing
            xcen[i] = -1
            ycen[i] = -1
            print('Unable to compute Y centroid around position '+ pos)
        dy = sumxsq*sumd/(sumc*sumxd)
        if np.abs(dy) > nhalf:  # Reject if computed Y centroid outside box
            xcen[i]=-1
            ycen[i]=-1
            print('Computed Y centroid for position '+ pos + ' out of range')
        ycen[i] = ymax-dy

        if npts == 1:
            xcen,ycen = xcen[0]+1,ycen[0]+1
        return xcen-1, ycen-1
    
    def findFIFInImage(self, image):
        '''
        Find FIF in image using intensity.
        '''
        #(0,0) is in lower left-hand corner of image
        # ____________
        # |            |
        # |            |
        # |  SubArray  |
        # |            |
        # |____________|
        # *(xOffset, yOffset)

        ###########################################################################
        ###Grayscale image
        ###########################################################################
        gray = cv2.GaussianBlur(image, (1, 31), 0)
        
        ###########################################################################
        ###Find FIF in image (minVal, maxVal, minLoc, maxLoc)
        ###########################################################################
        _, _, _, mL = cv2.minMaxLoc(gray)
        maxLoc = (mL[1],mL[0]) #minMaxLoc returns (y,x) format. Converting to (x,y) format.
        
        ###########################################################################
        ###Create subarray around FIF (slice array)
        ###########################################################################   int(round(widthOfSubimage/2))
        fifSubArray = image[int(maxLoc[0]-int(round(self.widthOfSubimage/2))):int(maxLoc[0]+int(round(self.widthOfSubimage/2))), int(maxLoc[1]-int(round(self.widthOfSubimage/2))):int(maxLoc[1]+int(round(self.widthOfSubimage/2)))]
        
        ###########################################################################
        ###View subarray and value of max-value pixel
        ########################################################################### 
        #cv2.imshow('fifSubArray',fifSubArray)
        #print(image[maxLoc[0],maxLoc[1]])
        return fifSubArray, self.widthOfSubimage, maxLoc
    
    def distanceFromPinholeImagetoOrigin(self, rows, columns, consoleLog, logFile, pixelSize, isFIF = False, fifLabel = '', isCCD = False, CCDLabel = '', triangleLabel = ''):
        '''
        Calcuate the distance to the sensor origin using centroided image.
        '''
        ###########################################################################
        ###Find distance in um to CCD Origin
        ###########################################################################       
        hypotenuse = np.sqrt(math.pow((rows),2)+math.pow((columns),2))
        faah = fileAndArrayHandling()
        faah.pageLogging(consoleLog, logFile, 
                    "Distance from pinhole center to sensor origin: " + str(hypotenuse) + "pixels or " + str(hypotenuse*pixelSize) + 'um')
        
        ###########################################################################
        ###Find location of Origin in CS5
        ###########################################################################       
        fC = focusCurve()
        if isFIF == True and isCCD == False:
            #pinhole is from a FIF
            fifLocationX = fC.fifLocationsCS5[fifLabel][0]
            fifLocationY = fC.fifLocationsCS5[fifLabel][1]
        elif isFIF == False and isCCD == True and triangleLabel != '':
            #pinhole is from 100um DMM (triangle)
            trianglePointX = fC.trianglePonitCCDLocationsCS5[triangleLabel][0]
            trianglePointY = fC.trianglePonitCCDLocationsCS5[triangleLabel][1]
        elif isFIF == False and isCCD == True and CCDLabel != '':
            #pinhole is at CCD center
            sensorCenterX = fC.fifLocationsCS5[triangleLabel][0]
            sensorCenterY = fC.fifLocationsCS5[triangleLabel][1]
        else:
            #pinhole type not selected
        
        
        
        return CS5OriginX, CS5OriginY
    