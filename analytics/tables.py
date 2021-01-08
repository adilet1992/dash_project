import pandas as pd
import numpy as np

def chg_month_to_word(month):
    d = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
         7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}
    return d[month.month] + ' ' + str(month.year)

def chg_npmonth_to_corr(month):
    return month.astype('M8[D]').astype('O')

#Tables of FPD_SPD_TPD by share of amount
def fpd_spd_tpd_0(dff):
    months = dff.MONTH_SIGN_CTR.unique()
    months.sort()
    tab = []
    for month in months:
        amount = dff[dff.MONTH_SIGN_CTR == month]['AMT_CREDIT'].sum()
        fpd0_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_FPD_0_HIST == 1)]['AMT_CREDIT'].sum() / amount
        spd0_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_SPD_0_HIST == 1)]['AMT_CREDIT'].sum() / amount
        tpd0_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_TPD_0_HIST == 1)]['AMT_CREDIT'].sum() / amount
        tab.append({'Месяц выдачи': month, 'Сумма выдачи (в млн.)': amount, 'FPD': fpd0_hist, 'SPD': spd0_hist, 'TPD': tpd0_hist})

    df_tab = pd.DataFrame(tab)
    df_tab = df_tab.reindex(['Месяц выдачи', 'Сумма выдачи (в млн.)', 'FPD', 'SPD', 'TPD'], axis=1)
    df_tab['Сумма выдачи (в млн.)'] = df_tab['Сумма выдачи (в млн.)'].apply(lambda x: int(x / 1000000))
    df_tab['FPD'] = df_tab.FPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['SPD'] = df_tab.SPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['TPD'] = df_tab.TPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['Месяц выдачи'] = df_tab['Месяц выдачи'].apply(lambda x: chg_month_to_word(x))

    df_tab2 = df_tab
    df_tab2['Сумма выдачи (в млн.)'] = df_tab2['Сумма выдачи (в млн.)'].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    return df_tab, df_tab2

def fpd_spd_tpd_5(dff):
    months = dff.MONTH_SIGN_CTR.unique()
    months.sort()
    tab = []
    for month in months:
        amount = dff[dff.MONTH_SIGN_CTR == month]['AMT_CREDIT'].sum()
        fpd5_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_FPD_5_HIST == 1)]['AMT_CREDIT'].sum() / amount
        spd5_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_SPD_5_HIST == 1)]['AMT_CREDIT'].sum() / amount
        tpd5_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_TPD_5_HIST == 1)]['AMT_CREDIT'].sum() / amount
        tab.append({'Месяц выдачи': month, 'Сумма выдачи (в млн.)': amount, 'FPD': fpd5_hist, 'SPD': spd5_hist, 'TPD': tpd5_hist})

    df_tab = pd.DataFrame(tab)
    df_tab = df_tab.reindex(['Месяц выдачи', 'Сумма выдачи (в млн.)', 'FPD', 'SPD', 'TPD'], axis=1)
    df_tab['Сумма выдачи (в млн.)'] = df_tab['Сумма выдачи (в млн.)'].apply(lambda x: int(x / 1000000))
    df_tab['FPD'] = df_tab.FPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['SPD'] = df_tab.SPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['TPD'] = df_tab.TPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['Месяц выдачи'] = df_tab['Месяц выдачи'].apply(lambda x: chg_month_to_word(x))

    df_tab2 = df_tab
    df_tab2['Сумма выдачи (в млн.)'] = df_tab2['Сумма выдачи (в млн.)'].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    return df_tab, df_tab2

def fpd_spd_tpd_15(dff):
    months = dff.MONTH_SIGN_CTR.unique()
    months.sort()
    tab = []
    for month in months:
        amount = dff[dff.MONTH_SIGN_CTR == month]['AMT_CREDIT'].sum()
        fpd15_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_FPD_15_HIST == 1)]['AMT_CREDIT'].sum() / amount
        spd15_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_SPD_15_HIST == 1)]['AMT_CREDIT'].sum() / amount
        tpd15_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_TPD_15_HIST == 1)]['AMT_CREDIT'].sum() / amount
        tab.append({'Месяц выдачи': month, 'Сумма выдачи (в млн.)': amount, 'FPD': fpd15_hist, 'SPD': spd15_hist, 'TPD': tpd15_hist})

    df_tab = pd.DataFrame(tab)
    df_tab = df_tab.reindex(['Месяц выдачи', 'Сумма выдачи (в млн.)', 'FPD', 'SPD', 'TPD'], axis=1)
    df_tab['Сумма выдачи (в млн.)'] = df_tab['Сумма выдачи (в млн.)'].apply(lambda x: int(x / 1000000))
    df_tab['FPD'] = df_tab.FPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['SPD'] = df_tab.SPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['TPD'] = df_tab.TPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['Месяц выдачи'] = df_tab['Месяц выдачи'].apply(lambda x: chg_month_to_word(x))

    df_tab2 = df_tab
    df_tab2['Сумма выдачи (в млн.)'] = df_tab2['Сумма выдачи (в млн.)'].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    return df_tab, df_tab2

