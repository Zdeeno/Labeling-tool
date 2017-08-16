import os


class FileWriter:

    def write_line(self, resolution, label_index, lt, rb, image_name, output_path, is_new_file):
        '''
        method writing line into output file
        :param resolution: (x, y) number of pixels
        :param label_index: int from 1
        :param lt: left top corner coordinates of bounding box (coordinates indexed from 0 to resolution - 1)
        :param rb: right bottom corner coordinates of bounding box (coordinates indexed from 0 to resolution - 1)
        :param image_name: string - name of image file
        :param output_path: string - absolute output folder path
        :param is_new_file: boolean - True if current line is first in text file
        :return: None
        '''
        raise NotImplementedError("Should have implemented this")


class FileWriterDebug(FileWriter):

    def write_line(self, resolution, label_index, lt, rb, image_name, output_path, is_new_file):
        base = os.path.splitext(image_name)[0]
        name = base + '.txt'
        if is_new_file:
            f = open(os.path.join(output_path, name), 'w')
        else:
            f = open(os.path.join(output_path, name), 'a')
        line = str(label_index) + ' ' + str(resolution) + ' ' + str(lt) + ' ' + str(rb) + '\n'
        f.write(line)


class FileWriterYolo(FileWriter):

    def write_line(self, resolution, label_index, lt, rb, image_name, output_path, is_new_file):
        base = os.path.splitext(image_name)[0]
        name = base + '.txt'

        my_lt = (lt[0] + 1, lt[1] + 1)
        my_rb = (rb[0] + 1, rb[1] + 1)
        center = ((my_rb[0] + my_lt[0])/2, (my_rb[1] + my_lt[1])/2)
        size = (my_rb[0] - my_lt[0], my_rb[1] - my_lt[1])

        if is_new_file:
            f = open(os.path.join(output_path, name), 'w')
        else:
            f = open(os.path.join(output_path, name), 'a')
        line = str(label_index-1) + ' ' + str(str.format("{0:.6f}", center[0]/resolution[0])) + ' ' + str(str.format("{0:.6f}", center[1]/resolution[1])) + ' ' + \
            str(str.format("{0:.6f}", size[0]/resolution[0])) + ' ' + str(str.format("{0:.6f}", size[1]/resolution[1])) + '\n'
        f.write(line)


class FileWriterCustom(FileWriter):

    def write_line(self, resolution, label_index, lt, rb, image_name, output_path, is_new_file):
        '''
        Here you can implement your own writer
        '''
        super(FileWriterCustom, self).write_line(resolution, label_index, lt, rb, image_name, output_path, is_new_file)
