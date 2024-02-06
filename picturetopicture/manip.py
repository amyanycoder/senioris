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

#Applies a Threshold to a subregion of the image
def ThreshApplier(img, region, thresh_type, thresh_value):
    height, width, channels = img.shape

    #the percentage of the image to be thresholded, rounded to the nearest pixel
    region_code = fsm.RegionCodeGetter(region)
    pixel_height = fsm.FractionToRegion(height, region_code)

    #defines a region, then thresholds it
    subregion = img[region[1]*codel_height:pixel_height, 0:width]
    thresh_region = cv2.threshold(subregion, thresh_value, 255, thresh_type)[1]

    return ImageMerger(img, thresh_region, width, pixel_height, region[1])


#Prints the sequence of three digit codes onto the image
def ThreeApplier(img, region, state_holder, properties, codes_deque):
    height, width, channels = img.shape

    #the percentage of the image to have text added on top, rounded to the nearest pixel
    region_code = fsm.RegionCodeGetter(region)
    pixel_height = fsm.FractionToRegion(height, region_code)

    subregion = img[region[1]*codel_height:pixel_height, 0:width]

    #picks the font from the first digit in the property code
    font = FontPicker(properties[0][0])
    #picks the color from the second digit in the property code
    color = FontColorPicker(properties[0][1], subregion)
    #picks the font size from the third digit in the property code
    font_size = FontSizePicker(properties[0][2], width)
    #picks the offset from the third digit in the function code
    

    print(cv2.getTextSize(str(region[0]), font, font_size, 1)[0][0] * 0.5)

    #prints the three essential codes for this statement:  The region code, the function code, and the properties code.
    subregion = cv2.putText(subregion, fsm.codeToString(region[0]), OffsetPicker(state_holder[0][2], region[0], font, font_size, width, region[1] + 1), font, font_size, color)
    subregion = cv2.putText(subregion, fsm.codeToString(state_holder[0]), OffsetPicker(state_holder[0][2], state_holder[0], font, font_size, width, state_holder[1] + 1), font, font_size, color)
    subregion = cv2.putText(subregion, fsm.codeToString(properties[0]), OffsetPicker(state_holder[0][2], properties[0], font, font_size, width, properties[1] + 1), font, font_size, color)
    
    #prints all other codes remaining in the deque.
    for x in codes_deque:
        subregion = cv2.putText(img, fsm.codeToString(x[0]), OffsetPicker(state_holder[0][2], x[0], font, font_size, width, x[1] + 1), font, font_size, color)

    return subregion
    #ImageMerger(img, subregion, width, pixel_height, region[1])



#Merges the altered subregion with the source code image
def ImageMerger(img, subregion, width, s_height, start_pixel):

    img[start_pixel*codel_height:s_height, 0:width] = subregion
    return img


#picks a font based off of the first digit of the three-digit proceedure code
def FontPicker(digit):
    if(digit == 0):
        return cv2.FONT_HERSHEY_SIMPLEX
    elif(digit == 1):
        return cv2.FONT_HERSHEY_COMPLEX
    else:
        return cv2.FONT_HERSHEY_SCRIPT_COMPLEX


#picks a color for the font based off of the second digit of the three-digit proceedure code
def FontColorPicker(digit, subregion):
    #picks white
    if(digit == 1):
        return (255, 255, 255)
    #picks the color of the top left corner of the subregion
    elif(digit == 2):
        color_temp = tuple(subregion[0,0])
        return tuple((int(color_temp[0]), int(color_temp[1]), int(color_temp[2])))
    #picks black
    else:
        return (0, 0, 0)

#picks a factor by which to multiply the font size by based on the third digit of the three digit proceedure code
def FontSizePicker(digit, width):
    factor = 0.0
    #small image
    if(digit == 0):
        factor = 0.5
    #medium image
    elif(digit == 1):
        factor = 1
    #large image
    else: 
        factor = 1.5
    
    return width / (200 / factor)

#sets an offset for the text, setting a consistent offset vertically and a left, center, or right orientation based on the function code.
#right and center align currently slightly off
def OffsetPicker(digit, text, font, font_size, width, codel):
    text_bounds, baseline = cv2.getTextSize((str(text)), font, font_size, 1)
    print(text_bounds)
    print(baseline)
    horizontal_offset = 0
    #centered image
    if(digit == 1):
        horizontal_offset = int((width - (text_bounds[0])) / 2)
    #right-aligned image
    elif(digit == 2):
        horizontal_offset = width - (text_bounds[0])
    #left-aligned image
    else: 
        horizontal_offset = 10

    vertical_offset = codel * codel_height - int((text_bounds[1]) * 0.5)

    return (horizontal_offset, vertical_offset)

#applies text to an image
#def TextApplier(img):