import wx
import numpy as np
import pandas as pd
import statsmodels.stats.multicomp as ml


class GenericClass(wx.Frame):
    def __init__(self, parent, dataframe, title, notebook, pages, data):
        '''
        the sole purpose of this class is to create a base for every
        selection window

        parent is the father window, My_Frame object
        dataframe the data to run test
        title is the title of window
        notebook is the object that holds Sheets objects
        pages is the page from the notebook, object type Sheet
        data is the entirely file
        '''
        wx.Frame.__init__(self, parent, wx.ID_ANY, title=title)
        self.dataframe = dataframe
        self.notebook = notebook
        self.pages = pages
        self.data = data

        self.panel = wx.Panel(self, wx.ID_ANY)  # on the panel you draw
        self.column_list = list(dataframe.columns.values)
        self.dataframe0 = pd.DataFrame()
        self.hold0 = ""  # hold0 holds what combobox0 has selected

        self.title = wx.StaticText(self.panel, wx.ID_ANY, "")
        self.info = wx.StaticText(self.panel, wx.ID_ANY, "")

        self.ok = wx.Button(self.panel, wx.ID_ANY, "OK")
        self.Bind(wx.EVT_BUTTON, self.onOk, self.ok)

        self.close = wx.Button(self.panel, wx.ID_ANY, "CLOSE")
        self.Bind(wx.EVT_BUTTON, self.onClose, self.close)

        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.info_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.combo_sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        self.combo_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.close_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.title_sizer.Add(self.title, 0, wx.ALIGN_LEFT, 5)
        self.info_sizer.Add(self.info, 0, wx.LEFT, 5)

    '''
    All of the functions with create, set and add have the purpose to allow
    the creation of different windows for selecting data
    The create functions are creating an object
    The add functions are setting the object in UI
    The set functions are setting out atributes
    The on functions are event handeling events
    '''
    def create_combobox0(self):
        '''
        creates the first combo box and everything to make it usable
        '''
        self.combobox0 = wx.ComboBox(self.panel, id=wx.ID_ANY,
                                     choices=self.column_list,
                                     style=wx.CB_READONLY | wx.CB_SORT)
        self.Bind(wx.EVT_COMBOBOX, self.onSelection0, self.combobox0)
        self.combo_sizer0.Add(self.combobox0, 0,
                              wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL,
                              5)

    def create_combobox1(self):
        '''
        creates the second combo box and everything to make it usable
        '''
        self.combobox1 = wx.ComboBox(self.panel, id=wx.ID_ANY,
                                     choices=self.column_list,
                                     style=wx.CB_READONLY | wx.CB_SORT)
        self.Bind(wx.EVT_COMBOBOX, self.onSelection1, self.combobox1)
        self.combo_sizer1.Add(self.combobox1, 0,
                              wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL,
                              5)

    def add_button_sizer_all_data(self):
        '''
        this functions is when you want to run something on all of the data
        '''
        self.big_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.add_close_button()
        self.add_ok_button()
        self.big_horizontal_sizer.Add(self.close_sizer, 0, wx.ALIGN_LEFT, 5)
        self.big_horizontal_sizer.Add(self.ok_sizer, 0, wx.ALIGN_RIGHT, 5)

    def add_ok_button(self):
        self.ok_sizer.Add(self.ok, 0, wx.RIGHT, 5)

    def add_close_button(self):
        self.close_sizer.Add(self.close, 0, wx.RIGHT, 5)

    def set_title(self, title_str):
        self.title.SetLabelText(title_str)

    def set_info(self, info_str):
        self.info.SetLabelText(info_str)

    def set_text_sizers(self):
        self.panel_sizer.Add(self.title_sizer, 0, wx.ALIGN_LEFT, 5)
        self.panel_sizer.Add(wx.StaticLine(self.panel,),
                             0, wx.ALL | wx.EXPAND, 5)
        self.panel_sizer.Add(self.info_sizer, 0, wx.ALIGN_LEFT, 5)

    def set_combobox0_sizer(self):
        self.panel_sizer.Add(self.combo_sizer0, 0, wx.LEFT, 5)

    def set_combobox1_sizer(self):
        self.panel_sizer.Add(self.combo_sizer1, 0, wx.LEFT, 5)

    def set_ok_sizer(self):
        self.panel_sizer.Add(self.ok_sizer, 0, wx.CENTER, 5)

    def set_close_sizer(self):
        self.panel_sizer.Add(self.close_sizer, 0, wx.CENTER, 5)

    def set_button_sizer_all_data(self):
        self.panel_sizer.Add(wx.StaticLine(self.panel,), 0,
                             wx.ALL | wx.EXPAND, 5)
        self.panel_sizer.Add(self.big_horizontal_sizer,
                             0, wx.ALIGN_CENTER_HORIZONTAL, 5)

    def find_sheet(self, name):
        # finds the sheet with name as a name
        # returns if it find it and the position of the sheet
        # this function cam be improve
        num = 0
        for i in self.pages:
            if i.return_name() == name:
                return(True, num)
            num += 1
        return(False, 0)  # the 0 is a place holder for avoiding compiler error

    def run_Tukey(self, t, name_list, z):
        # Run tukey for data at t,
        # the name_list is the naming of the columns
        # z is the score to run Tukey
        total_list = []
        total_list2 = []
        for i, j in zip(t, name_list):
            total_list = np.concatenate((total_list,
                                         np.reshape(i, len(i))))
            total_list2.extend([j]*len(i))

        num_array = np.asarray(total_list)
        symbol_group = np.asarray(total_list2)
        di = {'Score': num_array, 'Group': symbol_group}
        middle_frame = pd.DataFrame(di)
        mcobj = ml.MultiComparison(pd.to_numeric(middle_frame.Score,
                                                 errors="ignore"),
                                   middle_frame.Group)
        out = mcobj.tukeyhsd(z)
        return out

    def onOk(self, e):
        pass

    def onClose(self, e):
        self.Close()

    def onSelection0(self, e):
        pass

    def onSelection1(self, e):
        pass
