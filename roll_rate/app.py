import pandas as pd
import roll_rate.tables as tables
import roll_rate.graphs as graphs
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
from dash.dependencies import Output, Input, State
from sqlalchemy import create_engine
import datetime
import warnings
import numpy as np
from server import server

warnings.simplefilter('ignore')

con = create_engine("oracle+cx_oracle://MOLDAADI:b52$rtpu4@10.15.28.28:1521/?service_name=edwprod")
df = pd.read_sql("SELECT * FROM COLLECTION_DAILY ORDER BY BASE_YMD, PRODUCT", con=con)
df.columns = [col.upper() for col in df.columns]
df.PRODUCT = df.PRODUCT.replace('1Ипотека', 'Ипотека')
df.PRODUCT = df.PRODUCT.replace('7ИПЕБРР', 'ИПЕБРР')
df.PRODUCT = df.PRODUCT.replace('4Беззалоговые', 'Беззалоговые')
df.PRODUCT = df.PRODUCT.replace('8ЮР', 'ЮР')
df.PRODUCT = df.PRODUCT.replace('3Автокредиты', 'Автокредиты')
df.PRODUCT = df.PRODUCT.replace('5Кредитные_карты', 'Кредитные карты')
df.PRODUCT = df.PRODUCT.replace('2Баспана', 'Баспана')
df.PRODUCT = df.PRODUCT.replace('6Потребительские_кредиты', 'Потребительские кредиты')

df.BASE_YMD = df.BASE_YMD.apply(lambda x: datetime.date(x.year, x.month, x.day))
df['OPERDATE'] = df.BASE_YMD.apply(lambda x: datetime.date(x.year, x.month, 1))
df2 = df[df.BASE_YMD.isin(df.OPERDATE.unique())]

max_date = df.BASE_YMD.max()
curr_period_begin = datetime.date(max_date.year, max_date.month, 1)
df_daily = df[df.BASE_YMD >= (df.BASE_YMD.max() - datetime.timedelta(days=60))]

def add_currency(df):
    for col in df.columns[1:]:
        df[col] = df[col].apply(lambda x: int(x/1000000) if type(x) != str else x)
        df[col] = df[col].apply(lambda x: '{:,}'.format(x).replace(',', ' ') if type(x) != str else x)
    return df

def str_format(df):
    for col in df.columns[1:]:
        df[col] = df[col].apply(lambda x: int(x) if type(x) != str else x)
        df[col] = df[col].apply(lambda x: '{:,}'.format(int(x)).replace(',', ' ') if type(x) != str else x)
    return df

def percent_format(df):
    for col in df.columns[1:]:
        df[col] = df[col].apply(lambda x: str(round(x*100, 1)) + ' %' if type(x) != str else x)
    return df

def percent_format_2(df):
    for col in df.columns[1:]:
        df[col] = df[col].apply(lambda x: str(round(x*100, 1)) + ' %' if type(x) != str else x)

    df = df.replace('nan %', '')
    return df

def int_format(df):
    for col in df.columns[1:]:
        df[col] = df[col].apply(lambda x: int(x/1_000_000) if type(x) != str else x)
    return df

def hundred_format(df):
    for col in df.columns[1:]:
        df[col] = df[col].apply(lambda x: round(x*100, 1) if type(x) != str else x)
    return df

#################
# Monthly reports
#################
df_with_features = tables.create_features(df2)

df_total_debt = tables.total_debt(df_with_features)
df_total_debt = df_total_debt.replace(np.nan, '')
df_total_debt = add_currency(df_total_debt)

df_total_loan_ctid = tables.total_loan_ctid(df_with_features)
df_total_loan_ctid = df_total_loan_ctid.replace(np.nan, '')
df_total_loan_ctid = str_format(df_total_loan_ctid)

df_overdue_debt = tables.overdue_debt(df_with_features)
df_overdue_debt = df_overdue_debt.replace(np.nan, '')
df_overdue_debt = add_currency(df_overdue_debt)

df_overdue_count = tables.overdue_count(df_with_features)
df_overdue_count = df_overdue_count.replace(np.nan, '')
df_overdue_count = str_format(df_overdue_count)

df_debt_ratio = tables.debt_ratio(df_with_features)
df_debt_ratio = df_debt_ratio.replace(np.nan, '')
df_debt_ratio = percent_format(df_debt_ratio)

