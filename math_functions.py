import pandas as pd

from scipy import stats
from scipy.stats import f


def ssd(ser):
    '''
    calculate the sum of squared difference of a series
    ser is a series
    '''
    ser.dropna(axis=0, inplace=True)
    s1 = pow(ser, 2).sum()
    s2 = pow(ser.sum(), 2) / ser.size
    return s1 - s2


def dftoser(df):
    '''
    removes the empty values of the dataframe
    converts the dataframe to a series
    is a series that has all the columns of the dataframe in row
    '''
    df.dropna(axis=(0, 1), how='all', inplace=True)
    ser = pd.Series()
    for i in range(len(df.columns)):
        ser = ser.append(df.iloc[:, i])
    return(ser)


def ptl_anovaR(inframe):
    '''
    edw prepei na allakseis tous arithmous sta t
    repeated measures one way ANOVA data
    inframe is  a dataframe
    ss is sum of square
    wg is within group
    bg is between group
    ms is means square
    '''
    rows, cols = inframe.shape
    k = cols
    n_sbj = rows

    allser = dftoser(inframe)
    n_t = allser.size

    # Within group
    ss_wg = 0
    for i in range(k):
        ss_wg += ssd(inframe.iloc[:, i])
    df_wg = n_t - k
    t1 = (ss_wg, df_wg)

    # Between groups
    ss_t = ssd(allser)
    ss_bg = ss_t - ss_wg
    df_bg = n_t - k
    ms_bg = ss_bg / df_bg
    t0 = (ss_bg, df_bg, ms_bg)

    # Subjects
    subjects_means = pd.Series([0 for i in range(rows)])
    for i in range(rows):
        sm = inframe.iloc[i, :].mean(skipna=True)
        subjects_means.iloc[i] = sm

    ss_sb = k*ssd(subjects_means)
    df_sb = n_sbj - 1
    t3 = (ss_sb, df_sb)

    ss_er = ss_wg - ss_sb
    df_er = df_wg - df_sb
    ms_er = ss_er / df_er
    t2 = (ss_er, df_er, ms_er)

    df_t = n_t - 1
    t4 = (ss_t, df_t)

    if ms_er == 0:
        F = float("Inf")
    else:
        F = ms_bg / ms_er

    p = f.sf(F, df_bg, df_er, loc=0, scale=1)

    return t0, t1, t2, t3, t4, F, p


def ssd_df(indf):
    '''
    prepei na to ksana deis
    indf is a dataframe
    ssd_df computes the ssd: S(x)**2 - ((Sx)**2)/N for a DataFrame
    The 1st column (0-index) is the R-factor and is ommited from computations
    Returns a tuple consisting of:
    ss_n_all = The ssd: S(x)**2 - ((x)**2)/N factor
    n_all = The size of DataFrame data included in the computation
    '''
    n_all = sumx = sumx2 = 0
    for i in range(1, len(indf.columns)):
        ser = indf.iloc[:, i].dropna()
        sumx += ser.sum()
        sumx2 += pow(ser, 2).sum()
        n_all += ser.size

    sumx_sqed = pow(sumx, 2)
    ss_n_all = sumx2 - (sumx_sqed / n_all)
    return ss_n_all, n_all


def ssd_df_rc(df, axis=0):
    '''
    Function computes the ssd for the two way ANOVA rows or columns
    S((S(x)**2)/N) - ((Sx_all)**2)/N_all
    1st column (0-index) is the R-factor and is ommited from computations

    Input parameters:
    df: the DataFrame object
    axis=0 column-wise (working on columns data)
    axis=1 row-wise (working on rows data)

    Returns:
    The ssd for the ANOVA rows or columns of the input DataFrame
    '''
    ss_n_sum = 0
    ss_n_all = 0

    if axis == 0:
        # Compute the ss_n_sum quantity considering each SEPARATE Column in df
        for i in range(1, len(df.columns)):
            c_ser = df.iloc[:, i].dropna()
            ss_n_sum += pow(c_ser.sum(), 2) / c_ser.size
    elif axis == 1:
        r_factor = df.columns[0]
        anv_groups = df.groupby(r_factor)
        for symb, gp in anv_groups:
            # Compute the ss_n_sum quantity considerint each SEPARATE Row in df
            # Rows in df are ADDED columns in each anv_groups
            n_all = sumx = 0
            for i in range(1, len(gp.columns)):
                ser = gp.iloc[:, i].dropna()
                sumx += ser.sum()
                n_all += ser.size
            ss_n_sum += pow(sumx, 2) / n_all
    else:
        return None
    # Compute the ((Sx_all)**2)/N_all factor for ALL data in the DataFrame
    n_all = sumx = sumx_p2 = 0
    for i in range(1, len(df.columns)):
        ser = df.iloc[:, i].dropna()
        sumx += ser.sum()
        n_all += ser.size
    sumx_sqed = pow(sumx, 2)
    ss_n_all = sumx_sqed / n_all
    return ss_n_sum - ss_n_all


def ptl_anova2(inframe):
    '''
    Function:  ptl_anova2() for performing TWO way ANOVA on input data

    Input parameters:
    inframe: DataFrame with data groups as follows:
    Column 0: the R-factor determining grouping
    Other Columns: Data grouped according to C-factor

    Returns:
    F: the F statistic for the input data
    p: the p probability for statistical significance
    '''

    # Detecting the shape of inframe:
    rows, cols = inframe.shape

    # Detecting the R x C ANOVA design
    c = len(inframe.columns) - 1
    r_factor = inframe.columns[0]
    anv_groups = inframe.groupby(r_factor)
    r = len(anv_groups)

    # Computing ss_t and n_t with the ss_df() function
    ss_t, n_t = ssd_df(inframe)

    # Computing ss_wg with groupby.agg()
    ss_wg = 0
    ss_wg_cells = anv_groups.agg(ssd)
    ss_wg = ss_wg_cells.sum().sum()

    # Compute ss_bg by subtracking ss_wg from ss_t
    ss_bg = ss_t - ss_wg

    # ADDITIONAL computations in Two way ANOVA: ss_r, ss_c, ss_int
    # a) ss_c
    ss_c = ssd_df_rc(inframe, axis=0)
    # b) ss_r
    ss_r = ssd_df_rc(inframe, axis=1)
    # c) ss_int
    ss_int = ss_bg - ss_r - ss_c
    # degrees of freedom
    df_t = n_t - 1
    df_bg = r*c - 1
    df_wg = df_err = n_t - (r * c)
    df_r = r - 1
    df_c = c - 1
    df_int = df_r * df_c

    # Mean Square (MS) factors
    ms_r = ss_r / df_r
    ms_c = ss_c / df_c
    ms_int = ss_int / df_int
    ms_wg = ms_err = ss_wg / df_wg

    # F, p
    F_r = ms_r / ms_err
    p_r = f.sf(F_r, df_r, df_err, loc=0, scale=1)

    F_c = ms_c / ms_err
    p_c = f.sf(F_c, df_c, df_err, loc=0, scale=1)

    F_int = ms_int / ms_err
    p_int = f.sf(F_int, df_int, df_err, loc=0, scale=1)

    t1 = (ss_bg, df_bg)  # about the difference between groups
    t2 = (ss_r, df_r, ms_r, F_r, p_r)  # about rows
    t3 = (ss_c, df_c, ms_c, F_c, p_c)  # about columns
    t4 = (ss_int, df_int, ms_int, F_int, p_int)  # between groups, row, column
    t5 = (ss_wg, df_wg, ms_wg)  # about withing groups
    t6 = (ss_t, df_t)  # the totals

    return t1, t2, t3, t4, t5, t6
