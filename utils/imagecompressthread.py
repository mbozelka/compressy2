
import os
import threading
from PIL import Image
from utils.binary_quality_search import binary_quality_search
from utils.compressmodeenum import CM_ENUM


class ImageCompressThread(threading.Thread):

    compress_mode_enum = CM_ENUM

    def __init__(self, thread_num, image_path, output_dir, mode_quality, mode, notify_func):
        super(ImageCompressThread, self).__init__()
        self.image_path = image_path
        self.output_dir = output_dir
        self.mode_quality = mode_quality
        self.mode = mode
        self.notify_func = notify_func
        self.thread_num = thread_num

    def run (self):
        self._compress_image()

    def _compress_image(self):
        
        self.notify_func(index=self.thread_num, msg='0%')

        try:
            dir_path, file_name = os.path.split(self.image_path)
            output = self.output_dir + '/' + file_name
            quality = self.mode_quality
            format = self._map_format(self.image_path)
            im = Image.open(self.image_path)
            
            if format == 'JPEG':
                # convert current size to kb
                curr_size = os.stat(self.image_path).st_size / 1000
                target_size = quality

                if self.mode == self.compress_mode_enum['PERCENT']:
                    # Pil does not always save percentages to what is expected.
                    # To ensure the quality difference is exactly what is wanted
                    # the size difference is found in KB. Then _get_best_quality
                    # will find the true quality to save at.
                    target_size = curr_size * (quality / 100)
            
                
                # size is already smaller than
                # requested size, so just move
                # to output folder
                if target_size >= curr_size:
                    im.save(output, format=format, optimize=True)
                else:
                    # find the best quality to meet the requirements
                    target_size = self._get_best_quality(self.image_path, self.output_dir, target_size)
                    im.save(output, format=format, quality=target_size, optimize=True)

            else:
                # compressing a PNG
                # always run it through the optimizer
                im.save(output, format=format, optimize=True)

            self.notify_func(index=self.thread_num, msg='Done')

        except Exception as e:
            self.notify_func(index=self.thread_num, msg='Error')


    def _map_format(self, image_path):
        formats = {
            '.jpg' : 'JPEG',
            '.png' : 'PNG'
        }
        ext = os.path.splitext(image_path)[1].lower()
        return formats[ext]

    def _get_best_quality(self, image_path, output_dir, quality):
        return binary_quality_search(image_path, output_dir, quality, self._binary_search_callback)

    def _binary_search_callback(self, percent_done):
        self.notify_func(index=self.thread_num, msg=percent_done)