import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
import numpy as np
import roll_rates.graphs as graphs
import time
import datetime
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
from server import server

def date_to_str(date):
    day = str(date.day)
    month = str(date.month)
    year = str(date.year)
    if len(day) == 1:
        day = '0' + day
    if len(month) == 1:
        month = '0' + month

    return day + '.' + month + '.' + year

def str_to_date(s):
    return datetime.date(int(s.split('.')[2]), int(s.split('.')[1]), int(s.split('.')[0]))

def percent_repr(df):
    for col in df.columns[1:]:
        df[col] = df[col].apply(lambda x: str(round(x*100, 1)) + ' %')
    return df

def million_repr(df):
    for col in df.columns[1:]:
        df[col] = df[col].apply(lambda x: round(x/1_000_000, 1))
    return df

con = create_engine("oracle+cx_oracle://MOLDAADI:b52$rtpu4@10.15.28.28:1521/?service_name=edwprod")

df_week_count = pd.read_sql("SELECT * FROM WEEKLY_ROLL_RATE_COUNT ORDER BY BASE_YMD, PRODUCT", con=con)
df_week_count.columns = [col.upper() for col in df_week_count.columns]
df_week_count.BASE_YMD = df_week_count.BASE_YMD.apply(lambda x: datetime.date(x.year, x.month, x.day))
df_week_count.PRODUCT = df_week_count.PRODUCT.replace('99ИПЕБРР', 'ИПЕБРР')
df_week_count.PRODUCT = df_week_count.PRODUCT.replace('9Потребительские_кредиты', 'Потребительские кредиты')
df_week_count.PRODUCT = df_week_count.PRODUCT.replace('5Ипотека', 'Ипотека')
df_week_count.PRODUCT = df_week_count.PRODUCT.replace('7Беззалоговые', 'Беззалоговые')
df_week_count.PRODUCT = df_week_count.PRODUCT.replace('6Автокредиты', 'Автокредиты')
df_week_count.PRODUCT = df_week_count.PRODUCT.replace('8Кредитные_карты', 'Кредитные карты')
count_weeks = df_week_count.BASE_YMD.unique()
count_weeks.sort()

df_week_amount = pd.read_sql("SELECT * FROM WEEKLY_ROLL_RATE_SUM ORDER BY BASE_YMD, PRODUCT", con=con)
df_week_amount.columns = [col.upper() for col in df_week_amount.columns]
df_week_amount.BASE_YMD = df_week_amount.BASE_YMD.apply(lambda x: datetime.date(x.year, x.month, x.day))
df_week_amount.PRODUCT = df_week_amount.PRODUCT.replace('99ИПЕБРР', 'ИПЕБРР')
df_week_amount.PRODUCT = df_week_amount.PRODUCT.replace('9Потребительские_кредиты', 'Потребительские кредиты')
df_week_amount.PRODUCT = df_week_amount.PRODUCT.replace('5Ипотека', 'Ипотека')
df_week_amount.PRODUCT = df_week_amount.PRODUCT.replace('7Беззалоговые', 'Беззалоговые')
df_week_amount.PRODUCT = df_week_amount.PRODUCT.replace('6Автокредиты', 'Автокредиты')
df_week_amount.PRODUCT = df_week_amount.PRODUCT.replace('8Кредитные_карты', 'Кредитные карты')
amount_weeks = df_week_amount.BASE_YMD.unique()
amount_weeks.sort()

