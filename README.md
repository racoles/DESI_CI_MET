# DESI-CI-MET
Software for the DESI CI metrology program.

The DESI commissioning instrument (CI), will be used to commission the telescope control system, guiding, and
the Aetin Optics System that maintains optical alignment. It will be used to characterize the image quality and
optical distortions of the new corrector. The CI has five commercial cameras; one at the center of the focal surface
and four at the periphery of the field that are aligned with the cardinal directions. There are 22 illuminated
fiducials to calculate the transformations and further develop the systems that will place fibers within 5um RMS
of the target positions. We will use the commissioning instrument metrology program to measure the absolute
three axis Cartesian coordinates of the five CCDs and 22 illuminated fiducials on the commissioning instrument.

When the CI is installed in place of the future DESI focal plane system (FPS), the center CCD camera will
be aligned with the telescopes optical axis, and the other four cameras will will sit 90 degrees apart and at the
same radii as the Guide Focus and Alignment cameras (GFAs) that will sit on the FPS. The GFAs will be used
to guide the telescope and focus and align the DESI corrector, and we will use the cameras on the CI for the
same purpose. In a similar manner, the CI's illuminated fiducials will allow us to measure the parameters needed
such that the fixed illuminated fiducials (IFs) present on the focal plane system will be in focus when viewed by
the fiber view camera.

The DESI CI metrology software analyzes input images of IFs or camera CCDs and guides us in adjusting the IFs
or cameras such that they are properly aligned with the DESI aspheric focal plane. To make height adjustments
in the CS5 Z direction, the software accepts images of a IF or the DMM 100um pinhole that was projected onto
the TTF camera's surface, and creates a focus curve that solves for height adjustments. To guide our adjustment 
of the tip or tilt of the TTF, the DESI CI metrology software accepts images of the DMM 100um pinhole projected 
onto the TTF camera's surface at three locations that form the points of an equilateral triangle, and generates 
focus curves for each point that determine the tip and tilt of the camera relative to nominal values for those 
points.

To adjust the TTFs and IFs on the CI in the CS5 X-Y plane, the DESI CI metrology software uses centroiding
routines to locate a IF, or light from the 100um pinhole projected onto a camera CCD, in an image and find its
position relative to the CS5 origin compared to the nominal position.


Title: DESI_CI_MET 1.5
Author: Rebecca Coles
Updated on Feb 21, 2017
Created on Aug 18, 2018

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
    DESI_CI_MET_1.5: Ometech DESI commissioning instrument metrology complete (08/15/2018-08/17/2018)  
        Sheffield Cordax RS70 DCC CMM – 40” x 50” x 40” with Renishaw AR1probe changer, PH10 head, PH7 probe. 
        CMM manager software with reverse engineering capabilities as well as automated scanning.
        
Notes:

BackFocus
    Precision measurements of each camera's back focus is not necessary. Back focus measurements were only done to check that all 5 cameras are close to each other.

    We will measure the Z position of three points on each CCD as accurately as possible. 
    The 3 primary sources of error are:
    CMM (or HAAS) Z axis scale error ~ 2-3um CMM, (10 - 15 micron Haas)
    "best focus" determination error from the focus curves  of 100um pinhole onto CCD ~ 10 - 15um
    Ability to adjust the TTF to the desired value  with the micrometers  ~ 5um (not demonstrated yet)

    Therefore we should be able to meet the 50um Z spec for the CCDs
    
Sensor -> TTF Baseplate Distance:
    The sensor to TTF baseplate distance (according to the SolidWorks model):
    C: 86.88mm
    N,E,S,W: 104.512mm
