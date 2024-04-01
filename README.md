# Tower:  An Image-to-Image Esoteric Language
### By Amy Falk
### Implemented in partial fulfillment of the Bachelor of Arts in Computer Science at the College of Wooster

Note:  The entirety of Tower is contained within the Tower folder.  All other folders contain small applets that I wrote as a part of my learning process, and are preserved here to demonstrate that process.

## Compatibility
Requires Python version 3.10 or later.

Was designed and written in Windows 11.  Users of Unix based devices may have difficulty running programs in different folders, because of how Windows machines denote file hierarchies with backslashes and Unix machines use forward slashes.

## Introduction

Tower is an image-to-image based esoteric programming language designed to showcase the distorting nature of computer code.  When an image is input, the Tower interpreter extracts functions and rules from the image and uses them to modify the image, producing a distorted output image.  The interpreter is designed to work with any and all images (with a height of 600 pixels or greater) but the rules are simple enough that a programmer can make their own programs by making their own images.

## How to run

Tower is run from the command line, from the file tower.py.  Tower accepts two valid parameters as arguments:  A file path for an image to take as input, and the flag "-v" which runs the program in a verbose mode that displays images from throughout the interpretation process.  If the file is run without an image as input, it uses a default image.

The tower folder has two folders of programs to try out:  The first is testprograms, which each showcase how a different function works.  The other is examples, which features programs with interesting outputs.  Try experimenting with the included images, or run some images of your own!

## How it works

Tower works by using the process of Canny Edge Detection, a process that reduces an image into all black, with white edges.  Tower then splits this edge detection image into horizontal strips called *codels*.  Codels are 200 pixels high and span the width of the image.  This process is shown by running a program in verbose mode:  The first image displayed is the edge detection that is derived from the input image, and then each subsequent image is one of the codels.

Once Tower has this sequence of codels, it then generates a sequence of three digit base-3 codes.  These codes are derived from the sequence of codels, and their values stem from asking three key questions from the codel sequence:

Leftmost digit: Is the current codel's leftmost edge pixel further to the left (value of 2), the same within a threshold (value of 1), or less far left (value of 0) than the previous codel's leftmost edge pixel?

Middle digit:  Does the current codel have more edge pixels (value of 2), about the same number of edge pixels within a threshold (value of 1), or less edge pixels (value of 0) than the previous codel?

Rightmost digit: Is the current codel's rightmost edge pixel further to the right (value of 2), the same within a threshold (value of 1), or less far right (value of 0) than the previous codel's rightmost edge pixel?

### Example of base 3 code generation

As an example, let’s suppose that we are analyzing the second of two codels. These codels come from an image that is 200 pixels wide. The previous codel has its leftmost edge at left_pos = 80, has 5000 pixels that are edges (num_edges = 5000), and has its rightmost edge at right_pos = 196. The current codel has its leftmost edge at left_pos = 14, has 600 pixels that are edges (num_edges = 600), and has its rightmost edge at right_pos = 189. 

First, we need to establish our threshold values. For our leftmost and rightmost digits, Tower determines the threshold value (called the positional threshold value) to be 0.1*w* where *w* = the width of the image.   This means that for this theoretical image, the threshold for the left and right digits is 20 pixels. For Tower to evaluate the positions of the current codel’s left and rightmost edge to be equal to that of the previous codel, the values of the current codel need to fall within 20 pixels of that of the previous codel. Tower determines the middle digit threshold with the formula (*w* ∗ *h*)/100 where *w* = the width of the codel and *h* = the height of the codel. Since this image has a width of 200 and the height of every codel in Tower is 200, the area threshold value for this image is 400. 

With these values established, we can now find the intermediate code for the current codel. Beginning with our leftmost digit, we can see that the leftmost pixel of the current codel (at *x* = 14) is further to the left than the leftmost pixel of the previous codel even with the threshold value added (at *x* = 80 − 20, or *x* = 60), giving us a left digit value of 2. For the middle digit, we can see that the current codel’s number of edge pixels (600) is well below the previous codel’s number of edge pixels (5000) even with the addition of the threshold value, giving the middle digit a value of 0. Finally, for the rightmost value, we can see that while the current codel’s rightmost pixel is at a less far right position (*x* = 189) than the previous codel’s rightmost pixel (*x* = 196), the two values are within the threshold value (20 pixels) of each other. This makes the two values equivalent to the Tower interpreter, giving the rightmost digit a value of 1. This leaves us with an code of 201 generated from the comparison of these codels.  By comparing all of these codels this way, Tower generates a stream of three-digit codes that can then be translated into statements.

### Syntax

Each statement in Tower follows the same syntax:  

Scale Code -> Function Code -> One or more Property Codes (optional)

The Scale Code determines how much of the image the function should affect, as a fraction out of 27 (or 222, in base 3).  The region defined by the Scale Code always starts at the top of the image.

The Function Code denotes which function will be implemented on the region defined by the scale code.


The property code(s) is function specific, and determines important parameters for the function to run.

