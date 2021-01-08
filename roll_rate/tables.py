import pandas as pd
import datetime
import numpy as np

def create_features(df):
    df = df.reset_index()
    df.BASE_YMD = df.BASE_YMD.apply(lambda x: datetime.date(x.year, x.month, x.day))
    operdates = list(df.BASE_YMD.unique())
    operdates.sort()
    df['DEBT_RATIO'] = df['TOTAL_DEBT1'] / df.TOTAL_DEBT
    df['COUNT_RATIO'] = df.LOAN_CTID / df.TOTAL_LOAN_CTID
    df['LOAN_OPERDATE'] = df.BASE_YMD.apply(lambda x: df[df.BASE_YMD == x]['TOTAL_DEBT1'].sum())
    df['LOAN_RATIO'] = df['TOTAL_DEBT1'] / df['LOAN_OPERDATE']
    df['LOAN_CTID2'] = np.nan
    df['TOTAL_DEBT_2'] = np.nan
    for i in range(len(df)):
        oper = df.BASE_YMD.iloc[i]
        product = df.PRODUCT.iloc[i]
        if operdates.index(oper) > 0:
            if len(df[(df.PRODUCT == product) & (df.BASE_YMD == operdates[operdates.index(oper) - 1])]) > 0:
                df.at[i, 'LOAN_CTID2'] = df[(df.PRODUCT == product) & (df.BASE_YMD == operdates[operdates.index(oper) - 1])].LOAN_CTID.iloc[0]
            if len(df[(df.PRODUCT == product) & (df.BASE_YMD == operdates[operdates.index(oper) - 1])]) > 0:
                df.at[i, 'TOTAL_DEBT_2'] = df[(df.PRODUCT == product) & (df.BASE_YMD == operdates[operdates.index(oper) - 1])].TOTAL_DEBT1.iloc[0]

    df['COUNT_DYNAMIC'] = df.LOAN_CTID / df.LOAN_CTID2 - 1
    df['DEBT_DYNAMIC'] = df['TOTAL_DEBT1'] / df.TOTAL_DEBT_2 - 1

    df = df.drop(['LOAN_OPERDATE', 'LOAN_CTID2', 'TOTAL_DEBT_2'], axis=1)

    return df

def create_features_daily(df):
    df = df.reset_index()
    df.BASE_YMD = df.BASE_YMD.apply(lambda x: datetime.date(x.year, x.month, x.day))
    operdates = list(df.BASE_YMD.unique())
    operdates.sort()
    df['DEBT_RATIO'] = df['TOTAL_DEBT1'] / df.TOTAL_DEBT
    df['COUNT_RATIO'] = df.LOAN_CTID / df.TOTAL_LOAN_CTID
    df['LOAN_OPERDATE'] = df.BASE_YMD.apply(lambda x: df[df.BASE_YMD == x]['TOTAL_DEBT1'].sum())
    df['LOAN_RATIO'] = df['TOTAL_DEBT1'] / df['LOAN_OPERDATE']
    df['LOAN_CTID2'] = np.nan
    df['TOTAL_DEBT_2'] = np.nan
    for i in range(len(df)):
        oper = df.BASE_YMD.iloc[i]
        product = df.PRODUCT.iloc[i]
        if operdates.index(oper) > 0:
            if len(df[(df.PRODUCT == product) & (df.BASE_YMD == operdates[operdates.index(oper) - 1])]) > 0:
                df.at[i, 'LOAN_CTID2'] = df[(df.PRODUCT == product) & (df.BASE_YMD == operdates[operdates.index(oper) - 1])].LOAN_CTID.iloc[0]
            if len(df[(df.PRODUCT == product) & (df.BASE_YMD == operdates[operdates.index(oper) - 1])]) > 0:
                df.at[i, 'TOTAL_DEBT_2'] = df[(df.PRODUCT == product) & (df.BASE_YMD == operdates[operdates.index(oper) - 1])].TOTAL_DEBT1.iloc[0]

    df['COUNT_DYNAMIC'] = df.LOAN_CTID / df.LOAN_CTID2 - 1
    df['DEBT_DYNAMIC'] = df['TOTAL_DEBT1'] / df.TOTAL_DEBT_2 - 1

    df = df.drop(['LOAN_OPERDATE', 'LOAN_CTID2', 'TOTAL_DEBT_2'], axis=1)

    return df

