import wx
import pandas as pd

from scipy import stats
from Sheet import Sheet
from GenericClass import GenericClass
from ui_functions import give_MessageDialog


class OneANOVA(GenericClass):
    def __init__(self, parent, dataframe, title, notebook, pages, data):
        '''
        This class creates the window for running One way ANOVA
        This test runs on a number of columns selecting by the user
        So window is set out to do that thing
        '''
        GenericClass.__init__(self, parent, dataframe, title, notebook,
                              pages, data)

        self.set_title("ANOVA one way")
        self.set_info("* Select as many columns you like. \t \n"
                      + "Hold down CTRL and select by left click. \t \n"
                      + "The text entry will be used for Tukey test \t \n"
                      + "and the range should be between 0 and 1 \t")

        self.create_combobox0()

        self.list = []
        self.shapiro_list = []

        self.std_string = "Currently selected columns:\n >>"
        self.selected = wx.StaticText(self.panel, wx.ID_ANY, self.std_string)
        self.selected_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.selected_sizer.Add(self.selected, 0, wx.EXPAND
                                | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.clear_last = wx.Button(self.panel, wx.ID_ANY, "CLEAR LAST")
        self.Bind(wx.EVT_BUTTON, self.onClearLast, self.clear_last)

        self.combobox0.Bind(wx.EVT_KEY_DOWN, self.onCommand)

        self.text = wx.TextCtrl(self.panel, wx.ID_ANY, value="0.05")
        self.text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text_sizer.Add(self.text, 0,
                            wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL,
                            5)

        self.clear_all = wx.Button(self.panel, wx.ID_ANY, "CLEAR ALL")
        self.Bind(wx.EVT_BUTTON, self.onClearAll, self.clear_all)

        self.clear_last_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.clear_all_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.clear_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dialog_button_sizer = wx.BoxSizer(wx.VERTICAL)
        self.all_button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.clear_last_sizer.Add(self.clear_last, 0, wx.LEFT, 5)
        self.clear_all_sizer.Add(self.clear_all, 0, wx.LEFT, 5)
        self.clear_sizer.Add(self.clear_last_sizer, 0, wx.LEFT, 5)
        self.clear_sizer.Add(self.clear_all_sizer, 0, wx.LEFT, 5)

        self.set_text_sizers()
        self.set_combobox0_sizer()
        self.panel_sizer.Add(self.selected_sizer, 0, wx.RIGHT, 5)

        # text_sizer is a variable in OneANOVA
        # while the text_sizers is a method in GenericClass
        self.panel_sizer.Add(self.text_sizer, 0, wx.RIGHT, 5)

        self.add_close_button()
        self.add_ok_button()
        self.dialog_button_sizer.Add(self.close_sizer, 0, wx.RIGHT, 5)
        self.dialog_button_sizer.Add(self.ok_sizer, 0, wx.RIGHT, 5)

        self.all_button_sizer.Add(self.clear_sizer, 0, wx.LEFT, 5)
        self.all_button_sizer.AddSpacer(10)

        self.all_button_sizer.Add(self.dialog_button_sizer, 0, wx.RIGHT, 5)

        self.panel_sizer.Add(wx.StaticLine(self.panel,), 0,
                             wx.ALL | wx.EXPAND, 5)
        self.panel_sizer.Add(self.all_button_sizer, 0,
                             wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.panel.SetSizer(self.panel_sizer)
        self.panel_sizer.Fit(self)

        self.Show()

    def onClearLast(self, e):
        # removes the last selected column
        if self.list:
            last_name = self.list.pop()
            a_list = self.combobox0.GetItems()
            a_list.append(last_name)
            self.combobox0.SetItems(a_list)
            self.selected.SetLabelText(self.std_string)
            for i in self.list:
                self.selected.SetLabelText(self.selected.GetLabelText()
                                           + i + ",")
            self.selected.SetLabelText(self.selected.GetLabelText()
                                       [:len(self.selected.GetLabelText()) - 1]
                                       + ". ")  # , -> .

    def onClearAll(self, e):
        # clears all selcted columns
        self.selected.SetLabelText(self.std_string)
        self.list = self.list + self.combobox0.GetItems()
        self.combobox0.Clear()
        self.combobox0.SetItems(self.list)
        self.list[:] = []
        self.shapiro_list[:] = []

    def onSelection0(self, e):
        '''
        When user selects a column from combobox
        '''
        new = self.combobox0.GetStringSelection()
        place = self.combobox0.GetSelection()
        self.list.append(new)
        self.selected.SetLabelText(self.std_string)
        for i in self.list:
            self.selected.SetLabelText(self.selected.GetLabelText() + i + ",")

        self.selected.SetLabelText(self.selected.GetLabelText()
                                   [:len(self.selected.GetLabelText()) - 1]
                                   + ". ")
        self.combobox0.Delete(place)

    def onCommand(self, e):
        '''
        This will keep the combobox open if the user holds the Ctrl button
        '''
        k = e.GetKeyCode()
        if (k == wx.WXK_CONTROL) and (not self.combobox0.IsListEmpty()):
            self.combobox0.Popup()

    def onOk(self, e):
        try:
            z = float(self.text.GetValue())
            error = False
        except ValueError:
            error = True

        if len(self.list) < 2:
            msg = "You need to give more than one column"
            give_MessageDialog(self, msg, "Error", wx.ICON_ERROR)
        elif error:
            msg = "A string has been detected at the text book"
            give_MessageDialog(self, msg, "Error", wx.ICON_ERROR)
        elif z <= 0:
            msg = "The number must be greater than 0"
            give_MessageDialog(self, msg, "Error", wx.ICON_ERROR)
        elif z >= 1:
            msg = "The number must be smaller than 1"
            give_MessageDialgo(self, msg, "Error", wx.ICON_ERROR)
        else:
            try:
                count = []
                mean = []
                std = []
                self.shapiro_list = []
                replace_eval = []

                for i in self.list:
                    dataframe_na = self.dataframe[[i]].dropna()
                    desc = dataframe_na.describe()
                    count.append(desc.iat[0, 0])
                    mean.append(desc.iat[1, 0])
                    std.append(desc.iat[2, 0])
                    if (dataframe_na.shape[0] * dataframe_na.shape[1]) < 3:
                        msg = "The column " + i + " is not size of 3 "
                        give_MessageDialog(self, msg, "Error", wx.ICON_ERROR)
                        return None

                    self.shapiro_list.append(stats.shapiro(dataframe_na))
                    replace_eval.append(dataframe_na.to_numpy().flatten())

                t = tuple(replace_eval)
                s = stats.levene(*t)
                F, p = stats.f_oneway(*t)
                out = self.run_Tukey(t, self.list, z)

                # now you start the process to show the results
                name = "ANOVA one results"
                ok = False
                num = 0
                temp_dataframe = pd.DataFrame(columns=("A", "B", "C"))
                ok, num = self.find_sheet(name)
                if not ok:
                    # this is for creating the sheet for back end
                    temp_sheet = Sheet(self.notebook, name)
                    self.pages.append(temp_sheet)
                    self.notebook.AddPage(temp_sheet, name)
                    temp_sheet.create_new_sheet()
                    num = len(self.pages) - 1
                    temp_dataframe.loc[0] = ("Timestamp",
                                             "Test \n Sheet and Column",
                                             "Statistics")
                    self.data[name] = temp_dataframe

                self.pages[num].add_results_ANOVA(self.GetTitle(), self.list,
                                                  self.shapiro_list, s, F, p,
                                                  self.list, count, mean,
                                                  std, out, z)

                length = len(self.data[name])
                # for back end
                self.data[name].loc[length] = self.pages[num].last_value()
                msg = "Your data has been saved on the sheet with name" + name
                give_MessageDialog(self, msg, "Results saved",
                                   wx.ICON_INFORMATION)

            except Exception as e:
                give_MessageDialog(self, str(e), "Error", wx.ICON_ERROR)
