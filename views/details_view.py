import os
import wx

class DetailsView(wx.ScrolledWindow):
    def __init__(self, parent):
        super(DetailsView, self).__init__(parent)

    def set_layout(self, files, output_dir):

        self.SetScrollbars(1, 1, 1000, 1000)
        main = wx.BoxSizer(wx.VERTICAL)
        status_set = []

        for f in files:
            dir_path, file_name = os.path.split(f)
            _status = wx.StaticText(self, label='Waiting...')
            _path = wx.StaticText(self, label=output_dir + '/' + file_name)
            row = wx.BoxSizer(wx.HORIZONTAL)
            row.Add(_status, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)
            row.Add(_path, 1, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)
            main.Add(row, flag=wx.LEFT)
            status_set.append(_status)

        self.SetSizer(main)

        return status_set