df_month_count = pd.read_sql("SELECT * FROM MONTHLY_ROLL_RATE_COUNT ORDER BY BASE_YMD, PRODUCT", con=con)
df_month_count.columns = [col.upper() for col in df_month_count.columns]
df_month_count.BASE_YMD = df_month_count.BASE_YMD.apply(lambda x: datetime.date(x.year, x.month, x.day))
df_month_count.PRODUCT = df_month_count.PRODUCT.replace('99ИПЕБРР', 'ИПЕБРР')
df_month_count.PRODUCT = df_month_count.PRODUCT.replace('9Потребительские_кредиты', 'Потребительские кредиты')
df_month_count.PRODUCT = df_month_count.PRODUCT.replace('5Ипотека', 'Ипотека')
df_month_count.PRODUCT = df_month_count.PRODUCT.replace('7Беззалоговые', 'Беззалоговые')
df_month_count.PRODUCT = df_month_count.PRODUCT.replace('6Автокредиты', 'Автокредиты')
df_month_count.PRODUCT = df_month_count.PRODUCT.replace('8Кредитные_карты', 'Кредитные карты')
count_months = df_month_count.BASE_YMD.unique()
count_months.sort()

df_month_amount = pd.read_sql("SELECT * FROM MONTHLY_ROLL_RATE_SUM ORDER BY BASE_YMD, PRODUCT", con=con)
df_month_amount.columns = [col.upper() for col in df_month_amount.columns]
df_month_amount.BASE_YMD = df_month_amount.BASE_YMD.apply(lambda x: datetime.date(x.year, x.month, x.day))
df_month_amount.PRODUCT = df_month_amount.PRODUCT.replace('99ИПЕБРР', 'ИПЕБРР')
df_month_amount.PRODUCT = df_month_amount.PRODUCT.replace('9Потребительские_кредиты', 'Потребительские кредиты')
df_month_amount.PRODUCT = df_month_amount.PRODUCT.replace('5Ипотека', 'Ипотека')
df_month_amount.PRODUCT = df_month_amount.PRODUCT.replace('7Беззалоговые', 'Беззалоговые')
df_month_amount.PRODUCT = df_month_amount.PRODUCT.replace('6Автокредиты', 'Автокредиты')
df_month_amount.PRODUCT = df_month_amount.PRODUCT.replace('8Кредитные_карты', 'Кредитные карты')
amount_months = df_month_amount.BASE_YMD.unique()
amount_months.sort()

analysis_types = ['Еженедельный отчет по количеству', 'Еженедельный отчет по сумме', 'Ежемесячный отчет по количеству', 'Ежемесячный отчет по сумме']
products = df_week_count.PRODUCT.unique()
products.sort()

periods = df_week_count.BASE_YMD.unique()
periods.sort()

