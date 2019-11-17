import wx
import pandas as pd

from Sheet import Sheet
from scipy import stats
from GenericClass import GenericClass
from ui_functions import give_MessageDialog


class IndependenttTest(GenericClass):
    def __init__(self, parent, dataframe, title, notebook, pages, data):
        GenericClass.__init__(self, parent, dataframe, title, notebook,
                              pages, data)

        '''
        This class creates the window for running tTest independent
        And takes care the  back end proccess to put data in file
        '''

        self.dataframe1 = pd.DataFrame()
        self.hold1 = ""

        self.set_title("Independent")
        self.set_info("* 2 Coulmns only")
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

            column_name = (str(list(dataframe0)),
                           str(list(dataframe1)))

            # clear string from "" and () from start and end of the string
            column_name = (column_name[0][2: len(column_name[0]) - 2],
                           column_name[1][2: len(column_name[1]) - 2])
            description = (dataframe0.describe(),
                           dataframe1.describe())

            count = (description[0].iat[0, 0], description[1].iat[0, 0])
            mean = (description[0].iat[1, 0], description[1].iat[1, 0])
            std = (description[0].iat[2, 0], description[1].iat[2, 0])

            dataframe0 = dataframe0.dropna()
            dataframe1 = dataframe1.dropna()

            size0 = dataframe0.shape[0] * dataframe0.shape[1]
            size1 = dataframe1.shape[0] * datafrane1.shape[1]

            if size0 < 3:
                msg = "The first set of data is smaller than 3"
                give_MessageDialog(self, msg, "Error", wx.ICON_ERROR)
            elif size1 < 3:
                msg = "The second set of data is smaller that 3"
                give_MessageDialog(self, msg, "Error", wx.ICON_ERROR)
            else:
                try:
                    shapiro0 = stats.shapiro(dataframe0)
                    shapiro1 = stats.shapiro(dataframe1)

                    levene = stats.levene(dataframe0.to_numpy().flatten(),
                                          dataframe1.to_numpy().flatten())

                    if size0 == size1:
                        x, y = stats.ttest_ind(dataframe0, dataframe1)
                    else:
                        x, y = stats.ttest_ind(dataframe0, dataframe1,
                                               equal_var=False)

                    string0 = ""
                    string0 = ("The results of tTest independent is t = "
                               + str(x) + ", p = " + str(y))
                    give_MessageDialog(self, string0, "tTest",
                                       wx.ICON_INFORMATION)

                    # Check if the sheet to save data exist
                    man = stats.mannwhitneyu(dataframe0, dataframe1)
                    name = "tTest independent resutls"
                    ok, num = self.find_sheet(name)
                    if not ok:
                        temp_sheet = Sheet(self.notebook, name)
                        self.pages.append(temp_sheet)
                        self.notebook.AddPage(temp_sheet, name)
                        temp_sheet.create_new_sheet()
                        num = len(self.pages) - 1
                        # This is for back end
                        temp_dataframe = pd.DataFrame(columns=("A", "B", "C"))
                        temp_dataframe.loc[0] = ("Timestamp",
                                                 "Test \n Sheet and Column",
                                                 "Statistics")
                        self.data[name] = temp_dataframe

                    t = self.GetTitle()
                    cb0 = self.combobox0.GetStringSelection()
                    cb1 = self.combobox1.GetStringSelection()
                    self.pages[num].add_results_tTest_independent(t, cb0, cb1,
                                                                  x, y,
                                                                  shapiro0,
                                                                  shapiro1,
                                                                  levene,
                                                                  man,
                                                                  column_name,
                                                                  count, mean,
                                                                  std)

                    # This for the back end
                    pos = self.data[name]
                    val = self.pages[num].last_value()
                    self.data[name].loc[len(pos)] = val
                    msg = "Your data has been saved on sheet " + name
                    give_MessageDialog(self, msg, "Results saved",
                                       wx.ICON_INFORMATION)
                except ValueError as e:
                    msg = ("Ther is an error in your data.\n"
                           + "Probably a string")
                    give_MessageDialog(self, str(e), "Error", wx.ICON_ERROR)
                except Exception as exception:
                    msg = "Both must have a selected column"
                    give_MessageDialog(self, str(exception), "Error",
                                       wx.ICON_ERROR)

        except KeyError:
            give_MessageDialog(self,
                               "Both boxes must have a selected column",
                               "Error", wx.ICON_ERROR)
