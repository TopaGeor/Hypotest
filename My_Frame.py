import wx
import os

import pandas as pd

from My_Notebook import My_Notebook
from Sheet import Sheet
from AboutFrame import AboutFrame
from OneSampletTest import OneSampletTest
from IndependenttTest import IndependenttTest
from PairedtTest import PairedtTest
from OneANOVA import OneANOVA
from TwoANOVA import TwoANOVA
from RepeatedANOVA import RepeatedANOVA
from ui_functions import give_MessageDialog


class My_Frame(wx.Frame):
    def __init__(self, parent):
        '''
        This is our main frame, from here we will create all other frames
        '''
        wx.Frame.__init__(self, parent, title="Hypotest", size=(1200, 800))

        self.directory_name = ''
        self.file_name = ''
        self.type = ''

        self.panel = wx.Panel(self)
        self.CreateStatusBar()

        file_menu = wx.Menu()  # File menu
        menu_open = file_menu.Append(wx.ID_OPEN, "&Open", "Open file to edit")
        menu_save = file_menu.Append(wx.ID_SAVE, "&Save", "Save the file")
        menu_save_as = file_menu.Append(wx.ID_SAVEAS, "Save &As",
                                        "Save the file as a new file")
        file_menu.AppendSeparator()

        menu_print = file_menu.Append(wx.ID_ANY, "&Print", "Print a page")
        menu_about = file_menu.Append(wx.ID_ABOUT, "A&bout",
                                      "Info about the application")
        file_menu.AppendSeparator()

        menu_exit = file_menu.Append(wx.ID_EXIT, "E&xit",
                                     "Close the application")

        tTest_algo = wx.Menu()  # tTest menu
        tTest_1sample = tTest_algo.Append(wx.ID_ANY, "&One sample",
                                          "Use panda tTest for one sample")
        tTest_independent = tTest_algo.Append(wx.ID_ANY, "&Independent",
                                              "Use panda tTest independent")
        tTest_paired = tTest_algo.Append(wx.ID_ANY, "&Paired",
                                         "Use panda tTest paired")

        anova_algo = wx.Menu()  # ANOVA menu
        one_way = anova_algo.Append(wx.ID_ANY, "&One way",
                                    "Use panda one way ANOVA")
        two_way = anova_algo.Append(wx.ID_ANY, "&Two way",
                                    "Use two way ANOVA")
        repeated_way = anova_algo.Append(wx.ID_ANY, "&Repeated",
                                         "Use repeated ANOVA")

        menu_bar = wx.MenuBar()  # Create object to add the menus
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(tTest_algo, "&tTest")
        menu_bar.Append(anova_algo, "&ANOVA")

        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.onOpen, menu_open)
        self.Bind(wx.EVT_MENU, self.onSave, menu_save)
        self.Bind(wx.EVT_MENU, self.onSaveAs, menu_save_as)
        self.Bind(wx.EVT_MENU, self.onPrint, menu_print)
        self.Bind(wx.EVT_MENU, self.onAbout, menu_about)
        self.Bind(wx.EVT_MENU, self.onExit, menu_exit)

        self.Bind(wx.EVT_MENU, self.ontTest1, tTest_1sample)
        self.Bind(wx.EVT_MENU, self.ontTestIndependent, tTest_independent)
        self.Bind(wx.EVT_MENU, self.ontTestPaired, tTest_paired)

        self.Bind(wx.EVT_MENU, self.on1ANOVA, one_way)
        self.Bind(wx.EVT_MENU, self.on2ANOVA, two_way)
        self.Bind(wx.EVT_MENU, self.onRepeatedANOVA, repeated_way)

        self.Show()

    def onSave(self, e):
        # What happens when you hit Save
        # you need to change the numbers to strings or make a dictionary
        try:
            if self.type == 0:  # xls
                writer = pd.ExcelWriter(self.file_name)
            elif self.type == 1:  # xlsx
                writer = pd.ExcelWriter(self.file_name, engine='xlsxwriter')
            for i in self.data:
                self.data[i].to_excel(writer, sheet_name=i, index=False)
            writer.save()
        except AttributeError:
            give_MessageDialog(self, "Open a file first", "Error",
                               wx.ICON_ERROR)
        except Exception as exception:
            give_MessageDialog(self, str(exception), "Error", wx.ICON_ERROR)

    def onSaveAs(self, e):
        # What happens when you hit Save as
        try:
            # every second | is an new option
            wildcard = "Xls files (*.xls)|*.xls|XLSX files(*.xlsx)|*.xlsx"
            dlg = wx.FileDialog(self, "Save file", self.directory_name,
                                self.file_name, wildcard,
                                wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

            if dlg.ShowModal() == wx.ID_OK:
                self.file_name = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                self.type = dlg.GetFilterIndex()  # 0 is xls, 1 xlsx
                self.SetTitle("Hypotest: " + self.file_name)
                if self.type == 0:
                    writer = pd.ExcelWriter(dlg.GetFilename())
                elif self.type == 1:
                    writer = pd.ExcelWriter(dlg.GetFilename(),
                                            engine='xlsxwriter')

                for i in self.data:  # could that be better ?
                    self.data[i].to_excel(writer, sheet_name=i, index=False)

                writer.save()

            dlg.Destroy()

        except AttributeError:
            give_MessageDialog(self, "Open a file first", "Error",
                               wx.ICON_ERROR)
        except Exception as exception:
            give_MessageDialog(self, str(exception), "Error", wx.ICON_ERROR)

    def onAbout(self, e):
        about_frame = AboutFrame(self)

    def onPrint(self, e):
        # Needs more testing
        try:
            if self.file_name != '':
                grid_print = prout.PrintGrid(self,
                                             self.
                                             pages[self.notebook.page].
                                             returnGrid())
                grid_print.setAttributes()

                table = grid_print.GetTable()
                table.SetLandscape()
                grid_print.Preview()

            else:
                give_MessageDialog(self, "Open a file first", "Error",
                                   wx.ICON_ERROR)

        except Exception as exception:
            give_MessageDialog(self, str(exception), "Error", wx.ICON_ERROR)

    def onOpen(self, e):
        # every second | creates a new type of file
        # on the left is what goes in UI
        # on the right is what files are shown
        wildcard = "Xls files (*.xls)|*.xls|Xlsx files (*.xlsx)|*.xlsx"
        dlg = wx.FileDialog(self, "Choose a file", self.directory_name,
                            "", wildcard, wx.FD_OPEN)  # for files in wildcard

        if dlg.ShowModal() == wx.ID_OK:
            try:
                self.file_name = dlg.GetFilename()
                self.directory_name = dlg.GetDirectory()
                self.type = dlg.GetFilterIndex()
                path = os.path.join(self.directory_name, self.file_name)
                self.data = pd.read_excel(io=path, sheet_name=None,
                                          skip_rows=None)

            except FileNotFoundError:
                give_MessageDialog(self, "No such file or directory",
                                   "Error", wx.ICON_ERROR)
                dlg.Destroy()
                return None
            except Exception as exception:
                give_MessageDialog(self, str(exception), "Error",
                                   wx.ICON_ERROR)
                dlg.Destroy()
                return None
            dlg.Destroy()
        else:
            dlg.Destroy()
            return None

        self.SetTitle("Hypotest: " + self.file_name)
        self.notebook = None
        self.pages = []
        for child in self.panel.GetChildren():
            child.Destroy()

        self.notebook = My_Notebook(self.panel)
        for i in self.data:
            self.pages.append(Sheet(self.notebook, i))

        for i in self.pages:
            self.notebook.AddPage(i, i.return_name())

        panel_sizer = wx.BoxSizer()
        panel_sizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND)
        self.panel.SetSizer(panel_sizer)

        for i in self.pages:
            i.construct_grid(self.data[i.return_name()])

        self.panel.Layout()

    def ontTest1(self, e):
        # create frame for one Sample tTest
        try:
            var = self.notebook.GetPageText(self.notebook.page)
            one_frame = OneSampletTest(self, self.data[var], var,
                                       self.notebook, self.pages,
                                       self.data)
        except AttributeError:
            give_MessageDialog(self, "Open a file first",
                               "Error", wx.ICON_ERROR)
        except KeyError:
            give_MessageDialog(self, "We can not read this sheet",
                               "Error", wx.ICON_ERROR)
        except Exception as exception:
            give_MessageDialog(self, str(exception), "Error", wx.ICON_ERROR)

    def ontTestIndependent(self, e):
        # create frame for one tTest independent
        try:
            var = self.notebook.GetPageText(self.notebook.page)
            indepedent_frame = IndependenttTest(self, self.data[var],
                                                var, self.notebook,
                                                self.pages, self.data)
        except AttributeError:
            give_MessageDialog(self, "Open a file first",
                               "Error", wx.ICON_ERROR)
        except KeyError:
            give_MessageDialog(self, "We can not read this sheet",
                               "Error", wx.ICON_ERROR)
        except Exception as exception:
            give_MessageDialog(self, str(exception), "Error", wx.ICON_ERROR)

    def ontTestPaired(self, e):
        # create frame for one tTest paired
        try:
            var = self.notebook.GetPageText(self.notebook.page)
            paired_frame = PairedtTest(self, self.data[var], var,
                                       self.notebook, self.pages,
                                       self.data)
        except AttributeError:
            give_MessageDialog(self, "Open a file first",
                               "Error", wx.ICON_ERROR)
        except KeyError:
            give_MessageDialog(self, "We can not read this sheet",
                               "Error", wx.ICON_ERROR)
        except Exception as exception:
            give_MessageDialog(self, str(exception), "Error", wx.ICON_ERROR)

    def on1ANOVA(self, e):
        # create frame for one ANOVA
        try:
            var = self.notebook.GetPageText(self.notebook.page)
            one_ANOVA_frame = OneANOVA(self, self.data[var], var,
                                       self.notebook, self.pages, self.data)
        except AttributeError:
            give_MessageDialog(self, "Open a file first",
                               "Error", wx.ICON_ERROR)
        except KeyError:
            give_MessageDialog(self, "We can not read this sheet",
                               "Error", wx.ICON_ERROR)
        except Exception as exception:
            give_MessageDialog(self, str(exception), "Error", wx.ICON_ERROR)

    def on2ANOVA(self, e):
        # create frame for two ANOVA
        try:
            var = self.notebook.GetPageText(self.notebook.page)
            two_ANOVA_frame = TwoANOVA(self, self.data[var], var,
                                       self.notebook, self.pages,
                                       self.data)
        except AttributeError as e:
            give_MessageDialog(self, "Open a file first \n" + str(e),
                               "Error", wx.ICON_ERROR)
        except KeyError:
            give_MessageDialog(self, "We can not read this sheet",
                               "Error", wx.ICON_ERROR)
        except Exception as exception:
            give_MessageDialog(self, str(exception), "Error", wx.ICON_ERROR)

    def onRepeatedANOVA(self, e):
        # create frame for repeated ANOVA
        try:
            var = self.notebook.GetPageText(self.notebook.page)
            repeated_ANOVA_frame = RepeatedANOVA(self,
                                                 self.data[var], var,
                                                 self.notebook,
                                                 self.pages, self.data)
        except AttributeError:
            give_MessageDialog(self, "Open a file first",
                               "Error", wx.ICON_ERROR)
        except KeyError:
            give_MessageDialog(self, "We can not read this sheet",
                               "Error", wx.ICON_ERROR)
        except Exception as exception:
            give_MessageDialog(self, str(exception), "Error", wx.ICON_ERROR)

    def onExit(self, e):
        self.Close(True)
