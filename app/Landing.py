import wx

from Base import Base


class Landing(wx.Frame):

  """
  Superclass of wx.Frame 
  """

  def __init__(self, parent):


      wx.Frame.__init__(self, parent, -1, "Annotator", size=(800,600),
                        style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
      self.parent = parent
      dims = wx.Display().GetClientArea()
      self.screenWidth = dims[2]
      self.screenHeight = dims[3]



      

  