df_count_ratio = tables.count_ratio(df_with_features)
df_count_ratio = df_count_ratio.replace(np.nan, '')
df_count_ratio = percent_format(df_count_ratio)

df_loan_ratio = tables.loan_ratio(df_with_features)
df_loan_ratio = df_loan_ratio.replace(np.nan, '')
df_loan_ratio = percent_format(df_loan_ratio)

df_count_dynamic = tables.count_dynamic(df_with_features)
df_count_dynamic = df_count_dynamic.replace(np.nan, '')
df_count_dynamic = percent_format_2(df_count_dynamic)

df_debt_dynamic = tables.debt_dynamic(df_with_features)
df_debt_dynamic = df_debt_dynamic.replace(np.nan, '')
df_debt_dynamic = percent_format_2(df_debt_dynamic)

################
# Daily reports
################
df_with_features_daily = tables.create_features_daily(df_daily)

df_total_debt_daily = tables.total_debt(df_with_features_daily)
df_total_debt_daily = df_total_debt_daily.replace(np.nan, '')
df_total_debt_daily = add_currency(df_total_debt_daily)

df_total_loan_ctid_daily = tables.total_loan_ctid(df_with_features_daily)
df_total_loan_ctid_daily = df_total_loan_ctid_daily.replace(np.nan, '')
df_total_loan_ctid_daily = str_format(df_total_loan_ctid_daily)

df_overdue_debt_daily = tables.overdue_debt(df_with_features_daily)
df_overdue_debt_daily = df_overdue_debt_daily.replace(np.nan, '')
df_overdue_debt_daily = add_currency(df_overdue_debt_daily)

df_overdue_count_daily = tables.overdue_count(df_with_features_daily)
df_overdue_count_daily = df_overdue_count_daily.replace(np.nan, '')
df_overdue_count_daily = str_format(df_overdue_count_daily)

df_debt_ratio_daily = tables.debt_ratio(df_with_features_daily)
df_debt_ratio_daily = df_debt_ratio_daily.replace(np.nan, '')
df_debt_ratio_daily = percent_format(df_debt_ratio_daily)

df_count_ratio_daily = tables.count_ratio(df_with_features_daily)
df_count_ratio_daily = df_count_ratio_daily.replace(np.nan, '')
df_count_ratio_daily = percent_format(df_count_ratio_daily)

df_loan_ratio_daily = tables.loan_ratio(df_with_features_daily)
df_loan_ratio_daily = df_loan_ratio_daily.replace(np.nan, '')
df_loan_ratio_daily = percent_format(df_loan_ratio_daily)

df_count_dynamic_daily = tables.count_dynamic(df_with_features_daily)
df_count_dynamic_daily = df_count_dynamic_daily.replace(np.nan, '')
df_count_dynamic_daily = percent_format_2(df_count_dynamic_daily)

df_debt_dynamic_daily = tables.debt_dynamic(df_with_features_daily)
df_debt_dynamic_daily = df_debt_dynamic_daily.replace(np.nan, '')
df_debt_dynamic_daily = percent_format_2(df_debt_dynamic_daily)

app = dash.Dash(__name__, title='Динамика просроченной задолженности', server=server, url_base_pathname='/overdue/')