def str_date(date):
    day = str(date.day)
    month = str(date.month)
    year = str(date.year)
    if len(day) == 1:
        day = '0' + day
    if len(month) == 1:
        month = '0' + month

    return day + '.' + month + '.' + year


def total_debt(df):
    operdates = df.BASE_YMD.unique()
    operdates.sort()
    products = df.PRODUCT.unique()
    df2 = df.copy()
    df2.index = df2.PRODUCT
    df2 = df2.drop('PRODUCT', axis=1)
    df_all = pd.DataFrame(index=products)
    for operdate in operdates:
        temp = df2[df2.BASE_YMD == operdate][['TOTAL_DEBT']]
        df_all = pd.concat([df_all, temp], axis=1)

    operdates2 = [str_date(x) for x in operdates]
    df_all.columns = operdates2
    df_all = df_all.reset_index()
    df_all = df_all.rename(columns={'PRODUCT': 'Портфель (млн. тг.)'})

    sum_df = df_all.sum()
    dict_all = {}
    for i in range(len(sum_df)):
        if i == 0:
            dict_all[sum_df.index[i]] = 'Итого'
        elif i > 0:
            dict_all[sum_df.index[i]] = sum_df[i]

    df_all = df_all.append(dict_all, ignore_index=True)
    df_all = df_all.replace(np.nan, '')

    return df_all

def total_loan_ctid(df):
    operdates = df.BASE_YMD.unique()
    operdates.sort()
    products = df.PRODUCT.unique()
    df2 = df.copy()
    df2.index = df2.PRODUCT
    df2 = df2.drop('PRODUCT', axis=1)
    df_all = pd.DataFrame(index=products)
    for operdate in operdates:
        temp = df2[df2.BASE_YMD == operdate][['TOTAL_LOAN_CTID']]
        df_all = pd.concat([df_all, temp], axis=1)

    operdates2 = [str_date(x) for x in operdates]
    df_all.columns = operdates2
    df_all = df_all.reset_index()
    df_all = df_all.rename(columns={'PRODUCT': 'Количество договоров в портфеле'})

    sum_df = df_all.sum()
    dict_all = {}
    for i in range(len(sum_df)):
        if i == 0:
            dict_all[sum_df.index[i]] = 'Итого'
        elif i > 0:
            dict_all[sum_df.index[i]] = sum_df[i]

    df_all = df_all.append(dict_all, ignore_index=True)
    df_all = df_all.replace(np.nan, '')
    return df_all

def overdue_debt(df):
    operdates = df.BASE_YMD.unique()
    operdates.sort()
    products = df.PRODUCT.unique()
    df2 = df.copy()
    df2.index = df2.PRODUCT
    df2 = df2.drop('PRODUCT', axis=1)
    df_all = pd.DataFrame(index=products)
    for operdate in operdates:
        temp = df2[df2.BASE_YMD == operdate][['TOTAL_DEBT1']]
        df_all = pd.concat([df_all, temp], axis=1)

    operdates2 = [str_date(x) for x in operdates]
    df_all.columns = operdates2
    df_all = df_all.reset_index()
    df_all = df_all.rename(columns={'PRODUCT': 'Сумма просроченных ОД (млн. тг.)'})

    sum_df = df_all.sum()
    dict_all = {}
    for i in range(len(sum_df)):
        if i == 0:
            dict_all[sum_df.index[i]] = 'Итого'
        elif i > 0:
            dict_all[sum_df.index[i]] = sum_df[i]

    df_all = df_all.append(dict_all, ignore_index=True)
    df_all = df_all.replace(np.nan, '')

    return df_all

def overdue_count(df):
    operdates = df.BASE_YMD.unique()
    operdates.sort()
    products = df.PRODUCT.unique()
    df2 = df.copy()
    df2.index = df2.PRODUCT
    df2 = df2.drop('PRODUCT', axis=1)
    df_all = pd.DataFrame(index=products)
    for operdate in operdates:
        temp = df2[df2.BASE_YMD == operdate][['LOAN_CTID']]
        df_all = pd.concat([df_all, temp], axis=1)

    operdates2 = [str_date(x) for x in operdates]
    df_all.columns = operdates2
    df_all = df_all.reset_index()
    df_all = df_all.rename(columns={'PRODUCT': 'Количество просроченных договоров'})

    sum_df = df_all.sum()
    dict_all = {}
    for i in range(len(sum_df)):
        if i == 0:
            dict_all[sum_df.index[i]] = 'Итого'
        elif i > 0:
            dict_all[sum_df.index[i]] = sum_df[i]

    df_all = df_all.append(dict_all, ignore_index=True)
    df_all = df_all.replace(np.nan, '')

    return df_all

