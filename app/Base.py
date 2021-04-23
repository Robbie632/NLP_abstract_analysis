import wx

class Base(wx.Panel):
  """
  This panel class is for all other panels to be placed ontop of 
  """

  def __init__(self, parent, id, pos, size):

    wx.Panel.__init__(self, parent, id, pos, size)

    input_text = wx.TextCtrl(self, value="key_words")

    #this bit is not successfully binding
    input_text.Bind(wx.EVT_TEXT_ENTER, self.OnSubmit)


  def OnSubmit(self, event):

    print("do stuff")