monthly_layout = html.Div([
    ################
    # Total debt
    ################
    html.Div([
       html.H4('Ссудный портфель')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_total_debt', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_total_debt')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='total_debt',
            columns=[{'name': i, 'id': i} for i in df_total_debt.columns],
            data=df_total_debt.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '60px', 'width': '60px', 'maxWidth': '120px', 'font-family': 'arial', 'fontSize': '14px'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
         dcc.Graph(
             figure=graphs.total_debt_graph_2(int_format(tables.total_debt(df_with_features)))
         )
    ], style={'marginLeft': '250px'}),
    ##############
    # Total loan
    ##############
    html.Div([
        html.H4('Количество договоров в портфеле')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_total_loan_ctid', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_total_loan_ctid')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='total_loan_ctid',
            columns=[{'name': i, 'id': i} for i in df_total_loan_ctid.columns],
            data=df_total_loan_ctid.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '60px', 'width': '60px', 'maxWidth': '120px', 'font-family': 'arial', 'fontSize': '14px'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
        dcc.Graph(
            figure=graphs.total_debt_graph_2(tables.total_loan_ctid(df_with_features))
        )
    ], style={'marginLeft': '250px'}),
    ################
    # Overdue debt
    ################
    html.Div([
        html.H4('Сумма просроченных ОД')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_overdue_debt', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_overdue_debt')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='overdue_debt',
            columns=[{'name': i, 'id': i} for i in df_overdue_debt.columns],
            data=df_overdue_debt.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '60px', 'width': '60px', 'maxWidth': '120px', 'font-family': 'arial', 'fontSize': '14px'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
        dcc.Graph(
            figure=graphs.total_debt_graph_2(int_format(tables.overdue_debt(df_with_features)))
        )
    ], style={'marginLeft': '250px'}),
    ################
    # Overdue count
    ################
    html.Div([
        html.H4('Количество просроченных договоров')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_overdue_count', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_overdue_count')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='overdue_count',
            columns=[{'name': i, 'id': i} for i in df_overdue_count.columns],
            data=df_overdue_count.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '60px', 'width': '60px', 'maxWidth': '120px', 'font-family': 'arial', 'fontSize': '14px',
                        'overflow': 'hidden'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
        dcc.Graph(
            figure=graphs.total_debt_graph_2(tables.overdue_count(df_with_features))
        )
    ], style={'marginLeft': '250px'}),
    #############
    # Debt ratio
    #############
    html.Div([
        html.H4('Доля просроченной задолженности')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_debt_ratio', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_debt_ratio')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='debt_ratio',
            columns=[{'name': i, 'id': i} for i in df_debt_ratio.columns],
            data=df_debt_ratio.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '60px', 'width': '60px', 'maxWidth': '120px', 'font-family': 'arial', 'fontSize': '14px',
                        'overflow': 'hidden'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
        dcc.Graph(
            figure=graphs.scatter_graph(hundred_format(tables.debt_ratio(df_with_features)))
        )
    ], style={'marginLeft': '250px'}),
    ###############
    # Count ratio
    ###############
    html.Div([
        html.H4('Доля просроченных договоров')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_count_ratio', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_count_ratio')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='count_ratio',
            columns=[{'name': i, 'id': i} for i in df_count_ratio.columns],
            data=df_count_ratio.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '60px', 'width': '60px', 'maxWidth': '120px', 'font-family': 'arial', 'fontSize': '14px',
                        'overflow': 'hidden'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
        dcc.Graph(
            figure=graphs.scatter_graph(hundred_format(tables.count_ratio(df_with_features)))
        )
    ], style={'marginLeft': '250px'}),
    ###############
    # Loan ratio
    ###############
    html.Div([
        html.H4('Доля по ОД')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_loan_ratio', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_loan_ratio')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='loan_ratio',
            columns=[{'name': i, 'id': i} for i in df_loan_ratio.columns],
            data=df_loan_ratio.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '60px', 'width': '60px', 'maxWidth': '120px', 'font-family': 'arial', 'fontSize': '14px',
                        'overflow': 'hidden'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
        dcc.Graph(
            figure=graphs.scatter_graph(hundred_format(tables.loan_ratio(df_with_features)))
        )
    ], style={'marginLeft': '250px'}),
    ##############
    # Count dynamic
    ##############
    html.Div([
        html.H4('Динамика по количеству договоров')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_count_dynamic', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_count_dynamic')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='count_dynamic',
            columns=[{'name': i, 'id': i} for i in df_count_dynamic.columns],
            data=df_count_dynamic.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '60px', 'width': '60px', 'maxWidth': '120px', 'font-family': 'arial', 'fontSize': '14px',
                        'overflow': 'hidden'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
        dcc.Graph(
            figure=graphs.scatter_graph(hundred_format(tables.count_dynamic(df_with_features)))
        )
    ], style={'marginLeft': '250px'}),
    #############
    # Debt dynamic
    #############
    html.Div([
        html.H4('Динамика по ОД')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_debt_dynamic', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_debt_dynamic')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='debt_dynamic',
            columns=[{'name': i, 'id': i} for i in df_debt_dynamic.columns],
            data=df_debt_dynamic.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '60px', 'width': '60px', 'maxWidth': '120px', 'font-family': 'arial', 'fontSize': '14px',
                        'overflow': 'hidden'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
        dcc.Graph(
            figure=graphs.scatter_graph(hundred_format(tables.debt_dynamic(df_with_features)))
        )
    ], style={'marginLeft': '250px'}),
])

