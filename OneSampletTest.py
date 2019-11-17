import wx
import pandas as pd

from Sheet import Sheet
from scipy import stats
from GenericClass import GenericClass
from ui_functions import give_MessageDialog


class OneSampletTest(GenericClass):
    def __init__(self, parent, dataframe, title, notebook, pages, data):
        GenericClass.__init__(self, parent, dataframe, title, notebook,
                              pages, data)
        '''
        This class creates the window for running tTest one Sample
        And takes care the  back end proccess to put data in file
        '''

        self.set_title("One Sample")
        self.set_info("* 1 Column only")
        self.create_combobox0()

        self.text = wx.TextCtrl(self.panel, wx.ID_ANY, value="")
        self.text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text_sizer.Add(self.text, 0,
                            wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL,
                            5)
        self.set_text_sizers()

        self.set_combobox0_sizer()
        self.panel_sizer.Add(self.text_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.panel_sizer.Add(wx.StaticLine(self.panel,), 0,
                             wx.ALL | wx.EXPAND, 5)
        self.add_close_button()
        self.set_close_sizer()
        self.add_ok_button()
        self.set_ok_sizer()

        self.panel.SetSizer(self.panel_sizer)
        self.panel_sizer.Fit(self)  # fit in the window
        self.Show()

    def onOk(self, e):
        if self.combobox0.GetCurrentSelection() == - 1:
            give_MessageDialog(self, "You must select a column",
                               "Error", wx.ICON_ERROR)
            return None

        dataframe0 = self.dataframe[[self.combobox0.
                                     GetStringSelection()]]

        column_name = str(list(dataframe0))
        column_name = column_name[2: len(column_name) - 2]
        description = dataframe0.describe()
        count = description.iat[0, 0]
        mean = description.iat[1, 0]
        std = description.iat[2, 0]
        dataframe0_dropna = dataframe0.dropna()

        try:
            z = float(self.text.GetLineText(0))
            error = False
        except ValueError:
            give_MessageDialog(self, "A string has been detected",
                               "Error", wx.ICON_ERROR)
            return None
        except Exception as e:
            give_MessageDialog(self, str(e), "Error", wx.ICON_ERROR)
            return None

        if z < 0:
            give_MessageDialog(self, "A negative number has been detected",
                               "Error", wx.ICON_ERROR)
        elif (dataframe0_dropna.shape[0] * dataframe0_dropna.shape[1]) < 3:
            give_MessageDIalog(self, "The set of data is smaller than 3",
                               "Error", wx.ICON_ERROR)
        else:
            try:
                shap = stats.shapiro(dataframe0_dropna)
                x, y = stats.ttest_1samp(dataframe0_dropna, z)

                string0 = ''
                string0 = ("The result of tTest one sample is t = "
                           + str(x) + ", p = " + str(y))
                give_MessageDialog(self, string0, "tTest",
                                   wx.ICON_INFORMATION)

                name = "One sample tTest results"
                ok = False
                num = 0
                ok, num = self.find_sheet(name)

                if not ok:  # create new sheet for the resutls
                    temp_sheet = Sheet(self.notebook, name)
                    self.pages.append(temp_sheet)
                    self.notebook.AddPage(temp_sheet, name)
                    temp_sheet.create_new_sheet()
                    num = len(self.pages) - 1

                    temp_data = pd.DataFrame(columns=("A", "B", "C"))
                    temp_data.loc[0] = ("Timestamp",
                                        "Test \n Sheet and Column",
                                        "Statistics")
                    self.data[name] = temp_data

                title = self.GetTitle()
                string = self.combobox0.GetStringSelection()
                self.pages[num].add_results_tTest1_sample(title, string, x, y,
                                                          shap, z,
                                                          column_name, count,
                                                          mean, std)
                val = self.pages[num].last_value()
                self.data[name].loc[len(self.data[name])] = val
                msg = "Your data has been saved on sheet with name " + name
                give_MessageDialog(self, msg, "Results saved",
                                   wx.ICON_INFORMATION)
            except ValueError:
                msg = "There is an error in your data. \n Propably a string"
                give_MessageDialog(self, msg, "Error", wx.ICON_ERROR)
            except Exception as e:
                give_MessageDialog(self, str(e), "Error", wx.ICON_ERROR)