app = dash.Dash(__name__, title='Roll Rates', server=server, url_base_pathname='/roll_rates/')
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.Div([
        html.H4('Выберите период', style={'font-family': 'arial'})
    ], style={'marginLeft': '80px'}),
    html.Div([
        dcc.DatePickerRange(
            id='date_picker_range',
            min_date_allowed=df_week_amount.BASE_YMD.min(),
            max_date_allowed=df_week_amount.BASE_YMD.max(),
            start_date=df_week_amount.BASE_YMD.min(),
            end_date=df_week_amount.BASE_YMD.max(),
            display_format='DD.MM.YYYY',
            style={'font-family': 'arial', 'fontSize': '14px'}
        )
    ], style={'marginLeft': '80px', 'marginBottom': '20px'}),
    html.Div([
        html.Div([
            html.H4('Выберите тип анализа', style={'font-family': 'arial'})
        ], style={'marginLeft': '80px', 'width': '400px'}),
        html.Div([
            dcc.Dropdown(
                id='analysis_type',
                multi=False,
                value=analysis_types[3],
                options=[{'label': typee, 'value': typee} for typee in analysis_types],
                clearable=False,
                style={'font-family': 'arial', 'width': '400px', 'fontSize': '14px'}
            )
        ], style={'marginLeft': '80px'}),
        html.Div([
            html.H4('Выберите тип продукта', style={'font-family': 'arial'})
        ], style={'marginLeft': '80px', 'width': '400px'}),
        html.Div([
            dcc.Dropdown(
                id='product_type',
                multi=False,
                value=products[0],
                options=[{'label': product, 'value': product} for product in products],
                clearable=False,
                style={'font-family': 'arial', 'width': '400px', 'fontSize': '14px'}
            )
        ], style={'marginLeft': '80px'}),
    ], style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        html.Div([
            html.H4('Выберите период для скачивания отчета', style={'font-family': 'arial'})
        ], style={'marginLeft': '80px'}),
        html.Div([
            dcc.Dropdown(
                id='periods_dropdown',
                multi=False,
                value=periods[0],
                options=[{'label': period, 'value': period} for period in periods],
                clearable=False,
                style={'font-family': 'arial', 'width': '400px', 'fontSize': '14px'}
            )
        ], style={'marginLeft': '80px'}),
        html.Div([
            html.H4('Выберите тип отчета', style={'font-family': 'arial'})
        ], style={'marginLeft': '80px'}),
        html.Div([
            dcc.Dropdown(
                id='report_type',
                multi=False,
                value='Отчет по количеству и сумме',
                options=[{'label': report, 'value': report} for report in ['Отчет по количеству и сумме', 'Отчет по долям']],
                clearable=False,
                style={'font-family': 'arial', 'width': '400px', 'fontSize': '14px'}
            )
        ], style={'marginLeft': '80px'}),
    ], style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        html.Button('Скачать', id='download_button', n_clicks=0, style={'height': '25px', 'width': '100px'}),
        Download(id='download_report')
    ], style={'marginLeft': '1008px', 'marginTop': '20px'}),
    html.Div([
        dcc.Dropdown(
            id='sort_dropdown',
            multi=False,
            value='Сортировать даты по возрастанию',
            options=[{'label': sort_type, 'value': sort_type} for sort_type in ['Сортировать даты по возрастанию', 'Сортировать даты по убыванию']],
            clearable=False,
            style={'font-family': 'arial', 'width': '400px', 'fontSize': '14px'}
        )
    ], style={'marginLeft': '80px'}),
    html.Div([
        html.Button('Показать график', id='show_graphics', n_clicks=0, style={'height': '25px', 'width': '150px'})
    ], style={'marginLeft': '80px', 'marginTop': '50px'}),
    html.Div([

    ], id='graphs_layout'),
    dcc.Loading(
        id='loading',
        children=[html.Div(id='tables_layout')],
        type='cube',
        fullscreen=True,
        color='green'
    )
])

graph_layout = [
    html.Div([
        dcc.Dropdown(
            id='roll_types',
            multi=False,
            value='1-30',
            options=[{'label': roll_type, 'value': roll_type} for roll_type in ['1-30', '30-60', '60-90', '90-120']],
            clearable=False,
            style={'font-family': 'arial', 'fontSize': '14px', 'width': '100px'}
        )
    ], style={'marginTop': '20px', 'marginLeft': '80px'}),
    html.Div([
        html.Button('Создать', id='btn_create_graph', n_clicks=0, style={'height': '25px', 'width': '100px'})
    ], style={'marginTop': '20px', 'marginLeft': '80px'}),
    html.Div([

    ], style={'marginLeft': '80px'}, id='create_graph_layout')
]

