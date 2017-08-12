import os


class Filewriter_debug():

    def write_line(self, resolution, label_index, lt, rb, image_name, output_path, is_new_file):
        base = os.path.splitext(image_name)[0]
        name = base + '.txt'

        if is_new_file:
            f = open(os.path.join(output_path, name), 'w')
        else:
            f = open(os.path.join(output_path, name), 'a')
        line = str(label_index) + ' ' + str(resolution) + ' ' + str(lt) + ' ' + str(rb)
        f.write(line)
