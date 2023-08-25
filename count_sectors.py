# Import the necessary libraries
import cv2
import numpy as np

#enchance contrast and brightness
def ContBright(image):   
    alpha = 3.0 #[1.0-3.0]
    beta = 100 #[0 - 100]
    contrast_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return contrast_image
    
def findCenterRadius(img):
    '''
    return: center (x , y), radius
    '''
    # Read in the image
    image = img.copy()
    image = ContBright(image)
    # Convert the image to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Blur the image to reduce noise
    image = cv2.GaussianBlur(image, (5, 5), 0)
    # Threshold the image to create a binary image
    image = cv2.threshold(image, 240, 255, cv2.THRESH_BINARY)[1]
    # Find the contours in the image
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    (x,y),radius = cv2.minEnclosingCircle(largest_contour)
    center = (int(x),int(y))
    radius = int(radius)
    return center, radius

def sectCount(bboxes, img):
    center, radius = findCenterRadius(img)
    x = center[0]
    y = center[1]
    sec0 = 0
    sec1 = 0
    sec2 = 0
    sec3 = 0
    sec4 = 0
    rc = radius/(np.sqrt(4+1))
    for box in bboxes:
        y1, x1, y2, x2 = box
        x0 = (x1 + x2) / 2
        y0 = (y1 + y2) / 2
        if (x0 - center[0])**2 + (y0 - center[1])**2 <= rc*rc:
            sec0 +=1
        elif x - x0 < 0 and y - y0 > 0:
            sec3+= 1
        elif x - x0 > 0 and y-y0 > 0:
            sec1+=1
        elif x - x0 < 0 and y - y0 < 0:
            sec4+=1
        else:
            sec2+=1
    num_col_sectors = [sec0, sec1, sec2, sec3, sec4]
    return num_col_sectors