def fpd_spd_tpd_30(dff):
    months = dff.MONTH_SIGN_CTR.unique()
    months.sort()
    tab = []
    for month in months:
        amount = dff[dff.MONTH_SIGN_CTR == month]['AMT_CREDIT'].sum()
        fpd30_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_FPD_30_HIST == 1)]['AMT_CREDIT'].sum() / amount
        spd30_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_SPD_30_HIST == 1)]['AMT_CREDIT'].sum() / amount
        tpd30_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_TPD_30_HIST == 1)]['AMT_CREDIT'].sum() / amount
        tab.append({'Месяц выдачи': month, 'Сумма выдачи (в млн.)': amount, 'FPD': fpd30_hist, 'SPD': spd30_hist, 'TPD': tpd30_hist})

    df_tab = pd.DataFrame(tab)
    df_tab = df_tab.reindex(['Месяц выдачи', 'Сумма выдачи (в млн.)', 'FPD', 'SPD', 'TPD'], axis=1)
    df_tab['Сумма выдачи (в млн.)'] = df_tab['Сумма выдачи (в млн.)'].apply(lambda x: int(x / 1000000))
    df_tab['FPD'] = df_tab.FPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['SPD'] = df_tab.SPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['TPD'] = df_tab.TPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['Месяц выдачи'] = df_tab['Месяц выдачи'].apply(lambda x: chg_month_to_word(x))

    df_tab2 = df_tab
    df_tab2['Сумма выдачи (в млн.)'] = df_tab2['Сумма выдачи (в млн.)'].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    return df_tab, df_tab2

def fpd_spd_tpd_45(dff):
    months = dff.MONTH_SIGN_CTR.unique()
    months.sort()
    tab = []
    for month in months:
        amount = dff[dff.MONTH_SIGN_CTR == month]['AMT_CREDIT'].sum()
        fpd45_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_FPD_45_HIST == 1)]['AMT_CREDIT'].sum() / amount
        spd45_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_SPD_45_HIST == 1)]['AMT_CREDIT'].sum() / amount
        tpd45_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_TPD_45_HIST == 1)]['AMT_CREDIT'].sum() / amount
        tab.append({'Месяц выдачи': month, 'Сумма выдачи (в млн.)': amount, 'FPD': fpd45_hist, 'SPD': spd45_hist, 'TPD': tpd45_hist})

    df_tab = pd.DataFrame(tab)
    df_tab = df_tab.reindex(['Месяц выдачи', 'Сумма выдачи (в млн.)', 'FPD', 'SPD', 'TPD'], axis=1)
    df_tab['Сумма выдачи (в млн.)'] = df_tab['Сумма выдачи (в млн.)'].apply(lambda x: int(x / 1000000))
    df_tab['FPD'] = df_tab.FPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['SPD'] = df_tab.SPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['TPD'] = df_tab.TPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['Месяц выдачи'] = df_tab['Месяц выдачи'].apply(lambda x: chg_month_to_word(x))

    df_tab2 = df_tab
    df_tab2['Сумма выдачи (в млн.)'] = df_tab2['Сумма выдачи (в млн.)'].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    return df_tab, df_tab2

def fpd_spd_tpd_60(dff):
    months = dff.MONTH_SIGN_CTR.unique()
    months.sort()
    tab = []
    for month in months:
        amount = dff[dff.MONTH_SIGN_CTR == month]['AMT_CREDIT'].sum()
        fpd60_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_FPD_60_HIST == 1)]['AMT_CREDIT'].sum() / amount
        spd60_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_SPD_60_HIST == 1)]['AMT_CREDIT'].sum() / amount
        tpd60_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_TPD_60_HIST == 1)]['AMT_CREDIT'].sum() / amount
        tab.append({'Месяц выдачи': month, 'Сумма выдачи (в млн.)': amount, 'FPD': fpd60_hist, 'SPD': spd60_hist, 'TPD': tpd60_hist})

    df_tab = pd.DataFrame(tab)
    df_tab = df_tab.reindex(['Месяц выдачи', 'Сумма выдачи (в млн.)', 'FPD', 'SPD', 'TPD'], axis=1)
    df_tab['Сумма выдачи (в млн.)'] = df_tab['Сумма выдачи (в млн.)'].apply(lambda x: int(x / 1000000))
    df_tab['FPD'] = df_tab.FPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['SPD'] = df_tab.SPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['TPD'] = df_tab.TPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['Месяц выдачи'] = df_tab['Месяц выдачи'].apply(lambda x: chg_month_to_word(x))

    df_tab2 = df_tab
    df_tab2['Сумма выдачи (в млн.)'] = df_tab2['Сумма выдачи (в млн.)'].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    return df_tab, df_tab2

def fpd_spd_tpd_90(dff):
    months = dff.MONTH_SIGN_CTR.unique()
    months.sort()
    tab = []
    for month in months:
        amount = dff[dff.MONTH_SIGN_CTR == month]['AMT_CREDIT'].sum()
        fpd90_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_FPD_90_HIST == 1)]['AMT_CREDIT'].sum() / amount
        spd90_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_SPD_90_HIST == 1)]['AMT_CREDIT'].sum() / amount
        tpd90_hist = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_TPD_90_HIST == 1)]['AMT_CREDIT'].sum() / amount
        tab.append({'Месяц выдачи': month, 'Сумма выдачи (в млн.)': amount, 'FPD': fpd90_hist, 'SPD': spd90_hist, 'TPD': tpd90_hist})

    df_tab = pd.DataFrame(tab)
    df_tab = df_tab.reindex(['Месяц выдачи', 'Сумма выдачи (в млн.)', 'FPD', 'SPD', 'TPD'], axis=1)
    df_tab['Сумма выдачи (в млн.)'] = df_tab['Сумма выдачи (в млн.)'].apply(lambda x: int(x / 1000000))
    df_tab['FPD'] = df_tab.FPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['SPD'] = df_tab.SPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['TPD'] = df_tab.TPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['Месяц выдачи'] = df_tab['Месяц выдачи'].apply(lambda x: chg_month_to_word(x))

    df_tab2 = df_tab
    df_tab2['Сумма выдачи (в млн.)'] = df_tab2['Сумма выдачи (в млн.)'].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    return df_tab, df_tab2