### Functions

Here is the table that determines which Function Code corresponds to which function:

|Code|Function  |
|-|--|
|000  |Base3 (left)  |
|001  |Base3 (center)  |
|002  |Base3 (right)  |
| 010 |Sentence (left)  |
|011  |Sentence (center)  |
|012  |Sentence (right)  |
|020  |Python (tower.py)  |
|021  |Python (fsm.py)  |
|022  |Python (manip.py)  |
| 100 |Hexa  |
|101  |Hexa  |
|102  |Hexa  |
| 110 |Threshold  |
| 111 |Threshold (grayscale)  |
|112  |Canny  |
|120  |Sort (lightness)  |
| 121 |Sort (hue)  |
|122  |Sort (saturation)  |
|200  |Sort (saturation)  |
|201  |Sort (intensity)  |
|202  |Sort (intensity)  |
|210  |Sort (minimum)  |
|211  |Sort (minimum)  |
|212  |Print (left)  |
|220  |Print (center)  |
| 221 |Print (right)  |
| 222 |Skip Section  |



#### Base3 function

The Base3 function directly prints the Base 3 codes directly onto the image itself.  Depending on the specific function code called, these codes can be left aligned, right aligned, or centered.  Base3's font, color, and size properties are determined by the Text Code, a code it shares in common with Sentence and Hexa.

#### Sentence function

The Sentence function prints a natural English version of the code statement onto the image.  This can be left, center, or right aligned.  Sentence's font, color, and size properties are determined by the Text Code, a code it shares in common with Base3 and Hexa.

#### Python function

The Python function prints text from the interpreter's Python files onto the image.  The file printed from depends on the specific function code called, and the Python Code determines the font, font size, and specific code printed.

#### Hexa function

The Hexa function prints the text data from the image file itself onto the image.  Hexa's font, color, and size properties are determined by the Text Code, a code it shares in common with Base3 and Sentence.

#### Threshold function
The Threshold function thresholds the image.  The specific function code determines if it does so to a color or grayscale version of the image.  The Threshold Code determines the kind of thresholding applied, as well as the threshold value.

#### Canny function
The Canny function applies Canny Edge Detection to the image.  This function has no property code.

#### Sort function
The Sort function sorts an amount of the image's pixels.  The specific function code chosen determines which value the pixels are sorted by.  The Sort Code determines how many pixels to sort, which angle to sort them at, and whether to sort high, medium, or low values.

#### Print function
The Print function prints a string onto the image.  The specific function code chosen determines if this function is left, center, or right aligned.  The Print Code determines the font, color, and capitalization of the string.  The Print Code is followed by an unlimited number of Char codes, which each correspond to a specific ASCII character.

#### Skip function
The Skip function skips the current statement.  It has no procedure codes.

### Procedure Codes List

#### Text Code
|First Digit  |Font  |
|--|--|
|0  | Hershey Simplex |
| 1 | Hershey Complex |
| 2 | Hershey Script Complex |

| Second Digit | Font Color  |
|--|--|
|0  |Black  |
| 1 |White  |
|  2|Color of Top Left Pixel  |

| Third Digit | Font Size  |
|--|--|
|0  |Small |
| 1 |Medium|
|  2|Large  |


#### Python Code
|First Digit  |Start Position of Python Text Stream|
|--|--|
|0  | Top of File |
| 1 | 1/3 through File |
| 2 | 2/3 through file |

| Second Digit | Font Color  |
|--|--|
|0  |Black  |
| 1 |White  |
|  2|Color of Top Left Pixel  |

| Third Digit | Font Size  |
|--|--|
|0  |Small |
| 1 |Medium|
|  2|Large  |

#### Threshold Code
|First Digit  |Threshold Type|
|--|--|
|0  | Standard Binary|
| 1 | Inverse Binary |
| 2 | To Zero |

| Second Two Digits | |
|--|--|
|Threshold Value | 100n/9 + 100, where n is a decimal representation of the second and third digit

#### Sort Code
|First Digit  |Degree |
|--|--|
|0  | 0 |
| 1 | 45 |
| 2 | 90 |

| Second Digit | Sorted Section  |
|--|--|
|0  |Lowest values|
| 1 |Middle values|
|  2| Highest values |

| Third Digit | Percentage of Possible Values  |
|--|--|
|0  |50%|
| 1 |90%|
|  2|100%|

#### Print Code
|First Digit  |Font  |
|--|--|
|0  | Hershey Simplex |
| 1 | Hershey Complex |
| 2 | Hershey Script Complex |

| Second Digit | Font Color  |
|--|--|
|0  |Black  |
| 1 |White  |
|  2|Color of Top Left Pixel  |

| Third Digit | Capitalization |
|--|--|
|0  |lowercase|
| 1 |UPPERCASE|
|  2|Capitalized|

#### Char Code
|Code |Result  |
|--|--|
| 000 | Terminate String |
|001-222  | The ASCII character at n + 65 where n is a decimal representation of the base-3 code |

