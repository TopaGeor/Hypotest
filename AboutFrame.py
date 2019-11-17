import wx


class AboutFrame(wx.Frame):
    def __init__(self, parent):
        '''
        This frame creates the About window, the purpose of this window is
        to provide theoritical information about the tests.
        '''
        wx.Frame.__init__(self, parent, title="About", size=(700, 300))

        self.panel = wx.Panel(self)

        self.text = wx.StaticText(self.panel, wx.ID_ANY, "")

        self.text.SetLabelText("The development of Hypotest was done to"
                               + " support statisticl hypothesis testing"
                               + " using t-Test and ANOVA. \n"
                               + "The first row will be used to name"
                               + " the columns")

        general_menu = wx.Menu()
        general_info = general_menu.Append(wx.ID_ANY, "&Info", "General info")
        general_menu.AppendSeparator()
        general_exit = general_menu.Append(wx.ID_EXIT, "E&xit", "Close about")

        tTest_menu = wx.Menu()
        tTest_one_sample = tTest_menu.Append(wx.ID_ANY, "&One Sample",
                                             "One sample info")
        tTest_independent = tTest_menu.Append(wx.ID_ANY, "&Indepedence",
                                              "Indepedence info")
        tTest_paired = tTest_menu.Append(wx.ID_ANY, "&Paired", "Paired info")

        ANOVA_menu = wx.Menu()
        ANOVA_one_way = ANOVA_menu.Append(wx.ID_ANY, "&One way",
                                          "One way info")
        ANOVA_two_way = ANOVA_menu.Append(wx.ID_ANY, "&Two way",
                                          "Two way info")
        ANOVA_repeated = ANOVA_menu.Append(wx.ID_ANY, "&Repeated",
                                           "&Repeated info")

        bar = wx.MenuBar()
        bar.Append(general_menu, "&General info")
        bar.Append(tTest_menu, "&tTest info")
        bar.Append(ANOVA_menu, "&ANOVA info")

        self.SetMenuBar(bar)

        self.Bind(wx.EVT_MENU, self.onGeneral, general_info)
        self.Bind(wx.EVT_MENU, self.onExit, general_exit)

        self.Bind(wx.EVT_MENU, self.onOne_sample, tTest_one_sample)
        self.Bind(wx.EVT_MENU, self.onIndependent, tTest_independent)
        self.Bind(wx.EVT_MENU, self.onPaired, tTest_paired)

        self.Bind(wx.EVT_MENU, self.onANOVA_one_way, ANOVA_one_way)
        self.Bind(wx.EVT_MENU, self.onANOVA_two_way, ANOVA_two_way)
        self.Bind(wx.EVT_MENU, self.onANOVA_repeated, ANOVA_repeated)

        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)

        self.text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text_sizer.Add(self.text, 0, wx.LEFT, 5)

        self.panel_sizer.Add(self.text_sizer, 0, wx.ALIGN_LEFT, 5)

        self.Show()

    def onExit(self, e):
        self.Close(True)

    def onGeneral(self, e):
        self.text.SetLabelText("The development of Hypotest was done to"
                               + " support statisticl hypothesis testing"
                               + " using t-Test and ANOVA. \n"
                               + "The first row will be used for naming"
                               + " the columns.")

    def onOne_sample(self, e):
        self.text.SetLabelText("In One Sample tTest we are looking if the"
                               + " mean value of your sample is statistical"
                               + "different from the real \n mean.")

    def onIndependent(self, e):
        self.text.SetLabelText("In Independent tTest we are looking if an"
                               + " indepedent have impact on a depedent"
                               + " variable.")

    def onPaired(self, e):
        self.text.SetLabelText("In Paired tTest we are looking if the"
                               + "means of two related samples are"
                               + "different.")

    def onANOVA_one_way(self, e):
        self.text.SetLabelText("In one way ANOVA we are looking if the"
                               + "impact of single factor has on three or"
                               + "more groups.")

    def onANOVA_two_way(self, e):
        self.text.SetLabelText("In two way ANOVA we are looking if the"
                               + "combined impact of two independent variables"
                               + " have on \n one dependent"
                               + "variable.")

    def onANOVA_repeated(self, e):
        self.text.SetLabelText("In repeated ANOVA we are looking if "
                               + " the dependent variable that measured"
                               + " for the same subjects at \n different"
                               + " times or under different conditions. \n"
                               + " Is equal to paired tTest but for more"
                               + " related samples.")