def fpd_spd_tpd_active(dff):
    months = dff.MONTH_SIGN_CTR.unique()
    months.sort()
    tab = []
    for month in months:
        amount = dff[dff.MONTH_SIGN_CTR == month]['AMT_CREDIT'].sum()
        fpd_active = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_FPD_ACTIVE == 1)]['AMT_CREDIT'].sum() / amount
        spd_active = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_SPD_ACTIVE == 1)]['AMT_CREDIT'].sum() / amount
        tpd_active = dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_TPD_ACTIVE == 1)]['AMT_CREDIT'].sum() / amount
        tab.append({'Месяц выдачи': month, 'Сумма выдачи (в млн.)': amount, 'FPD': fpd_active, 'SPD': spd_active, 'TPD': tpd_active})

    df_tab = pd.DataFrame(tab)
    df_tab = df_tab.reindex(['Месяц выдачи', 'Сумма выдачи (в млн.)', 'FPD', 'SPD', 'TPD'], axis=1)
    df_tab['Сумма выдачи (в млн.)'] = df_tab['Сумма выдачи (в млн.)'].apply(lambda x: int(x / 1000000))
    df_tab['FPD'] = df_tab.FPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['SPD'] = df_tab.SPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['TPD'] = df_tab.TPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['Месяц выдачи'] = df_tab['Месяц выдачи'].apply(lambda x: chg_month_to_word(x))

    df_tab2 = df_tab
    df_tab2['Сумма выдачи (в млн.)'] = df_tab2['Сумма выдачи (в млн.)'].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    return df_tab, df_tab2

#Tables of FPD_SPD_TPD by share of count
def fpd_spd_tpd_0_sc(dff):
    months = dff.MONTH_SIGN_CTR.unique()
    months.sort()
    tab = []
    for month in months:
        common = len(dff[dff.MONTH_SIGN_CTR == month])
        fpd0_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_FPD_0_HIST == 1)]) / common
        spd0_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_SPD_0_HIST == 1)]) / common
        tpd0_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_TPD_0_HIST == 1)]) / common
        tab.append({'Месяц выдачи': month, 'Кол-во выдачи': common, 'FPD': fpd0_hist, 'SPD': spd0_hist, 'TPD': tpd0_hist})

    df_tab = pd.DataFrame(tab)
    df_tab = df_tab.reindex(['Месяц выдачи', 'Кол-во выдачи', 'FPD', 'SPD', 'TPD'], axis=1)
    df_tab['FPD'] = df_tab.FPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['SPD'] = df_tab.SPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['TPD'] = df_tab.TPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['Месяц выдачи'] = df_tab['Месяц выдачи'].apply(lambda x: chg_month_to_word(x))

    df_tab2 = df_tab
    df_tab2['Кол-во выдачи'] = df_tab2['Кол-во выдачи'].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    return df_tab, df_tab2

def fpd_spd_tpd_5_sc(dff):
    months = dff.MONTH_SIGN_CTR.unique()
    months.sort()
    tab = []
    for month in months:
        common = len(dff[dff.MONTH_SIGN_CTR == month])
        fpd5_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_FPD_5_HIST == 1)]) / common
        spd5_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_SPD_5_HIST == 1)]) / common
        tpd5_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_TPD_5_HIST == 1)]) / common
        tab.append({'Месяц выдачи': month, 'Кол-во выдачи': common, 'FPD': fpd5_hist, 'SPD': spd5_hist, 'TPD': tpd5_hist})

    df_tab = pd.DataFrame(tab)
    df_tab = df_tab.reindex(['Месяц выдачи', 'Кол-во выдачи', 'FPD', 'SPD', 'TPD'], axis=1)
    df_tab['FPD'] = df_tab.FPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['SPD'] = df_tab.SPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['TPD'] = df_tab.TPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['Месяц выдачи'] = df_tab['Месяц выдачи'].apply(lambda x: chg_month_to_word(x))

    df_tab2 = df_tab
    df_tab2['Кол-во выдачи'] = df_tab2['Кол-во выдачи'].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    return df_tab, df_tab2

def fpd_spd_tpd_15_sc(dff):
    months = dff.MONTH_SIGN_CTR.unique()
    months.sort()
    tab = []
    for month in months:
        common = len(dff[dff.MONTH_SIGN_CTR == month])
        fpd15_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_FPD_15_HIST == 1)]) / common
        spd15_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_SPD_15_HIST == 1)]) / common
        tpd15_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_TPD_15_HIST == 1)]) / common
        tab.append({'Месяц выдачи': month, 'Кол-во выдачи': common, 'FPD': fpd15_hist, 'SPD': spd15_hist, 'TPD': tpd15_hist})

    df_tab = pd.DataFrame(tab)
    df_tab = df_tab.reindex(['Месяц выдачи', 'Кол-во выдачи', 'FPD', 'SPD', 'TPD'], axis=1)
    df_tab['FPD'] = df_tab.FPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['SPD'] = df_tab.SPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['TPD'] = df_tab.TPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['Месяц выдачи'] = df_tab['Месяц выдачи'].apply(lambda x: chg_month_to_word(x))

    df_tab2 = df_tab
    df_tab2['Кол-во выдачи'] = df_tab2['Кол-во выдачи'].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    return df_tab, df_tab2

def fpd_spd_tpd_30_sc(dff):
    months = dff.MONTH_SIGN_CTR.unique()
    months.sort()
    tab = []
    for month in months:
        common = len(dff[dff.MONTH_SIGN_CTR == month])
        fpd30_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_FPD_30_HIST == 1)]) / common
        spd30_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_SPD_30_HIST == 1)]) / common
        tpd30_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_TPD_30_HIST == 1)]) / common
        tab.append({'Месяц выдачи': month, 'Кол-во выдачи': common, 'FPD': fpd30_hist, 'SPD': spd30_hist, 'TPD': tpd30_hist})

    df_tab = pd.DataFrame(tab)
    df_tab = df_tab.reindex(['Месяц выдачи', 'Кол-во выдачи', 'FPD', 'SPD', 'TPD'], axis=1)
    df_tab['FPD'] = df_tab.FPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['SPD'] = df_tab.SPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['TPD'] = df_tab.TPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['Месяц выдачи'] = df_tab['Месяц выдачи'].apply(lambda x: chg_month_to_word(x))

    df_tab2 = df_tab
    df_tab2['Кол-во выдачи'] = df_tab2['Кол-во выдачи'].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    return df_tab, df_tab2

