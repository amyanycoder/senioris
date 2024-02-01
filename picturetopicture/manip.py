import cv2
import fsm

codel_height = 200

#Applies Canny Edge Detection to a subregion of the image
def CannyApplier(img, region):
    height, width, channels = img.shape
    #the percentage of the image to be cannied, rounded to the nearest pixel
    region_code = fsm.RegionCodeGetter(region)
    pixel_height = fsm.FractionToRegion(height, region_code)

    #defines a subregion, and cannies it
    subregion = img[region[1]*codel_height:pixel_height, 0:width]
    canny_region = cv2.Canny(subregion, threshold1 = 100, threshold2 = 200)
    canny_region = cv2.cvtColor(canny_region, cv2.COLOR_GRAY2RGB)

    return ImageMerger(img, canny_region, width, pixel_height, region[1])


#Merges the altered subregion with the source code image
def ImageMerger(img, subregion, width, s_height, start_pixel):

    img[start_pixel*codel_height:s_height, 0:width] = subregion
    return img

