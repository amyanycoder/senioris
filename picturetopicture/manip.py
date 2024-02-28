from collections import deque
import textwrap
import cv2
import fsm
from py_algorithms.sort import new_merge_sort
from pixelsort import pixelsort
from PIL import Image
import sys
import numpy as np

codel_height = 200

#Applies Canny Edge Detection to a subregion of the image
def CannyApplier(img, region):
    height, width, channels = img.shape
    #the percentage of the image to be cannied, rounded to the nearest pixel
    region_code = fsm.RegionCodeGetter(region)
    pixel_height = fsm.FractionToRegion(height, region_code)

    #defines a subregion, and cannies it
    subregion = img
    canny_region = cv2.Canny(subregion, threshold1 = 100, threshold2 = 200)
    canny_region = cv2.cvtColor(canny_region, cv2.COLOR_GRAY2RGB)

    return ImageMerger(img, canny_region, width, pixel_height, region[1])

#Applies a Threshold to a subregion of the image
def ThreshApplier(img, region, thresh_type, thresh_value, grey):
    height, width, channels = img.shape


    #the percentage of the image to be thresholded, rounded to the nearest pixel
    region_code = fsm.RegionCodeGetter(region)
    pixel_height = fsm.FractionToRegion(height, region_code)

    grey_img = img
    #defines a region, grayscales the image if necessary, then thresholds it
    if grey == True:
        grey_img = cv2.cvtColor(grey_img, cv2.COLOR_RGB2GRAY)
        grey_img = cv2.cvtColor(grey_img, cv2.COLOR_GRAY2RGB)

    thresh_region = cv2.threshold(grey_img, thresh_value, 255, thresh_type)[1]
   
    return ImageMerger(img, thresh_region, width, pixel_height, region[1])


#Prints the sequence of three digit codes onto the image
def ThreeApplier(img, region, state_holder, properties, codes_deque):
    height, width, channels = img.shape

    #the percentage of the image to have text added on top, rounded to the nearest pixel
    region_code = fsm.RegionCodeGetter(region)
    pixel_height = fsm.FractionToRegion(height, region_code)
    subregion = img

    text_properties = GetTextProperties(properties[0], subregion, width)
    

    #prints the three essential codes for this statement:  The region code, the function code, and the properties code.
    subregion = cv2.putText(subregion, fsm.codeToString(region[0]), OffsetPicker(state_holder[0][2], region[0], text_properties[0], text_properties[2], width, region[1] + 1, 0), text_properties[0], text_properties[2], text_properties[1])
    subregion = cv2.putText(subregion, fsm.codeToString(state_holder[0]), OffsetPicker(state_holder[0][2], state_holder[0], text_properties[0], text_properties[2], width, state_holder[1] + 1, 0), text_properties[0], text_properties[2], text_properties[1])
    subregion = cv2.putText(subregion, fsm.codeToString(properties[0]), OffsetPicker(state_holder[0][2], properties[0], text_properties[0], text_properties[2], width, properties[1] + 1, 0), text_properties[0], text_properties[2], text_properties[1])
    
    #prints all other codes remaining in the deque.
    for x in codes_deque:
        subregion = cv2.putText(subregion, fsm.codeToString(x[0]), OffsetPicker(state_holder[0][2], x[0], text_properties[0], text_properties[2], width, x[1] + 1, 0), text_properties[0], text_properties[2], text_properties[1], int(text_properties[2]))

    return ImageMerger(img, subregion, width, pixel_height, region[1])


def SentenceApplier(img, region, sentence, state_holder, properties):
    height, width, channels = img.shape

    #the percentage of the image to have text added on top, rounded to the nearest pixel
    region_code = fsm.RegionCodeGetter(region)
    pixel_height = fsm.FractionToRegion(height, region_code)
    subregion = img

    sentence = sentence.replace("\n", "")

    text_properties = GetTextProperties(properties[0], subregion, width)

    #breaks up code sentence so that they all text fits on the image
    (text_width, text_height), _ = cv2.getTextSize(sentence, text_properties[0], text_properties[2], 1)
    line_width = text_width
    lines = 1
    lines_deque = deque()

    while line_width > width:
        lines += 1
        line_width = int(text_width / lines)

    line_chars = int(len(sentence) / lines)

    i = 0
    while i < lines:
        lines_deque.append(sentence[i * line_chars : (i + 1) * line_chars]) 
        i += 1


    #prints the code sentence (up to this point) at the top of the subregion
    i = 0
    while len(lines_deque) > 0:
        current = lines_deque.popleft()
        print(int(text_properties[2]))
        subregion = cv2.putText(subregion, current, OffsetPicker(state_holder[0][2], current, text_properties[0], text_properties[2], width, region[1] + 1, i * text_height + i * int(text_height * .2) + int(0.01 * width)), text_properties[0], text_properties[2], text_properties[1], int(text_properties[2]))
        i += 1

    return ImageMerger(img, subregion, width, pixel_height, region[1])