def fpd_spd_tpd_45_sc(dff):
    months = dff.MONTH_SIGN_CTR.unique()
    months.sort()
    tab = []
    for month in months:
        common = len(dff[dff.MONTH_SIGN_CTR == month])
        fpd45_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_FPD_45_HIST == 1)]) / common
        spd45_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_SPD_45_HIST == 1)]) / common
        tpd45_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_TPD_45_HIST == 1)]) / common
        tab.append({'Месяц выдачи': month, 'Кол-во выдачи': common, 'FPD': fpd45_hist, 'SPD': spd45_hist, 'TPD': tpd45_hist})

    df_tab = pd.DataFrame(tab)
    df_tab = df_tab.reindex(['Месяц выдачи', 'Кол-во выдачи', 'FPD', 'SPD', 'TPD'], axis=1)
    df_tab['FPD'] = df_tab.FPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['SPD'] = df_tab.SPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['TPD'] = df_tab.TPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['Месяц выдачи'] = df_tab['Месяц выдачи'].apply(lambda x: chg_month_to_word(x))

    df_tab2 = df_tab
    df_tab2['Кол-во выдачи'] = df_tab2['Кол-во выдачи'].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    return df_tab, df_tab2

def fpd_spd_tpd_60_sc(dff):
    months = dff.MONTH_SIGN_CTR.unique()
    months.sort()
    tab = []
    for month in months:
        common = len(dff[dff.MONTH_SIGN_CTR == month])
        fpd60_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_FPD_60_HIST == 1)]) / common
        spd60_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_SPD_60_HIST == 1)]) / common
        tpd60_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_TPD_60_HIST == 1)]) / common
        tab.append({'Месяц выдачи': month, 'Кол-во выдачи': common, 'FPD': fpd60_hist, 'SPD': spd60_hist, 'TPD': tpd60_hist})

    df_tab = pd.DataFrame(tab)
    df_tab = df_tab.reindex(['Месяц выдачи', 'Кол-во выдачи', 'FPD', 'SPD', 'TPD'], axis=1)
    df_tab['FPD'] = df_tab.FPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['SPD'] = df_tab.SPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['TPD'] = df_tab.TPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['Месяц выдачи'] = df_tab['Месяц выдачи'].apply(lambda x: chg_month_to_word(x))

    df_tab2 = df_tab
    df_tab2['Кол-во выдачи'] = df_tab2['Кол-во выдачи'].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    return df_tab, df_tab2

def fpd_spd_tpd_90_sc(dff):
    months = dff.MONTH_SIGN_CTR.unique()
    months.sort()
    tab = []
    for month in months:
        common = len(dff[dff.MONTH_SIGN_CTR == month])
        fpd90_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_FPD_90_HIST == 1)]) / common
        spd90_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_SPD_90_HIST == 1)]) / common
        tpd90_hist = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_TPD_90_HIST == 1)]) / common
        tab.append({'Месяц выдачи': month, 'Кол-во выдачи': common, 'FPD': fpd90_hist, 'SPD': spd90_hist, 'TPD': tpd90_hist})

    df_tab = pd.DataFrame(tab)
    df_tab = df_tab.reindex(['Месяц выдачи', 'Кол-во выдачи', 'FPD', 'SPD', 'TPD'], axis=1)
    df_tab['FPD'] = df_tab.FPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['SPD'] = df_tab.SPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['TPD'] = df_tab.TPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['Месяц выдачи'] = df_tab['Месяц выдачи'].apply(lambda x: chg_month_to_word(x))

    df_tab2 = df_tab
    df_tab2['Кол-во выдачи'] = df_tab2['Кол-во выдачи'].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    return df_tab, df_tab2

def fpd_spd_tpd_active_sc(dff):
    months = dff.MONTH_SIGN_CTR.unique()
    months.sort()
    tab = []
    for month in months:
        common = len(dff[dff.MONTH_SIGN_CTR == month])
        fpd_active = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_FPD_ACTIVE == 1)]) / common
        spd_active = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_SPD_ACTIVE == 1)]) / common
        tpd_active = len(dff[(dff.MONTH_SIGN_CTR == month) & (dff.FLAG_TPD_ACTIVE == 1)]) / common
        tab.append({'Месяц выдачи': month, 'Кол-во выдачи': common, 'FPD': fpd_active, 'SPD': spd_active, 'TPD': tpd_active})

    df_tab = pd.DataFrame(tab)
    df_tab = df_tab.reindex(['Месяц выдачи', 'Кол-во выдачи', 'FPD', 'SPD', 'TPD'], axis=1)
    df_tab['FPD'] = df_tab.FPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['SPD'] = df_tab.SPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['TPD'] = df_tab.TPD.apply(lambda x: str(round(x * 100, 2)) + '%')
    df_tab['Месяц выдачи'] = df_tab['Месяц выдачи'].apply(lambda x: chg_month_to_word(x))

    df_tab2 = df_tab
    df_tab2['Кол-во выдачи'] = df_tab2['Кол-во выдачи'].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    return df_tab, df_tab2

