import wx
import pandas as pd
import numpy as np

from Sheet import Sheet
from scipy import stats
from GenericClass import GenericClass
from ui_functions import give_MessageDialog


class PairedtTest(GenericClass):
    def __init__(self, parent, dataframe, title, notebook, pages, data):
        GenericClass.__init__(self, parent, dataframe, title, notebook,
                              pages, data)

        '''
        This class creates the window for running tTest paired
        And takes care the  back end proccess to put data in file
        '''

        self.dataframe1 = pd.DataFrame()
        self.hold1 = ""

        self.set_title("Paired")
        self.set_info("* 2 Columns only")
        self.create_combobox0()
        self.create_combobox1()

        self.set_text_sizers()
        self.set_combobox0_sizer()
        self.set_combobox1_sizer()

        self.panel_sizer.Add(wx.StaticLine(self.panel,), 0,
                             wx.ALL | wx.EXPAND, 5)
        self.add_close_button()
        self.set_close_sizer()
        self.add_ok_button()
        self.set_ok_sizer()

        self.panel.SetSizer(self.panel_sizer)
        self.panel_sizer.Fit(self)
        self.Show()

    '''
    onSelection functions
    First you add the current object to the other list
    Then you remove the new selected object from the other list
    '''

    def onSelection0(self, e):
        if self.hold0:
            self.combobox1.Append(self.hold0)
        self.hold0 = self.combobox0.GetStringSelection()
        try:
            self.combobox1.Delete(self.combobox1.GetItems().index(self.hold0))
        except Exception as e:
            msg = "An error occurred"
            give_MessageDialog(self, msg, "Error", wx.ICON_ERROR)

    def onSelection1(self, e):
        if self.hold1:
            self.combobox0.Append(self.hold1)
        self.hold1 = self.combobox1.GetStringSelection()
        try:
            self.combobox0.Delete(self.combobox0.GetItems().index(self.hold1))
        except Exception as e:
            msg = "An error occurred"
            give_MessageDialog(self, msg, "Error", wx.ICON_ERROR)

    def onOk(self, e):
        try:
            dataframe0 = self.dataframe[[self.hold0]]
            dataframe1 = self.dataframe[[self.hold1]]

            frames = [dataframe0, dataframe1]
            result = pd.concat(frames, axis=1)  # outter join
            results_dropna = result.dropna()  # you take data in pairs

            dataframe0 = results_dropna[[self.hold0]]
            dataframe1 = results_dropna[[self.hold1]]

            column_name = (str(list(dataframe0)),
                           str(list(dataframe1)))

            # remove "" and () from the string
            column_name = (column_name[0][2: len(column_name[0]) - 2],
                           column_name[1][2: len(column_name[1]) - 2])

            description = (dataframe0.describe(), dataframe1.describe())
            count = (description[0].iat[0, 0], description[1].iat[0, 0])
            mean = (description[0].iat[1, 0], description[1].iat[1, 0])
            std = (description[0].iat[2, 0], description[1].iat[2, 0])

            size0 = dataframe0.shape[0] * dataframe0.shape[1]
            size1 = dataframe1.shape[0] * dataframe1.shape[1]

            if size0 <= 3:
                msg = "The first set of data is not size of 3"
                give_MessageDialog(self, msg, "Error", wx.ICON_ERROR)
            elif size1 <= 3:
                msg = "The second set of data is not size of 3"
                give_MessageDialog(self, msg, "Error", wx.ICON_ERROR)
            elif size0 != size1:
                msg = ("The data is not of the same length. \n"
                       + "The empty variable will be remove automaticly")
                give_MessageDialog(self, msg, "tTest", wx.ICON_ERROR)
            else:
                try:
                    shapiro0 = stats.shapiro(dataframe0)
                    shapiro1 = stats.shapiro(dataframe1)
                    string = ""

                    levene = stats.levene(dataframe0.to_numpy().flatten(),
                                          dataframe1.to_numpy().flatten())

                    x, y = stats.ttest_rel(dataframe0, dataframe1)
                    string = ("The results of tTest paired is t = " + str(x)
                              + ", p = " + str(y))
                    give_MessageDialog(self, string,
                                       "tTest", wx.ICON_INFORMATION)

                    wil = stats.wilcoxon(dataframe0.to_numpy().flatten(),
                                         dataframe1.to_numpy().flatten())

                    name = "tTest paired results"
                    ok, num = self.find_sheet(name)

                    if not ok:
                        temp_sheet = Sheet(self.notebook, name)
                        self.pages.append(temp_sheet)
                        self.notebook.AddPage(temp_sheet, name)
                        temp_sheet.create_new_sheet()
                        num = len(self.pages) - 1
                        # This is for backend
                        temp_dataframe = pd.DataFrame(columns=("A", "B", "C"))
                        temp_dataframe.loc[0] = ("Timestamp",
                                                 "Test \n Sheet and Column",
                                                 "Statistics")
                        self.data[name] = temp_dataframe

                    cb0 = self.combobox0.GetStringSelection()
                    cb1 = self.combobox1.GetStringSelection()
                    self.pages[num].add_results_paired_tTest(self.GetTitle(),
                                                             cb0, cb1, x, y,
                                                             shapiro0,
                                                             shapiro1,
                                                             levene,
                                                             wil,
                                                             column_name,
                                                             count, mean,
                                                             std)

                    # This for the backend
                    val = self.pages[num].last_value()
                    self.data[name].loc[len(self.data[name])] = val
                    msg = "Your data has been saved on the sheet with name "
                    give_MessageDialog(self, msg + name, "Results saved",
                                       wx.ICON_INFORMATION)
                except ValueError:
                    msg = "There is an error in data. \n Probably a string"
                    give_MessageDialog(self, msg, "Error", wx.ICON_ERROR)
                except Exception as e:
                    give_MessageDialog(self, str(e), "Error", wx.ICON_ERROR)

        except KeyError:
            give_MessageDialog(self, "Both boxes must have a selected column",
                               "Error", wx.ICON_ERROR)
