import sys
import cv2
img = cv2.imread("patch.jpg", cv2.IMREAD_ANYCOLOR)
 
while True:
    resize_img = cv2.resize(img, (378, 504))
    edges = cv2.Canny(resize_img, threshold1 = 100, threshold2 = 200)
    cv2.imshow("Patch", edges)
    cv2.waitKey(0)

    sys.exit() # to exit from all the processes
 
cv2.destroyAllWindows() # destroy all windows