def debt_ratio(df):
    operdates = df.BASE_YMD.unique()
    operdates.sort()
    products = df.PRODUCT.unique()
    df2 = df.copy()
    df2.index = df2.PRODUCT
    df2 = df2.drop('PRODUCT', axis=1)
    df_all = pd.DataFrame(index=products)
    for operdate in operdates:
        temp = df2[df2.BASE_YMD == operdate][['DEBT_RATIO']]
        df_all = pd.concat([df_all, temp], axis=1)

    operdates2 = [str_date(x) for x in operdates]
    df_all.columns = operdates2
    df_all = df_all.reset_index()
    df_all = df_all.rename(columns={'PRODUCT': 'Доля просроченной задолженности'})
    df_all = df_all.replace(np.nan, '')

    return df_all

def count_ratio(df):
    operdates = df.BASE_YMD.unique()
    operdates.sort()
    products = df.PRODUCT.unique()
    df2 = df.copy()
    df2.index = df2.PRODUCT
    df2 = df2.drop('PRODUCT', axis=1)
    df_all = pd.DataFrame(index=products)
    for operdate in operdates:
        temp = df2[df2.BASE_YMD == operdate][['COUNT_RATIO']]
        df_all = pd.concat([df_all, temp], axis=1)

    operdates2 = [str_date(x) for x in operdates]
    df_all.columns = operdates2
    df_all = df_all.reset_index()
    df_all = df_all.rename(columns={'PRODUCT': 'Доля просроченных договоров'})
    df_all = df_all.replace(np.nan, '')

    return df_all

def loan_ratio(df):
    operdates = df.BASE_YMD.unique()
    operdates.sort()
    products = df.PRODUCT.unique()
    df2 = df.copy()
    df2.index = df2.PRODUCT
    df2 = df2.drop('PRODUCT', axis=1)
    df_all = pd.DataFrame(index=products)
    for operdate in operdates:
        temp = df2[df2.BASE_YMD == operdate][['LOAN_RATIO']]
        df_all = pd.concat([df_all, temp], axis=1)

    operdates2 = [str_date(x) for x in operdates]
    df_all.columns = operdates2
    df_all = df_all.reset_index()
    df_all = df_all.rename(columns={'PRODUCT': 'Доля по ОД'})
    df_all = df_all.replace(np.nan, '')

    return df_all

def count_dynamic(df):
    operdates = df.BASE_YMD.unique()
    operdates.sort()
    products = df.PRODUCT.unique()
    df2 = df.copy()
    df2.index = df2.PRODUCT
    df2 = df2.drop('PRODUCT', axis=1)
    df_all = pd.DataFrame(index=products)
    for operdate in operdates:
        temp = df2[df2.BASE_YMD == operdate][['COUNT_DYNAMIC']]
        df_all = pd.concat([df_all, temp], axis=1)

    operdates2 = [str_date(x) for x in operdates]
    df_all.columns = operdates2
    df_all = df_all.reset_index()
    df_all = df_all.rename(columns={'PRODUCT': 'Динамика по кол-ву договоров'})
    df_all = df_all.replace(np.nan, '')

    return df_all

def debt_dynamic(df):
    operdates = df.BASE_YMD.unique()
    operdates.sort()
    products = df.PRODUCT.unique()
    df2 = df.copy()
    df2.index = df2.PRODUCT
    df2 = df2.drop('PRODUCT', axis=1)
    df_all = pd.DataFrame(index=products)
    for operdate in operdates:
        temp = df2[df2.BASE_YMD == operdate][['DEBT_DYNAMIC']]
        df_all = pd.concat([df_all, temp], axis=1)

    operdates2 = [str_date(x) for x in operdates]
    df_all.columns = operdates2
    df_all = df_all.reset_index()
    df_all = df_all.rename(columns={'PRODUCT': 'Динамика по ОД'})
    df_all = df_all.replace(np.nan, '')

    return df_all