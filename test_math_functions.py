import unittest
import math_functions as mf
import pandas as pd
from numpy import testing


class TestMathFunctions(unittest.TestCase):

    def setUp(self):
        self.ser0 = pd.Series([1, 2, 3])

        dic0 = {"1": [1, 2, 3], "2": [4, 5, 6], "3": [7, 8, 9]}
        self.df0 = pd.DataFrame(dic0)
        self.ser1 = pd.Series([i for i in range(1, 10)],
                              index=[0, 1, 2, 0, 1, 2, 0, 1, 2])

        dic1 = {"1": ["A1", "A1", "A2", "A2"], "2": [1, 2, 3, 4],
                "3": [5, 6, 7, 8]}
        self.df1 = pd.DataFrame(dic1)

        self.repeated_results = ((54.0, 6, 9.0), (6.0, 6), (0.0, 4, 0.0),
                                 (6.0, 2), (60.0, 8), float("Inf"), 0.0)
        self.ssd_df_results = (17.5, 6)

        self.two_results = ((40.0, 3), (8.0, 1, 8.0, 16.0, 0.0161),
                            (32.0, 1, 32.0, 64.0, 0.0013),
                            (0.0, 1, 0.0, 0.0, 1), (2.0, 4, 0.5),
                            (42.0, 7.0))

    def test_ssd(self):
        self.assertAlmostEqual(mf.ssd(self.ser0), 2)

    def test_dftoser(self):
        for i, j in zip(mf.dftoser(self.df0), self.ser1):
            self.assertAlmostEqual(i, j)

    def test_ptl_anovaR(self):
        self.assertAlmostEqual(mf.ptl_anovaR(self.df0), self.repeated_results)

    def test_ssd_df(self):
        self.assertAlmostEqual(mf.ssd_df(self.df0), self.ssd_df_results)

    def test_ssd_df_rc(self):
        self.assertAlmostEqual(mf.ssd_df_rc(self.df0), 13.5)

    def test_ptl_anova2(self):
        for i, j in zip(mf.ptl_anova2(self.df1), self.two_results):
            for k, l in zip(i, j):
                self.assertAlmostEqual(k, l, places=4)