daily_layout = html.Div([
    html.Div([
        html.H4('Выберите период', style={'font-family': 'arial'})
    ], style={'marginLeft': '100px'}),
    html.Div([
        dcc.DatePickerRange(
            id='date_picker_range',
            min_date_allowed=df.BASE_YMD.max() - datetime.timedelta(days=60),
            max_date_allowed=df.BASE_YMD.max() + datetime.timedelta(days=1),
            start_date=df.BASE_YMD.max() - datetime.timedelta(days=60),
            end_date=df.BASE_YMD.max(),
            display_format='DD.MM.YYYY',
            style={'font-family': 'arial'}
        )
    ], style={'marginLeft': '100px', 'marginTop': '20px'}),
    ################
    # Total debt
    ################
    html.Div([
       html.H4('Ссудный портфель')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_total_debt_daily', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_total_debt_daily')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='total_debt_daily',
            columns=[{'name': i, 'id': i} for i in df_total_debt_daily.columns],
            data=df_total_debt_daily.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '80px', 'width': '80px', 'maxWidth': '200px', 'font-family': 'arial', 'fontSize': '14px'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
         dcc.Graph(
             id='total_debt_daily_graph',
             figure=graphs.total_debt_graph_2(int_format(tables.total_debt(df_with_features_daily)))
         )
    ], style={'marginLeft': '250px'}),
    ##############
    # Total loan
    ##############
    html.Div([
        html.H4('Количество договоров в портфеле')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_total_loan_ctid_daily', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_total_loan_ctid_daily')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='total_loan_ctid_daily',
            columns=[{'name': i, 'id': i} for i in df_total_loan_ctid_daily.columns],
            data=df_total_loan_ctid_daily.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '80px', 'width': '80px', 'maxWidth': '200px', 'font-family': 'arial', 'fontSize': '14px'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
        dcc.Graph(
            id='total_loan_ctid_daily_graph',
            figure=graphs.total_debt_graph_2(tables.total_loan_ctid(df_with_features_daily))
        )
    ], style={'marginLeft': '250px'}),
    ################
    # Overdue debt
    ################
    html.Div([
        html.H4('Сумма просроченных ОД')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_overdue_debt_daily', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_overdue_debt_daily')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='overdue_debt_daily',
            columns=[{'name': i, 'id': i} for i in df_overdue_debt_daily.columns],
            data=df_overdue_debt_daily.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '80px', 'width': '80px', 'maxWidth': '200px', 'font-family': 'arial', 'fontSize': '14px'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
        dcc.Graph(
            id='overdue_debt_daily_graph',
            figure=graphs.total_debt_graph_2(int_format(tables.overdue_debt(df_with_features_daily)))
        )
    ], style={'marginLeft': '250px'}),
    ################
    # Overdue count
    ################
    html.Div([
        html.H4('Количество просроченных договоров')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_overdue_count_daily', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_overdue_count_daily')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='overdue_count_daily',
            columns=[{'name': i, 'id': i} for i in df_overdue_count_daily.columns],
            data=df_overdue_count_daily.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '80px', 'width': '80px', 'maxWidth': '200px', 'font-family': 'arial', 'fontSize': '14px',
                        'overflow': 'hidden'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
        dcc.Graph(
            id='overdue_count_daily_graph',
            figure=graphs.total_debt_graph_2(tables.overdue_count(df_with_features_daily))
        )
    ], style={'marginLeft': '250px'}),
    #############
    # Debt ratio
    #############
    html.Div([
        html.H4('Доля просроченной задолженности')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_debt_ratio_daily', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_debt_ratio_daily')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='debt_ratio_daily',
            columns=[{'name': i, 'id': i} for i in df_debt_ratio_daily.columns],
            data=df_debt_ratio_daily.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '80px', 'width': '80px', 'maxWidth': '200px', 'font-family': 'arial', 'fontSize': '14px',
                        'overflow': 'hidden'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
        dcc.Graph(
            id='debt_ratio_daily_graph',
            figure=graphs.scatter_graph(hundred_format(tables.debt_ratio(df_with_features_daily)))
        )
    ], style={'marginLeft': '250px'}),
    ###############
    # Count ratio
    ###############
    html.Div([
        html.H4('Доля просроченных договоров')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_count_ratio_daily', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_count_ratio_daily')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='count_ratio_daily',
            columns=[{'name': i, 'id': i} for i in df_count_ratio_daily.columns],
            data=df_count_ratio_daily.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '80px', 'width': '80px', 'maxWidth': '200px', 'font-family': 'arial', 'fontSize': '14px',
                        'overflow': 'hidden'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
        dcc.Graph(
            id='count_ratio_daily_graph',
            figure=graphs.scatter_graph(hundred_format(tables.count_ratio(df_with_features_daily)))
        )
    ], style={'marginLeft': '250px'}),
    ###############
    # Loan ratio
    ###############
    html.Div([
        html.H4('Доля по ОД')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_loan_ratio_daily', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_loan_ratio_daily')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='loan_ratio_daily',
            columns=[{'name': i, 'id': i} for i in df_loan_ratio_daily.columns],
            data=df_loan_ratio_daily.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '80px', 'width': '80px', 'maxWidth': '200px', 'font-family': 'arial', 'fontSize': '14px',
                        'overflow': 'hidden'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
        dcc.Graph(
            id='loan_ratio_daily_graph',
            figure=graphs.scatter_graph(hundred_format(tables.loan_ratio(df_with_features_daily)))
        )
    ], style={'marginLeft': '250px'}),
    ###############
    # Count dynamic
    ###############
    html.Div([
        html.H4('Динамика по количеству договоров')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_count_dynamic_daily', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_count_dynamic_daily')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='count_dynamic_daily',
            columns=[{'name': i, 'id': i} for i in df_count_dynamic_daily.columns],
            data=df_count_dynamic_daily.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '80px', 'width': '80px', 'maxWidth': '200px', 'font-family': 'arial', 'fontSize': '14px',
                        'overflow': 'hidden'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
        dcc.Graph(
            id='count_dynamic_daily_graph',
            figure=graphs.scatter_graph(hundred_format(tables.count_dynamic(df_with_features_daily)))
        )
    ], style={'marginLeft': '250px'}),
    #############
    # Debt dynamic
    #############
    html.Div([
        html.H4('Динамика по ОД')
    ], style={'textAlign': 'center', 'font-family': 'arial', 'fontSize': '25px'}),
    html.Div([
        html.Button('Экспорт таблицы', id='btn_debt_dynamic_daily', style={'width': '160px', 'height': '25px', 'color': 'white',
                                                                   'backgroundColor': 'green'}, n_clicks=0),
        Download(id='download_debt_dynamic_daily')
    ], style={'marginLeft': '100px'}),
    html.Div([
        dash_table.DataTable(
            id='debt_dynamic_daily',
            columns=[{'name': i, 'id': i} for i in df_debt_dynamic_daily.columns],
            data=df_debt_dynamic_daily.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': 'green', 'color': 'white'},
            style_cell={'textAlign': 'left', 'minWidth': '80px', 'width': '80px', 'maxWidth': '200px', 'font-family': 'arial', 'fontSize': '14px',
                        'overflow': 'hidden'}
        )
    ], style={'marginBottom': '30px', 'marginLeft': '100px', 'marginRight': '100px', 'marginTop': '30px'}),
    html.Div([
        dcc.Graph(
            id='debt_dynamic_daily_graph',
            figure=graphs.scatter_graph(hundred_format(tables.debt_dynamic(df_with_features_daily)))
        )
    ], style={'marginLeft': '250px'}),
])

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='monthly_overdue', children=[
        dcc.Tab(label='Ежемесячная динамика просроченной задолженности', value='monthly_overdue', children=[monthly_layout]),
        dcc.Tab(label='Ежедневная динамика просроченной задолженности', value='daily_overdue', children=[daily_layout])
    ], style={'fontSize': '20px', 'height': '80px', 'font-family': 'arial'})
])
###################
# Monthly callbacks
###################
@app.callback(
    Output('download_total_debt', 'data'), [Input('btn_total_debt', 'n_clicks')]
)
def download_total_debt(n_clicks):
    if n_clicks > 0:
        df_download = tables.total_debt(df_with_features)
        return send_data_frame(df_download.to_excel, "total_debt.xlsx", index=False)

