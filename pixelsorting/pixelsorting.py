import cv2
import sys
import numpy as np
from py_algorithms.sort import new_merge_sort
from pixelsort import pixelsort
from PIL import Image




def vert_sort(img):
    height, width, channels = img.shape


    print()
    

def main():
    default_img = "barbiecrop.png"
    if __name__ == "__main__":
        if(len(sys.argv) < 2):
            print("No image specified.  Using default image file.")
            img = cv2.imread(default_img, cv2.IMREAD_ANYCOLOR)
        elif(len(sys.argv) == 2):
            img = cv2.imread(sys.argv[1], cv2.IMREAD_ANYCOLOR)
        else:
            img = cv2.imread(default_img, cv2.IMREAD_ANYCOLOR)


    im_pil = Image.fromarray(img)

    im_pil = pixelsort(im_pil, None, None, 0, 20, "minimum", "threshold", 0.25, 0.75, 45)
    im_np = np.asarray(im_pil)
    

    cv2.imshow("img", im_np)
    cv2.waitKey(0)
    cv2.imwrite("test.jpg", im_np)


if __name__ == "__main__":
    main()