import wx
import wx.lib.platebtn as platebtn
import os
from utils.dropzone import DropZone
from utils.defaultmessagesenum import DEFAULT_MESSAGES
from utils.compressmodeenum import CM_ENUM
from utils.imagecompressthread import ImageCompressThread
from utils.alert import alert


class DnDPanel(wx.Panel):
    def __init__(self, parent):
        super(DnDPanel, self).__init__(parent)
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



class CompressSettingsView(wx.Panel):
    def __init__(self, parent):
        super(CompressSettingsView, self).__init__(parent)

        # Drag and Drop view
        self._dnd_panel = DnDPanel(self)

        # Files selected view
        self._files_count_text = wx.StaticText(self, label='', style=wx.ST_ELLIPSIZE_END)
        self._clear_files_btn = wx.Button(self, label='Clear')

        # directory selecrtor
        self._selected_folder_text = wx.StaticText(self, label='', style=wx.ST_ELLIPSIZE_END)
        self._select_dir_btn = wx.Button(self, label='Select')
        
        # kb controlls
        self._kb_slider = wx.Slider(self, value=500, minValue=1, maxValue=1000)
        self._kb_text = wx.StaticText(self, label='')
        self._kb_select = wx.RadioButton(self, label='')

        # percent controlls
        self._percent_slider = wx.Slider(self, value=50, minValue=1, maxValue=99)
        self._percent_text = wx.StaticText(self, label='')
        self._percent_select = wx.RadioButton(self, label='')

        # submit button
        self._compress_btn = wx.Button(self, label='Compress')

        # register components back to the controll
        parent.register_components(
            dnd_panel=self._dnd_panel,
            files_count_text=self._files_count_text,
            selected_folder_text=self._selected_folder_text,
            kb_slider=self._kb_slider,
            kb_select=self._kb_select,
            kb_text=self._kb_text,
            percent_slider=self._percent_slider,
            percent_select=self._percent_select,
            percent_text=self._percent_text,
            clear_files_btn=self._clear_files_btn,
            select_dir_btn=self._select_dir_btn,
            compress_btn=self._compress_btn
        )

        # define the layout
        self._set_layout()


    def _set_layout(self):
        main = wx.BoxSizer(wx.VERTICAL)
        
        #file drop
        dndRow = wx.BoxSizer(wx.HORIZONTAL)
        dndRow.Add(self._dnd_panel, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        
        # file count
        fileCountRow = wx.BoxSizer(wx.HORIZONTAL)
        fileCountRow.Add(self._files_count_text, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        fileCountRow.Add(self._clear_files_btn, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)

        # directory selector layout
        dirRow = wx.BoxSizer(wx.HORIZONTAL)
        dirRow.Add(self._selected_folder_text, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        dirRow.Add(self._select_dir_btn, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)

        # kb controll layout
        kbRow = wx.BoxSizer(wx.HORIZONTAL)
        kbRow.Add(self._kb_select, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        kbRow.Add(self._kb_slider, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        kbRow.Add(self._kb_text, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)

        # percent controll layout
        percentRow = wx.BoxSizer(wx.HORIZONTAL)
        percentRow.Add(self._percent_select, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        percentRow.Add(self._percent_slider, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        percentRow.Add(self._percent_text, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)

        # percent controll layout
        compressRow = wx.BoxSizer(wx.HORIZONTAL)
        compressRow.Add(self._compress_btn, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)

        main.Add(dndRow, 0, wx.EXPAND|wx.ALL, 5)
        main.Add(fileCountRow, 0, wx.EXPAND|wx.ALL, 5)
        main.Add(dirRow, 0, wx.EXPAND|wx.ALL, 5)
        main.Add(percentRow, 0, wx.EXPAND|wx.ALL, 5)
        main.Add(kbRow, 0, wx.EXPAND|wx.ALL, 5)
        main.Add(compressRow, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(main)


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



class MainFrame(wx.Frame):
    def __init__(self, parent, size, title=''):
        super(MainFrame, self).__init__(parent, title=title, size=size)
        self._kb_compress_val = None
        self._percent_compress_val = None
        self._compress_mode = None
        self._output_dir = None

        # Set Main View
        CompressSettingsView(self)

        #events
        self.Bind(wx.EVT_SLIDER, self._on_slider_upatde)
        self.Bind(wx.EVT_RADIOBUTTON, self._on_slider_selection)
        self.Bind(wx.EVT_BUTTON, self._on_press)


    def register_components(self, dnd_panel, files_count_text, selected_folder_text, 
                                kb_slider, kb_text, kb_select, percent_slider, 
                                percent_select, percent_text, clear_files_btn, select_dir_btn, 
                                compress_btn):
        self._dnd_panel = dnd_panel
        self._files_count_text = files_count_text
        self._selected_folder_text = selected_folder_text
        self._kb_slider = kb_slider
        self._kb_select = kb_select
        self._kb_text = kb_text
        self._percent_slider = percent_slider
        self._percent_select = percent_select
        self._percent_text = percent_text
        self._set_initial_states()
        self._clear_files_btn = clear_files_btn
        self._select_dir_btn = select_dir_btn
        self._compress_btn = compress_btn

    def _on_press(self, event):
        btn = event.EventObject

        if btn == self._compress_btn:
            self._compress_files()

        if btn == self._clear_files_btn:
            self._dropTarget.clear_target_list()
            self._file_list_updated()

        if btn == self._select_dir_btn:
            self._select_output_dir()


    def _compress_files(self):
        files = self._dropTarget.get_target_list()
        file_count = len(files)

        if self._output_dir == None or file_count == 0:
            alert('You must drop some files and select an output folder.', 'Oops!')
            return
        
        mode_quality = self._percent_compress_val if self._compress_mode == CM_ENUM['PERCENT'] else self._kb_compress_val
        details_frame = DetailsFrame(
            self, 
            title='Output Details',
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
                self._update_output_label('Output Dir: ' + path)

        except  Exception as e:
            self._output_dir = None
            self._update_output_label('Output Dir: ' + DEFAULT_MESSAGES['OUTPUT_DIR'])



    def _on_slider_upatde(self, event):
        slider = event.EventObject
        
        if slider == self._percent_slider:
            self._percent_compress_val = slider.GetValue()
            self._update_slider_label(self._percent_slider, self._percent_text, CM_ENUM['PERCENT'])

        if slider == self._kb_slider:
            self._kb_compress_val = slider.GetValue()
            self._update_slider_label(self._kb_slider, self._kb_text, CM_ENUM['KB'])
        

    def _on_slider_selection(self, event):
        radio_btn = event.EventObject

        if radio_btn == self._kb_select:
            self._kb_slider.Enable(True)
            self._percent_slider.Enable(False)
            self._compress_mode = CM_ENUM['KB']

        elif radio_btn == self._percent_select:
            self._kb_slider.Enable(False)
            self._percent_slider.Enable(True)
            self._compress_mode = CM_ENUM['PERCENT']

    def _set_initial_states(self):
        self._selected_folder_text.SetLabel('Output Dir: ' + DEFAULT_MESSAGES['OUTPUT_DIR'])
        self._files_count_text.SetLabel('Files Count: 0')
        self._compress_mode = CM_ENUM['PERCENT']
        self._percent_compress_val = self._percent_slider.GetValue()
        self._kb_compress_val = self._kb_slider.GetValue()

        self._percent_select.SetValue(True)
        self._kb_slider.Enable(False)

        self._update_slider_label(self._percent_slider, self._percent_text, CM_ENUM['PERCENT'])
        self._update_slider_label(self._kb_slider, self._kb_text, CM_ENUM['KB'])

        # drag and drop pannel
        self._dropTarget = DropZone(self._file_list_updated)
        self._dnd_panel.SetDropTarget(self._dropTarget)

    def _update_slider_label(self, slider, label, symbol):
        val = str(slider.GetValue()) + symbol
        label.SetLabel(val)

    def _update_output_label(self, path):
        self._selected_folder_text.SetLabel('Output Dir: ' + path)

    def _file_list_updated(self):
        count = len(self._dropTarget.get_target_list())
        self._files_count_text.SetLabel('Files Count: ' + str(count))



class Compressy2(wx.App):
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)
        
        # This catches events when the app is asked to activate by some other
        # process
        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)
        
    def OnInit(self):

        self.frame = MainFrame(None, size=(500, 480), title='Compressy2')
        self.frame.Show()

        return True
    
    def MacReopenApp(self):
        self.GetTopWindow().Raise()

    def BringWindowToFront(self):
        try: # it's possible for this event to come when the frame is closed
            self.GetTopWindow().Raise()
        except:
            pass
        
    def OnActivate(self, event):
        # if this is an activate event, rather than something else, like iconize.
        if event.GetActive():
            self.BringWindowToFront()



if __name__ == '__main__':
    app = Compressy2(False)
    app.MainLoop()