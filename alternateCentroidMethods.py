'''
@title alternateCentroidMethods
@author: Rick Pogge (edited by Rebecca Coles)
Updated on Feb 21, 2018
Created on Feb 21, 2018

alternateCentroidMethods
    Alternate centroiding methods. Created by Rick Pogge (pogge.1@osu.edu).
'''

# Import #######################################################################################
import os, sys, getopt, subprocess, shlex, signal
import math
import numpy as np
from astropy.io import fits

import scipy
from scipy import ndimage
from scipy.optimize import curve_fit
################################################################################################

#----------------------------------------------------------------
#
# findPeak() - find the peak pixel nearest an XY pixel location
#
# Finds the peak pixel within radius of the given X,Y coordinates
#

def findPeak(image,x,y,radius=2):
    ny,nx = image.shape
    # search rectangle, make sure within the image boundaries
    xmin = int(max(0,x-radius))
    xmax = int(min(nx,x+radius))
    ymin = int(max(0,y-radius))
    ymax = int(min(ny,y+radius))
    maxPix = np.amax(image[ymin:ymax,xmin:xmax])
    maxIdx = np.argwhere(image[ymin:ymax,xmin:xmax]==maxPix)
    # even if many found, choose the first
    return maxIdx[0][1]+xmin,maxIdx[0][0]+ymin,maxPix

#----------------------------------------------------------------
# Centroid Methods
#----------------------------------------------------------------
#
# gmsCentroid() - Gaussian Marginal Sum (GMS) Centroid Method
#
# arguments:
#   image - 2D image
#   x (float): x pixel coordinate of the center of the object subimage
#   y (float): y pixel coordinate of the center of the object subimage
#   xWid (float): x-axis half width of the subimage in pixels
#   yWid (float): y-axis half width of the subimage in pixels
#   axis (string): axis to centroid along, 'x', 'y', or 'both'
#                  default: both
#   verbose (bool): print verbose output
#
# raises exceptions if garbage
# returns:
#    axis='both':  xCen, yCen, xErr, yErr
#    axis='x': xCen, xErr
#    axis='y': yCen, yErr
#


def gmsCentroid(image,x,y,xWid,yWid,axis='both',verbose=False):
    ny,nx = image.shape
    if axis.lower() == 'both':
        doXaxis = True
        doYaxis = True
    elif axis.lower() == 'x':
        doXaxis = True
        doYaxis = False
        yCen = None
        yErr = None
    elif axis.lower() == 'y':
        doXaxis = False
        doYaxis = True
        xCen = None
        xErr = None
    else:
        raise Exception("Invalid axis '%s' - must be one of {x,y,both}" % (axis))

    # Subimage region, make sure it is within the image boundaries

    xmin = int(max( 0,x-xWid))
    xmax = int(min(nx,x+xWid))
    ymin = int(max( 0,y-yWid))
    ymax = int(min(ny,y+yWid))
    boxImg = np.array(image[ymin:ymax,xmin:xmax]) # cut out the sub image

    # Form the marginal sums along the working axis

    if doXaxis:
        xMS  = boxImg.mean(axis=0)  # X marginal sum
        xPix = xmin+np.arange(len(xMS))

    if doYaxis:
        yMS  = boxImg.mean(axis=1)  # Y marginal sum
        yPix = ymin+np.arange(len(yMS))

    # Guesses of the Gaussian fit parameters common to both axes

    bkg0 = np.median(boxImg)
    s0 = 1.0

    # Marginal sum Gaussian fits
    
    if doXaxis:
        maxX = np.amax(xMS)
        x0 = xPix[np.argwhere(xMS==maxX)][0]
        a0 = maxX-bkg0
        px=[bkg0,a0,x0,s0]
        xCoeff,varX = curve_fit(skyGauss,xPix,xMS,p0=px)
        xFit = skyGauss(xPix,*xCoeff)
        xCen = xCoeff[2]
        xErr = math.sqrt(varX[2,2])
        xBkg = xCoeff[0]

    if doYaxis:
        maxY = np.amax(yMS)
        y0 = yPix[np.argwhere(yMS==maxY)][0]
        a0 = maxY-bkg0
        py=[bkg0,a0,y0,s0]
        yCoeff,varY = curve_fit(skyGauss,yPix,yMS,p0=py)
        yFit = skyGauss(yPix,*yCoeff)
        yCen = yCoeff[2]
        yErr = math.sqrt(varY[2,2])
        yBkg = yCoeff[0]

    # Some quality checks

    # If either fit sigma is <0, probable failure even if a formal
    # fit was found (curve_fit raised no exceptions)

    #if doXaxis and xCoeff[3] < s0:
    #    raise Exception('Cannot compute X centroid - sigX=%.3f < %.3f' % (xCoeff[3],s0))

    #if doYaxis and yCoeff[3] < s0:
    #    raise Exception('Cannot compute Y centroid - sigY=%.3f < %.3f' % (yCoeff[3],s0))

    # Cleanup

    del boxImg
    if doXaxis:
        del xPix
        del xMS
    if doYaxis:
        del yPix
        del yMS

    # Return data

    if doXaxis and doYaxis:
        return xCen,yCen,xErr,yErr
    elif doXaxis and not doYaxis:
        return xCen,xErr
    elif doYaxis and not doXaxis:
        return yCen,yErr

