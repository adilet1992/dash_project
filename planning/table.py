import pandas as pd
import numpy as np
import datetime

def date_to_word(date):
    d = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
         9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}

    return d[date.month] + ' ' + str(date.year)

def thousand_format(x):
    return '{:,}'.format(int(x)).replace(',', ' ')

def percent_format(x):
    return str(round(x*100, 1)) + ' %'

def percent_format_2(x):
    return str(round(x*100, 2)) + ' %'

def convert_date_to_str(x):
    day = str(x.day)
    month = str(x.month)
    year = str(x.year)

    if len(day) == 1:
        day = '0' + day
    if len(month) == 1:
        month = '0' + month

    return day + '.' + month + '.' + year

def create_ar_table(df, product):
    df = df[df.PRODUCT2 == product]
    df2 = df
    df2['REVIEW'] = df2.CNT - df2.CANCEL
    df2 = df2[['WEEK', 'REVIEW', 'ACC', 'ACC2', 'ACC_LOAN']]
    df2 = df2.groupby('WEEK').sum().reset_index()
    df2 = df2[['WEEK', 'REVIEW', 'ACC', 'ACC2', 'ACC_LOAN']]
    df2['AR_W_ALT'] = df2.ACC/df2.REVIEW
    df2['AR_WO_ALT'] = df2.ACC2/df2.REVIEW
    df2['CONV_W_ALT'] = df2.ACC_LOAN/df2.ACC
    df2['CONV_WO_ALT'] = df2.ACC_LOAN/df2.ACC2

    df2 = df2[['WEEK', 'REVIEW', 'AR_WO_ALT', 'AR_W_ALT', 'CONV_WO_ALT', 'CONV_W_ALT']]
    df2['REVIEW'] = df2['REVIEW'].apply(lambda x: thousand_format(x))
    df2['AR_W_ALT'] = df2['AR_W_ALT'].apply(lambda x: percent_format(x))
    df2['AR_WO_ALT'] = df2['AR_WO_ALT'].apply(lambda x: percent_format(x))
    df2['CONV_W_ALT'] = df2['CONV_W_ALT'].apply(lambda x: percent_format(x))
    df2['CONV_WO_ALT'] = df2['CONV_WO_ALT'].apply(lambda x: percent_format(x))
    df2['WEEK'] = df2['WEEK'].apply(lambda x: convert_date_to_str(x) + ' - ' + convert_date_to_str(x + datetime.timedelta(days=6)))

    df2 = df2.rename(columns={'WEEK': 'Дата', 'REVIEW': 'Кол-во рассмотренных заявок', 'AR_W_ALT': 'Уровень одобрения с учетом альт. %',
                              'AR_WO_ALT': 'Уровень одобрения без учета альт. %', 'CONV_W_ALT': 'Конверсия в выдачу с учетом альт. %',
                              'CONV_WO_ALT': 'Конверсия в выдачу без учета альт. %'})

    return df2

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

    df_all = df_all[['Поколение выдачи', 'Сумма выдачи (в млн.)'] + [x for x in df_all.columns[2:] if int(x.split()[0]) >= 1]]

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

def create_eri_table(df_eri, df_del):
    df_eri2 = df_eri.groupby('MONTH_SIGN_CTR').agg(
        ALL_COUNT=pd.NamedAgg(column='LOAN_CTID', aggfunc='count'),
        FPD_15_SUM=pd.NamedAgg(column='FLAG_FPD_15_HIST', aggfunc='sum'),
        SPD_15_SUM=pd.NamedAgg(column='FLAG_SPD_15_HIST', aggfunc='sum'),
        TPD_15_SUM=pd.NamedAgg(column='FLAG_TPD_15_HIST', aggfunc='sum'),
    )
    df_eri2['FPD_15_SHARE'] = df_eri2['FPD_15_SUM'] / df_eri2['ALL_COUNT']
    df_eri2['SPD_15_SHARE'] = df_eri2['SPD_15_SUM'] / df_eri2['ALL_COUNT']
    df_eri2['TPD_15_SHARE'] = df_eri2['TPD_15_SUM'] / df_eri2['ALL_COUNT']
    eri = df_eri2[['ALL_COUNT', 'FPD_15_SHARE', 'SPD_15_SHARE', 'TPD_15_SHARE']]

    df_del2 = df_del.groupby('MONTH_SIGN_CTR').agg(
        ALL_COUNT=pd.NamedAgg(column='LOAN_CTID', aggfunc='count'),
        SUM_30_MOB=pd.NamedAgg(column='FLAG_30_MOB', aggfunc='sum'),
        SUM_60_MOB=pd.NamedAgg(column='FLAG_60_MOB', aggfunc='sum'),
        SUM_90_MOB=pd.NamedAgg(column='FLAG_90_MOB', aggfunc='sum')
    )
    df_del2['SHARE_30_MOB'] = df_del2['SUM_30_MOB'] / df_del2['ALL_COUNT']
    df_del2['SHARE_60_MOB'] = df_del2['SUM_60_MOB'] / df_del2['ALL_COUNT']
    df_del2['SHARE_90_MOB'] = df_del2['SUM_90_MOB'] / df_del2['ALL_COUNT']
    dell = df_del2[['SHARE_30_MOB', 'SHARE_60_MOB', 'SHARE_90_MOB']]
    df_all = pd.concat([eri, dell], axis=1)
    df_all = df_all.reset_index()
    df_all.MONTH_SIGN_CTR = df_all.MONTH_SIGN_CTR.apply(lambda x: date_to_word(x))
    df_all.ALL_COUNT = df_all.ALL_COUNT.apply(lambda x: thousand_format(x))
    df_all.FPD_15_SHARE = df_all.FPD_15_SHARE.apply(lambda x: percent_format_2(x))
    df_all.SPD_15_SHARE = df_all.SPD_15_SHARE.apply(lambda x: percent_format_2(x))
    df_all.TPD_15_SHARE = df_all.TPD_15_SHARE.apply(lambda x: percent_format_2(x))
    df_all.SHARE_30_MOB = df_all.SHARE_30_MOB.apply(lambda x: percent_format_2(x))
    df_all.SHARE_60_MOB = df_all.SHARE_60_MOB.apply(lambda x: percent_format_2(x))
    df_all.SHARE_90_MOB = df_all.SHARE_90_MOB.apply(lambda x: percent_format_2(x))

    df_all = df_all.rename(columns={'MONTH_SIGN_CTR': 'Дата', 'ALL_COUNT': 'Кол-во контрактов', 'FPD_15_SHARE': 'Доля FPD15',
                                    'SPD_15_SHARE': 'Доля SPD15', 'TPD_15_SHARE': 'Доля TPD15', 'SHARE_30_MOB': 'Доля 30+@3mob',
                                    'SHARE_60_MOB': 'Доля 60+@6mob', 'SHARE_90_MOB': 'Доля 90+@12mob'})

    return df_all