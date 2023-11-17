import sys
import cv2
img = cv2.imread("patch.jpg", cv2.IMREAD_ANYCOLOR)
contours = []
codels = [0, 1, 2, 3, 4, 5, 6, 7]
 
#performs canny edge detection on image and displays result 
resize_img = cv2.resize(img, (378, 504))
cv2.findContours(img, contours, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(img, contours, -1, (255,255,255))
cv2.imshow("Patch", edges)
cv2.waitKey(0)

#cuts image into codels
i = 0
while i < 8:
    codels.insert(i, img[63*i:63*(i+1), 0:378])
    i += 1

#displays codels one at a time
x = 0
while x < 8:
    cv2.imshow("code", codels[x])
    cv2.waitKey(0)
    x += 1