#---------------------------------------------------------------------------
#
# smsBisector() - Sobel Marginal Sum (SMS) Bisector Method
#
# Returns xCen, yCen, and median in the box
#
# arguments:
#   image - 2D image
#   x (float): x pixel coordinate of the center of the object subimage
#   y (float): y pixel coordinate of the center of the object subimage
#   xWid (float): x-axis half width of the subimage in pixels
#   yWid (float): y-axis half width of the subimage in pixels
#   axis (string): axis to centroid along, 'x', 'y', or 'both'
#                  default: both
#   clipStars (bool): clip stars within the box (default: False)
#   wfac (float): width factor for inner/outer box for clipping (default: 1)
#   verbose (bool): print verbose output
#
# raises exceptions if garbage
# returns: xCen, yCen, medBox
#    bkgMed = median signal inside box
#
# ** Note to RC:
#    You can get rid of the clipStars, wfac, and bkgMed bits as these
#    are specific to using the SMS Bisector method for finding slit
#    mask boxes on images that might have star or galaxy image inside
#    the slit.  Not needed if you know the sharp-sided, flat-topped
#    profile being centroided is empty of structure.
#


def smsBisector(image,x,y,xWid,yWid,axis='both',clipStars=False,wfac=1,verbose=False):
    ny,nx = image.shape
    if axis.lower() == 'both':
        doXaxis = True
        doYaxis = True
        do2D = True
    elif axis.lower() == 'x':
        doXaxis = True
        doYaxis = False
        do2D = False
        yCen = None
    elif axis.lower() == 'y':
        doXaxis = False
        doYaxis = True
        do2D = False
        xCen = None
    else:
        raise Exception("Invalid axis '%s' - must be one of {x,y,both}" % (axis))

    # Two rectangles:
    #   1) Main Box: 2*wfac*(xWid x yWid) for subimage
    #   2) Inner Box: xWid x wWid for star clipping
    
    # Make sure the main box is within the image boundaries

    xmin = int(max( 0,x-wfac*xWid))
    xmax = int(min(nx,x+wfac*xWid))
    ymin = int(max( 0,y-wfac*yWid))
    ymax = int(min(ny,y+wfac*yWid))
    subImg = np.array(image[ymin:ymax,xmin:xmax])

    # Star clipping needed in the inner box?

    bkgMed = 0.0
    if clipStars:
        xhw = xWid/2  # half-width
        yhw = yWid/2
        y1=int(y-yhw) 
        y2=int(y+yhw) 
        x1=int(x-xhw) 
        x2=int(x+xhw)
        bkgMed = np.median(image[y1:y2,x1:x2])
        bkgSig = math.sqrt(bkgMed)
        thresh = bkgMed + 2*bkgSig
        if np.any(subImg>thresh):
            subImg[subImg>thresh] = bkgMed

    # Form the marginal sums along the working axis and compute a 1D
    # squared Sobel filtered marginal sum

    if doXaxis:
        xMS  = subImg.mean(axis=0)  # X marginal sum
        xPix = xmin+np.arange(len(xMS))
        xSobel = ndimage.sobel(xMS,0)
        xSobel *= xSobel
        xSobel[0] = 0.0
        xSobel[len(xSobel)-1]=0.0

    if doYaxis:
        yMS  = subImg.mean(axis=1)  # Y marginal sum
        yPix = ymin+np.arange(len(yMS))
        ySobel = ndimage.sobel(yMS,0)
        ySobel *= ySobel
        ySobel[0] = 0.0
        ySobel[len(ySobel)-1]=0.0

    # Find the peaks of the squared-sobel filter marginal sums.  The
    # guess is that the peaks are in each half of the profile.  These
    # give us the initial guesses for the two-Gaussian fits.

    xLeft = 0.0
    yLeft = 0.0
    xRight = 0.0
    yRight = 0.0
    if doXaxis:
        lengthSobelX = int(round(len(xSobel)/2))
        xm1 = xmin + np.argmax(xSobel[:(lengthSobelX)])
        xa1 = np.amax(xSobel[:(lengthSobelX)])
        xs1 = 1.0

        xm2 = xmin + 0.5*int(round(len(xSobel))) + np.argmax(xSobel[(lengthSobelX):])
        xa2 = np.amax(xSobel[(lengthSobelX):])
        xs2 = 1.0

        px = [xa1,xm1,xs1,xa2,xm2,xs2]

        try:
            xCoeff,xCov = curve_fit(twoGauss,xPix,xSobel,p0=px)
        except:
            raise Exception('smsBisector() - fit failed on X marginal sum')

        xFit = twoGauss(xPix,*xCoeff)
        xCen = 0.5*(xCoeff[1] + xCoeff[4])
        xLeft = xCoeff[1]
        xRight = xCoeff[4]

    if doYaxis:
        lengthSobelY = int(round(len(ySobel)/2))
        ym1 = ymin + np.argmax(ySobel[:(lengthSobelY)])
        ya1 = np.amax(ySobel[:(lengthSobelY)])
        ys1 = 1.0

        ym2 = ymin + 0.5*int(round(len(ySobel))) + np.argmax(ySobel[(lengthSobelY):]) 
        ya2 = np.amax(ySobel[(lengthSobelY):])
        ys2 = 1.0

        py = [ya1,ym1,ys1,ya2,ym2,ys2]

        try:
            yCoeff,yCov = curve_fit(twoGauss,yPix,ySobel,p0=py)
        except:
            raise Exception('smsBisector() - fit failed on Y marginal sum')

        yFit = twoGauss(yPix,*yCoeff)
        yCen = 0.5*(yCoeff[1] + yCoeff[4])
        yLeft = yCoeff[1]
        yRight = yCoeff[4]

    # Quality checks here someday...

    # Diagnostic output if running in verbose mode

    if doXaxis and verbose:
        print("  X: Peaks %.2f %.2f, Bisector %.2f s1=%.2f s2=%.2f" % (xCoeff[1],xCoeff[4],xCen,xCoeff[2],xCoeff[5]))
        print("  Slit X Width: %.2f pixels" % (xCoeff[4]-xCoeff[1]))
    if doYaxis and verbose:
        print("  Y: Peaks %.2f %.2f, Bisector %.2f s1=%.2f s2=%.2f" % (yCoeff[1],yCoeff[4],yCen,yCoeff[2],yCoeff[5]))
        print("  Slit Y Width: %.2f pixels" % (yCoeff[4]-yCoeff[1]))

    # Clean up

    del subImg
    if doXaxis:
        del xPix
        del xSobel
        del xMS
    if doYaxis:
        del yPix
        del ySobel
        del yMS

    # Return data

    return xCen,yCen,bkgMed

