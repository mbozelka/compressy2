import wx

def alert(msg, title):
    style = wx.OK|wx.CENTER|wx.ICON_INFORMATION
    wx.MessageBox(msg, title, style)