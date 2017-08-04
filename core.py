import tkinter as tk
from PIL import ImageTk, Image
import os

IMAGE_RESOLUTION = (1200, 700)
PATH = '/home/zdeeno/Pictures/dataset'
curr_img = None
curr_img_index = None

def resize_image(image):
    ratio = max(image.size[0]/IMAGE_RESOLUTION[0], image.size[1]/IMAGE_RESOLUTION[1])
    ret_x = image.size[0]/ratio - 2
    ret_y = image.size[1]/ratio - 2
    image = image.resize((int(ret_x), int(ret_y)), Image.ANTIALIAS)
    return image


def show_image(path):
    image = Image.open(path)
    image = resize_image(image)
    photo = ImageTk.PhotoImage(image)
    global curr_img
    curr_img = photo
    item = canvas.create_image(int(IMAGE_RESOLUTION[0] / 2), int(IMAGE_RESOLUTION[1] / 2), image=photo)
    canvas.pack(side='top', expand=True, fill='both')
    return item


def iterate_files(folder_path):
    directory = os.fsencode(folder_path)
    ret = []

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        file_path = os.path.join(folder_path, filename)

        try:
            image = Image.open(file_path)
            ret.append(file_path)
        except: OSError

    return ret


def leftKey(event):
    global curr_img_index
    if curr_img_index is not None:
        curr_img_index -= 1
    if curr_img_index >= len(img_buffer):
        curr_img_index = 0
    show_image(img_buffer[curr_img_index])


def rightKey(event):
    global curr_img_index
    if curr_img_index is not None:
        curr_img_index += 1
    if curr_img_index >= len(img_buffer):
        curr_img_index = 0
    show_image(img_buffer[curr_img_index])


root = tk.Tk()
canvas = tk.Canvas(root, height=IMAGE_RESOLUTION[1], width=IMAGE_RESOLUTION[0])
root.bind('<Left>', leftKey)
root.bind('<Right>', rightKey)
# img_item = show_image(PATH)
img_buffer = iterate_files(PATH)
if len(img_buffer) > 0:
    curr_img_index = 0
    show_image(img_buffer[0])
root.mainloop()


