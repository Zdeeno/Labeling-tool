import tkinter as tk
from tkinter import font
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import os


class ImageProperty():
    def __init__(self, path, resolution):
        self.resolution = resolution
        self.path = path
        self.rectangles = []
        self.saved = False

    def get_next_class(self):
        ret = 0
        for rect in self.rectangles:
            if rect['class'] > ret:
                ret = rect['class']
        return ret + 1


class Core():
    def __init__(self, filewriter):
        self.COLORS = ('red', 'blue', 'green', 'yellow', 'cyan', 'goldenrod', 'coral', 'brown', 'IndianRed4', 'orchid', 'black',
        'pink', 'azure4', 'orange', 'orange4', 'pink4', 'IndianRed1', 'chartreuse4', 'chocolate')
        self.IMAGE_RESOLUTION = (1200, 700)
        self.filewriter = filewriter
        self.curr_img = None
        self.curr_img_index = None
        self.images = []
        self.curr_rect_holder = None
        self.curr_rect_pt = None
        self.creating_rect = False
        self.class_index = None
        self.curr_rect_index = None
        self.bar_rects = []
        self.bar_texts = []
        self.image_x = None
        self.image_y = None
        self.im_path = None
        self.out_path = None
        self.ratio = None

        self.root = tk.Tk()
        self.FONT = font.Font(family="Helvetica", size=30, weight="bold")
        self.FONT2 = font.Font(family="Helvetica", size=16)
        self.canvas = tk.Canvas(self.root, height=self.IMAGE_RESOLUTION[1], width=self.IMAGE_RESOLUTION[0])
        self.bar = tk.Canvas(self.root, height=int(self.IMAGE_RESOLUTION[1] / 8), width=self.IMAGE_RESOLUTION[0], bg='white')

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(expand=1, side=tk.TOP, fill=tk.X)
        tk.Button(self.top_frame, text='    INPUT    ', command=self.input_dialog).pack(side=tk.LEFT)
        self.input_entry = tk.Entry(self.top_frame)
        self.input_entry.pack(fill=tk.X, side=tk.RIGHT, expand=1)
        self.input_entry.config(state='readonly')

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(expand=1, side=tk.TOP, fill=tk.X)
        tk.Button(self.top_frame, text='    OUTPUT    ', command=self.output_dialog).pack(side=tk.LEFT)
        self.output_entry = tk.Entry(self.top_frame)
        self.output_entry.pack(fill=tk.X, side=tk.RIGHT, expand=1)
        self.output_entry.config(state='readonly')

        self.text = tk.Label(self.root, text='0/0', font=self.FONT2)
        self.text.pack(expand=1, side=tk.TOP, fill=tk.X)

        self.root.bind('<Left>', self.leftKey)
        self.root.bind('<Right>', self.rightKey)
        self.root.bind('<Up>', self.upKey)
        self.root.bind('<Down>', self.downKey)
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Motion>", self.motion)
        self.canvas.bind('<Button-3>', self.write_file)
        self.bar.bind('<Button-1>', self.bar_click)
        self.bar.bind('<Button-3>', self.bar_delete)

        self.root.mainloop()

    def resize_image(self, image):
        image.resolution = self.IMAGE_RESOLUTION
        self.ratio = max(image.size[0] / image.resolution[0], image.size[1] / image.resolution[1])
        ret_x = int(round(image.size[0] / self.ratio))
        ret_y = int(round(image.size[1] / self.ratio))
        self.image_x = (int(round(image.resolution[0] / 2 - ret_x / 2)), int(round(image.resolution[0] / 2 + ret_x / 2)))
        self.image_y = (int(round(image.resolution[1] / 2 - ret_y / 2)), int(round(image.resolution[1] / 2 + ret_y / 2)))
        image = image.resize((ret_x, ret_y), Image.ANTIALIAS)
        return image

    def show_image(self, path):
        # clear:
        self.canvas.delete("all")
        self.bar.delete("all")
        # open image
        image = Image.open(path)
        image = self.resize_image(image)
        photo = ImageTk.PhotoImage(image)
        self.curr_img = photo
        item = self.canvas.create_image(int(self.IMAGE_RESOLUTION[0] / 2), int(self.IMAGE_RESOLUTION[1] / 2), image=photo)
        # create rectangles
        self.curr_rect_index = None
        i = 0
        for rect in self.images[self.curr_img_index].rectangles:
            self.images[self.curr_img_index].rectangles[i]['holder'] = self.canvas.create_rectangle(rect['position'],
                                                width=2, outline=self.COLORS[(rect['class'] - 1) % len(self.COLORS)])
            i += 1
        # update bar
        self.init_bar()
        self.update_bar()
        # apply
        self.canvas.pack(side='top', expand=True, fill='both')
        self.bar.pack(side='bottom', expand=True, fill='both')
        self.text.config(text=(str(self.curr_img_index+1) + '/' + str(len(self.images))))
        return item

    def iterate_files(self, folder_path):
        directory = os.fsencode(folder_path)
        ret = []

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            file_path = os.path.join(folder_path, filename)

            try:
                image = Image.open(file_path)
                yield image.size, file_path
            except:
                OSError


    def leftKey(self, event):
        if self.curr_img_index is not None:
            self.curr_img_index -= 1
        if self.curr_img_index >= len(self.images):
            self.curr_img_index = 0
        self.show_image(self.images[self.curr_img_index].path)
        self.curr_rect_index = None

    def rightKey(self, event):
        if self.curr_img_index is not None:
            self.curr_img_index += 1
        if self.curr_img_index >= len(self.images):
            self.curr_img_index = 0
        self.show_image(self.images[self.curr_img_index].path)
        self.curr_rect_index = None

    def upKey(self, event):
        if self.curr_rect_index is not None:
            self.images[self.curr_img_index].rectangles[self.curr_rect_index]['class'] += 1
            holder = self.images[self.curr_img_index].rectangles[self.curr_rect_index]['holder']
            self.canvas.itemconfig(holder, outline=self.COLORS[
                (self.images[self.curr_img_index].rectangles[self.curr_rect_index]['class'] - 1) % len(
                    self.COLORS)])
            self.images[self.curr_img_index].saved = False
            self.update_bar()

    def downKey(self, event):
        if self.curr_rect_index is not None and self.images[self.curr_img_index].rectangles[self.curr_rect_index][
                'class'] > 1:
            self.images[self.curr_img_index].rectangles[self.curr_rect_index]['class'] -= 1
            holder = self.images[self.curr_img_index].rectangles[self.curr_rect_index]['holder']
            self.canvas.itemconfig(holder, outline=self.COLORS[
                (self.images[self.curr_img_index].rectangles[self.curr_rect_index]['class'] - 1) % len(
                    self.COLORS)])
            self.images[self.curr_img_index].saved = False
            self.update_bar()

    def left_click(self, event):
        if not self.creating_rect:
            if self.image_x[0] < event.x < self.image_x[1] and self.image_y[0] < event.y < self.image_x[1]:
                self.curr_rect_pt = (event.x, event.y)
                self.class_index = self.images[self.curr_img_index].get_next_class()
                self.curr_rect_holder = self.canvas.create_rectangle(*self.curr_rect_pt, self.curr_rect_pt[0] + 2,
                                                                self.curr_rect_pt[1] + 2,
                                                                width=2, outline=self.COLORS[
                        (self.class_index - 1) % len(self.COLORS)])
                self.creating_rect = True
        else:
            self.images[self.curr_img_index].rectangles.append({'class': self.class_index,
                                                                'position': self.canvas.coords(self.curr_rect_holder),
                                                                'holder': self.curr_rect_holder})
            self.creating_rect = False
            self.curr_rect_holder = False
            self.curr_rect_index = len(self.images[self.curr_img_index].rectangles) - 1
            self.images[self.curr_img_index].saved = False
            self.update_bar()

    def motion(self, event):
        if self.creating_rect and self.image_x[0] <= event.x <= self.image_x[1] and self.image_y[0] < event.y < \
                self.image_x[1]:
            pt = (event.x, event.y)
            if self.curr_rect_pt[0] > pt[0]:
                self.canvas.coords(self.curr_rect_holder, *pt, *self.curr_rect_pt)
            else:
                self.canvas.coords(self.curr_rect_holder, *self.curr_rect_pt, *pt)

    def update_bar(self):
        if self.images[self.curr_img_index].saved:
            self.bar.configure(background='green')
        else:
            self.bar.configure(background='white')
        for i in range(len(self.images[self.curr_img_index].rectangles)):
            rec = self.images[self.curr_img_index].rectangles[i]
            index = rec['class']
            color = self.COLORS[(index - 1) % len(self.COLORS)]
            self.bar.itemconfig(self.bar_rects[i], outline=color, fill=color)
            self.bar.itemconfig(self.bar_texts[i], fill='white', text=str(index), anchor='center', font=self.FONT)

    def bar_click(self, event):
        width = int(self.IMAGE_RESOLUTION[0] / 10) - 2
        index = int((event.x - 10) / width)
        if index < len(self.images[self.curr_img_index].rectangles):
            self.curr_rect_index = index

    def bar_delete(self, event):
        width = int(self.IMAGE_RESOLUTION[0] / 10) - 2
        index = int((event.x - 10) / width)
        if index < len(self.images[self.curr_img_index].rectangles):
            self.curr_rect_index = None
            holder = self.images[self.curr_img_index].rectangles[index]['holder']
            self.images[self.curr_img_index].rectangles.pop(index)
            self.canvas.delete(holder)
            self.images[self.curr_img_index].saved = False
            self.bar.delete("all")
            self.init_bar()
            self.update_bar()

    def init_bar(self):
        self.bar_rects.clear()
        self.bar_texts.clear()
        width = int(self.IMAGE_RESOLUTION[0] / 10) - 2
        height = int(self.IMAGE_RESOLUTION[1] / 8) - 10
        for i in range(10):
            r = self.bar.create_rectangle(i * width + 10, 10, (i + 1) * width + 10, height, outline='white', fill='white')
            t = self.bar.create_text(i * width + 10 + int(width / 2), 5 + int(height / 2), fill='white', text=str('X'),
                                anchor='center', font=self.FONT)
            self.bar_rects.append(r)
            self.bar_texts.append(t)

    def input_dialog(self):
        dirname = filedialog.askdirectory(title="Specify input directory")
        self.im_path = dirname
        self.input_entry.config(state='normal')
        self.input_entry.delete(first=0, last=tk.END)
        self.input_entry.insert(0, str(self.im_path))
        self.input_entry.config(state='readonly')
        print(self.iterate_files(self.im_path))
        for resolution, path in self.iterate_files(self.im_path):
            self.images.append(ImageProperty(path, resolution))
        if len(self.images) > 0:
            self.curr_img_index = 0
            self.show_image(self.images[0].path)

    def output_dialog(self):
        dirname = filedialog.askdirectory(title="Specify output directory")
        self.out_path = dirname
        self.output_entry.config(state='normal')
        self.output_entry.delete(first=0, last=tk.END)
        self.output_entry.insert(0, str(self.out_path))
        self.output_entry.config(state='readonly')

    def write_file(self, event):
        image = self.images[self.curr_img_index]
        res = tuple(image.resolution)
        i = 0
        diffx = self.image_x[0]
        diffy = self.image_y[0]
        if self.out_path is None:
            messagebox.showwarning(
                "Saving",
                "You must specify output path first!\n"
            )
            return
        for rec in image.rectangles:
            lt = (int((rec['position'][0] - diffx) * self.ratio), int((rec['position'][1] - diffy) * self.ratio))
            rb = [int((rec['position'][2] - diffx) * self.ratio) - 1, int((rec['position'][3] - diffy) * self.ratio) - 1]
            if rb[0] >= res[0]:
                rb[0] = res[0] - 1
            if rb[1] >= res[1]:
                rb[1] = res[1] - 1
            self.filewriter.write_line(res,
                                       rec['class'],
                                       lt,
                                       tuple(rb),
                                       str(os.path.basename(image.path)),
                                       str(self.out_path),
                                       i == 0)
            i += 1
        self.images[self.curr_img_index].saved = True
        self.update_bar()