@app.callback(
    Output('tables_layout', 'children'), [Input('analysis_type', 'value'), Input('product_type', 'value'),
                                          Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date'), Input('sort_dropdown', 'value')]
)
def create_table_layout(analysis_type, product_type, start_date, end_date, sort_type):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))

    if analysis_type == 'Еженедельный отчет по количеству':
        df = df_week_count
    if analysis_type == 'Еженедельный отчет по сумме':
        df = df_week_amount
    if analysis_type == 'Ежемесячный отчет по количеству':
        df = df_month_count
    if analysis_type == 'Ежемесячный отчет по сумме':
        df = df_month_amount

    direct = ['Soft']*5
    if product_type == 'Кредитные карты' or product_type == 'Беззалоговые':
        direct = ['Soft']*5
    if product_type == 'Ипотека' or product_type == 'Потребительские кредиты' or product_type == 'Автокредиты':
        direct = ['Soft']*2 + ['Hard']*3
    if product_type == 'ИПЕБРР':
        direct = ['Soft'] + ['Hard']*4

    df2 = df[(df.PRODUCT == product_type) & (df.BASE_YMD >= start_date) & (df.BASE_YMD <= end_date)]
    tables = []
    bases = list(df2.BASE_YMD.unique())

    isReverse = False
    if sort_type == 'Сортировать даты по убыванию':
        isReverse = True

    bases.sort(reverse=isReverse)

    for base in bases:
        df_temp = df2[df2.BASE_YMD == base]
        dfr = pd.DataFrame(index=['1-30', '30-60', '60-90', '90-120'], columns=['0', '1-30', '30-60', '60-90', '90-120', '121'])
        for ind in dfr.index:
            for col in dfr.columns:
                ind_name = '(' + ind + ')'
                col_name = '(' + col + ')'
                name = ind_name + ' -> ' + col_name
                name_2 = ind_name + '->' + col_name
                try:
                    if name in df2.columns:
                        dfr.at[ind, col] = df_temp[name].iloc[0]
                    else:
                        dfr.at[ind, col] = df_temp[name_2].iloc[0]
                except KeyError:
                    dfr.at[ind, col] = np.nan

        dfr['col_sum'] = dfr.sum(axis=1)
        dfr.loc['Всего'] = dfr.sum(axis=0).tolist()
        dfr = dfr.reset_index()

        dfr = dfr.rename(columns={'index': date_to_str(base)})
        dfr2 = dfr.copy()
        for col in dfr.columns[1:]:
            try:
                dfr2[col] = dfr2[col]/dfr2.col_sum
            except ZeroDivisionError:
                dfr2[col] = 0
        if analysis_type == 'Еженедельный отчет по сумме' or analysis_type == 'Ежемесячный отчет по сумме':
            dfr = million_repr(dfr)
        dfr = dfr.replace(np.nan, 'x')
        dfr2['Target'] = [0.9, 0.7, 0.5, 0.3, 0]
        dfr2['Исп-ние'] = dfr2['0'] - dfr2['Target']
        dfr2 = percent_repr(dfr2)
        dfr2 = dfr2.replace('nan %', 'x')
        dfr = dfr.drop('col_sum', axis=1)
        dfr2 = dfr2.drop('col_sum', axis=1)
        dfr.insert(1, 'Под-ние', direct)
        dfr2.insert(1, 'Под-ние', direct)
        dfr2.at[len(dfr2)-1, 'Target'] = ''
        dfr2.at[len(dfr2)-1, 'Исп-ние'] = ''

        temp_html = html.Div([
            html.Div([
                dcc.Graph(
                    figure=graphs.table_image(dfr)
                )
            ], style={'width': '49%', 'display': 'inline-block'}),
            html.Div([
                dcc.Graph(
                    figure=graphs.table_image(dfr2)
                )
            ], style={'width': '49%', 'display': 'inline-block'})
        ])

        tables.append(temp_html)
    time.sleep(1)
    return tables

@app.callback(
    [Output('date_picker_range', 'min_date_allowed'), Output('date_picker_range', 'max_date_allowed'),
     Output('date_picker_range', 'start_date'), Output('date_picker_range', 'end_date')],
    [Input('analysis_type', 'value')]
)
def update_dates_range(analysis_type):
    if analysis_type == 'Еженедельный отчет по количеству':
        min_date = min(count_weeks)
        max_date = max(count_weeks)
        start_date = min(count_weeks[-8:])
        end_date = max(count_weeks)

    if analysis_type == 'Еженедельный отчет по сумме':
        min_date = min(amount_weeks)
        max_date = max(amount_weeks)
        start_date = min(amount_weeks[-8:])
        end_date = max(amount_weeks)

    if analysis_type == 'Ежемесячный отчет по количеству':
        min_date = min(count_months)
        max_date = max(count_months)
        start_date = min(count_months[-12:])
        end_date = max(count_months)

    if analysis_type == 'Ежемесячный отчет по сумме':
        min_date = min(amount_months)
        max_date = max(amount_months)
        start_date = min(amount_months[-12:])
        end_date = max(amount_months)

    return min_date, max_date, start_date, end_date