@app.callback(
    Output('download_total_loan_ctid', 'data'), [Input('btn_total_loan_ctid', 'n_clicks')]
)
def download_total_loan_ctid(n_clicks):
    if n_clicks > 0:
        df_download = tables.total_loan_ctid(df_with_features)
        return send_data_frame(df_download.to_excel, "total_loan_ctid.xlsx", index=False)

@app.callback(
    Output('download_overdue_debt', 'data'), [Input('btn_overdue_debt', 'n_clicks')]
)
def download_overdue_debt(n_clicks):
    if n_clicks > 0:
        df_download = tables.overdue_debt(df_with_features)
        return send_data_frame(df_download.to_excel, "overdue_debt.xlsx", index=False)

@app.callback(
    Output('download_overdue_count', 'data'), [Input('btn_overdue_count', 'n_clicks')]
)
def download_overdue_count(n_clicks):
    if n_clicks > 0:
        df_download = tables.overdue_count(df_with_features)
        return send_data_frame(df_download.to_excel, "overdue_count.xlsx", index=False)

@app.callback(
    Output('download_debt_ratio', 'data'), [Input('btn_debt_ratio', 'n_clicks')]
)
def download_debt_ratio(n_clicks):
    if n_clicks > 0:
        df_download = tables.debt_ratio(df_with_features)
        return send_data_frame(df_download.to_excel, "debt_ratio.xlsx", index=False)