#----------------------------------------------------------------
#
# 1D Gaussian functions
#
# skyGauss is used by the GMS centroid method
# twoGauss is used by the SMS bisector method
# oneGauss is for reference but unused
#
#   oneGauss = 1D Gaussian, no background
#              f(x) = a*exp(-(x-m)^2/2*s^2)
#
#   skyGauss = 1D Gaussian with constant background
#              f(x) = b + a*exp(-(x-m)^2/2*s^2)
#
#   twoGauss = Two 1D Gaussians, no background
#              f(x) = a1*exp(-(x-m1)^2/2*s1^2) + a2*exp(-(x-m2)^2/2*s2^2)
#
# Written in the form required by scipy.optimize.curve_fit()
#

def oneGauss(x,*p):
    a,m,s=p
    return a*np.exp(-(x-m)**2/(2*s**2))

def twoGauss(x,*p):
    a1,m1,s1,a2,m2,s2=p
    return a1*np.exp(-(x-m1)**2/(2*s1**2)) + a2*np.exp(-(x-m2)**2/(2*s2**2))

def skyGauss(x,*p):
    b,a,m,s=p
    return b + a*np.exp(-(x-m)**2/(2*s**2))

#----------------------------------------------------------------
#
# findCentroid() - iterative GMS method centroid fitting
#
# Uses gmsCentroid() and sets up an iterative centroid loop
# to try to get the best centroid.  Convergence is change in 
# centroid less than tol (computed as a radial offset between
# the pre- and post-iteration measurements).  Wil iterate up
# to maxiter times.
#
# Example of how to implement gmsCentroid().  Substitute a
# suitable version of smsBisector() for centroiding flat-topped
# box images.
#


def findCentroid(img,x0,y0,cenRad,maxiter=5,tol=0.01,verbose=False):
    # first iteration: use the guess provided
    try:
        xCen0,yCen0,xErr,yErr = gmsCentroid(img,x0,y0,cenRad,cenRad,axis='both')
        gotStar = True
    except Exception as err:
        errStr = err
        gotStar = False

    if not gotStar:
        raise Exception('initial centroid failed - %s' % (errStr))

    if verbose:
        print("  iteration 1: X=%.3f+/-%.3f Y=%.3f+/-%.3f"  % (xCen0+1,yCen0+1,xErr,yErr))

    # Iterate until convergence or maxiter

    for i in range(maxiter-1):
        try:
            xCen,yCen,xErr,yErr = gmsCentroid(img,xCen0,yCen0,cenRad,cenRad,axis='both')
            gotStar = True
        except:
            gotStar = False

        if not gotStar:
            raise Exception('Could not compute refined centroid')

        dX = xCen - xCen0
        dY = yCen - yCen0
        if verbose:
            print("  iteration %d: X=%.3f+/-%.3f Y=%.3f+/-%.3f dX=%.3f dY=%.3f"  % (i+2,xCen+1,xErr,yCen+1,yErr,dX,dY))
        dR = math.sqrt(dX*dX+dY*dY)
        if dR <= tol:
            return xCen,yCen,xErr,yErr
        else:
            xCen0 = xCen
            yCen0 = yCen
    
    # no convergence, raise exception

    raise Exception('Did not converge within %.2f pix in %d iterations' % (tol,maxiter))
