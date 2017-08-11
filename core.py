import tkinter as tk
from tkinter import font
from tkinter import filedialog
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


COLORS = ('red', 'blue', 'green', 'yellow', 'cyan', 'goldenrod', 'coral', 'brown', 'IndianRed4', 'orchid', 'black',
          'pink', 'azure4', 'orange', 'orange4', 'pink4', 'IndianRed1', 'chartreuse4', 'chocolate')
IMAGE_RESOLUTION = (1200, 700)
curr_img = None
curr_img_index = None
images = []
curr_rect_holder = None
curr_rect_pt = None
creating_rect = False
class_index = None
curr_rect_index = None
bar_rects = []
bar_texts = []
image_x = None
image_y = None
im_path = None
out_path = None


def resize_image(image):
    ratio = max(image.size[0]/IMAGE_RESOLUTION[0], image.size[1]/IMAGE_RESOLUTION[1])
    ret_x = image.size[0]/ratio - 2
    ret_y = image.size[1]/ratio - 2
    global image_x, image_y
    image_x = (int(IMAGE_RESOLUTION[0]/2 - ret_x/2), int(IMAGE_RESOLUTION[0]/2 + ret_x/2))
    image_y = (int(IMAGE_RESOLUTION[1]/2 - ret_y/2), int(IMAGE_RESOLUTION[1]/2 + ret_y/2))
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
    global curr_rect_index
    curr_rect_index = None
    for rect in images[curr_img_index].rectangles:
        canvas.create_rectangle(rect['position'], width=2, outline=COLORS[(rect['class'] - 1) % len(COLORS)])
    # update bar
    init_bar()
    update_bar()
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


def upKey(event):
    if curr_rect_index is not None:
        images[curr_img_index].rectangles[curr_rect_index]['class'] += 1
        holder = images[curr_img_index].rectangles[curr_rect_index]['holder']
        canvas.itemconfig(holder, outline=COLORS[(images[curr_img_index].rectangles[curr_rect_index]['class'] - 1) % len(COLORS)])
        update_bar()


def downKey(event):
    if curr_rect_index is not None and images[curr_img_index].rectangles[curr_rect_index]['class'] > 1:
        images[curr_img_index].rectangles[curr_rect_index]['class'] -= 1
        holder = images[curr_img_index].rectangles[curr_rect_index]['holder']
        canvas.itemconfig(holder, outline=COLORS[(images[curr_img_index].rectangles[curr_rect_index]['class'] - 1) % len(COLORS)])
        update_bar()


def left_click(event):
    global creating_rect, curr_rect_pt, curr_rect_holder, class_index, curr_rect_index
    if not creating_rect:
        if image_x[0] < event.x < image_x[1] and image_y[0] < event.y < image_x[1]:
            curr_rect_pt = (event.x, event.y)
            class_index = images[curr_img_index].get_next_class()
            curr_rect_holder = canvas.create_rectangle(*curr_rect_pt, curr_rect_pt[0] + 2, curr_rect_pt[1] + 2,
                                                       width=2, outline=COLORS[(class_index - 1) % len(COLORS)])
            creating_rect = True
    else:
        images[curr_img_index].rectangles.append({'class': class_index,
                                                  'position': canvas.coords(curr_rect_holder),
                                                  'holder': curr_rect_holder})
        creating_rect = False
        curr_rect_holder = False
        curr_rect_index = len(images[curr_img_index].rectangles) - 1
        update_bar()


def motion(event):
    global curr_rect_pt, curr_rect_holder, creating_rect
    if creating_rect and image_x[0] < event.x < image_x[1] and image_y[0] < event.y < image_x[1]:
        pt = (event.x, event.y)
        if curr_rect_pt[0] > pt[0]:
            canvas.coords(curr_rect_holder, *pt, *curr_rect_pt)
        else:
            canvas.coords(curr_rect_holder, *curr_rect_pt, *pt)


