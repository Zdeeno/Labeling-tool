# Labeling-tool
This is very simple graphical tool for creating bounding rectangles and appropriate text files, suitable for training neural networks.
It should work for `python 3.4+` (tested on conda python 3.6.2, Ubuntu and macOS) using built in python GUI module `tkinter` and `PIL` for images.

## Input:
Input is folder with set of images (image format must be supported by PIL).

## Output:
Output is text file with information about all rectangles in current image. There is one text file for every image.
Output can be modular due to class `FileWriter` which ensures writing output into file.
Currently only writer for `Darknet YOLO` is implemented.
You can implement `FileWriter` interface if you need different output format. 

## GUI:
From top to bottom:
1. Input folder
2. Output folder
3. Image number
4. Canvas with currently displayed image
5. Bar with rectangles
6. Current bar index

![Alt text](screenshot.png?raw=true "Optional Title")

## Controls:
* `Arrows - left, right` : Previous and next image.
* `Arrows - up, down` or `Mousewheel` : Change class of currently chosen rectangle.
* `Left mouse button` : When clicked on canvas, it starts creating rectangle. When clicked on bar, it chooses rectangle to modify.
* `Right mouse button ` : When clicked on canvas last item is deleted. When clicked on bar, chosen item is deleted.
* `Spacebar` : Save rectangles into file and go to next frame.
* `Mousewheel click` : Save rectangles into file. This is visualised by green color of bar's background.

## Running:
1. Run tool simply by command `python Labeling-tool.py`
2. Choose input/output folders
3. Work can start