@app.callback(
    [Output('periods_dropdown', 'value'), Output('periods_dropdown', 'options')],
    [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date'), Input('analysis_type', 'value')]
)
def update_period_list(start_date, end_date, analysis_type):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))

    if analysis_type == 'Еженедельный отчет по количеству':
        df = df_week_count[(df_week_count.BASE_YMD >= start_date) & (df_week_count.BASE_YMD <= end_date)]
    if analysis_type == 'Еженедельный отчет по сумме':
        df = df_week_amount[(df_week_amount.BASE_YMD >= start_date) & (df_week_amount.BASE_YMD <= end_date)]
    if analysis_type == 'Ежемесячный отчет по количеству':
        df = df_month_count[(df_month_count.BASE_YMD >= start_date) & (df_month_count.BASE_YMD <= end_date)]
    if analysis_type == 'Ежемесячный отчет по сумме':
        df = df_month_amount[(df_month_amount.BASE_YMD >= start_date) & (df_month_amount.BASE_YMD <= end_date)]

    periods = df.BASE_YMD.unique()
    periods.sort()
    periods = [date_to_str(x) for x in periods]

    return periods[0], [{'label': period, 'value': period} for period in periods]

@app.callback(
    Output('download_report', 'data'), [Input('download_button', 'n_clicks')], [State('analysis_type', 'value'), State('product_type', 'value'),
                                                                                State('periods_dropdown', 'value'), State('report_type', 'value')]
)
def download_report(n_clicks, analysis_type, product, period, report_type):
    if n_clicks > 0:
        if analysis_type == 'Еженедельный отчет по количеству':
            df = df_week_count[(df_week_count.BASE_YMD == str_to_date(period)) & (df_week_count.PRODUCT == product)]
        if analysis_type == 'Еженедельный отчет по сумме':
            df = df_week_amount[(df_week_amount.BASE_YMD == str_to_date(period)) & (df_week_amount.PRODUCT == product)]
        if analysis_type == 'Ежемесячный отчет по количеству':
            df = df_month_count[(df_month_count.BASE_YMD == str_to_date(period)) & (df_month_count.PRODUCT == product)]
        if analysis_type == 'Ежемесячный отчет по сумме':
            df = df_month_amount[(df_month_amount.BASE_YMD == str_to_date(period)) & (df_month_amount.PRODUCT == product)]

        direct = ['Soft'] * 5
        if product == 'Кредитные карты' or product == 'Беззалоговые':
            direct = ['Soft'] * 5
        if product == 'Ипотека' or product == 'Потребительские кредиты' or product == 'Автокредиты':
            direct = ['Soft'] * 2 + ['Hard'] * 3
        if product == 'ИПЕБРР':
            direct = ['Soft'] + ['Hard'] * 4

        dfr = pd.DataFrame(index=['1-30', '30-60', '60-90', '90-120'], columns=['0', '1-30', '30-60', '60-90', '90-120', '121'])
        for ind in dfr.index:
            for col in dfr.columns:
                ind_name = '(' + ind + ')'
                col_name = '(' + col + ')'
                name = ind_name + ' -> ' + col_name
                name_2 = ind_name + '->' + col_name
                try:
                    if name in df.columns:
                        dfr.at[ind, col] = df[name].iloc[0]
                    else:
                        dfr.at[ind, col] = df[name_2].iloc[0]
                except KeyError:
                    dfr.at[ind, col] = np.nan

        dfr['col_sum'] = dfr.sum(axis=1)
        dfr.loc['Всего'] = dfr.sum(axis=0).tolist()
        dfr = dfr.reset_index()

        dfr = dfr.rename(columns={'index': period})
        dfr2 = dfr.copy()
        for col in dfr.columns[1:]:
            try:
                dfr2[col] = dfr2[col] / dfr2.col_sum
            except ZeroDivisionError:
                dfr2[col] = 0
        if analysis_type == 'Еженедельный отчет по сумме' or analysis_type == 'Ежемесячный отчет по сумме':
            dfr = million_repr(dfr)
        dfr = dfr.replace(np.nan, 'x')
        dfr2['Target'] = [0.9, 0.7, 0.5, 0.3, 0]
        dfr2['Исп-ние'] = dfr2['0'] - dfr2['Target']
        dfr2 = percent_repr(dfr2)
        dfr2 = dfr2.replace('nan %', 'x')
        dfr = dfr.drop('col_sum', axis=1)
        dfr2 = dfr2.drop('col_sum', axis=1)
        dfr.insert(1, 'Под-ние', direct)
        dfr2.insert(1, 'Под-ние', direct)
        dfr2.at[len(dfr2) - 1, 'Target'] = ''
        dfr2.at[len(dfr2) - 1, 'Исп-ние'] = ''

        if report_type == 'Отчет по количеству и сумме':
            return send_data_frame(dfr.to_excel, filename=period + "_" + product + '.xlsx', index=False)

        if report_type == 'Отчет по долям':
            return send_data_frame(dfr2.to_excel, filename=period + "_" + product + '.xlsx', index=False)

