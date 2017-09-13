import wx
import os
from utils.alert import alert

class DropZone(wx.FileDropTarget):
    def __init__(self, cb):
        super(DropZone, self).__init__()
        self.target_list = []
        self.cb = cb

    def OnDropFiles(self, x, y, entry_list):
        _dups = []

        for entry in entry_list:
            try:
                if os.path.isdir(entry):
                    f_list = os.listdir(entry)
                    
                    for f in f_list:
                        full_path = entry + '/' + f
                        if self._is_dup(full_path):
                            _dups.append(full_path)
                        elif self._isImage(full_path) and not os.path.isdir(full_path):
                            self.target_list.append(full_path)

                else:
                    if self._is_dup(entry):
                        _dups.append(entry)
                    elif self._isImage(entry):
                        self.target_list.append(entry)

            except  Exception as e:
                self.clear_target_list()
        
        file_length = len(self.target_list)
        if file_length > 0:
            alert(str(file_length) + ' files ready to be compressed.', 'Files Added')
        self.cb()
        return True

    def _isImage(self, file_path):
        return os.path.splitext(file_path)[1].lower() in ['.jpg', '.png']

    def _is_dup(self, _path):
        return _path in self.target_list

    def clear_target_list(self):
        self.target_list = []

    def get_target_list(self):
        return self.target_list