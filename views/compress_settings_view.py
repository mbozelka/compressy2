import wx
from views.dnd_view import DnDView

class CompressSettingsView(wx.Panel):
    def __init__(self, parent):
        super(CompressSettingsView, self).__init__(parent)

        # Drag and Drop view
        self.dnd_panel = DnDView(self)

        # Files selected view
        self.files_count_text = wx.StaticText(self, label='', style=wx.ST_ELLIPSIZE_END)
        self.clear_files_btn = wx.Button(self, label='Clear')

        # directory selecrtor
        self.selected_folder_text = wx.StaticText(self, label='', style=wx.ST_ELLIPSIZE_END)
        self.select_dir_btn = wx.Button(self, label='Select')
        
        # kb controlls
        self.kb_slider = wx.Slider(self, value=500, minValue=1, maxValue=1000)
        self.kb_text = wx.StaticText(self, label='')
        self.kb_select = wx.RadioButton(self, label='')

        # percent controlls
        self.percent_slider = wx.Slider(self, value=50, minValue=1, maxValue=99)
        self.percent_text = wx.StaticText(self, label='')
        self.percent_select = wx.RadioButton(self, label='')

        # submit button
        self.compress_btn = wx.Button(self, label='Compress')

        # define the layout
        self._set_layout()

        #events
        self.Bind(wx.EVT_SLIDER, self._on_slider_upatde)
        self.Bind(wx.EVT_RADIOBUTTON, self._on_slider_selection)
        self.Bind(wx.EVT_BUTTON, self._on_press)

    def _on_slider_upatde(self, event):
        event.Skip()

    def _on_slider_selection(self, event):
        event.Skip()

    def _on_press(self, event):
        event.Skip()

    def _set_layout(self):
        main = wx.BoxSizer(wx.VERTICAL)
        
        #file drop
        dndRow = wx.BoxSizer(wx.HORIZONTAL)
        dndRow.Add(self.dnd_panel, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        
        # file count
        fileCountRow = wx.BoxSizer(wx.HORIZONTAL)
        fileCountRow.Add(self.files_count_text, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        fileCountRow.Add(self.clear_files_btn, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)

        # directory selector layout
        dirRow = wx.BoxSizer(wx.HORIZONTAL)
        dirRow.Add(self.selected_folder_text, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        dirRow.Add(self.select_dir_btn, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)

        # kb controll layout
        kbRow = wx.BoxSizer(wx.HORIZONTAL)
        kbRow.Add(self.kb_select, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        kbRow.Add(self.kb_slider, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        kbRow.Add(self.kb_text, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)

        # percent controll layout
        percentRow = wx.BoxSizer(wx.HORIZONTAL)
        percentRow.Add(self.percent_select, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        percentRow.Add(self.percent_slider, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        percentRow.Add(self.percent_text, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)

        # percent controll layout
        compressRow = wx.BoxSizer(wx.HORIZONTAL)
        compressRow.Add(self.compress_btn, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)

        main.Add(dndRow, 0, wx.EXPAND|wx.ALL, 5)
        main.Add(fileCountRow, 0, wx.EXPAND|wx.ALL, 5)
        main.Add(dirRow, 0, wx.EXPAND|wx.ALL, 5)
        main.Add(percentRow, 0, wx.EXPAND|wx.ALL, 5)
        main.Add(kbRow, 0, wx.EXPAND|wx.ALL, 5)
        main.Add(compressRow, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(main)