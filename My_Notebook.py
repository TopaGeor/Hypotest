import wx


class My_Notebook(wx.Notebook):
    '''
    This class creates pages so we can draw the sheets into them
    The parent is a wx Frame object where the pages will be shown
    '''
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.NB_BOTTOM)
        self.page = 0  # The current page
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onPageChanged)

    def onPageChanged(self, event):
        self.page = self.GetSelection()
        event.Skip()
