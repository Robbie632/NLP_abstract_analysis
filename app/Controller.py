import wx
from Landing import Landing
from Base import Base


class Controller(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)


        dims = wx.Display().GetClientArea()
        self.screenWidth = dims[2]
        self.screenHeight = dims[3]
      
        #instantiate a wx.Panel subclass
        basePanel = Base(self, id=-1, 
                         pos=wx.DefaultPosition, 
                         size = wx.Size(self.screenWidth, self.screenHeight ))
        
        basePanel.SetBackgroundColour("green")

        #pass basePanel to Landing class as wxpython parent
        self.landing = Landing(basePanel)

        self.landing.Bind(wx.EVT_CLOSE, self.onClose)

    def onClose(self, event):

      self.basePanel.Destroy()
      self.landing.Destroy()
      self.Destroy()

        
    def OnCloseWindow(self, e):
        self.Destroy()
