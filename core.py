import tkinter as tk
from PIL import ImageTk, Image
import os


class ImageProperty():
    def __init__(self, path):
        self.path = path
        self.rectangles = []

    def get_next_class(self):
        ret = 0
        for rect in self.rectangles:
            if rect['class'] > ret:
                ret = rect['class']
        return ret + 1

COLORS = ('red', 'blue', 'green', 'yellow', 'cyan', 'goldenrod', 'coral', 'brown', 'orchid', 'black')
IMAGE_RESOLUTION = (1200, 700)
PATH = '/home/zdeeno/Pictures/dataset'
curr_img = None
curr_img_index = None
images = []
curr_rect_holder = None
curr_rect_pt = None
creating_rect = False
class_index = None


def resize_image(image):
    ratio = max(image.size[0]/IMAGE_RESOLUTION[0], image.size[1]/IMAGE_RESOLUTION[1])
    ret_x = image.size[0]/ratio - 2
    ret_y = image.size[1]/ratio - 2
    image = image.resize((int(ret_x), int(ret_y)), Image.ANTIALIAS)
    return image


def show_image(path):
    # clear:
    canvas.delete("all")
    bar.delete("all")
    # open image
    image = Image.open(path)
    image = resize_image(image)
    photo = ImageTk.PhotoImage(image)
    global curr_img
    curr_img = photo
    item = canvas.create_image(int(IMAGE_RESOLUTION[0] / 2), int(IMAGE_RESOLUTION[1] / 2), image=photo)
    # create rectangles
    for rect in images[curr_img_index].rectangles:
        canvas.create_rectangle(rect['position'], width=2, outline=COLORS[rect['class'] - 1])
    # apply
    canvas.pack(side='top', expand=True, fill='both')
    bar.pack(side='bottom', expand=True, fill='both')
    return item


def iterate_files(folder_path):
    directory = os.fsencode(folder_path)
    ret = []

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        file_path = os.path.join(folder_path, filename)

        try:
            Image.open(file_path)
            ret.append(file_path)
        except: OSError

    return ret


def leftKey(event):
    global curr_img_index
    if curr_img_index is not None:
        curr_img_index -= 1
    if curr_img_index >= len(images):
        curr_img_index = 0
    show_image(images[curr_img_index].path)


def rightKey(event):
    global curr_img_index
    if curr_img_index is not None:
        curr_img_index += 1
    if curr_img_index >= len(images):
        curr_img_index = 0
    show_image(images[curr_img_index].path)


def left_click(event):
    global creating_rect, curr_rect_pt, curr_rect_holder, class_index
    if not creating_rect:
        curr_rect_pt = (event.x, event.y)
        class_index = images[curr_img_index].get_next_class()
        curr_rect_holder = canvas.create_rectangle(*curr_rect_pt, curr_rect_pt[0] + 2, curr_rect_pt[1] + 2,
                                                   width=2, outline=COLORS[class_index - 1])
        creating_rect = True
    else:
        images[curr_img_index].rectangles.append({'class': class_index,
                                                  'position': canvas.coords(curr_rect_holder)})
        creating_rect = False
        curr_rect_holder = False


def motion(event):
    global curr_rect_pt, curr_rect_holder, creating_rect
    if creating_rect:
        pt = (event.x, event.y)
        if curr_rect_pt[0] > pt[0]:
            canvas.coords(curr_rect_holder, *pt, *curr_rect_pt)
        else:
            canvas.coords(curr_rect_holder, *curr_rect_pt, *pt)


root = tk.Tk()
canvas = tk.Canvas(root, height=IMAGE_RESOLUTION[1], width=IMAGE_RESOLUTION[0])
bar = tk.Canvas(root, height=int(IMAGE_RESOLUTION[1]/8), width=IMAGE_RESOLUTION[0], bg='white')
root.bind('<Left>', leftKey)
root.bind('<Right>', rightKey)
canvas.bind("<Button-1>", left_click)
canvas.bind("<Motion>", motion)
# img_item = show_image(PATH)
for im_path in iterate_files(PATH):
    images.append(ImageProperty(im_path))
if len(images) > 0:
    curr_img_index = 0
    show_image(images[0].path)
root.mainloop()


