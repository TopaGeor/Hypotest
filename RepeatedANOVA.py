import wx
import pandas as pd

from Sheet import Sheet
from GenericClass import GenericClass
from ui_functions import give_MessageDialog
from math_functions import ptl_anovaR


class RepeatedANOVA(GenericClass):
    def __init__(self, parent, dataframe, title, notebook, pages, data):
        '''
        This class creates the window for running Repeated ANOVA
        This test runs all of the data
        So window is set out to do that thing
        '''
        GenericClass.__init__(self, parent, dataframe, title, notebook,
                              pages, data)

        self.set_title("ANOVA repeated")
        info = ("The repeated ANOVA will run at the entire frame. \n"
                + "So hit ok and you will get your resutls.")
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
            bg, wg, error, subjects, total, F, p = ptl_anovaR(dataframe0)
        except Exception as e:
            give_MessageDialog(self, str(e), "Error", wx.ICON_ERROR)
            return

        a_list = []
        for i in dataframe0:
            dataframe_na = dataframe0[[i]].dropna()
            a_list.append(dataframe_na.to_numpy().flatten())
            t = tuple(a_list)

        out = self.run_Tukey(t, self.dataframe.columns, 0.05)
        name = "Repeated ANOVA results"
        ok = False
        number = 0
        ok, number = self.find_sheet(name)
        local_dataframe = pd.DataFrame(columns=("A", "B", "C"))

        if not ok:
            # creates the sheet to save data
            new_sheet = Sheet(self.notebook, name)
            self.pages.append(new_sheet)
            self.notebook.AddPage(new_sheet, name)
            new_sheet.create_new_sheet()
            number = len(self.pages) - 1
            local_dataframe.loc[0] = ("Timestamp",
                                      "Test \n Sheet and Coulumn",
                                      "Statistics")
            self.data[name] = local_dataframe

        self.pages[number].add_results_rANOVA(self.GetTitle(),
                                              bg, wg, error,
                                              subjects, total,
                                              F, p, out)

        length = len(self.data[name])
        self.data[name].loc[length] = self.pages[number].last_value()

        msg = "Your data has been saved on the sheet with name"
        give_MessageDialog(self, msg + name, "Results saved",
                           wx.ICON_INFORMATION)
