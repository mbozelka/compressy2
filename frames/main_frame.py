import wx
from frames.details_frame import DetailsFrame
from views.compress_settings_view  import CompressSettingsView
from utils.alert import alert
from utils.drop_zone import DropZone
from utils.defaultmessagesenum import DEFAULT_MESSAGES
from utils.compressmodeenum import CM_ENUM

class MainFrame(wx.Frame):
    def __init__(self, parent, size, title=''):
        super(MainFrame, self).__init__(parent, title=title, size=size, style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self._kb_compress_val = None
        self._percent_compress_val = None
        self._compress_mode = None
        self._output_dir = None
        self._dropTarget = DropZone(self._file_list_updated)

        # Comrpess Settings view
        self.cs_view = CompressSettingsView(self)
        self._set_initial_states()

        #events
        self.Bind(wx.EVT_SLIDER, self._on_slider_upatde)
        self.Bind(wx.EVT_RADIOBUTTON, self._on_slider_selection)
        self.Bind(wx.EVT_BUTTON, self._on_press)


    def _on_press(self, event):
        btn = event.EventObject

        if btn == self.cs_view.compress_btn:
            self._compress_files()

        if btn == self.cs_view.clear_files_btn:
            self._dropTarget.clear_target_list()
            self._file_list_updated()

        if btn == self.cs_view.select_dir_btn:
            self._select_output_dir()


    def _compress_files(self):
        files = self._dropTarget.get_target_list()
        file_count = len(files)

        if file_count == 0:
            alert('You have not dropped any files.', 'Oops!')
            return
        
        mode_quality = self._percent_compress_val if self._compress_mode == CM_ENUM['PERCENT'] else self._kb_compress_val
        details_frame = DetailsFrame(
            self, 
            title='Output Status',
            files=files, 
            output_dir=self._output_dir, 
            quality=mode_quality, 
            mode=self._compress_mode
        )
        details_frame.Show()
        details_frame.compress()
        self._dropTarget.clear_target_list()
        self._file_list_updated()    


    def _select_output_dir(self):
        dir_win = wx.DirDialog(self, message='Select Output Directory', defaultPath='')

        try:
            win_return = dir_win.ShowModal()

            if win_return == wx.ID_OK:
                path = dir_win.GetPath()
                self._output_dir = path
                self._update_output_label(path)

        except  Exception as e:
            self._output_dir = None
            self._update_output_label(DEFAULT_MESSAGES['OUTPUT_DIR'])



    def _on_slider_upatde(self, event):
        slider = event.EventObject
        
        if slider == self.cs_view.percent_slider:
            self._percent_compress_val = slider.GetValue()
            self._update_slider_label(self.cs_view.percent_slider, self.cs_view.percent_text, CM_ENUM['PERCENT'])

        if slider == self.cs_view.kb_slider:
            self._kb_compress_val = slider.GetValue()
            self._update_slider_label(self.cs_view.kb_slider, self.cs_view.kb_text, CM_ENUM['KB'])
        

    def _on_slider_selection(self, event):
        radio_btn = event.EventObject

        if radio_btn == self.cs_view.kb_select:
            self.cs_view.kb_slider.Enable(True)
            self.cs_view.percent_slider.Enable(False)
            self._compress_mode = CM_ENUM['KB']

        elif radio_btn == self.cs_view.percent_select:
            self.cs_view.kb_slider.Enable(False)
            self.cs_view.percent_slider.Enable(True)
            self._compress_mode = CM_ENUM['PERCENT']

    def _set_initial_states(self):
        self._update_output_label(DEFAULT_MESSAGES['OUTPUT_DIR'])
        self._file_list_updated()
        self._compress_mode = CM_ENUM['PERCENT']
        self._percent_compress_val = self.cs_view.percent_slider.GetValue()
        self._kb_compress_val = self.cs_view.kb_slider.GetValue()

        self.cs_view.percent_select.SetValue(True)
        self.cs_view.kb_slider.Enable(False)

        self._update_slider_label(self.cs_view.percent_slider, self.cs_view.percent_text, CM_ENUM['PERCENT'])
        self._update_slider_label(self.cs_view.kb_slider, self.cs_view.kb_text, CM_ENUM['KB'])

        # drag and drop pannel
        self.cs_view.dnd_panel.SetDropTarget(self._dropTarget)

    def _update_slider_label(self, slider, label, symbol):
        val = str(slider.GetValue()) + symbol
        label.SetLabel(val)

    def _update_output_label(self, path):
        self.cs_view.selected_folder_text.SetLabel('Output Dir: ' + path)

    def _file_list_updated(self):
        count = len(self._dropTarget.get_target_list())
        self.cs_view.files_count_text.SetLabel('Files Count: ' + str(count))