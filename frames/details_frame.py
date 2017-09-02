import wx
from views.details_view import DetailsView
from utils.imagecompressthread import ImageCompressThread

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
        self.status_set = self.details_view.set_layout(self._files)

    def compress(self):
        file_count = len(self._files)

        for i in range(0, file_count):

            ic_thread = ImageCompressThread(thread_num=i, image_path=self._files[i], output_dir=self._output_dir, 
                mode_quality=self._quality, mode=self._compress_mode, notify_func=self._update_status)
            ic_thread.start()

    def _update_status(self, index, msg):
        self.status_set[index].SetLabel(msg)