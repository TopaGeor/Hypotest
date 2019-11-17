import wx
import pandas as pd

from Sheet import Sheet
from GenericClass import GenericClass
from ui_functions import give_MessageDialog
from math_functions import ptl_anova2


class TwoANOVA(GenericClass):
    def __init__(self, parent, dataframe, title, notebook,
                 pages, data):
        '''
        This class creates the window for running Two way ANOVA
        This test runs all of the data
        So window is set out to do that thing
        '''
        GenericClass.__init__(self, parent, dataframe, title,
                              notebook, pages, data)
        self.set_title("ANOVA two way")
        info = ("The ANOVA two way will run at the entire frame.\n"
                + "So hit ok and you will get the results. \n"
                + "The first column will be the factors - categories")

        self.set_info(info)
        self.set_text_sizers()
        self.add_button_sizer_all_data()
        self.set_button_sizer_all_data()

        self.panel.SetSizer(self.panel_sizer)
        self.panel_sizer.Fit(self)
        self.Show()

    def onOk(self, e):
        dataframe0 = self.dataframe
        if dataframe0.shape[1] < 3:
            msg = "You need more than two columns"
            give_MessageDialog(self, msg, "Error", wx.ICON_ERROR)
            return
        try:
            bg, rows, columns, interaction, wg, total = ptl_anova2(dataframe0)
        except Exception as exception:
            give_MessageDialog(self, str(exception), "Error", wx.ICON_ERROR)

        out = False
        if(columns[4] <= 0.05):
            j = 0
            alist = []
            for i in dataframe0.columns[1:]:
                alist.append(dataframe0[i].dropna())

            t = tuple(alist)
            out = self.run_Tukey(t, dataframe0.columns[1:], 0.05)

        # proccess to save the data
        name = "Two way ANOVA results"
        ok = False
        number = 0
        ok, number = self.find_sheet(name)
        local_dataframe = pd.DataFrame(columns=("A", "B", "C"))
        if not ok:
            new_sheet = Sheet(self.notebook, name)
            self.pages.append(new_sheet)
            self.notebook.AddPage(new_sheet, name)
            new_sheet.create_new_sheet()
            number = len(self.pages) - 1
            local_dataframe.loc[0] = ("Timestamp",
                                      "Test \n Sheet and Column",
                                      "Statistics")
            self.data[name] = local_dataframe

        # front end
        self.pages[number].add_results_2ANOVA(self.GetTitle(), bg, rows,
                                              columns, interaction, wg,
                                              total, out)
        # back end
        length = len(self.data[name])
        self.data[name].loc[length] = self.pages[number].last_value()

        msg = "Your data has been saved on the sheet with name "
        give_MessageDialog(self, msg + name, "Results saved",
                           wx.ICON_INFORMATION)