@app.callback(
    Output('download_count_ratio', 'data'), [Input('btn_count_ratio', 'n_clicks')]
)
def download_count_ratio(n_clicks):
    if n_clicks > 0:
        df_download = tables.count_ratio(df_with_features)
        return send_data_frame(df_download.to_excel, "count_ratio.xlsx", index=False)

@app.callback(
    Output('download_loan_ratio', 'data'), [Input('btn_loan_ratio', 'n_clicks')]
)
def download_loan_ratio(n_clicks):
    if n_clicks > 0:
        df_download = tables.loan_ratio(df_with_features)
        return send_data_frame(df_download.to_excel, "loan_ratio.xlsx", index=False)

@app.callback(
    Output('download_count_dynamic', 'data'), [Input('btn_count_dynamic', 'n_clicks')]
)
def download_count_dynamic(n_clicks):
    if n_clicks > 0:
        df_download = tables.count_dynamic(df_with_features)
        return send_data_frame(df_download.to_excel, "count_dynamic.xlsx", index=False)

@app.callback(
    Output('download_debt_dynamic', 'data'), [Input('btn_debt_dynamic', 'n_clicks')]
)
def download_debt_dynamic(n_clicks):
    if n_clicks > 0:
        df_download = tables.debt_dynamic(df_with_features)
        return send_data_frame(df_download.to_excel, "debt_dynamic.xlsx", index=False)

##################
# Daily callbacks
##################
@app.callback(
    Output('download_total_debt_daily', 'data'), [Input('btn_total_debt_daily', 'n_clicks')],
    [State('date_picker_range', 'start_date'), State('date_picker_range', 'end_date')]
)
def download_total_debt_daily(n_clicks, start_date, end_date):
    if n_clicks > 0:
        start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
        end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
        df_download = tables.total_debt(df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)])
        return send_data_frame(df_download.to_excel, "total_debt_daily.xlsx", index=False)

@app.callback(
    Output('download_total_loan_ctid_daily', 'data'), [Input('btn_total_loan_ctid_daily', 'n_clicks')],
    [State('date_picker_range', 'start_date'), State('date_picker_range', 'end_date')]
)
def download_total_loan_ctid_daily(n_clicks, start_date, end_date):
    if n_clicks > 0:
        start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
        end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
        df_download = tables.total_loan_ctid(df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)])
        return send_data_frame(df_download.to_excel, "total_loan_ctid_daily.xlsx", index=False)

@app.callback(
    Output('download_overdue_debt_daily', 'data'), [Input('btn_overdue_debt_daily', 'n_clicks')],
    [State('date_picker_range', 'start_date'), State('date_picker_range', 'end_date')]
)
def download_overdue_debt_daily(n_clicks, start_date, end_date):
    if n_clicks > 0:
        start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
        end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
        df_download = tables.overdue_debt(df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)])
        return send_data_frame(df_download.to_excel, "overdue_debt_daily.xlsx", index=False)

@app.callback(
    Output('download_overdue_count_daily', 'data'), [Input('btn_overdue_count_daily', 'n_clicks')],
    [State('date_picker_range', 'start_date'), State('date_picker_range', 'end_date')]
)
def download_overdue_count_daily(n_clicks, start_date, end_date):
    if n_clicks > 0:
        start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
        end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
        df_download = tables.overdue_count(df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)])
        return send_data_frame(df_download.to_excel, "overdue_count_daily.xlsx", index=False)

@app.callback(
    Output('download_debt_ratio_daily', 'data'), [Input('btn_debt_ratio_daily', 'n_clicks')],
    [State('date_picker_range', 'start_date'), State('date_picker_range', 'end_date')]
)
def download_debt_ratio_daily(n_clicks, start_date, end_date):
    if n_clicks > 0:
        start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
        end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
        df_download = tables.debt_ratio(df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)])
        return send_data_frame(df_download.to_excel, "debt_ratio_daily.xlsx", index=False)

