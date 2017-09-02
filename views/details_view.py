
import wx

class DetailsView(wx.ScrolledWindow):
    def __init__(self, parent):
        super(DetailsView, self).__init__(parent)

    def set_layout(self, files):

        self.SetScrollbars(1, 1, 1000, 1000)
        main = wx.BoxSizer(wx.VERTICAL)
        status_set = []

        for f in files:
            _status = wx.StaticText(self, label='Waiting...')
            _path = wx.StaticText(self, label=f)
            row = wx.BoxSizer(wx.HORIZONTAL)
            row.Add(_status, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)
            row.Add(_path, 1, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)
            main.Add(row, flag=wx.LEFT)
            status_set.append(_status)

        self.SetSizer(main)

        return status_set