@app.callback(
    [Output('graphs_layout', 'children'), Output('show_graphics', 'children')], [Input('show_graphics', 'n_clicks')]
)
def add_graphs_layout(n_clicks):
    if n_clicks % 2 == 1:
        return graph_layout, 'Скрыть график'
    else:
        return [html.Div([])], 'Показать график'

@app.callback(
    Output('create_graph_layout', 'children'), [Input('btn_create_graph', 'n_clicks')],
    [State('roll_types', 'value'), State('date_picker_range', 'start_date'), State('date_picker_range', 'end_date'),
     State('analysis_type', 'value'), State('product_type', 'value')]
)
def create_graph(n_clicks, roll_type, start_date, end_date, analysis_type, product):
    if n_clicks > 0:
        start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
        end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))

        if analysis_type == 'Еженедельный отчет по количеству':
            df = df_week_count[(df_week_count.BASE_YMD >= start_date) & (df_week_count.BASE_YMD <= end_date) & (df_week_count.PRODUCT == product)]
        if analysis_type == 'Еженедельный отчет по сумме':
            df = df_week_amount[(df_week_amount.BASE_YMD >= start_date) & (df_week_amount.BASE_YMD <= end_date) & (df_week_amount.PRODUCT == product)]
        if analysis_type == 'Ежемесячный отчет по количеству':
            df = df_month_count[(df_month_count.BASE_YMD >= start_date) & (df_month_count.BASE_YMD <= end_date) & (df_month_count.PRODUCT == product)]
        if analysis_type == 'Ежемесячный отчет по сумме':
            df = df_month_amount[(df_month_amount.BASE_YMD >= start_date) & (df_month_amount.BASE_YMD <= end_date) & (df_month_amount.PRODUCT == product)]

        df = df.sort_values(by='BASE_YMD')
        value_1 = '(' + roll_type + ')->'
        value_2 = '(' + roll_type + ') ->'
        df2 = df[['BASE_YMD'] + [x for x in df.columns if x.find(value_1) != -1 or x.find(value_2) != -1]]
        df2['COMMON'] = 0
        for col in df2.columns:
            if col != 'BASE_YMD' and col != 'COMMON':
                df2['COMMON'] += df2[col]

        to_zero = '(' + roll_type + ')->(0)'
        to_zero_2 = '(' + roll_type + ') -> (0)'
        try:
            df2["SHARE"] = df2[to_zero]/df2['COMMON']
        except KeyError:
            df2['SHARE'] = df2[to_zero_2]/df2['COMMON']

        df2 = df2[['BASE_YMD', 'SHARE']]
        df2.SHARE = df2.SHARE.apply(lambda x: round(x*100, 1))

        return html.Div([dcc.Graph(figure=graphs.roll_rate_graph(df2))])

if __name__ == '__main__':
    app.run_server(debug=True)