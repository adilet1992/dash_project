import pandas as pd
import numpy as np

def date_to_word(date):
    d = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
         9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}

    return d[date.month] + ' ' + str(date.year)

def vintage_5_plus(df):
    given_months = df.GIVEN_MONTH.unique()
    given_months.sort()

    df_all = pd.DataFrame(index=given_months)

    geners = list(df.GEN.unique())
    geners.sort()

    for gen in geners:
        df_month = df[df.GEN == gen][['GIVEN_MONTH', 'LOAN_SUM', 'DEBT_AMOUNT_5_PLUS']].groupby('GIVEN_MONTH').sum()
        df_month['SHARE'] = round(df_month.DEBT_AMOUNT_5_PLUS / df_month.LOAN_SUM * 100, 2).astype(str) + '%'
        df_all = pd.concat([df_all, df_month[['SHARE']]], axis=1)

    df_all.columns = [str(gen) + ' месяц' for gen in geners]
    df_all.index = [date_to_word(given_month) for given_month in given_months]
    df_all = df_all.replace(np.nan, '')
    df_all = df_all.reset_index()
    df_all = df_all.rename(columns={'index': 'Поколение выдачи'})

    df_loan_sum = df[['GIVEN_MONTH', 'LOAN_SUM']].groupby('GIVEN_MONTH').sum()
    df_loan_sum = df_loan_sum.LOAN_SUM.tolist()
    df_loan_sum = ['{:,}'.format(int(x / 1000000)).replace(',', ' ') for x in df_loan_sum]

    df_all = df_all.replace('nan%', '0.0%')
    df_all = df_all.replace('inf%', '0.0%')
    df_all.insert(1, 'Сумма выдачи (в млн.)', df_loan_sum)

    df_all = df_all[
        ['Поколение выдачи', 'Сумма выдачи (в млн.)'] + [x for x in df_all.columns[2:] if int(x.split()[0]) >= 1]]

    return df_all

def vintage_30_plus(df):
    given_months = df.GIVEN_MONTH.unique()
    given_months.sort()

    df_all = pd.DataFrame(index=given_months)

    geners = list(df.GEN.unique())
    geners.sort()

    for gen in geners:
        df_month = df[df.GEN == gen][['GIVEN_MONTH', 'LOAN_SUM', 'DEBT_AMOUNT_30_PLUS']].groupby('GIVEN_MONTH').sum()
        df_month['SHARE'] = round(df_month.DEBT_AMOUNT_30_PLUS / df_month.LOAN_SUM * 100, 2).astype(str) + '%'
        df_all = pd.concat([df_all, df_month[['SHARE']]], axis=1)

    df_all.columns = [str(gen) + ' месяц' for gen in geners]
    df_all.index = [date_to_word(given_month) for given_month in given_months]
    df_all = df_all.replace(np.nan, '')
    df_all = df_all.reset_index()
    df_all = df_all.rename(columns={'index': 'Поколение выдачи'})

    df_loan_sum = df[['GIVEN_MONTH', 'LOAN_SUM']].groupby('GIVEN_MONTH').sum()
    df_loan_sum = df_loan_sum.LOAN_SUM.tolist()
    df_loan_sum = ['{:,}'.format(int(x / 1000000)).replace(',', ' ') for x in df_loan_sum]

    df_all = df_all.replace('nan%', '0.0%')
    df_all = df_all.replace('inf%', '0.0%')
    df_all.insert(1, 'Сумма выдачи (в млн.)', df_loan_sum)

    df_all = df_all[['Поколение выдачи', 'Сумма выдачи (в млн.)'] + [x for x in df_all.columns[2:] if int(x.split()[0]) >= 2]]

    return df_all

def vintage_60_plus(df):
    given_months = df.GIVEN_MONTH.unique()
    given_months.sort()

    df_all = pd.DataFrame(index=given_months)

    geners = list(df.GEN.unique())
    geners.sort()

    for gen in geners:
        df_month = df[df.GEN == gen][['GIVEN_MONTH', 'LOAN_SUM', 'DEBT_AMOUNT_60_PLUS']].groupby('GIVEN_MONTH').sum()
        df_month['SHARE'] = round(df_month.DEBT_AMOUNT_60_PLUS / df_month.LOAN_SUM * 100, 2).astype(str) + '%'
        df_all = pd.concat([df_all, df_month[['SHARE']]], axis=1)

    df_all.columns = [str(gen) + ' месяц' for gen in geners]
    df_all.index = [date_to_word(given_month) for given_month in given_months]
    df_all = df_all.replace(np.nan, '')
    df_all = df_all.reset_index()
    df_all = df_all.rename(columns={'index': 'Поколение выдачи'})

    df_loan_sum = df[['GIVEN_MONTH', 'LOAN_SUM']].groupby('GIVEN_MONTH').sum()
    df_loan_sum = df_loan_sum.LOAN_SUM.tolist()
    df_loan_sum = ['{:,}'.format(int(x / 1000000)).replace(',', ' ') for x in df_loan_sum]

    df_all = df_all.replace('nan%', '0.0%')
    df_all = df_all.replace('inf%', '0.0%')
    df_all.insert(1, 'Сумма выдачи (в млн.)', df_loan_sum)

    df_all = df_all[['Поколение выдачи', 'Сумма выдачи (в млн.)'] + [x for x in df_all.columns[2:] if int(x.split()[0]) >= 3]]

    return df_all

def vintage_90_plus(df):
    given_months = df.GIVEN_MONTH.unique()
    given_months.sort()

    df_all = pd.DataFrame(index=given_months)

    geners = list(df.GEN.unique())
    geners.sort()

    for gen in geners:
        df_month = df[df.GEN == gen][['GIVEN_MONTH', 'LOAN_SUM', 'DEBT_AMOUNT_90_PLUS']].groupby('GIVEN_MONTH').sum()
        df_month['SHARE'] = round(df_month.DEBT_AMOUNT_90_PLUS / df_month.LOAN_SUM *100, 2).astype(str) + '%'
        df_all = pd.concat([df_all, df_month[['SHARE']]], axis=1)

    df_all.columns = [str(gen) + ' месяц' for gen in geners]
    df_all.index = [date_to_word(given_month) for given_month in given_months]
    df_all = df_all.replace(np.nan, '')
    df_all = df_all.reset_index()
    df_all = df_all.rename(columns={'index': 'Поколение выдачи'})

    df_loan_sum = df[['GIVEN_MONTH', 'LOAN_SUM']].groupby('GIVEN_MONTH').sum()
    df_loan_sum = df_loan_sum.LOAN_SUM.tolist()
    df_loan_sum = ['{:,}'.format(int(x/1000000)).replace(',', ' ') for x in df_loan_sum]

    df_all = df_all.replace('nan%', '0.0%')
    df_all = df_all.replace('inf%', '0.0%')
    df_all.insert(1, 'Сумма выдачи (в млн.)', df_loan_sum)

    df_all = df_all[['Поколение выдачи', 'Сумма выдачи (в млн.)'] + [x for x in df_all.columns[2:] if int(x.split()[0]) >= 4]]

    return df_all