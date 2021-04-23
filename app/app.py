
import wx
from multiprocessing import Process
from Controller import Controller


class Start:

  """
  Class for starting app
  """

  def __init__(self):
    pass

  def runApp(self):

    """
    runs app
    """

    app = wx.App()

    frame = Controller(None, "test")
    frame.Show(True)
    
    frame.Maximize()
    app.MainLoop()


if __name__=="__main__":
  app = Start()
  app.runApp()
    
