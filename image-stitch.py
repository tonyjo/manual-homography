# -*- coding: utf-8 -*-
'''
This Program stitches two images based on user input correspondences
Author: Tony Joseph
'''

import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys
import os
import argparse

# Global Variables:
points1 = []
points2 = []
counts1 = 0
counts2 = 0

'''
Function to Capture mouse action of Left Image
'''
def pointCaptureLeft(event,x,y,flags,param):
    global points1, counts1
    if event == cv2.EVENT_LBUTTONDOWN:
        points1.append((x,y))
        counts1 = counts1 + 1
    elif event == cv2.EVENT_LBUTTONUP:
        print "Picture 1 clicked, count =  ", counts1
        # draw a rectangle around the region of interest
        cv2.circle(image1, points1[(counts1-1)], 10, (0, 255, 0), -1)
        cv2.imshow("Left_image", image1)

'''
Function to Capture mouse action of Right Image
'''
def pointCaptureRight(event,x,y,flags,param):
    global points2, counts2
    if event == cv2.EVENT_LBUTTONDOWN:
        points2.append((x,y))
        counts2 = counts2 + 1
    elif event == cv2.EVENT_LBUTTONUP:
        print "Picture 2 clicked, count = ", counts2
        # draw a rectangle around the region of interest
        cv2.circle(image2, points2[(counts2-1)], 10, (0, 255, 0), -1)
        cv2.imshow("Left_image", image2)

'''
Function takes input images and the correspondences, to stitch them
by computing the homography
'''
def getImageStitch(image1, image2, points1, points2, syfail):
    n1 = len(points1)
    n2 = len(points2)

    if n1 != n2:
        print 'Sorry, You did not select equal points in left and right image.'
        result = syfail
    else:
        h = np.ones([9,1])
        A = []
        # Assuming Random 4 matches:
        points1 = np.array(points1)
        points2 = np.array(points2)

        # Get and Normalize coordinates:
        x = points2[:,0]
        y = points2[:,1]

        x_ = points1[:,0]
        y_ = points1[:,1]


        # Self Construction
        for i in range(n1):
            A.append([x[i], y[i], 1, 0, 0, 0, (-1*x[i]*x_[i]), (-1*y[i]*x_[i]), (-1*x_[i])])
            A.append([0, 0, 0, x[i], y[i], 1, (-1*x[i]*y_[i]), (-1*y[i]*y_[i]), (-1*y_[i])])

        A = np.array(A)

        '''
        An Example of 4 input matches:
        A = [[x[0], y[0], 1, 0, 0, 0, (-1*x[0]*x_[0]), (-1*y[0]*x_[0]), (-1*x_[0])],
             [0, 0, 0, x[0], y[0], 1, (-1*x[0]*y_[0]), (-1*y[0]*y_[0]), (-1*y_[0])],
             [x[1], y[1], 1, 0, 0, 0, (-1*x[1]*x_[1]), (-1*y[1]*x_[1]), (-1*x_[1])],
             [0, 0, 0, x[1], y[1], 1, (-1*x[1]*y_[1]), (-1*y[1]*y_[1]), (-1*y_[1])],
             [x[2], y[2], 1, 0, 0, 0, (-1*x[2]*x_[2]), (-1*y[2]*x_[2]), (-1*x_[2])],
             [0, 0, 0, x[2], y[2], 1, (-1*x[2]*y_[2]), (-1*y[2]*y_[2]), (-1*y_[2])],
             [x[3], y[3], 1, 0, 0, 0, (-1*x[3]*x_[3]), (-1*y[3]*x_[3]), (-1*x_[3])],
             [0, 0, 0, x[3], y[3], 1, (-1*x[3]*y_[3]), (-1*y[3]*y_[3]), (-1*y_[3])]]
        '''

        U,s,V = np.linalg.svd(A)
        h = V[-1,:]
        H = np.reshape(h, (3,3))
        print 'Computed Homography:', H

        # Opencv Construction
        #h1, status = cv2.findHomography(points2, points1)
        #print h1

        # Stitch Image with prespective geometry:
        stitch_image = cv2.warpPerspective(image2, H, (image1.shape[1] + image2.shape[1], image1.shape[0]))
        stitch_image[0:image2.shape[0], 0:image2.shape[1]] = image1

    return (stitch_image)


'''
Calling Functions to Stitch Image.
'''
print 'System Input:', sys.argv

syfail =  cv2.imread("sysfail.jpg")
image1 =  cv2.imread(sys.argv[1])
image2 =  cv2.imread(sys.argv[2])

image3 =  cv2.imread(sys.argv[1])
image4 =  cv2.imread(sys.argv[2])

image1_gy = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
image2_gy = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

cv2.namedWindow("Left_image")
cv2.moveWindow("Left_image", 0,250)
cv2.resizeWindow("Left_image", 500,400)
cv2.setMouseCallback("Left_image", pointCaptureLeft)

cv2.namedWindow("Right_image")
cv2.moveWindow("Right_image", 300, 300)
cv2.resizeWindow("Right_image", 500,400)
cv2.setMouseCallback("Right_image", pointCaptureRight)

# Keep looping until the 'c' key is pressed
while True:
    # Display the image and wait for a keypress
    cv2.imshow("Left_image", image1)
    cv2.imshow("Right_image", image2)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("c"):
        break

# Call the Stitching function:
stitched_image = getImageStitch(image3, image4, points1, points2, syfail)
# Display the Output Image:
cv2.namedWindow("Stitched_image")
cv2.moveWindow("Stitched_image", 300,250)
cv2.imshow("Stitched_image", stitched_image)
cv2.waitKey(0)
