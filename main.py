import wx
from frames.main_frame import MainFrame

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