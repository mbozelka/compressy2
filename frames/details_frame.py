import wx
import os
from views.details_view import DetailsView
from utils.imagecompressthread import ImageCompressThread
from utils.create_folder import create_folder

class DetailsFrame(wx.Frame):
    def __init__(self, parent, title, files, output_dir, quality, mode):
        super(DetailsFrame, self).__init__(parent, title=title)
        self._files = files
        self._output_dir = output_dir
        self._quality = quality
        self._compress_mode = mode
        self.status_set = []

        # Set Details View
        self.details_view = DetailsView(self)
        self.status_set = self.details_view.set_layout(self._files, output_dir)

    def compress(self):
        file_count = len(self._files)

        for i in range(0, file_count):
            output = self._get_output_folder(self._files[i])
            ic_thread = ImageCompressThread(thread_num=i, image_path=self._files[i], output_dir=output, 
                mode_quality=self._quality, mode=self._compress_mode, notify_func=self._update_status)
            ic_thread.start()

    def _update_status(self, index, msg):
        self.status_set[index].SetLabel(msg)

    def _get_output_folder(self, file):
        if self._output_dir:
            return self._output_dir
        
        dir_path, file_name = os.path.split(file)
        output = dir_path + '/optimized'
        create_folder(output)
        return output