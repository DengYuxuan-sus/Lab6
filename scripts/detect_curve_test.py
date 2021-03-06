import imp
import numpy
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mplimg
import rospy
from sensor_msgs.msg import Image
import cv_bridge

def easy_binarization(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray[img_gray>127] = 255
    img_gray[img_gray<=127] = 0
    return img_gray

binary = easy_binarization(cv2.imread('scripts/curve.png'))



def find_line_fit(img, nwindows=15, margin=20, minumpyix=5):
        histogram = numpy.sum(img[img.shape[0]//2:,:], axis=0)
        # Create an output image to draw on and  visualize the result
        out_img = numpy.dstack((img, img, img)) * 255
        # Find the peak of the left and right halves of the histogram
        # These will be the starting point for the left and right lines
        midpoint = numpy.int(histogram.shape[0]/2)
        leftx_base = numpy.argmax(histogram[:midpoint])
        rightx_base = numpy.argmax(histogram[midpoint:]) + midpoint

        # Set height of windows
        window_height = numpy.int(img.shape[0]/nwindows)
        # Identify the x and y positions of all nonzero pixels in the image
        nonzero = img.nonzero() 
        nonzeroy = numpy.array(nonzero[0])
        nonzerox = numpy.array(nonzero[1])
        # Current positions to be updated for each window
        leftx_current = leftx_base
        rightx_current = rightx_base
        # Create empty lists to receive left and right lane pixel indices
        left_lane_inds = []
        right_lane_inds = []

        # Step through the windows one by one

        for window in range(nwindows):
            # Identify window boundaries in x and y (and right and left)
            win_y_low = img.shape[0] - (window+1)*window_height
            win_y_high = img.shape[0] - window*window_height
            win_xleft_low = leftx_current - margin
            win_xleft_high = leftx_current + margin
            win_xright_low = rightx_current - margin
            win_xright_high = rightx_current + margin
            # Draw the windows on the visualization image
            cv2.rectangle(out_img,(win_xleft_low,win_y_low),(win_xleft_high,win_y_high),
           (0,255,0), 2)
            cv2.rectangle(out_img,(win_xright_low,win_y_low),(win_xright_high,win_y_high),
            (0,255,0), 2)
            # Identify the nonzero pixels in x and y within the window
            good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) &
            (nonzerox >= win_xleft_low) &  (nonzerox < win_xleft_high)).nonzero()[0]
            good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) &
            (nonzerox >= win_xright_low) &  (nonzerox < win_xright_high)).nonzero()[0]
            # Append these indices to the lists
            left_lane_inds.append(good_left_inds)
            right_lane_inds.append(good_right_inds)
            # If you found > minumpyix pixels, recenter next window on their mean position
            if len(good_left_inds) > minumpyix:
                leftx_current = numpy.int(numpy.mean(nonzerox[good_left_inds]))
            if len(good_right_inds) > minumpyix:
                rightx_current = numpy.int(numpy.mean(nonzerox[good_right_inds]))

    # Concatenate the arrays of indices
    # 
        left_lane_inds = numpy.concatenate(left_lane_inds)
        right_lane_inds = numpy.concatenate(right_lane_inds)

    # Extract left and right line pixel positions
        leftx = nonzerox[left_lane_inds]
        lefty = nonzeroy[left_lane_inds]
        rightx = nonzerox[right_lane_inds]
        righty = nonzeroy[right_lane_inds]

    # to plot
        out_img[nonzeroy[left_lane_inds], nonzerox[left_lane_inds]] = [255, 0, 0]
        out_img[nonzeroy[right_lane_inds], nonzerox[right_lane_inds]] = [0, 0, 255]

    # Fit a second order polynomial to each
        left_fit = numpy.polyfit(lefty, leftx, 2)
        right_fit = numpy.polyfit(righty, rightx, 2)

        return left_fit, right_fit, out_img

# Generate x and y values for plotting
def get_fit_xy(img, left_fit, right_fit):
        ploty = numpy.linspace(0, img.shape[0]-1, img.shape[0])
        left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
        right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]

        return left_fitx, right_fitx, ploty

left_fit, right_fit, out_img = find_line_fit(binary, nwindows=15, margin=10, minumpyix=5)
left_fitx, right_fitx, ploty = get_fit_xy(binary, left_fit, right_fit)

def measure_curvature_real(left_fitx, right_fitx, ploty, left_fit, right_fit):

    # Define conversions in x and y from pixels space to meters
    ym_per_pix = 16.0/720 # meters per pixel in y dimension
    xm_per_pix = 3.7/1000 # meters per pixel in x dimension
    
    leftx = left_fitx*xm_per_pix
    rightx = right_fitx*xm_per_pix
    ploty = ploty*ym_per_pix
    
    left_fit_cr = numpy.polyfit(ploty, leftx, 2)
    right_fit_cr = numpy.polyfit(ploty, rightx, 2)

    # Define y-value where we want radius of curvature
    # We'll choose the maximum y-value, corresponding to the bottom of the image
    y_eval = numpy.max(ploty)
    
    # Implement the calculation of R_curve (radius of curvature) 
    left_curverad = ((1 + (2*left_fit_cr[0]*y_eval*ym_per_pix + left_fit_cr[1])**2)**1.5) / numpy.absolute(2*left_fit_cr[0])
    right_curverad = ((1 + (2*right_fit_cr[0]*y_eval*ym_per_pix + right_fit_cr[1])**2)**1.5) / numpy.absolute(2*right_fit_cr[0])
    
    return left_curverad, right_curverad



def calculate_curv_and_pos(binary_warped,leftx, rightx, ploty):
    # Define y-value where we want radius of curvature
        ploty = numpy.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0] )

        leftx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
        rightx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]

        lane_width = numpy.absolute(leftx[binary_warped.shape[0]-1] - rightx[binary_warped.shape[0]-1])
    
        lane_xm_per_pix = 3.7 / (lane_width*5)  
        veh_pos = (((leftx[binary_warped.shape[0]-1] + rightx[binary_warped.shape[0]-1]) * lane_xm_per_pix) / 2.)

        cen_pos = ((binary_warped.shape[1] * lane_xm_per_pix) / 2.)

        distance_from_center = veh_pos - cen_pos +0.06
    
        # Define conversions in x and y from pixels space to meters
        #  ym_per_pix = 30/720 # meters per pixel in y dimension
        #  xm_per_pix = 3.7/700 # meters per pixel in x dimension
        ym_per_pix = 30/binary_warped.shape[0] # meters per pixel in y dimension
    #     xm_per_pix = 3.7/binary_warped.shape[1]  # meters per pixel in x dimension
        xm_per_pix = lane_xm_per_pix
        y_eval = numpy.max(ploty)
        # Fit new polynomials to x,y in world space
    
        left_fit_cr = numpy.polyfit(ploty*ym_per_pix, leftx*xm_per_pix, 2)

        right_fit_cr = numpy.polyfit(ploty*ym_per_pix, rightx*xm_per_pix, 2)
        # Calculate the new radii of curvature

        left_curverad = ((1 + (2*left_fit_cr[0]*y_eval*ym_per_pix + left_fit_cr[1])**2)**1.5) / numpy.absolute(2*left_fit_cr[0])
        right_curverad = ((1 + (2*right_fit_cr[0]*y_eval*ym_per_pix + right_fit_cr[1])**2)**1.5) / numpy.absolute(2*right_fit_cr[0])

        curvature = ((left_curverad + right_curverad) / 2)

        return curvature,distance_from_center

left,right=measure_curvature_real(left_fitx,right_fitx,ploty,left_fit,right_fit)
print(left,right)