#Tables of Approval rate analytics
def appr_table(ar):
    rus_columns = ['Дата', 'Заявки нерассмотренные скоринговой системой', 'Заявки рассмотренные скоринговой системой',
                   'Одобренные заявки с учетом альтернативных предложений',
                   'Уровень одобрения с учетом альтернативных предложений, %',
                   'Одобренные заявки без учета альтернативных предложений',
                   'Уровень одобрения без учета альтернативных предложений, %', 'Запрошенная сумма', 'Одобренная сумма',
                   'Количество выданных займов', 'Выданная сумма',
                   'Уровень выдачи от одобренной суммы, %', 'Конверсия в выдачу с учетом альтернативных предложений',
                   'Конверсия в выдачу без учета альтернативных предложений']

    ar2 = ar.groupby('DREG').sum().reset_index()
    ar2['REVIEWED'] = ar2.CNT - ar2.CANCEL
    ar2['AR_W_ALT'] = ar2.ACC / ar2.REVIEWED
    ar2['AR_WO_ALT'] = ar2.ACC2 / ar2.REVIEWED
    ar2['ISSUE_RATE'] = ar2.LOAN_AMT / ar2.ACC_AMT
    ar2['LOAN_S_MIN'] = ar2.LOAN_S_MIN.apply(lambda x: '{:,}'.format(int(x)).replace(',', ' '))
    ar2['ACC_AMT'] = ar2.ACC_AMT.apply(lambda x: '{:,}'.format(int(x)).replace(',', ' '))
    ar2['LOAN_AMT'] = ar2.LOAN_AMT.apply(lambda x: '{:,}'.format(int(x)).replace(',', ' '))
    ar2['CONVERCY_W_A'] = ar2.ACC_LOAN / ar2.ACC
    ar2['CONVERCY_WO_A'] = ar2.ACC_LOAN / ar2.ACC2
    ar2['AR_W_ALT'] = ar2.AR_W_ALT.apply(lambda x: str(round(x * 100, 1)) + ' %')
    ar2['AR_WO_ALT'] = ar2.AR_WO_ALT.apply(lambda x: str(round(x * 100, 1)) + ' %')
    ar2['ISSUE_RATE'] = ar2.ISSUE_RATE.apply(lambda x: str(round(x * 100, 1)) + ' %')
    ar2['CONVERCY_W_A'] = ar2.CONVERCY_W_A.apply(lambda x: str(round(x * 100, 1)) + ' %')
    ar2['CONVERCY_WO_A'] = ar2.CONVERCY_WO_A.apply(lambda x: str(round(x * 100, 1)) + ' %')
    ar2['ISSUE_RATE'] = ar2.ISSUE_RATE.apply(lambda x: '' if x.find('nan') != -1 else x)
    ar2['CONVERCY_W_A'] = ar2.CONVERCY_W_A.apply(lambda x: '' if x.find('nan') != -1 else x)
    ar2['CONVERCY_WO_A'] = ar2.CONVERCY_WO_A.apply(lambda x: '' if x.find('nan') != -1 else x)
    ar2['AR_W_ALT'] = ar2.AR_W_ALT.apply(lambda x: '' if x.find('nan') != -1 else x)
    ar2['AR_WO_ALT'] = ar2.AR_WO_ALT.apply(lambda x: '' if x.find('nan') != -1 else x)
    ar2 = ar2.reindex(
        ['DREG', 'CANCEL', 'REVIEWED', 'ACC', 'AR_W_ALT', 'ACC2', 'AR_WO_ALT', 'LOAN_S_MIN', 'ACC_AMT', 'ACC_LOAN',
         'LOAN_AMT', 'ISSUE_RATE', 'CONVERCY_W_A', 'CONVERCY_WO_A'], axis=1)
    ar2.columns = rus_columns

    return ar2

def appr_table_week(ar):
    rus_columns = ['Дата', 'Заявки нерассмотренные скоринговой системой', 'Заявки рассмотренные скоринговой системой',
                   'Одобренные заявки с учетом альтернативных предложений',
                   'Уровень одобрения с учетом альтернативных предложений, %',
                   'Одобренные заявки без учета альтернативных предложений',
                   'Уровень одобрения без учета альтернативных предложений, %', 'Запрошенная сумма', 'Одобренная сумма',
                   'Количество выданных займов', 'Выданная сумма',
                   'Уровень выдачи от одобренной суммы, %', 'Конверсия в выдачу с учетом альтернативных предложений',
                   'Конверсия в выдачу без учета альтернативных предложений']

    ar = ar.sort_values(by='DREG')
    ar2 = ar.groupby('WEEK', sort=False).sum().reset_index()
    ar2['REVIEWED'] = ar2.CNT - ar2.CANCEL
    ar2['AR_W_ALT'] = ar2.ACC / ar2.REVIEWED
    ar2['AR_WO_ALT'] = ar2.ACC2 / ar2.REVIEWED
    ar2['ISSUE_RATE'] = ar2.LOAN_AMT / ar2.ACC_AMT
    ar2['LOAN_S_MIN'] = ar2.LOAN_S_MIN.apply(lambda x: '{:,}'.format(int(x)).replace(',', ' '))
    ar2['ACC_AMT'] = ar2.ACC_AMT.apply(lambda x: '{:,}'.format(int(x)).replace(',', ' '))
    ar2['LOAN_AMT'] = ar2.LOAN_AMT.apply(lambda x: '{:,}'.format(int(x)).replace(',', ' '))
    ar2['CONVERCY_W_A'] = ar2.ACC_LOAN / ar2.ACC
    ar2['CONVERCY_WO_A'] = ar2.ACC_LOAN / ar2.ACC2
    ar2['AR_W_ALT'] = ar2.AR_W_ALT.apply(lambda x: str(round(x * 100, 1)) + ' %')
    ar2['AR_WO_ALT'] = ar2.AR_WO_ALT.apply(lambda x: str(round(x * 100, 1)) + ' %')
    ar2['ISSUE_RATE'] = ar2.ISSUE_RATE.apply(lambda x: str(round(x * 100, 1)) + ' %')
    ar2['CONVERCY_W_A'] = ar2.CONVERCY_W_A.apply(lambda x: str(round(x * 100, 1)) + ' %')
    ar2['CONVERCY_WO_A'] = ar2.CONVERCY_WO_A.apply(lambda x: str(round(x * 100, 1)) + ' %')
    ar2['ISSUE_RATE'] = ar2.ISSUE_RATE.apply(lambda x: '' if x.find('nan') != -1 else x)
    ar2['CONVERCY_W_A'] = ar2.CONVERCY_W_A.apply(lambda x: '' if x.find('nan') != -1 else x)
    ar2['CONVERCY_WO_A'] = ar2.CONVERCY_WO_A.apply(lambda x: '' if x.find('nan') != -1 else x)
    ar2['AR_W_ALT'] = ar2.AR_W_ALT.apply(lambda x: '' if x.find('nan') != -1 else x)
    ar2['AR_WO_ALT'] = ar2.AR_WO_ALT.apply(lambda x: '' if x.find('nan') != -1 else x)
    ar2 = ar2.reindex(
        ['WEEK', 'CANCEL', 'REVIEWED', 'ACC', 'AR_W_ALT', 'ACC2', 'AR_WO_ALT', 'LOAN_S_MIN', 'ACC_AMT', 'ACC_LOAN',
         'LOAN_AMT', 'ISSUE_RATE', 'CONVERCY_W_A', 'CONVERCY_WO_A'], axis=1)
    ar2.columns = rus_columns

    return ar2

