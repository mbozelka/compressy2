
import wx

class DnDView(wx.Panel):
    def __init__(self, parent):
        super(DnDView, self).__init__(parent)
        self.SetBackgroundColour('white')
        self._label = wx.StaticText(self, label='Drag-N-Drop')
        self._set_layout()

    def _set_layout(self):
        main = wx.BoxSizer(wx.VERTICAL)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(0, 250, 0)
        row.Add(self._label, 0, wx.CENTER|wx.ALIGN_CENTER_VERTICAL)
        main.Add(row, flag=wx.CENTER)
        self.SetSizer(main)