def update_bar():
    for i in range(len(images[curr_img_index].rectangles)):
        rec = images[curr_img_index].rectangles[i]
        index = rec['class']
        color = COLORS[(index - 1) % len(COLORS)]
        bar.itemconfig(bar_rects[i], outline=color, fill=color)
        bar.itemconfig(bar_texts[i], fill='white', text=str(index), anchor='center', font=FONT)


def bar_click(event):
    global curr_rect_index
    width = int(IMAGE_RESOLUTION[0] / 10) - 2
    index = int((event.x - 10)/width)
    if index < len(images[curr_img_index].rectangles):
        curr_rect_index = index


def bar_delete(event):
    global curr_rect_index
    width = int(IMAGE_RESOLUTION[0] / 10) - 2
    index = int((event.x - 10) / width)
    if index < len(images[curr_img_index].rectangles):
        curr_rect_index = None
        holder = images[curr_img_index].rectangles[index]['holder']
        images[curr_img_index].rectangles.pop(index)
        canvas.delete(holder)
        bar.delete("all")
        init_bar()
        update_bar()


def init_bar():
    bar_rects.clear()
    bar_texts.clear()
    width = int(IMAGE_RESOLUTION[0] / 10) - 2
    height = int(IMAGE_RESOLUTION[1] / 8) - 10
    for i in range(10):
        r = bar.create_rectangle(i * width + 10, 10, (i + 1) * width + 10, height, outline='white', fill='white')
        t = bar.create_text(i * width + 10 + int(width / 2), 5 + int(height / 2), fill='white', text=str('X'),
                            anchor='center', font=FONT)
        bar_rects.append(r)
        bar_texts.append(t)


def input_dialog():
    dirname = filedialog.askdirectory(title="Specify input directory")
    global im_path, curr_img_index
    im_path = dirname
    input_entry.config(state='normal')
    input_entry.delete(first=0, last=tk.END)
    input_entry.insert(0, str(im_path))
    input_entry.config(state='readonly')
    for im_path in iterate_files(im_path):
        images.append(ImageProperty(im_path))
    if len(images) > 0:
        curr_img_index = 0
        show_image(images[0].path)


def output_dialog():
    dirname = filedialog.askdirectory(title="Specify output directory")
    global out_path
    out_path = dirname
    output_entry.config(state='normal')
    output_entry.delete(first=0, last=tk.END)
    output_entry.insert(0, str(out_path))
    output_entry.config(state='readonly')


root = tk.Tk()
FONT = font.Font(family="Helvetica", size=30, weight="bold")
canvas = tk.Canvas(root, height=IMAGE_RESOLUTION[1], width=IMAGE_RESOLUTION[0])
bar = tk.Canvas(root, height=int(IMAGE_RESOLUTION[1]/8), width=IMAGE_RESOLUTION[0], bg='white')

top_frame = tk.Frame(root)
top_frame.pack(expand=1, side=tk.TOP, fill=tk.X)
tk.Button(top_frame, text='    INPUT    ', command=input_dialog).pack(side=tk.LEFT)
input_entry = tk.Entry(top_frame)
input_entry.pack(fill=tk.X, side=tk.RIGHT, expand=1)
input_entry.config(state='readonly')

top_frame = tk.Frame(root)
top_frame.pack(expand=1, side=tk.TOP, fill=tk.X)
tk.Button(top_frame, text='    OUTPUT    ', command=output_dialog).pack(side=tk.LEFT)
output_entry = tk.Entry(top_frame)
output_entry.pack(fill=tk.X, side=tk.RIGHT, expand=1)
output_entry.config(state='readonly')

root.bind('<Left>', leftKey)
root.bind('<Right>', rightKey)
canvas.bind("<Button-1>", left_click)
canvas.bind("<Motion>", motion)
bar.bind('<Button-1>', bar_click)
bar.bind('<Button-3>', bar_delete)
root.bind('<Up>', upKey)
root.bind('<Down>', downKey)

root.mainloop()


