import sys
import cv2
img = cv2.imread("patch.jpg", cv2.IMREAD_ANYCOLOR)
codels = [0, 1, 2, 3, 4, 5, 6, 7]
 
#performs canny edge detection on image and displays result 
resize_img = cv2.resize(img, (378, 504))
edges = cv2.Canny(resize_img, threshold1 = 100, threshold2 = 200)
cv2.imshow("Patch", edges)
cv2.waitKey(0)

#cuts image into codels
i = 0
while i < 8:
    codels.insert(i, edges[63*i:63*(i+1), 0:378])
    i += 1

#displays codels one at a time
for z in range (0,8):
    cv2.imshow("code", codels[z])
    cv2.waitKey(0)
    q = 0
    for y in range(0,378):
        for x in range(0, 63):
            #checks to see if the current pixel is not black
            if(codels[z][x,y] != 0):
                q += 1
    print(q)

print("we made it out")