def appr_table_month(ar):
    rus_columns = ['Дата', 'Заявки нерассмотренные скоринговой системой', 'Заявки рассмотренные скоринговой системой',
                   'Одобренные заявки с учетом альтернативных предложений',
                   'Уровень одобрения с учетом альтернативных предложений, %',
                   'Одобренные заявки без учета альтернативных предложений',
                   'Уровень одобрения без учета альтернативных предложений, %', 'Запрошенная сумма', 'Одобренная сумма',
                   'Количество выданных займов', 'Выданная сумма',
                   'Уровень выдачи от одобренной суммы, %', 'Конверсия в выдачу с учетом альтернативных предложений',
                   'Конверсия в выдачу без учета альтернативных предложений']

    ar = ar.sort_values(by='DREG')
    ar2 = ar.groupby('MONTH_IN_WORD', sort=False).sum().reset_index()
    ar2['REVIEWED'] = ar2.CNT - ar2.CANCEL
    ar2['AR_W_ALT'] = ar2.ACC / ar2.REVIEWED
    ar2['AR_WO_ALT'] = ar2.ACC2 / ar2.REVIEWED
    ar2['ISSUE_RATE'] = ar2.LOAN_AMT / ar2.ACC_AMT
    ar2['LOAN_S_MIN'] = ar2.LOAN_S_MIN.apply(lambda x: '{:,}'.format(int(x)).replace(',', ' '))
    ar2['ACC_AMT'] = ar2.ACC_AMT.apply(lambda x: '{:,}'.format(int(x)).replace(',', ' '))
    ar2['LOAN_AMT'] = ar2.LOAN_AMT.apply(lambda x: '{:,}'.format(int(x)).replace(',', ' '))
    ar2['CONVERCY_W_A'] = ar2.ACC_LOAN / ar2.ACC
    ar2['CONVERCY_WO_A'] = ar2.ACC_LOAN / ar2.ACC2
    ar2['AR_W_ALT'] = ar2.AR_W_ALT.apply(lambda x: str(round(x * 100, 1)) + ' %')
    ar2['AR_WO_ALT'] = ar2.AR_WO_ALT.apply(lambda x: str(round(x * 100, 1)) + ' %')
    ar2['ISSUE_RATE'] = ar2.ISSUE_RATE.apply(lambda x: str(round(x * 100, 1)) + ' %')
    ar2['CONVERCY_W_A'] = ar2.CONVERCY_W_A.apply(lambda x: str(round(x * 100, 1)) + ' %')
    ar2['CONVERCY_WO_A'] = ar2.CONVERCY_WO_A.apply(lambda x: str(round(x * 100, 1)) + ' %')
    ar2['ISSUE_RATE'] = ar2.ISSUE_RATE.apply(lambda x: '' if x.find('nan') != -1 else x)
    ar2['CONVERCY_W_A'] = ar2.CONVERCY_W_A.apply(lambda x: '' if x.find('nan') != -1 else x)
    ar2['CONVERCY_WO_A'] = ar2.CONVERCY_WO_A.apply(lambda x: '' if x.find('nan') != -1 else x)
    ar2['AR_W_ALT'] = ar2.AR_W_ALT.apply(lambda x: '' if x.find('nan') != -1 else x)
    ar2['AR_WO_ALT'] = ar2.AR_WO_ALT.apply(lambda x: '' if x.find('nan') != -1 else x)
    ar2 = ar2.reindex(
        ['MONTH_IN_WORD', 'CANCEL', 'REVIEWED', 'ACC', 'AR_W_ALT', 'ACC2', 'AR_WO_ALT', 'LOAN_S_MIN', 'ACC_AMT',
         'ACC_LOAN', 'LOAN_AMT', 'ISSUE_RATE', 'CONVERCY_W_A', 'CONVERCY_WO_A'], axis=1)
    ar2.columns = rus_columns

    return ar2

def reason_table(ar):
    ar = ar.sort_values(by='DREG')
    months = ar.MONTH_IN_WORD.unique()
    df_ = pd.DataFrame(index=ar.GROUPOFREJECT.unique())
    for month in months:
        ar_ = ar[ar.MONTH_IN_WORD == month].groupby('GROUPOFREJECT')['CNT'].sum()
        ar_ = ar_ / ar_.sum()
        df_ = pd.concat([df_, ar_], axis=1)
    df_.columns = months
    df_ = df_.replace(np.nan, '')
    for col in df_.columns:
        df_[col] = df_[col].apply(lambda x: str(round(x * 100, 1)) + ' %' if x != '' else x)

    df_ = df_.reset_index()
    df_ = df_.rename(columns={'index': 'Отказы'})
    return df_

