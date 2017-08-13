# Labeling-tool
This is very simple graphical tool for creating bounding rectangles and appropriate text files.
It should work for python 3.4+ (tested for 3.6 on Ubuntu) using built in python GUI module `tkinter` and `PIL` for images.

## Input:
Input is folder with set of images (image format must be supported by PIL).

## Output:
Output is text file with information about all rectangles in current image. There is one text file for every image.
Output can be modular due to class `FileWriter` which ensures writing output into file.
Currently only writer for `Darknet YOLO` is implemented.
You can implement `FileWriter` interface if you need different output format. 

## GUI:
From top to bottom:
* Input folder
* Output folder
* Image number
* Canvas with currently displayed image
* Bar with rectangles

## Controls:
* `Arrows - left, right` : Previous and next image.
* `Arrows - up, down` : Change class of currently chosen rectangle.
* `Left mouse button` : When clicked on canvas, it starts creating rectangle. When clicked on bar, it chooses clicked rectangle to modify.
* `Right mouse button ` : When clicked on canvas it saves rectangles into file. This is visualised by green background of bar. When clicked on item in bar, item is deleted.

## Running:
Run tool simply by command `python Labeling-tool.py`, then choose input and output folders and work can start.