def PrintApplier(img, region, state_holder, properties, codes_deque):
    height, width, channels = img.shape

    #the percentage of the image to have text added on top, rounded to the nearest pixel
    region_code = fsm.RegionCodeGetter(region)
    pixel_height = fsm.FractionToRegion(height, region_code)
    subregion = img
    text_properties = GetTextProperties(properties[0], subregion, width)
    

    #runs through the codes deque and generates a phrase by converting to unicode
    statement = ""
    for x in codes_deque:
        if fsm.base3(x[0]) == 0:
            break

        char = chr(fsm.base3(x[0]) + 64)
        statement += char

    subregion = cv2.putText(subregion, statement, OffsetPicker(state_holder[0][2], statement, text_properties[0], text_properties[2], width, 0, int(0.1 * width)), text_properties[0], text_properties[2], text_properties[1], int(text_properties[2]))

    return ImageMerger(img, subregion, width, pixel_height, region[1])


def PythonApplier(img, region, state_holder, properties, file):
    height, width, channels = img.shape

    py = open(file, "r")

    #the percentage of the image to have text added on top, rounded to the nearest pixel
    region_code = fsm.RegionCodeGetter(region)
    pixel_height = fsm.FractionToRegion(height, region_code)
    subregion = img
    text_properties = GetTextProperties(properties[0], subregion, width)

    lines = py.read().split("\n")

    #chooses starting index based on the first digit of the properties code.
    start = int(properties[0][0] / 3 * len(lines))
    lines = lines[start:len(lines) - 1]


    (text_width, text_height), _ = cv2.getTextSize(lines[0], text_properties[0], text_properties[2], 1)


    for x in lines:
        subregion = cv2.putText(subregion, x, (0, int(lines.index(x) * text_height * 1.25)), cv2.FONT_HERSHEY_SIMPLEX, text_properties[2], text_properties[1], int(text_properties[2]))

    py.close()

    return ImageMerger(img, subregion, width, pixel_height, region[1])


def HexApplier(img, region, state_holder, properties, file):
    height, width, channels = img.shape

    py = open(file, "rb")

    #the percentage of the image to have text added on top, rounded to the nearest pixel
    region_code = fsm.RegionCodeGetter(region)
    pixel_height = fsm.FractionToRegion(height, region_code)
    subregion = img
    text_properties = GetTextProperties(properties[0], subregion, width)


    stream = str(py.read())

    lines = []

    i = 0
    while i < len(stream):
        lines.append(stream[i:i+50])
        i += 50


    (text_width, text_height), _ = cv2.getTextSize(lines[0], text_properties[0], text_properties[2], 1)

    for x in lines:
        subregion = cv2.putText(subregion, x, (0, int(lines.index(x) * text_height * 1.25)), cv2.FONT_HERSHEY_SIMPLEX, text_properties[2], text_properties[1], int(text_properties[2]))

    py.close()

    return ImageMerger(img, subregion, width, pixel_height, region[1])


def PixelSorter(img, region, sort_mode, lower_bound, upper_bound, degree):
    height, width, channels = img.shape

    #the percentage of the image to have text added on top, rounded to the nearest pixel
    region_code = fsm.RegionCodeGetter(region)
    pixel_height = fsm.FractionToRegion(height, region_code)
    subregion = img


    
    #takes an image, sorts the pixels, and converts it back into cv2 format
    im_pil = Image.fromarray(img)
    im_pil = pixelsort(im_pil, None, None, 0, 20, sort_mode, "threshold", lower_bound, upper_bound, degree)
    subregion = cv2.cvtColor(np.asarray(im_pil), cv2.COLOR_RGBA2RGB)
    
    return ImageMerger(img, subregion, width, pixel_height, region[1])


def Skip(img, region):
    height, width, channels = img.shape

    #the percentage of the image to have text added on top, rounded to the nearest pixel
    region_code = fsm.RegionCodeGetter(region)
    pixel_height = fsm.FractionToRegion(height, region_code)
    subregion = img
    
    return ImageMerger(img, subregion, width, pixel_height, region[1])


#returns font, font_size, and color in a tuple
def GetTextProperties(properties_code, subregion, width):
    #picks the font from the first digit in the property code
    font = FontPicker(properties_code[0])
    #picks the color from the second digit in the property code
    font_color = FontColorPicker(properties_code[1], subregion)
    #picks the font size from the third digit in the property code
    font_size = FontSizePicker(properties_code[2], width)

    return (font, font_color, font_size)


#Merges the altered subregion with the source code image
def ImageMerger(img, subregion, width, s_height, start_pixel):
    crop = subregion[start_pixel*codel_height:s_height, 0:width]  

    img[start_pixel*codel_height:s_height, 0:width] = crop
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
        factor = 0.25
    #medium image
    elif(digit == 1):
        factor = 0.5
    #large image
    else: 
        factor = 1
    
    return width / (200 / factor)


#sets an offset for the text, setting a consistent offset vertically and a left, center, or right orientation based on the function code.
#right and center align currently slightly off
def OffsetPicker(digit, text, font, font_size, width, codel, vert_offset):
    text_bounds, baseline = cv2.getTextSize((str(text)), font, font_size, 1)

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

    vertical_offset = codel * codel_height - int((text_bounds[1]) * 0.5) + vert_offset

    return (horizontal_offset, vertical_offset)