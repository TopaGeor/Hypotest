import wx
import sys
import datetime
import time
import pandas as pd
import wx.grid as gridlib

from ui_functions import give_MessageDialog


class Sheet(wx.Panel):
    def __init__(self, parent, title):
        '''
        This class will create the spreadsheets
        It will create the new spreadsheets where the results will be saved
        There is a specif function for every test
        Add more coments to the functions and what is every argument
        '''
        wx.Panel.__init__(self, parent)
        self.name = title

    def return_name(self):
        return self.name

    def create_new_sheet(self):
        self.my_grid = gridlib.Grid(self)
        self.my_grid.CreateGrid(1, 3)
        self.my_grid.SetCellValue(0, 0, "Timsestamp")
        self.my_grid.SetCellValue(0, 1, "Test \n Sheet and Column")
        self.my_grid.SetCellValue(0, 2, "Statistics")
        self.my_grid.AutoSizeRows(setAsMin=True)
        self.my_grid.AutoSizeColumns(setAsMin=True)
        self.my_grid.EnableEditing(False)

        grid_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer.Add(self.my_grid, 1, wx.SHAPED)
        self.SetSizer(grid_sizer)

        self.Layout()

    def num_to_float(self, a):
        support_str = str(a)
        support_str = support_str[1: len(support_str) - 1]
        support_str = float(support_str)
        return self.select_symbol(support_str)

    def select_symbol(self, a):
        if abs(a) < 0.0001:
            return "< 0.0001"
        else:
            return "= {:.4f}".format(a)

    def add_results_tTest1_sample(self, sheet_name, col_name, x, y, shap, z,
                                  name, count, mean, std):
        # Create shapiro string
        shapiro_str = ("Shapiro: w"
                       + self.select_symbol(shap[0])
                       + ", p"
                       + self.select_symbol(shap[1]))

        # Create the tTest string
        tTest_str = ("tTest against "
                     + str(z)
                     + " as population value: t"
                     + self.num_to_float(x)
                     + ", p"
                     + self.num_to_float(y))

        self.my_grid.AppendRows(1)
        nrow = self.my_grid.GetNumberRows() - 1
        self.my_grid.SetCellValue(nrow, 0,
                                  datetime.datetime.fromtimestamp(time.time()).
                                  strftime("%d-%m-%Y %H:%M:%S"))

        info = "tTest one sample \n" + sheet_name + " " + col_name
        self.my_grid.SetCellValue(nrow, 1, info)

        results = (name + "\n"
                   + "Count = " + str(round(count, 4))
                   + ", Mean " + self.select_symbol(mean)
                   + ", Std " + self.select_symbol(std) + "\n \n"
                   + "Normality: \n" + shapiro_str + "\n \n"
                   + "statistics: \n" + tTest_str)

        self.my_grid.SetCellValue(nrow, 2, results)
        self.my_grid.AutoSizeColumns(setAsMin=True)
        self.my_grid.AutoSizeRows(setAsMin=True)

    def add_results_tTest_independent(self, sheet_name, col0_name, col1_name,
                                      x, y, shap0, shap1, levene, mw, name,
                                      count, mean, std):

        # create shapiro string
        shapiro_str = ("Shapiro(" + col0_name + "):"
                       + " w " + self.select_symbol(shap0[0])
                       + ", p " + self.select_symbol(shap0[1])
                       + "\n"
                       + "Shapiro(" + col1_name + "):"
                       + " w " + self.select_symbol(shap1[0])
                       + ", p " + self.select_symbol(shap1[1])
                       + "\n")

        # create Levene string
        levene_str = ("Levene: s" + self.num_to_float(levene[0])
                      + ", p " + self.num_to_float(levene[1]))

        # create tTest string
        tTest_str = ("tTest: t" + self.num_to_float(x)
                     + ", p " + self.num_to_float(y))

        # Mann Witney string
        mann_str = ("Mann-Whitney: u" + self.select_symbol(mw[0])
                    + ", p " + self.select_symbol(mw[1]))

        self.my_grid.AppendRows(1)
        nrows = self.my_grid.GetNumberRows() - 1
        self.my_grid.SetCellValue(nrows, 0,
                                  datetime.datetime.
                                  fromtimestamp(time.time()).
                                  strftime("%d-%m-%Y %H:%M:%S"))

        info = ("tTest independent \n" + sheet_name + ", "
                + col0_name + ", " + col1_name)
        self.my_grid.SetCellValue(nrows, 1, info)
        results = (name[0] + "\n"
                   + "Count = " + str(count[0])
                   + ", Mean " + self.select_symbol(mean[0])
                   + ", Std " + self.select_symbol(std[0]) + "\n" + "\n"
                   + name[1] + "\n"
                   + "Count = " + str(count[1])
                   + ", Mean " + self.select_symbol(mean[1])
                   + ", Std " + self.select_symbol(std[1]) + "\n" + "\n"
                   + "Normality: \n" + shapiro_str + "\n"
                   + "Varience: \n" + levene_str + "\n"
                   + "Statistics: \n" + tTest_str + "\n"
                   + mann_str)
        self.my_grid.SetCellValue(nrows, 2, results)

        self.my_grid.AutoSizeColumns(setAsMin=True)
        self.my_grid.AutoSizeRows(setAsMin=True)

    def add_results_paired_tTest(self, sheet_name,
                                 col0_name, col1_name, x, y, shap0, shap1,
                                 levene, wilc, name, count, mean, std):

        # create shapiro string
        normality_str = ("Shapiro(" + col0_name + "):"
                         + " w " + self.select_symbol(shap0[0])
                         + ", p " + self.select_symbol(shap0[1]) + "\n"
                         + "Shapiro(" + col1_name + "):"
                         + " w " + self.select_symbol(shap1[0])
                         + ", p " + self.select_symbol(shap1[1]) + "\n")

        # create varience string
        varience_str = ("Levene: s" + self.num_to_float(levene[0])
                        + ", p " + self.num_to_float(levene[1]))

        # create tTest string
        tTest_str = ("tTest: t" + self.num_to_float(x)
                     + ", p " + self.num_to_float(y))

        # create Wilcoxon string wx
        wilc_str = ("Wilcoxon: s " + self.select_symbol(wilc[0])
                    + " p " + self.select_symbol(wilc[1]))

        self.my_grid.AppendRows(1)
        nrows = self.my_grid.GetNumberRows() - 1
        self.my_grid.SetCellValue(nrows, 0,
                                  datetime.datetime.fromtimestamp(time.time()).
                                  strftime("%d-%m-%Y %H:%M:%S"))

        info = ("tTest Paired \n"
                + sheet_name + ", " + col0_name + ", " + col1_name)
        self.my_grid.SetCellValue(nrows, 1, info)
        results = (name[0] + "\n"
                   + "Count = " + str(count[0])
                   + ", Mean " + self.select_symbol(mean[0])
                   + ", Std " + self.select_symbol(std[0]) + "\n" + "\n"
                   + name[1] + "\n"
                   + "Count = " + str(count[1])
                   + ", Mean " + self.select_symbol(mean[1])
                   + ", Std " + self.select_symbol(std[1]) + "\n" + "\n"
                   + "Normality: \n" + normality_str + "\n"
                   + "Varience: \n" + varience_str + "\n \n"
                   + "Statistics: \n" + tTest_str + "\n" + wilc_str)
        self.my_grid.SetCellValue(nrows, 2, results)
        self.my_grid.AutoSizeColumns(setAsMin=True)
        self.my_grid.AutoSizeRows(setAsMin=True)

    def add_results_ANOVA(self, sheet_name, name_list,
                          shap, s, F, p, dtf_names, count,
                          mean, std, out, z):

        details = ""
        for n, c, m, t in zip(dtf_names, count, mean, std):
            details += (n + "\n"
                        + "Count = " + str(c)
                        + ", Mean " + self.select_symbol(m)
                        + ", Std " + self.select_symbol(t) + "\n" + "\n")

        names = ""
        shapiro_res = ""
        for i, j in zip(name_list, shap):  # get all of shapiro results
            names += i + ", "
            shapiro_res += ("Shapiro(" + i + "): w " + self.select_symbol(j[0])
                            + ", p " + self.select_symbol(j[1]) + "\n")

        names = names[:len(names) - 2]

        # create string for Levene
        levene_str = ("Levene: s" + self.num_to_float(s[0])
                      + ", p " + self.num_to_float(s[1]))

        # create string for statistics
        stats_str = ("ANOVA one way: F" + self.num_to_float(F)
                     + ", p " + self.num_to_float(p))

        # create string for the results from tukey
        res_Tukey = ""
        group_list = out.groupsunique.tolist()
        k = 0
        for i in group_list:
            for j in group_list[group_list.index(i) + 1:]:
                res_Tukey += ("Group (" + i + ", " + j + "):"
                              + " meandiff "
                              + self.select_symbol(out.meandiffs[k])
                              + ", lower "
                              + self.select_symbol(out.confint[k][0])
                              + ", upper "
                              + self.select_symbol(out.confint[k][1])
                              + ", reject = "
                              + str(out.reject[k]) + "\n")
                k += 1

        res_Tukey = res_Tukey[:len(res_Tukey) - 1]

        self.my_grid.AppendRows(1)
        nrows = self.my_grid.GetNumberRows() - 1
        self.my_grid.SetCellValue(nrows, 0,
                                  datetime.datetime.fromtimestamp(time.time()).
                                  strftime("%d-%m-%Y %H:%M:%S"))

        info = "ANOVA one way: \n" + sheet_name + " " + names
        self.my_grid.SetCellValue(nrows, 1, info)

        results = (details + "Normality: \n" + shapiro_res + "\n"
                   + "Varience: \n" + levene_str + "\n \n"
                   + "Statistics: \n" + stats_str + "\n \n"
                   + "Post-hoc Tukey's test: \n a = " + str(z) + "\n"
                   + res_Tukey)
        self.my_grid.SetCellValue(nrows, 2, results)

        self.my_grid.AutoSizeColumns(setAsMin=True)
        self.my_grid.AutoSizeRows(setAsMin=True)

    def add_results_2ANOVA(self, sheet_name, bg, rows, columns, interaction,
                           wg, total, out):
        results_Tukey = ""
        if(out is not False):
            group_list = out.groupsunique.tolist()
            k = 0
            for i in group_list:
                for j in group_list[group_list.index(i) + 1:]:
                    results_Tukey += ("Group (" + i + ", " + j + "):"
                                      + "meandiff "
                                      + self.select_symbol(out.meandiffs[k])
                                      + ", lower "
                                      + self.select_symbol(out.confint[k][0])
                                      + ", upper "
                                      + self.select_symbol(out.confint[k][1])
                                      + ", reject = "
                                      + str(out.reject[k]) + "\n")
                    k += 1
            results_Tukey = results_Tukey[:len(results_Tukey) - 1]
            results_Tukey = ("\n \n" + "Post-hoc Tukey's test: \n" +
                             "a = 0.05 \n" + results_Tukey)
        else:
            res_Tukey = ("\n \n" + "Because the p in columns is larger than"
                         + "0.05 the Tukey test will reject ever hypothesis")

        self.my_grid.AppendRows(1)
        nrows = self.my_grid.GetNumberRows() - 1
        self.my_grid.SetCellValue(nrows, 0,
                                  datetime.datetime.fromtimestamp(time.time()).
                                  strftime("%d-%m-%Y %H:%M:%S"))

        info = "ANOVA two way: \n" + sheet_name
        self.my_grid.SetCellValue(nrows, 1, info)

        results = ("The SS is sum of square,"
                   + " the df is degrees of freedom,"
                   + " ms is mean square. \n \n"
                   + "Between Groups: \n"
                   + "SS " + self.select_symbol(bg[0])
                   + ", df = " + str(bg[1]) + "\n \n"
                   + "Rows:\n"
                   + "SS " + self.select_symbol(rows[0])
                   + ", df = " + str(rows[1])
                   + ", ms " + self.select_symbol(rows[2])
                   + ", F = " + self.select_symbol(rows[3])
                   + ", p " + self.select_symbol(rows[4]) + "\n \n"
                   + "Columns: \n"
                   + "SS " + self.select_symbol(columns[0])
                   + ", df = " + str(columns[1])
                   + ", ms " + self.select_symbol(columns[2])
                   + ", F " + self.select_symbol(columns[3])
                   + "Interaction:\n"
                   + "SS " + self.select_symbol(interaction[0])
                   + ", df = " + str(interaction[1])
                   + ", ms " + self.select_symbol(interaction[2])
                   + ", F " + self.select_symbol(interaction[3])
                   + ", p " + self.select_symbol(interaction[4]) + "\n \n"
                   + "Within Groups: \n"
                   + "SS " + self.select_symbol(wg[0])
                   + ", df = " + str(wg[1])
                   + ", ms " + self.select_symbol(wg[2]) + "\n \n"
                   + "Total: \n"
                   + "SS " + self.select_symbol(total[0])
                   + ", df = " + str(total[1]) + results_Tukey)

        self.my_grid.SetCellValue(nrows, 2, results)
        self.my_grid.AutoSizeColumns(setAsMin=True)
        self.my_grid.AutoSizeRows(setAsMin=True)

    def add_results_rANOVA(self, sheet_name, bg, wg, error, subjects, total,
                           F, p, out):
        result_Tukey = ""
        group_list = out.groupsunique.tolist()
        k = 0
        for i in group_list:
            for j in group_list[group_list.index(i) + 1:]:
                result_Tukey += ("Group (" + i + ", " + j + "): "
                                 + "meandiff "
                                 + self.select_symbol(out.meandiffs[k])
                                 + ", lower "
                                 + self.select_symbol(out.confint[k][0])
                                 + ", upper "
                                 + self.select_symbol(out.confint[k][1])
                                 + ", reject = " + str(out.reject[k]) + "\n")
                k += 1

        result_Tukey = result_Tukey[:len(result_Tukey) - 1]
        result_Tukey = ("\n \n" + "Post-hoc Tukey's test: \n"
                        + " a = 0.05 \n" + result_Tukey)

        self.my_grid.AppendRows(1)
        nrows = self.my_grid.GetNumberRows() - 1
        self.my_grid.SetCellValue(nrows, 0, datetime.datetime.
                                  fromtimestamp(time.time()).
                                  strftime("%d-%m-%Y %H:%M:%S"))

        info = "ANOVA Repeated: \n" + sheet_name
        self.my_grid.SetCellValue(nrows, 1, info)
        results = ("The SS is sum of square, the df is degrees of freedom,"
                   + "ms is the mean square. \n\n"
                   + "Between groups(effect):\n"
                   + "SS " + self.select_symbol(bg[0])
                   + ", df = " + str(bg[1])
                   + ", MS " + self.select_symbol(bg[2]) + "\n\n"
                   + "Within groups: \n"
                   + "SS " + self.select_symbol(wg[0])
                   + ", df = " + str(wg[1])
                   + "Error:\n"
                   + "SS " + self.select_symbol(error[0])
                   + ", df = " + str(error[1])
                   + ", MS " + self.select_symbol(error[2]) + "\n\n"
                   + "Subjects:\n"
                   + "SS " + self.select_symbol(subjects[0])
                   + ", df = " + str(subjects[1]) + "\n\n"
                   + "Total:\n"
                   + "SS " + self.select_symbol(total[0])
                   + "df = " + str(total[1])
                   + "F " + self.select_symbol(F)
                   + ", p " + self.select_symbol(p) + result_Tukey)
        self.my_grid.SetCellValue(nrows, 2, results)

        self.my_grid.AutoSizeColumns(setAsMin=True)
        self.my_grid.AutoSizeRows(setAsMin=True)

    def last_value(self):
        # Return last values
        pos = self.my_grid.GetNumberRows() - 1
        tup = (self.my_grid.GetCellValue(pos, 0),
               self.my_grid.GetCellValue(pos, 1),
               self.my_grid.GetCellValue(pos, 2))
        return tup

    def return_grid(self):
        return self.my_grid

    def construct_grid(self, data):
        self.my_grid = gridlib.Grid(self)
        self.my_grid.CreateGrid(len(data.index), len(data.columns))

        for i in range(0, len(data.index)):
            for j in range(0, len(data.columns)):
                if(pd.notnull(data.iat[i, j])):
                    self.my_grid.SetCellValue(i, j, str(data.iat[i, j]))
                else:
                    self.my_grid.SetCellValue(i, j, " ")

        j = 0
        for i in data.columns:
            if isinstance(i, str):
                self.my_grid.SetColLabelValue(j, i)
            else:
                self.my_grid.SetColLabelValue(j, str(i))
            j += 1

        self.my_grid.AutoSizeRows(setAsMin=True)
        self.my_grid.AutoSizeColumns(setAsMin=True)
        self.my_grid.EnableEditing(False)
        grid_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer.Add(self.my_grid, 1, wx.SHAPED)

        self.SetSizer(grid_sizer)