@app.callback(
    Output('download_count_ratio_daily', 'data'), [Input('btn_count_ratio_daily', 'n_clicks')],
    [State('date_picker_range', 'start_date'), State('date_picker_range', 'end_date')]
)
def download_count_ratio_daily(n_clicks, start_date, end_date):
    if n_clicks > 0:
        start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
        end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
        df_download = tables.count_ratio(df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)])
        return send_data_frame(df_download.to_excel, "count_ratio_daily.xlsx", index=False)

@app.callback(
    Output('download_loan_ratio_daily', 'data'), [Input('btn_loan_ratio_daily', 'n_clicks')],
    [State('date_picker_range', 'start_date'), State('date_picker_range', 'end_date')]
)
def download_loan_ratio_daily(n_clicks, start_date, end_date):
    if n_clicks > 0:
        start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
        end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
        df_download = tables.loan_ratio(df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)])
        return send_data_frame(df_download.to_excel, "loan_ratio_daily.xlsx", index=False)

@app.callback(
    Output('download_count_dynamic_daily', 'data'), [Input('btn_count_dynamic_daily', 'n_clicks')],
    [State('date_picker_range', 'start_date'), State('date_picker_range', 'end_date')]
)
def download_count_dynamic_daily(n_clicks, start_date, end_date):
    if n_clicks > 0:
        start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
        end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
        df_download = tables.count_dynamic(df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)])
        return send_data_frame(df_download.to_excel, "count_dynamic_daily.xlsx", index=False)

@app.callback(
    Output('download_debt_dynamic_daily', 'data'), [Input('btn_debt_dynamic_daily', 'n_clicks')],
    [State('date_picker_range', 'start_date'), State('date_picker_range', 'end_date')]
)
def download_debt_dynamic_daily(n_clicks, start_date, end_date):
    if n_clicks > 0:
        start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
        end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
        df_download = tables.debt_dynamic(df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)])
        return send_data_frame(df_download.to_excel, "debt_dynamic_daily.xlsx", index=False)