def reason_graph_table(ar):
    ar = ar.sort_values(by='DREG')
    months = ar.MONTH_IN_WORD.unique()
    tab = []
    for month in months:
        total = ar[ar.MONTH_IN_WORD == month].CNT.sum()
        appr = ar[(ar.MONTH_IN_WORD == month) & (ar.GROUPOFREJECT == 'Одобрено')].CNT.sum()
        tab.append({'Месяц выдачи': month, 'Одобрено': appr / total, 'Отказано': 1 - appr / total})
    df_tab = pd.DataFrame(tab)
    df_tab['Одобрено'] = df_tab['Одобрено'].apply(lambda x: str(round(x * 100, 1)) + ' %')
    df_tab['Отказано'] = df_tab['Отказано'].apply(lambda x: str(round(x * 100, 1)) + ' %')
    return df_tab

def reason_alerts_table(ar):
    ar = ar.sort_values(by='DREG')
    months = ar.MONTH_IN_WORD.unique()
    df_ = pd.DataFrame(index=ar.GROUPOFALERTS.unique())
    for month in months:
        ar_ = ar[ar.MONTH_IN_WORD == month].groupby('GROUPOFALERTS')['CNT'].sum()
        ar_ = ar_ / ar_.sum()
        df_ = pd.concat([df_, ar_], axis=1)
    df_.columns = months
    df_ = df_.replace(np.nan, '')
    for col in df_.columns:
        df_[col] = df_[col].apply(lambda x: str(round(x * 100, 1)) + ' %' if x != '' else x)

    df_ = df_.reset_index()
    df_ = df_.rename(columns={'index': 'Отказы'})
    return df_

def reason_names_table(ar):
    ar = ar.sort_values(by='DREG')
    months = ar.MONTH_IN_WORD.unique()
    df_ = pd.DataFrame(index=ar.REASON_NAME.unique())
    for month in months:
        ar_ = ar[ar.MONTH_IN_WORD == month].groupby('REASON_NAME')['CNT'].sum()
        ar_ = ar_ / ar_.sum()
        df_ = pd.concat([df_, ar_], axis=1)
    df_.columns = months
    df_ = df_.replace(np.nan, '')
    for col in df_.columns:
        df_[col] = df_[col].apply(lambda x: str(round(x * 100, 1)) + ' %' if x != '' else x)

    df_ = df_.reset_index()
    df_ = df_.rename(columns={'index': 'Отказы'})
    return df_

def create_pivot(ar, pivot_cols, pivot_rows, pivot_value, pivot_type, pivot_addition):
    if pivot_addition == 'Без вычислений':
        piv = pd.pivot_table(ar, index=pivot_rows, columns=pivot_cols, values=pivot_value, aggfunc=pivot_type, fill_value='')
        for col in piv.columns:
            piv[col] = piv[col].apply(lambda x: '{:,}'.format(int(x)).replace(',', ' ') if x != '' else x)
        piv = piv.reset_index()

        return piv
    if pivot_addition == 'Доля от суммы столбца':
        piv = pd.pivot_table(ar, index=pivot_rows, columns=pivot_cols, values=pivot_value, aggfunc=pivot_type, fill_value=0)
        for col in piv.columns:
            sum_col = piv[col].sum()
            if sum_col > 0:
                piv[col] = piv[col]/sum_col

        for col in piv.columns:
            piv[col] = piv[col].apply(lambda x: str(round(x*100, 2)) + '%')
        piv = piv.reset_index()

        return piv

    if pivot_addition == 'Доля от общей суммы':
        piv = pd.pivot_table(ar, index=pivot_rows, columns=pivot_cols, values=pivot_value, aggfunc=pivot_type, fill_value=0)
        sum_all = sum([piv[col].sum() for col in piv.columns])
        if sum_all > 0:
            piv = piv/sum_all

        for col in piv.columns:
            piv[col] = piv[col].apply(lambda x: str(round(x * 100, 2)) + '%')
        piv = piv.reset_index()

        return piv


def arbitrary_pivot(ar, values, pivot_rows):
    pivots = []
    for value in values:
        name = value[0]
        formula = value[1]
        operation = value[2]

        formula = chg_to_right_formula(formula, ar)
        ar[name] = pd.eval(formula)
        d_operations = {'Сумма': np.sum, 'Среднее': np.mean, 'Медиана': np.median, 'Максимум': np.max, 'Минимум': np.min}
        pivot = pd.pivot_table(ar, index=pivot_rows, aggfunc={name: d_operations[operation]}, values=name)
        pivots.append(pivot)

    df_all = pd.concat(pivots, axis=1)
    #df_all = df_all.replace(np.nan, 0)
    sum_all = 0
    for col in df_all.columns:
        sum_all += df_all[col].sum()

    for value in values:
        name = value[0]
        additional = value[3]
        other = value[4]
        if additional == 'Доля от суммы столбца':
            df_all[name] = df_all[name]/df_all[name].sum()
            df_all[name] = df_all[name].apply(lambda x: str(round(x*100, 1)) + '%')
        if additional == 'Доля от общей суммы':
            df_all[name] = df_all[name]/sum_all
            df_all[name] = df_all[name].apply(lambda x: str(round(x * 100, 1)) + '%')
        if additional == 'Доля от суммы другого значения' and other:
            other = chg_to_right_formula(other, ar)
            ar[other] = pd.eval(other)
            pivot_other = pd.pivot_table(ar, index=pivot_rows, aggfunc={other: np.sum}, values=other)
            df_all[name] = df_all[name]/pivot_other[other]
            df_all[name] = df_all[name].apply(lambda x: str(round(x * 100, 1)) + '%')

    df_all = df_all.reset_index()
    return df_all

