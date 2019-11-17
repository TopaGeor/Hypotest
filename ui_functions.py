import wx


def give_MessageDialog(parent, message, title, icon):
    """
    This creates a window that informs the user
    parent = the window that call the function
    message = text that display the window
    title = title of the window
    icon = the standard icon that
    """
    if type(message) is not str:
        raise TypeError("The message is not a string")
        return None

    if type(title) is not str:
        raise TypeError("The title is not a string")
        return None

    dlg = wx.MessageDialog(parent, message, title, icon)
    dlg.ShowModal()
    dlg.Destroy()
    return None