@app.callback(
    [Output('total_debt_daily', 'columns'), Output('total_debt_daily', 'data')], [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_total_debt_daily(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]
    df_total_debt_daily_2 = tables.total_debt(df_with_features_daily_2)
    df_total_debt_daily_2 = add_currency(df_total_debt_daily_2)

    return [{'name': i, 'id': i} for i in df_total_debt_daily_2.columns], df_total_debt_daily_2.to_dict('records')

@app.callback(
    Output('total_debt_daily_graph', 'figure'), [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_total_debt_daily_graph(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]

    return graphs.total_debt_graph_2(int_format(tables.total_debt(df_with_features_daily_2)))

@app.callback(
    [Output('total_loan_ctid_daily', 'columns'), Output('total_loan_ctid_daily', 'data')], [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_total_loan_ctid_daily(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]
    df_total_loan_ctid_daily_2 = tables.total_loan_ctid(df_with_features_daily_2)
    df_total_loan_ctid_daily_2 = str_format(df_total_loan_ctid_daily_2)

    return [{'name': i, 'id': i} for i in df_total_loan_ctid_daily_2.columns], df_total_loan_ctid_daily_2.to_dict('records')

@app.callback(
    Output('total_loan_ctid_daily_graph', 'figure'), [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_total_loan_ctid_daily_graph(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]

    return graphs.total_debt_graph_2(tables.total_loan_ctid(df_with_features_daily_2))

@app.callback(
    [Output('overdue_debt_daily', 'columns'), Output('overdue_debt_daily', 'data')], [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_overdue_debt_daily(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]
    df_overdue_debt_daily_2 = tables.overdue_debt(df_with_features_daily_2)
    df_overdue_debt_daily_2 = add_currency(df_overdue_debt_daily_2)

    return [{'name': i, 'id': i} for i in df_overdue_debt_daily_2.columns], df_overdue_debt_daily_2.to_dict('records')

@app.callback(
    Output('overdue_debt_daily_graph', 'figure'), [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_overdue_debt_daily_graph(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]

    return graphs.total_debt_graph_2(int_format(tables.overdue_debt(df_with_features_daily_2)))

@app.callback(
    [Output('overdue_count_daily', 'columns'), Output('overdue_count_daily', 'data')], [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_overdue_count_daily(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]
    df_overdue_count_daily_2 = tables.overdue_count(df_with_features_daily_2)
    df_overdue_count_daily_2 = str_format(df_overdue_count_daily_2)

    return [{'name': i, 'id': i} for i in df_overdue_count_daily_2.columns], df_overdue_count_daily_2.to_dict('records')

@app.callback(
    Output('overdue_count_daily_graph', 'figure'), [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_overdue_count_daily_graph(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]

    return graphs.total_debt_graph_2(tables.overdue_count(df_with_features_daily_2))

@app.callback(
    [Output('debt_ratio_daily', 'columns'), Output('debt_ratio_daily', 'data')], [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_debt_ratio_daily(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]
    df_debt_ratio_daily_2 = tables.debt_ratio(df_with_features_daily_2)
    df_debt_ratio_daily_2 = percent_format(df_debt_ratio_daily_2)

    return [{'name': i, 'id': i} for i in df_debt_ratio_daily_2.columns], df_debt_ratio_daily_2.to_dict('records')

@app.callback(
    Output('debt_ratio_daily_graph', 'figure'), [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_debt_ratio_daily_graph(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]

    return graphs.scatter_graph(hundred_format(tables.debt_ratio(df_with_features_daily_2)))

@app.callback(
    [Output('count_ratio_daily', 'columns'), Output('count_ratio_daily', 'data')], [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_count_ratio_daily(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]
    df_count_ratio_daily_2 = tables.count_ratio(df_with_features_daily_2)
    df_count_ratio_daily_2 = percent_format(df_count_ratio_daily_2)

    return [{'name': i, 'id': i} for i in df_count_ratio_daily_2.columns], df_count_ratio_daily_2.to_dict('records')

@app.callback(
    Output('count_ratio_daily_graph', 'figure'), [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_count_ratio_daily_graph(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]

    return graphs.scatter_graph(hundred_format(tables.count_ratio(df_with_features_daily_2)))

@app.callback(
    [Output('loan_ratio_daily', 'columns'), Output('loan_ratio_daily', 'data')], [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_loan_ratio_daily(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]
    df_loan_ratio_daily_2 = tables.loan_ratio(df_with_features_daily_2)
    df_loan_ratio_daily_2 = percent_format(df_loan_ratio_daily_2)

    return [{'name': i, 'id': i} for i in df_loan_ratio_daily_2.columns], df_loan_ratio_daily_2.to_dict('records')

@app.callback(
    Output('loan_ratio_daily_graph', 'figure'), [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_loan_ratio_daily_graph(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]

    return graphs.scatter_graph(hundred_format(tables.loan_ratio(df_with_features_daily_2)))

@app.callback(
    [Output('count_dynamic_daily', 'columns'), Output('count_dynamic_daily', 'data')], [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_count_dynamic_daily(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]
    df_count_dynamic_daily_2 = tables.count_dynamic(df_with_features_daily_2)
    df_count_dynamic_daily_2 = percent_format_2(df_count_dynamic_daily_2)

    return [{'name': i, 'id': i} for i in df_count_dynamic_daily_2.columns], df_count_dynamic_daily_2.to_dict('records')

@app.callback(
    Output('count_dynamic_daily_graph', 'figure'), [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_count_dynamic_daily_graph(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]

    return graphs.scatter_graph(hundred_format(tables.count_dynamic(df_with_features_daily_2)))

@app.callback(
    [Output('debt_dynamic_daily', 'columns'), Output('debt_dynamic_daily', 'data')], [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_debt_dynamic_daily(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]
    df_debt_dynamic_daily_2 = tables.debt_dynamic(df_with_features_daily_2)
    df_debt_dynamic_daily_2 = percent_format_2(df_debt_dynamic_daily_2)

    return [{'name': i, 'id': i} for i in df_debt_dynamic_daily_2.columns], df_debt_dynamic_daily_2.to_dict('records')

@app.callback(
    Output('debt_dynamic_daily_graph', 'figure'), [Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date')]
)
def update_debt_dynamic_daily_graph(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df_with_features_daily_2 = df_with_features_daily[(df_with_features_daily.BASE_YMD >= start_date) & (df_with_features_daily.BASE_YMD <= end_date)]

    return graphs.scatter_graph(hundred_format(tables.debt_dynamic(df_with_features_daily_2)))

if __name__ == '__main__':
    app.run_server(debug=True)