def chg_to_right_formula(s, ar):
    k = 0
    d = {}

    for col in ar.columns:
        if col in s:
            s = s[:s.find(col)] + chr(97 + k) + s[s.find(col) + len(col):]
            d[chr(97 + k)] = 'ar.' + col
            k += 1

    res = ""
    for c in s:
        if c in d:
            res += d[c]
        else:
            res += c

    return res

def vintage_table_5(df):
    given_months = list(df.GIVEN_MONTH.unique())
    given_months.sort()

    report_months = list(df.REPORT_MONTH.unique())
    report_months.sort(reverse=True)

    main_df = pd.DataFrame(index=given_months)
    for report_month in report_months:
        data = df[df.REPORT_MONTH == report_month][['GIVEN_MONTH', 'DEBT_AMOUNT_5_PLUS', 'LOAN_SUM']]
        data = data.groupby('GIVEN_MONTH').sum()
        data['RATIO'] = round(data['DEBT_AMOUNT_5_PLUS'] / data['LOAN_SUM'] * 100, 2).astype(str) + '%'
        main_df = pd.concat([main_df, data['RATIO']], axis=1)

    main_df.columns = [chg_month_to_word(chg_npmonth_to_corr(report_month)) for report_month in report_months]
    main_df.index = [chg_month_to_word(chg_npmonth_to_corr(given_month)) for given_month in given_months]
    main_df = main_df.replace(np.nan, '')
    main_df = main_df.reset_index()
    #main_df = main_df.reset_index().rename(columns={main_df.index.name: 'Поколение выдачи'})
    main_df.columns = ['Поколение выдачи'] + [chg_month_to_word(chg_npmonth_to_corr(report_month)) for report_month in report_months]

    return main_df

def vintage_table_30(df):
    given_months = list(df.GIVEN_MONTH.unique())
    given_months.sort()

    report_months = list(df.REPORT_MONTH.unique())
    report_months.sort(reverse=True)

    main_df = pd.DataFrame(index=given_months)
    for report_month in report_months:
        data = df[df.REPORT_MONTH == report_month][['GIVEN_MONTH', 'DEBT_AMOUNT_30_PLUS', 'LOAN_SUM']]
        data = data.groupby('GIVEN_MONTH').sum()
        data['RATIO'] = round(data['DEBT_AMOUNT_30_PLUS'] / data['LOAN_SUM'] * 100, 2).astype(str) + '%'
        main_df = pd.concat([main_df, data['RATIO']], axis=1)

    main_df.columns = [chg_month_to_word(chg_npmonth_to_corr(report_month)) for report_month in report_months]
    main_df.index = [chg_month_to_word(chg_npmonth_to_corr(given_month)) for given_month in given_months]
    main_df = main_df.replace(np.nan, '')
    main_df = main_df.reset_index()
    #main_df = main_df.reset_index().rename(columns={main_df.index.name: 'Поколение выдачи'})
    main_df.columns = ['Поколение выдачи'] + [chg_month_to_word(chg_npmonth_to_corr(report_month)) for report_month in report_months]

    return main_df

def vintage_table_60(df):
    given_months = list(df.GIVEN_MONTH.unique())
    given_months.sort()

    report_months = list(df.REPORT_MONTH.unique())
    report_months.sort(reverse=True)

    main_df = pd.DataFrame(index=given_months)
    for report_month in report_months:
        data = df[df.REPORT_MONTH == report_month][['GIVEN_MONTH', 'DEBT_AMOUNT_60_PLUS', 'LOAN_SUM']]
        data = data.groupby('GIVEN_MONTH').sum()
        data['RATIO'] = round(data['DEBT_AMOUNT_60_PLUS'] / data['LOAN_SUM'] * 100, 2).astype(str) + '%'
        main_df = pd.concat([main_df, data['RATIO']], axis=1)

    main_df.columns = [chg_month_to_word(chg_npmonth_to_corr(report_month)) for report_month in report_months]
    main_df.index = [chg_month_to_word(chg_npmonth_to_corr(given_month)) for given_month in given_months]
    main_df = main_df.replace(np.nan, '')
    main_df = main_df.reset_index()
    #main_df = main_df.reset_index().rename(columns={main_df.index.name: 'Поколение выдачи'})
    main_df.columns = ['Поколение выдачи'] + [chg_month_to_word(chg_npmonth_to_corr(report_month)) for report_month in report_months]

    return main_df

def vintage_table_90(df):
    given_months = list(df.GIVEN_MONTH.unique())
    given_months.sort()

    report_months = list(df.REPORT_MONTH.unique())
    report_months.sort(reverse=True)

    main_df = pd.DataFrame(index=given_months)
    for report_month in report_months:
        data = df[df.REPORT_MONTH == report_month][['GIVEN_MONTH', 'DEBT_AMOUNT_90_PLUS', 'LOAN_SUM']]
        data = data.groupby('GIVEN_MONTH').sum()
        data['RATIO'] = round(data['DEBT_AMOUNT_90_PLUS'] / data['LOAN_SUM'] * 100, 2).astype(str) + '%'
        main_df = pd.concat([main_df, data['RATIO']], axis=1)

    main_df.columns = [chg_month_to_word(chg_npmonth_to_corr(report_month)) for report_month in report_months]
    main_df.index = [chg_month_to_word(chg_npmonth_to_corr(given_month)) for given_month in given_months]
    main_df = main_df.replace(np.nan, '')
    main_df = main_df.reset_index()
    #main_df = main_df.reset_index().rename(columns={main_df.index.name: 'Поколение выдачи'})
    main_df.columns = ['Поколение выдачи'] + [chg_month_to_word(chg_npmonth_to_corr(report_month)) for report_month in report_months]

    return main_df
