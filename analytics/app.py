import pandas as pd
import cx_Oracle
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import datetime
import dash_bootstrap_components as dbc
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
import analytics.tables as tables
import analytics.graphs as graphs
import os
import datetime
import numpy as np
import sqlalchemy
import json
from server import server

external_stylesheets = [
    'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap-grid.min.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title='Retail Risk Analytics', update_title='Обновляется...',
                server=server, url_base_pathname='/')
app.config.suppress_callback_exceptions = True

client_path = '//10.20.42.54/share_all/dashboards/settings/'
server_path = '/home/user/Desktop/share/dashboards/settings/'

try:
    with open(client_path + 'settings.json', 'r') as file:
        settings = json.load(file)
except FileNotFoundError:
    with open(server_path + 'settings.json', 'r') as file:
        settings = json.load(file)

try:
    with open(client_path + 'patterns.json', 'r', encoding='utf-8') as p:
        patterns = json.load(p)
except FileNotFoundError:
    with open(server_path + 'patterns.json', 'r', encoding='utf-8') as p:
        patterns = json.load(p)

user = settings['user']
password = settings['password']
host = settings['host']
port = settings['port']
db = settings['db']
engine = sqlalchemy.create_engine('oracle+cx_oracle://' + user + ':' + password + '@' + host + ':' + port + '/?service_name=' + db)

df = pd.read_sql("SELECT * FROM " + settings['rri_table_name'] + " WHERE " + settings['rri_month'] + " >= TO_DATE('01.01.2019', 'DD.MM.YYYY')", engine)
df_ar = pd.read_sql("SELECT * FROM " + settings['ar_table_name'] + " WHERE " + settings['ar_date'] + " >= TO_DATE('01.01.2020', 'DD.MM.YYYY')", engine)
dfv = pd.read_sql("SELECT * FROM " + settings['v_table_name'] + " WHERE " + settings['v_given_month'] + " >= TO_DATE('01.01.2019', 'DD.MM.YYYY')", engine)

df = df[df.loan_ctid != '14100000000000285927504']
df.columns = [col.upper() for col in df.columns]
df_ar.columns = [col.upper() for col in df_ar.columns]
dfv.columns = [col.upper() for col in dfv.columns]

df = df.rename(columns={settings['rri_amount']: 'AMT_CREDIT', settings['rri_month']: 'MONTH_SIGN_CTR', settings['rri_fpd_0']: 'FLAG_FPD_0_HIST',
                        settings['rri_spd_0']: 'FLAG_SPD_0_HIST', settings['rri_tpd_0']: 'FLAG_TPD_0_HIST', settings['rri_fpd_5']: 'FLAG_FPD_5_HIST',
                        settings['rri_spd_5']: 'FLAG_SPD_5_HIST', settings['rri_tpd_5']: 'FLAG_TPD_5_HIST', settings['rri_fpd_15']: 'FLAG_FPD_15_HIST',
                        settings['rri_spd_15']: 'FLAG_SPD_15_HIST', settings['rri_tpd_15']: 'FLAG_TPD_15_HIST', settings['rri_fpd_30']: 'FLAG_FPD_30_HIST',
                        settings['rri_spd_30']: 'FLAG_SPD_30_HIST', settings['rri_tpd_30']: 'FLAG_TPD_30_HIST', settings['rri_fpd_45']: 'FLAG_FPD_45_HIST',
                        settings['rri_spd_45']: 'FLAG_SPD_45_HIST', settings['rri_tpd_45']: 'FLAG_TPD_45_HIST', settings['rri_fpd_60']: 'FLAG_FPD_60_HIST',
                        settings['rri_spd_60']: 'FLAG_SPD_60_HIST', settings['rri_tpd_60']: 'FLAG_TPD_60_HIST', settings['rri_fpd_90']: 'FLAG_FPD_90_HIST',
                        settings['rri_spd_90']: 'FLAG_SPD_90_HIST', settings['rri_tpd_90']: 'FLAG_TPD_90_HIST', settings['rri_fpd_active']: 'FLAG_FPD_ACTIVE',
                        settings['rri_spd_active']: 'FLAG_SPD_ACTIVE', settings['rri_tpd_active']: 'FLAG_TPD_ACTIVE'})

df_ar = df_ar.rename(columns={settings['ar_date']: 'DREG', settings['ar_cancel']: 'CANCEL', settings['ar_cnt']: 'CNT', settings['ar_acc']: 'ACC',
                              settings['ar_acc2']: 'ACC2', settings['ar_loan_s_min']: 'LOAN_S_MIN', settings['ar_acc_amt']: 'ACC_AMT',
                              settings['ar_acc_loan']: 'ACC_LOAN', settings['ar_loan_amt']: 'LOAN_AMT', settings['ar_groupofreject']: 'GROUPOFREJECT',
                              settings['ar_groupofalerts']: 'GROUPOFALERTS', settings['ar_week']: 'WEEK'})

dfv = dfv.rename(columns={settings['v_given_month']: 'GIVEN_MONTH', settings['v_report_month']: 'REPORT_MONTH', settings['v_loan_sum']: 'LOAN_SUM',
                          settings['v_debt_5']: 'DEBT_AMOUNT_5_PLUS', settings['v_debt_30']: 'DEBT_AMOUNT_30_PLUS',
                          settings['v_debt_60']: 'DEBT_AMOUNT_60_PLUS', settings['v_debt_90']: 'DEBT_AMOUNT_90_PLUS', settings['v_age']: 'AGE',
                          settings['v_products']: 'PRODUCTS', settings['v_program']: 'PROGRAMM', settings['v_city']: 'CITY2', settings['v_segment']: 'SEGMENT'})

def chg_month_to_word(month):
    d = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
         7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}
    return d[month.month] + ' ' + str(month.year)

def chg_npmonth_to_corr(month):
    return month.astype('M8[D]').astype('O')

def chg_word_to_month(word):
    month = word.split()[0]
    year = int(word.split()[1])
    d = {'Январь': 1, 'Февраль': 2, 'Март': 3, 'Апрель': 4, 'Май': 5, 'Июнь': 6,
         'Июль': 7, 'Август': 8, 'Сентябрь': 9, 'Октябрь': 10, 'Ноябрь': 11, 'Декабрь': 12}
    return datetime.date(year, d[month], 1)

def chg_str_to_date(str_date):
    year = int(str_date.split('-')[0])
    month = int(str_date.split('-')[1])
    day = int(str_date.split('-')[2])

    return datetime.date(year, month, day)

def chg_date_to_week(month, day):
    d_month = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
               9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'}

    if day >= 1 and day <= 7:
        week = 1
    if day >= 8 and day <= 14:
        week = 2
    if day >= 15 and day <= 21:
        week = 3
    if day >= 22 and day <= 28:
        week = 4
    if day >= 29:
        week = 5

    return str(week) + ' неделя ' + d_month[month]

#df_ar['WEEK_IN_WORD'] = df_ar.DREG.apply(lambda x: chg_date_to_week(x.month, x.day))
df_ar['DREG'] = df_ar.DREG.apply(lambda x: datetime.date(x.year, x.month, x.day))
df_ar['WEEK'] = df_ar.WEEK.apply(lambda x: datetime.date(x.year, x.month, x.day))
df_ar['MONTH_IN_WORD'] = df_ar.DREG.apply(lambda x: chg_month_to_word(x))
df_ar['TYPEOFCLIENTS'] = df_ar.TYPEOFCLIENTS.replace('.Пенсионер', 'Пенсионер')
df_ar['TYPEOFCLIENTS'] = df_ar.TYPEOFCLIENTS.replace('`', 'Стандарт')
df_ar['TYPEOFCLIENTS'] = df_ar.TYPEOFCLIENTS.replace('KZ', 'Стандарт')
df_ar['CHALLENGER'] = df_ar['CHALLENGER'].fillna(value=np.nan)
df_ar['SCORE_CARD_NAME'] = df_ar['SCORE_CARD_NAME'].fillna(value=np.nan)
df_ar['COR'] = df_ar['COR'].replace(np.nan, 0)
df_ar['COR'] = df_ar['COR'].astype(int)
df_ar['COR'] = df_ar['COR'].astype(str)
df_ar['COR'] = df_ar['COR'].replace('0', '')
df_ar['CHALLENGER'] = df_ar['CHALLENGER'].replace(np.nan, '')
df_ar['SCORE_CARD_NAME'] = df_ar['SCORE_CARD_NAME'].replace(np.nan, '')

flag_active_loans = df.FLAG_ACTIVE_LOAN.unique()

products = df.PRODUCT.unique()
products.sort()

months = df.MONTH_SIGN_CTR.unique()
months.sort()
months_word = []
if len(months) > 0:
    for month in months:
        months_word.append(chg_month_to_word(chg_npmonth_to_corr(month)))

regions = df.REGION_.unique()
regions.sort()

analysis_types = ['FPD SPD TPD с просрочкой больше дня', 'FPD SPD TPD с просрочкой больше 5 дней',
                  'FPD SPD TPD с просрочкой больше 15 дней', 'FPD SPD TPD с просрочкой больше 30 дней',
                  'FPD SPD TPD с просрочкой больше 45 дней', 'FPD SPD TPD с просрочкой больше 60 дней',
                  'FPD SPD TPD с просрочкой больше 90 дней', 'Действующие FPD SPD TPD']

analysis_forms = ['Доля по сумме выдачи', 'Доля по количеству выдачи']

analysis_layout = [
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H5('Типы ранних риск индикаторов')
                    ], style={'marginBottom': '10px', 'borderBottom': '3px solid green'}),
                    dcc.Dropdown(
                        multi=False,
                        id='analysis_dd',
                        options=[{'label': analysis_type, 'value': analysis_type} for analysis_type in analysis_types],
                        value=analysis_types[0],
                        clearable=False,
                        style={'width': '500px'}
                    )
                ], style={'marginLeft': '30px', 'marginTop': '30px'}),
                html.Div([
                    html.Div([
                        html.H5('Типы анализа')
                    ], style={'marginBottom': '10px', 'borderBottom': '3px solid green'}),
                    dcc.Dropdown(
                        multi=False,
                        id='analysis_form_dd',
                        options=[{'label': analysis, 'value': analysis} for analysis in analysis_forms],
                        value=analysis_forms[0],
                        style={'width': '500px'},
                        clearable=False
                    )
                ], style={'marginLeft': '30px', 'marginTop': '20px'}),
                html.Div([
                    dbc.Row([
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.H5('Регионы')
                                    ])
                                ]),
                                dbc.Col([
                                    html.Div([
                                        html.Button('Обновить', id='btn_region_update', n_clicks=0,
                                                    style={'width': '80px', 'height': '25px', 'marginLeft': '310px',
                                                           'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                    ])
                                ])
                            ])
                        ], style={'marginLeft': '15px', 'marginTop': '30px'})
                    ])
                ], style={'borderBottom': '3px solid green', 'width': '500px', 'marginLeft': '30px'}),
                html.Div([
                    dcc.Dropdown(
                        multi=True,
                        id='regions_dd',
                        options=[{'label': region, 'value': region} for region in regions],
                        value=regions,
                        style={'width': '500px', 'fontSize': '14px'},
                        placeholder='Выберите регионы'
                    )
                ], style={'marginLeft': '30px', 'marginTop': '10px'})
            ], width='auto'),
            dbc.Col([
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H5('Продукты')
                            ])
                        ]),
                        dbc.Col([
                            html.Div([
                                html.Button('Обновить', id='btn_product_update', n_clicks=0,
                                                style={'width': '80px', 'height': '25px', 'marginLeft': '225px',
                                                       'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                            ])
                        ])
                    ])
                ], style={'marginTop': '30px', 'marginLeft': '30px', 'borderBottom': '3px solid green'}),
                html.Div([
                    dcc.Dropdown(
                        multi=True,
                        id='products_dd',
                        options=[{'label': product, 'value': product} for product in products],
                        value=products,
                        style={'width': '600px', 'fontSize': '14px'},
                        placeholder='Выберите продукты'
                    )
                ], style={'marginLeft': '30px', 'marginTop': '10px', 'marginBottom': '30px'})
            ], width='auto'),
            dbc.Col([
                html.Div([
                    dbc.Row([
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.H5('Месяц выдачи')
                                    ], style={'marginLeft': '15px'})
                                ]),
                                dbc.Col([
                                    html.Div([
                                        html.Button('Обновить', id='btn_month_update', n_clicks=0,
                                                    style={'width': '80px', 'height': '25px', 'marginLeft': '350px',
                                                           'fontSize': '12px', 'border': '1px solid', 'borderRadius': '3px'})
                                    ])
                                ])
                            ])
                        ])
                    ])
                ], style={'borderBottom': '3px solid green', 'marginTop': '30px', 'marginLeft': '30px', 'marginRight': '30px'}),
                html.Div([
                    dcc.Dropdown(
                        multi=True,
                        id='months_dd',
                        options=[{'label': month, 'value': month} for month in months_word],
                        value=months_word,
                        style={'width': '600px', 'fontSize': '14px'},
                        placeholder='Выберите месяц'
                    )
                ], style={'marginLeft': '30px', 'marginTop': '10px', 'marginBottom': '30px'}),
                html.Div([
                    html.Div([
                        html.H5('Активность кредита')
                    ], style={'borderBottom': '3px solid green', 'marginBottom': '10px'}),
                    dcc.Dropdown(
                        multi=True,
                        id='active_loans_dd',
                        options=[{'label': flag_active_loan, 'value': flag_active_loan} for flag_active_loan in
                                 flag_active_loans],
                        value=flag_active_loans,
                        style={'width': '600px', 'fontSize': '14px'},
                        placeholder='Выберите активность'
                    )
                ], style={'margin': '30px'})
            ], width='auto')
        ]),
        dbc.Row([
           html.Div([], id='fpd_spd_tpd_title', style={'marginTop': '80px', 'borderBottom': '5px solid green'})
        ], align='center', justify='center'),
        dbc.Row([
            html.Div([
                html.Button(children='Выгрузить таблицу', n_clicks=0, id='btn_download_fpd',
                            style={'width': '180px', 'height': '25px', 'marginLeft': '90px', 'marginTop': '20px', 'backgroundColor': 'green',
                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid', 'color': 'white'}),
                Download(id='download-fpd')
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='table'
                    )
                ], style={'marginTop': '30px'})
            ], width='auto'),
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='graph'
                    )
                ], style={'marginTop': '30px'})
            ])
        ]),
        dbc.Row([
            html.Div([
                html.Button(children='Добавить регионы для сравнения', n_clicks=0, id='btn_add_to_comp',
                            style={'width': '280px', 'height': '25px', 'marginLeft': '60px', 'marginTop': '10px', 'marginBottom': '30px',
                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
            ])
        ]),
        dbc.Row([
            html.Div([], id='comp_regions_layout')
        ])
    ])
]

comp_regions_layout = [
    html.Div([
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.H5('Регионы для сравнения')
                ], width='auto'),
                dbc.Col([
                    html.Button('Обновить', id='btn_comp_region_update', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '145px',
                                                                                            'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                ], width='auto')
            ])
        ], style={'marginLeft': '60px'}),
        dbc.Row([
            html.Div([
                dcc.Dropdown(
                    multi=True,
                    id='comp_regions_dd',
                    options=[{'label': region, 'value': region} for region in regions],
                    value=regions,
                    style={'width': '500px', 'fontSize': '14px'},
                    placeholder='Выберите регионы'
                )
            ], style={'marginLeft': '75px', 'marginTop': '10px'})
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='comp_table'
                    )
                ], style={'marginTop': '20px'})
            ], width='auto'),
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='comp_graph'
                    )
                ], style={'marginTop': '20px'})
            ])
        ])
    ])
]

settings_layout = [
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5('Основные настройки')
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'textAlign': 'center'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Имя пользователя')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='main_user_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['user']
                                )
                            ])
                        ])
                    ])
                ]),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Пароль')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='main_password_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['password'],
                                    type='password'
                                )
                            ])
                        ])
                    ])
                ]),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Имя хоста')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='main_host_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['host']
                                )
                            ])
                        ])
                    ])
                ]),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Имя сервиса')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='main_service_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['db']
                                )
                            ])
                        ])
                    ])
                ]),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Порт')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='main_port_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['port']
                                )
                            ])
                        ])
                    ])
                ]),
            ]),
            dbc.Col([

            ]),
            dbc.Col([

            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5('Настройки страницы Анализа ранних риск индикаторов')
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'textAlign': 'center'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Имя таблицы')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_table_name_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_table_name']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Сумма выдачи')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_amount_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_amount']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Месяц выдачи')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_month_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_month']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('FPD с просрочкой больше 0')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_fpd0_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_fpd_0']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('SPD с просрочкой больше 0')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_spd0_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_spd_0']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('TPD с просрочкой больше 0')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_tpd0_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_tpd_0']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('FPD с просрочкой больше 5')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_fpd5_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_fpd_5']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('SPD с просрочкой больше 5')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_spd5_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_spd_5']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('TPD с просрочкой больше 5')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_tpd5_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_tpd_5']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('FPD с просрочкой больше 15')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_fpd15_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_fpd_15']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('SPD с просрочкой больше 15')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_spd15_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_spd_15']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('TPD с просрочкой больше 15')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_tpd15_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_tpd_15']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('FPD с просрочкой больше 30')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_fpd30_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_fpd_30']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('SPD с просрочкой больше 30')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_spd30_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_spd_30']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('TPD с просрочкой больше 30')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_tpd30_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_tpd_30']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('FPD с просрочкой больше 45')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_fpd45_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_fpd_45']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('SPD с просрочкой больше 45')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_spd45_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_spd_45']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('TPD с просрочкой больше 45')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_tpd45_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_tpd_45']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('FPD с просрочкой больше 60')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_fpd60_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_fpd_60']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('SPD с просрочкой больше 60')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_spd60_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_spd_60']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('TPD с просрочкой больше 60')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_tpd60_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_tpd_60']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('FPD с просрочкой больше 90')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_fpd90_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_fpd_90']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('SPD с просрочкой больше 90')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_spd90_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_spd_90']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('TPD с просрочкой больше 90')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_tpd90_hist_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_tpd_90']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('FPD с действующей просрочкой')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_fpd_active_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_fpd_active']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('SPD с действующей просрочкой')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_spd_active_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_spd_active']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('TPD с действующей просрочкой')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='rri_tpd_active_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['rri_tpd_active']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    html.Button('Сохранить данные', id='btn_save_settings', n_clicks=0,
                                style={'width': '150px', 'height': '30px', 'fontSize': '14px', 'border': '1px solid', 'borderRadius': '4px'})
                ], style={'marginTop': '20px', 'marginLeft': '150px'}),
                html.Div([
                ], id='text_save_settings'),
                html.Div([
                    html.Button('Перезагрузить', id='btn_restart_system', n_clicks=0,
                                style={'width': '150px', 'height': '30px', 'fontSize': '14px', 'border': '1px solid', 'borderRadius': '4px', 'backgroundColor': 'red', 'color': 'white'})
                ], style={'marginTop': '20px', 'marginLeft': '150px'}),
                html.Div([
                ], id='text_restart_system')
            ]),
            dbc.Col([
                html.Div([
                    html.H5('Настройки страницы Анализа уровня одобрения')
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'textAlign': 'center'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Наименование таблицы')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='ar_table_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['ar_table_name']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Дата')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='ar_date_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['ar_date']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Заявки нерассмотренные скор. системой')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='ar_cancel_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['ar_cancel']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Общее кол-во заявок')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='ar_cnt_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['ar_cnt']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Одоб. заявки с учетом альтер. предложений')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='ar_acc_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['ar_acc']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Одоб. заявки без учета альтер. предложений')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='ar_acc2_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['ar_acc2']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Запрошенная сумма')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='ar_loan_s_min_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['ar_loan_s_min']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Одобренная сумма')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='ar_acc_amt_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['ar_acc_amt']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Кол-во выданных займов')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='ar_acc_loan_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['ar_acc_loan']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Выданная сумма')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='ar_loan_amt_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['ar_loan_amt']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Группа отказов')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='ar_group_reject_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['ar_groupofreject']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Подгруппа отказов')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='ar_group_alert_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['ar_groupofalerts']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Начало недели')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='ar_week_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['ar_week']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
            ]),
            dbc.Col([
                html.Div([
                    html.H5('Настройки страницы Анализа винтажей')
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'textAlign': 'center'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Наименование таблицы')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='v_table_name_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['v_table_name']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Поколение выдачи')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='v_given_month_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['v_given_month']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Отчетная дата')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='v_report_month_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['v_report_month']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Сумма выдачи')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='v_loan_sum_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['v_loan_sum']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('ОД с просрочкой больше 5 дней')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='v_debt_5_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['v_debt_5']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('ОД с просрочкой больше 30 дней')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='v_debt_30_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['v_debt_30']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('ОД с просрочкой больше 60 дней')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='v_debt_60_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['v_debt_60']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('ОД с просрочкой больше 90 дней')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='v_debt_90_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['v_debt_90']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Возраст')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='v_age_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['v_age']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Продукты')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='v_products_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['v_products']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Программы')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='v_programs_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['v_program']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Регионы')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='v_city_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['v_city']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Label('Сегменты')
                            ], style={'textAlign': 'right'})
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='v_segment_input',
                                    style={'borderRadius': '5px', 'border': '1px solid'},
                                    value=settings['v_segment']
                                )
                            ])
                        ])
                    ])
                ], style={'marginLeft': '20px', 'marginTop': '10px'}),
            ])
        ])
    ])
]

#Approval rate analysis layout

ar_date = df_ar.DREG.unique()
ar_date.sort()

group_of_products = df_ar.GROUPOFPRODUCT.unique()
group_of_products.sort()

ar_products = df_ar.PRODUCT.unique()
ar_products.sort()

ar_cities = df_ar.CITY.unique()
ar_cities.sort()

ar_segments = df_ar.SEGMENT.unique()
ar_segments.sort()

ar_type_of_clients = df_ar.TYPEOFCLIENTS.unique()
ar_type_of_clients.sort()

ar_otdels = df_ar.LONGNAME.unique()

ar_strategies = df_ar.STRATEGY.unique()
ar_strategies.sort()

ar_cors = df_ar.COR.unique()
ar_cors.sort()

ar_challengers = df_ar.CHALLENGER.unique()
ar_challengers.sort()

ar_score_names = df_ar.SCORE_CARD_NAME.unique()
ar_score_names.sort()

group_of_rejects = df_ar.GROUPOFREJECT.unique()
group_of_rejects.sort()

group_of_alerts = df_ar.GROUPOFALERTS.unique()
group_of_alerts.sort()

reason_names = df_ar.REASON_NAME.unique()
reason_names.sort()

v_ages = dfv.AGE.unique()
v_ages.sort()

v_products = dfv.PRODUCTS.unique()
v_products.sort()

v_programs = dfv.PROGRAMM.unique()
v_programs.sort()

v_segments = dfv.SEGMENT.unique()
v_segments.sort()

v_cities = dfv.CITY2.unique()
v_cities.sort()

v_groups = ['Просрочка 5+', 'Просрочка 30+', 'Просрочка 60+', 'Просрочка 90+']

ar_layout = [
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H5('Период анализа')
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.DatePickerRange(
                            id='ar-date-picker',
                            min_date_allowed=min(ar_date),
                            max_date_allowed=max(ar_date),
                            month_format='DD.MM.YYYY',
                            display_format='DD.MM.YYYY',
                            with_portal=True,
                            first_day_of_week=1,
                            start_date=min(ar_date),
                            end_date=max(ar_date),
                            style={'width': '500px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px'})
                ], style={'marginTop': '20px', 'width': '520px', 'marginLeft': '20px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Группы продуктов')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_ar_groups', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='ar-group-product-dd',
                            multi=True,
                            options=[{'label': product, 'value': product} for product in group_of_products],
                            value=group_of_products,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Продукты')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_ar_products', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='ar-products-dd',
                            multi=True,
                            options=[{'label': product, 'value': product} for product in ar_products],
                            value=ar_products,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        html.H5('Разбить по периодам')
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='ar-periodtype-dd',
                            multi=False,
                            options=[{'label': period, 'value': period} for period in ['По дням', 'По неделям', 'По месяцам']],
                            value='По месяцам',
                            style={'fontSize': '14px', 'width': '500px'},
                            clearable=False
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px'})
                ], style={'marginLeft': '20px', 'marginTop': '120px', 'width': '520px'})
            ]),
            dbc.Col([
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Регионы')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_ar_regions', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='ar-cities-dd',
                            multi=True,
                            options=[{'label': city, 'value': city} for city in ar_cities],
                            value=ar_cities,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Отделения')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_ar_otdels', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='ar-otdels-dd',
                            multi=True,
                            options=[{'label': otdel, 'value': otdel} for otdel in ar_otdels],
                            value=ar_otdels,
                            style={'fontSize': '14px', 'height': '200px', 'display': 'inline-block', 'overflowY': 'scroll'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
            ]),
            dbc.Col([
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Типы клиентов')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_ar_clienttype', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='ar-clienttype-dd',
                            multi=True,
                            options=[{'label': client, 'value': client} for client in ar_type_of_clients],
                            value=ar_type_of_clients,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Категории клиента')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_ar_segments', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='ar-segments-dd',
                            multi=True,
                            options=[{'label': segment, 'value': segment} for segment in ar_segments],
                            value=ar_segments,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Стратегии')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_ar_strategies', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='ar-strategies-dd',
                            multi=True,
                            options=[{'label': strategy, 'value': strategy} for strategy in ar_strategies],
                            value=ar_strategies,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Коры')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_ar_cors', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='ar-cors-dd',
                            multi=True,
                            options=[{'label': cor, 'value': cor} for cor in ar_cors],
                            value=ar_cors,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Челленджеры')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_ar_challengers', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='ar-challengers-dd',
                            multi=True,
                            options=[{'label': challenger, 'value': challenger} for challenger in ar_challengers],
                            value=ar_challengers,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Скоркарты')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_ar_scorenames', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='ar-scorenames-dd',
                            multi=True,
                            options=[{'label': score, 'value': score} for score in ar_score_names],
                            value=ar_score_names,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
            ])
        ]),
        dbc.Row([
            html.Div([
                html.Button(children='Выгрузить таблицу', n_clicks=0, id='btn_download_ar',
                            style={'width': '180px', 'height': '25px', 'marginLeft': '80px', 'marginTop': '50px', 'backgroundColor': 'green',
                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid', 'color': 'white'}),
                Download(id='download-ar')
            ])
        ]),
        dbc.Row([
            html.Div([
                dcc.Graph(
                    id='ar-table'
                )
            ])
        ]),
        dbc.Row([
            html.Div([
                dcc.Graph(
                    id='ar-graph'
                )
            ])
        ]),
        dbc.Row([
            html.Div([
                html.Button('Добавить сводную таблицу', id='btn_add_pivot', n_clicks=0, style={'width': '180px', 'height': '25px', 'marginLeft': '40px',
                                                                                               'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid',
                                                                                               'marginBottom': '20px'})
            ])
        ]),
        dbc.Row([
            html.Div([], id='pivot-layout')
        ])
    ])
]

reason_layout = [
html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H5('Период анализа')
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.DatePickerRange(
                            id='reason-date-picker',
                            min_date_allowed=min(ar_date),
                            max_date_allowed=max(ar_date),
                            month_format='DD.MM.YYYY',
                            display_format='DD.MM.YYYY',
                            with_portal=True,
                            first_day_of_week=1,
                            start_date=min(ar_date),
                            end_date=max(ar_date),
                            style={'width': '500px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px'})
                ], style={'marginTop': '20px', 'width': '520px', 'marginLeft': '20px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Группы продуктов')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_reason_groups', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='reason-group-product-dd',
                            multi=True,
                            options=[{'label': product, 'value': product} for product in group_of_products],
                            value=group_of_products,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Продукты')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_reason_products', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='reason-products-dd',
                            multi=True,
                            options=[{'label': product, 'value': product} for product in ar_products],
                            value=ar_products,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
            ]),
            dbc.Col([
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Регионы')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_reason_regions', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='reason-cities-dd',
                            multi=True,
                            options=[{'label': city, 'value': city} for city in ar_cities],
                            value=ar_cities,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Отделения')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_reason_otdels', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='reason-otdels-dd',
                            multi=True,
                            options=[{'label': otdel, 'value': otdel} for otdel in ar_otdels],
                            value=ar_otdels,
                            style={'fontSize': '14px', 'height': '200px', 'display': 'inline-block', 'overflowY': 'scroll'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
            ]),
            dbc.Col([
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Типы клиентов')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_reason_clienttype', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='reason-clienttype-dd',
                            multi=True,
                            options=[{'label': client, 'value': client} for client in ar_type_of_clients],
                            value=ar_type_of_clients,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Категории клиента')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_reason_segments', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='reason-segments-dd',
                            multi=True,
                            options=[{'label': segment, 'value': segment} for segment in ar_segments],
                            value=ar_segments,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Стратегии')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_reason_strategies', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='reason-strategies-dd',
                            multi=True,
                            options=[{'label': strategy, 'value': strategy} for strategy in ar_strategies],
                            value=ar_strategies,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Коры')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_reason_cors', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='reason-cors-dd',
                            multi=True,
                            options=[{'label': cor, 'value': cor} for cor in ar_cors],
                            value=ar_cors,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Челленджеры')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_reason_challengers', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='reason-challengers-dd',
                            multi=True,
                            options=[{'label': challenger, 'value': challenger} for challenger in ar_challengers],
                            value=ar_challengers,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Скоркарты')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_reason_scorenames', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='reason-scorenames-dd',
                            multi=True,
                            options=[{'label': score, 'value': score} for score in ar_score_names],
                            value=ar_score_names,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
            ])
        ]),
        dbc.Row([
            html.Div([html.H2('Анализ по группам отказов')], style={'marginTop': '30px', 'borderBottom': '5px solid green'})
        ], align='center', justify='center'),
        dbc.Row([
            html.Div([
                html.Button(children='Выгрузить таблицу', n_clicks=0, id='btn_download_rg',
                            style={'width': '180px', 'height': '25px', 'marginLeft': '90px', 'marginTop': '50px', 'backgroundColor': 'green',
                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid', 'color': 'white'}),
                Download(id='download-rg')
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='reason-table'
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='reason-graph'
                    )
                ])
            ])
        ]),
        dbc.Row([
            html.Div([html.H2('Анализ по подгруппам отказов')], style={'marginTop': '30px', 'borderBottom': '5px solid green'})
        ], align='center', justify='center'),
        dbc.Row([
            html.Div([
                html.Button(children='Выгрузить таблицу', n_clicks=0, id='btn_download_ra',
                            style={'width': '180px', 'height': '25px', 'marginLeft': '300px', 'marginTop': '50px', 'backgroundColor': 'green',
                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid', 'color': 'white'}),
                Download(id='download-ra')
            ])
        ]),
        dbc.Row([
            html.Div([
                dcc.Graph(
                    id='reason-alert-table'
                )
            ])
        ], align='center', justify='center')
    ])
]

patterns_list = list(patterns.keys())
pattern_layout = [
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H5('Период анализа')
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.DatePickerRange(
                            id='pattern-date-picker',
                            min_date_allowed=min(ar_date),
                            max_date_allowed=max(ar_date),
                            month_format='DD.MM.YYYY',
                            display_format='DD.MM.YYYY',
                            with_portal=True,
                            first_day_of_week=1,
                            start_date=min(ar_date),
                            end_date=max(ar_date),
                            style={'width': '500px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px'})
                ], style={'marginTop': '20px', 'width': '520px', 'marginLeft': '20px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Группы продуктов')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_pattern_groups', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='pattern-group-product-dd',
                            multi=True,
                            options=[{'label': product, 'value': product} for product in group_of_products],
                            value=group_of_products,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Продукты')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_pattern_products', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='pattern-products-dd',
                            multi=True,
                            options=[{'label': product, 'value': product} for product in ar_products],
                            value=ar_products,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        html.H5('Список шаблонов')
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='pattern-list-dd',
                            multi=False,
                            options=[{'label': pattern, 'value': pattern} for pattern in patterns_list],
                            value=patterns_list[0],
                            style={'fontSize': '14px', 'width': '500px'},
                            clearable=False
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px'})
                ], style={'marginLeft': '20px', 'marginTop': '120px', 'width': '520px'})
            ]),
            dbc.Col([
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Регионы')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_pattern_regions', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='pattern-cities-dd',
                            multi=True,
                            options=[{'label': city, 'value': city} for city in ar_cities],
                            value=ar_cities,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Отделения')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_pattern_otdels', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='pattern-otdels-dd',
                            multi=True,
                            options=[{'label': otdel, 'value': otdel} for otdel in ar_otdels],
                            value=ar_otdels,
                            style={'fontSize': '14px', 'height': '200px', 'display': 'inline-block', 'overflowY': 'scroll'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
            ]),
            dbc.Col([
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Типы клиентов')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_pattern_clienttype', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='pattern-clienttype-dd',
                            multi=True,
                            options=[{'label': client, 'value': client} for client in ar_type_of_clients],
                            value=ar_type_of_clients,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Категории клиента')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_pattern_segments', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='pattern-segments-dd',
                            multi=True,
                            options=[{'label': segment, 'value': segment} for segment in ar_segments],
                            value=ar_segments,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Стратегии')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_pattern_strategies', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='pattern-strategies-dd',
                            multi=True,
                            options=[{'label': strategy, 'value': strategy} for strategy in ar_strategies],
                            value=ar_strategies,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Коры')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_pattern_cors', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='pattern-cors-dd',
                            multi=True,
                            options=[{'label': cor, 'value': cor} for cor in ar_cors],
                            value=ar_cors,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Челленджеры')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_pattern_challengers', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='pattern-challengers-dd',
                            multi=True,
                            options=[{'label': challenger, 'value': challenger} for challenger in ar_challengers],
                            value=ar_challengers,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Скоркарты')
                                ])
                            ]),
                            dbc.Col([
                                html.Div([
                                    html.Button('Обновить', id='btn_pattern_scorenames', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '160px',
                                                                                                     'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                                ])
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green'}),
                    html.Div([
                        dcc.Dropdown(
                            id='pattern-scorenames-dd',
                            multi=True,
                            options=[{'label': score, 'value': score} for score in ar_score_names],
                            value=ar_score_names,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px', 'width': '500px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px', 'width': '520px'}),
            ])
        ]),
        dbc.Row([
            html.Div([
                html.Button(children='Выгрузить таблицу', n_clicks=0, id='btn_download_pattern',
                            style={'width': '180px', 'height': '25px', 'marginLeft': '450px', 'marginTop': '50px', 'backgroundColor': 'green',
                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid', 'color': 'white'}),
                Download(id='download-pattern')
            ])
        ]),
        dbc.Row([
            html.Div([
            ], id='pattern-table')
        ], align='center', justify='center')
    ])
]

pivot_operations = ['Сумма', 'Среднее', 'Медиана', 'Минимум', 'Максимум']
pivot_additions = ['Без вычислений', 'Доля от суммы столбца', 'Доля от общей суммы', 'Доля от суммы другого значения']
pivot_layout = [
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H5('Строки')
                    ], style={'marginLeft': '20px'}),
                    html.Div([
                        dcc.Dropdown(
                            id='pivot-rows-dd',
                            options=[{'label': col, 'value': col} for col in df_ar.columns],
                            value=None,
                            multi=True,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px'})
                ], style={'marginTop': '20px', 'marginLeft': '20px', 'width': '250px'})
            ], width='auto'),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H5('Колонны')
                    ], style={'marginLeft': '20px'}),
                    html.Div([
                        dcc.Dropdown(
                            id='pivot-columns-dd',
                            options=[{'label': col, 'value': col} for col in df_ar.columns],
                            value=None,
                            multi=True,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px'})
                ], style={'marginTop': '20px', 'marginLeft': '20px', 'width': '250px'})
            ], width='auto'),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H5('Доп. операции')
                    ], style={'marginLeft': '20px'}),
                    html.Div([
                        dcc.Dropdown(
                            id='pivot-addition-dd',
                            options=[{'label': val, 'value': val} for val in ['Без вычислений', 'Доля от суммы столбца', 'Доля от общей суммы']],
                            value='Без вычислений',
                            multi=False,
                            clearable=False,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px'})
                ], style={'marginTop': '20px', 'marginLeft': '20px', 'width': '250px'})
            ], width='auto'),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H5('Значение')
                    ], style={'marginLeft': '20px'}),
                    html.Div([
                        dcc.Dropdown(
                            id='pivot-value-dd',
                            options=[{'label': col, 'value': col} for col in df_ar.columns],
                            value=None,
                            multi=False,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px'}),
                ], style={'marginTop': '20px', 'marginLeft': '20px', 'width': '250px'}),
            ], width='auto'),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H5('Операции')
                    ], style={'marginLeft': '20px'}),
                    html.Div([
                        dcc.Dropdown(
                            id='pivot-type-dd',
                            options=[{'label': val, 'value': val} for val in pivot_operations],
                            value=None,
                            multi=False,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginLeft': '20px'})
                ], style={'marginTop': '20px', 'marginLeft': '20px', 'width': '250px'}),
            ], width='auto')
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H5('Добавить колонки с произвольной формулой')
                    ], style={'marginLeft': '20px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px'})
            ], width='auto')
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H6('Наименование колонки №1'),
                        dcc.Input(
                            id='first-svod-column-name',
                            style={'border': '1px solid gray', 'borderRadius': '3px', 'width': '220px', 'height': '35px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Формула'),
                        dcc.Input(
                            id='first-svod-column-formula',
                            style={'border': '1px solid gray', 'borderRadius': '3px', 'width': '220px', 'height': '35px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Операции'),
                        dcc.Dropdown(
                            id='first-svod-column-operation',
                            options=[{'label': val, 'value': val} for val in pivot_operations],
                            value='Сумма',
                            multi=False,
                            clearable=False,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Дополнительные операции'),
                        dcc.Dropdown(
                            id='first-svod-column-addit',
                            options=[{'label': val, 'value': val} for val in pivot_additions],
                            value='Без вычислений',
                            multi=False,
                            clearable=False,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Формула другого значения'),
                        dcc.Input(
                            id='first-svod-column-other',
                            style={'border': '1px solid gray', 'borderRadius': '3px', 'width': '220px', 'height': '35px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px', 'marginBottom': '10px'})
                ], style={'marginLeft': '40px', 'marginTop': '20px', 'border': '1px solid black', 'borderRadius': '3px'})
            ], width='auto'),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H6('Наименование колонки №2'),
                        dcc.Input(
                            id='second-svod-column-name',
                            style={'border': '1px solid gray', 'borderRadius': '3px', 'width': '220px', 'height': '35px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Формула'),
                        dcc.Input(
                            id='second-svod-column-formula',
                            style={'border': '1px solid gray', 'borderRadius': '3px', 'width': '220px', 'height': '35px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Операции'),
                        dcc.Dropdown(
                            id='second-svod-column-operation',
                            options=[{'label': val, 'value': val} for val in pivot_operations],
                            value='Сумма',
                            multi=False,
                            clearable=False,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Дополнительные операции'),
                        dcc.Dropdown(
                            id='second-svod-column-addit',
                            options=[{'label': val, 'value': val} for val in pivot_additions],
                            value='Без вычислений',
                            multi=False,
                            clearable=False,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Формула другого значения'),
                        dcc.Input(
                            id='second-svod-column-other',
                            style={'border': '1px solid gray', 'borderRadius': '3px', 'width': '220px', 'height': '35px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px', 'marginBottom': '10px'})
                ], style={'marginLeft': '40px', 'marginTop': '20px', 'border': '1px solid black', 'borderRadius': '3px'})
            ], width='auto'),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H6('Наименование колонки №3'),
                        dcc.Input(
                            id='third-svod-column-name',
                            style={'border': '1px solid gray', 'borderRadius': '3px', 'width': '220px',
                                   'height': '35px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Формула'),
                        dcc.Input(
                            id='third-svod-column-formula',
                            style={'border': '1px solid gray', 'borderRadius': '3px', 'width': '220px',
                                   'height': '35px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Операции'),
                        dcc.Dropdown(
                            id='third-svod-column-operation',
                            options=[{'label': val, 'value': val} for val in pivot_operations],
                            value='Сумма',
                            multi=False,
                            clearable=False,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Дополнительные операции'),
                        dcc.Dropdown(
                            id='third-svod-column-addit',
                            options=[{'label': val, 'value': val} for val in pivot_additions],
                            value='Без вычислений',
                            multi=False,
                            clearable=False,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Формула другого значения'),
                        dcc.Input(
                            id='third-svod-column-other',
                            style={'border': '1px solid gray', 'borderRadius': '3px', 'width': '220px', 'height': '35px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px', 'marginBottom': '10px'})
                ], style={'marginLeft': '40px', 'marginTop': '20px', 'border': '1px solid black', 'borderRadius': '3px'})
            ], width='auto'),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H6('Наименование колонки №4'),
                        dcc.Input(
                            id='fourth-svod-column-name',
                            style={'border': '1px solid gray', 'borderRadius': '3px', 'width': '220px', 'height': '35px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Формула'),
                        dcc.Input(
                            id='fourth-svod-column-formula',
                            style={'border': '1px solid gray', 'borderRadius': '3px', 'width': '220px', 'height': '35px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Операции'),
                        dcc.Dropdown(
                            id='fourth-svod-column-operation',
                            options=[{'label': val, 'value': val} for val in pivot_operations],
                            value='Сумма',
                            multi=False,
                            clearable=False,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Дополнительные операции'),
                        dcc.Dropdown(
                            id='fourth-svod-column-addit',
                            options=[{'label': val, 'value': val} for val in pivot_additions],
                            value='Без вычислений',
                            multi=False,
                            clearable=False,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Формула другого значения'),
                        dcc.Input(
                            id='fourth-svod-column-other',
                            style={'border': '1px solid gray', 'borderRadius': '3px', 'width': '220px', 'height': '35px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px', 'marginBottom': '10px'})
                ], style={'marginLeft': '40px', 'marginTop': '20px', 'border': '1px solid black', 'borderRadius': '3px'})
            ], width='auto'),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H6('Наименование колонки №5'),
                        dcc.Input(
                            id='fifth-svod-column-name',
                            style={'border': '1px solid gray', 'borderRadius': '3px', 'width': '220px', 'height': '35px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Формула'),
                        dcc.Input(
                            id='fifth-svod-column-formula',
                            style={'border': '1px solid gray', 'borderRadius': '3px', 'width': '220px', 'height': '35px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Операции'),
                        dcc.Dropdown(
                            id='fifth-svod-column-operation',
                            options=[{'label': val, 'value': val} for val in pivot_operations],
                            value='Сумма',
                            multi=False,
                            clearable=False,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Дополнительные операции'),
                        dcc.Dropdown(
                            id='fifth-svod-column-addit',
                            options=[{'label': val, 'value': val} for val in pivot_additions],
                            value='Без вычислений',
                            multi=False,
                            clearable=False,
                            style={'fontSize': '14px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px'}),
                    html.Div([
                        html.H6('Формула другого значения'),
                        dcc.Input(
                            id='fifth-svod-column-other',
                            style={'border': '1px solid gray', 'borderRadius': '3px', 'width': '220px', 'height': '35px'}
                        )
                    ], style={'marginTop': '10px', 'marginLeft': '10px', 'marginRight': '10px', 'marginBottom': '10px'})
                ], style={'marginLeft': '40px', 'marginTop': '20px', 'border': '1px solid black', 'borderRadius': '3px'})
            ], width='auto')
        ]),
        dbc.Row([
            html.Div([
                html.Button('Создать', id='btn_create_pivot', n_clicks=0,
                            style={'width': '80px', 'height': '25px', 'marginLeft': '55px', 'marginTop': '20px', 'marginBottom': '20px',
                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
            ])
        ]),
        dbc.Row([
            html.Div([
            ], id='pivot-table')
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Input(
                        id='save-pattern-input',
                        placeholder='Введите наименование шаблона',
                        style={'border': '1px solid gray', 'borderRadius': '3px', 'width': '300px', 'height': '25px',
                               'marginLeft': '40px', 'marginBottom': '20px', 'marginTop': '20px', 'fontSize': '12px'}
                    )
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([
                    html.Button('Сохранить', id='btn_save_pattern', n_clicks=0,
                                style={'width': '100px', 'height': '25px', 'fontSize': '12px', 'borderRadius': '3px',
                                       'border': '1px solid', 'marginTop': '20px', 'marginBottom': '20px'})
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([

                ], id='save-pattern-label')
            ], width='auto')
        ])
    ])
]

vintage_layout = [
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Продукты')
                                ])
                            ]),
                            dbc.Col([
                                html.Button('Обновить', id='btn_v_products', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '180px',
                                                                                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green', 'marginTop': '20px'}),
                    html.Div([
                        dcc.Dropdown(
                            id='dcc-vintage-products',
                            multi=True,
                            options=[{'label': v_product, 'value': v_product} for v_product in v_products],
                            value=v_products,
                            style={'fontSize': '14px', 'width': '550px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Программы')
                                ])
                            ]),
                            dbc.Col([
                                html.Button('Обновить', id='btn_v_programs', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '180px',
                                                                                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green', 'marginTop': '20px'}),
                    html.Div([
                        dcc.Dropdown(
                            id='dcc-vintage-programs',
                            multi=True,
                            options=[{'label': v_program, 'value': v_program} for v_program in v_programs],
                            value=v_programs,
                            style={'fontSize': '14px', 'width': '550px', 'height': '300px', 'display': 'inline-block', 'overflowY': 'scroll'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px'}),
                html.Div([
                    html.Div([
                        html.H5('Разбить по просрочкам')
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green', 'marginTop': '50px'}),
                    html.Div([
                        dcc.Dropdown(
                            id='dcc-vintage-groups',
                            multi=False,
                            options=[{'label': v_group, 'value': v_group} for v_group in v_groups],
                            value=v_groups[0],
                            style={'fontSize': '14px', 'width': '550px'},
                            clearable=False
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px'})
                ], style={'marginLeft': '20px'})
            ], width='auto'),
            dbc.Col([
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Регионы')
                                ])
                            ]),
                            dbc.Col([
                                html.Button('Обновить', id='btn_v_cities', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '180px',
                                                                                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green', 'marginTop': '20px'}),
                    html.Div([
                        dcc.Dropdown(
                            id='dcc-vintage-cities',
                            multi=True,
                            options=[{'label': v_city, 'value': v_city} for v_city in v_cities],
                            value=v_cities,
                            style={'fontSize': '14px', 'width': '550px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Сегменты')
                                ])
                            ]),
                            dbc.Col([
                                html.Button('Обновить', id='btn_v_segments', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '180px',
                                                                                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green', 'marginTop': '20px'}),
                    html.Div([
                        dcc.Dropdown(
                            id='dcc-vintage-segments',
                            multi=True,
                            options=[{'label': v_segment, 'value': v_segment} for v_segment in v_segments],
                            value=v_segments,
                            style={'fontSize': '14px', 'width': '550px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px'}),
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H5('Возрасты')
                                ])
                            ]),
                            dbc.Col([
                                html.Button('Обновить', id='btn_v_ages', n_clicks=0, style={'width': '80px', 'height': '25px', 'marginLeft': '180px',
                                                                                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid'})
                            ])
                        ])
                    ], style={'marginLeft': '20px', 'borderBottom': '3px solid green', 'marginTop': '20px'}),
                    html.Div([
                        dcc.Dropdown(
                            id='dcc-vintage-ages',
                            multi=True,
                            options=[{'label': v_age, 'value': v_age} for v_age in v_ages],
                            value=v_ages,
                            style={'fontSize': '14px', 'width': '550px'}
                        )
                    ], style={'marginLeft': '20px', 'marginTop': '10px'})
                ], style={'marginLeft': '20px', 'marginTop': '20px'})
            ], width='auto')
        ]),
        dbc.Row([
            html.Div([
                html.Button(children='Выгрузить таблицу', n_clicks=0, id='btn_download_vintage',
                            style={'width': '180px', 'height': '25px', 'marginLeft': '80px', 'marginTop': '30px', 'backgroundColor': 'green',
                                   'fontSize': '12px', 'borderRadius': '3px', 'border': '1px solid', 'color': 'white'}),
                Download(id='download-vintage')
            ])
        ]),
        dbc.Row([
            html.Div([
                dcc.Graph(
                    id='vintage-table'
                )
            ])
        ]),
        #dbc.Row([
        #    html.Div([
        #        dcc.Graph(
        #            id='vintage-graph'
        #        )
        #    ])
        #])
    ])
]

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='analysis', children=[
        dcc.Tab(label='Анализ ранних риск индикаторов', value='analysis', children=analysis_layout),
        dcc.Tab(label='Анализ уровня одобрения', value='ar_analysis', children=ar_layout),
        dcc.Tab(label='Причины отказа', value='reason_reject', children=reason_layout),
        dcc.Tab(label='Сохраненные шаблоны', value='pattern', children=pattern_layout),
        dcc.Tab(label='Анализ по винтажам', value='vintage', children=vintage_layout),
        #dcc.Tab(label='Настройки', value='settings', children=settings_layout)
    ], style={'fontSize': '20px', 'height': '80px'})
])

@app.callback(
    [Output('comp_regions_layout', 'children'), Output('btn_add_to_comp', 'children')], [Input('btn_add_to_comp', 'n_clicks')]
)
def add_comp_region_layout(n_clicks):
    if n_clicks % 2 == 1:
        return comp_regions_layout, 'Скрыть регионы'
    return html.Div([]), 'Добавить регионы для сравнения'

@app.callback(
    [Output('months_dd', 'options'), Output('months_dd', 'value')],
    [Input('btn_month_update', 'n_clicks'), Input('regions_dd', 'value'), Input('products_dd', 'value')]
)
def update_months(n_clicks, regions, products):
    df2 = df
    if regions:
        df2 = df2[df2.REGION_.isin(regions)]
    if products:
        df2 = df2[df2.PRODUCT.isin(products)]
    months = df2.MONTH_SIGN_CTR.unique()
    months.sort()
    months_word = []
    for month in months:
        months_word.append(chg_month_to_word(chg_npmonth_to_corr(month)))

    return [{'label': month, 'value': month} for month in months_word], months_word

@app.callback(
    [Output('products_dd', 'options'), Output('products_dd', 'value')],
    [Input('btn_product_update', 'n_clicks')]
)
def update_products(n_clicks):
    products = df.PRODUCT.unique()
    products.sort()
    return [{'label': product, 'value': product} for product in products], products

@app.callback(
    [Output('regions_dd', 'options'), Output('regions_dd', 'value')],
    [Input('btn_region_update', 'n_clicks')]
)
def update_regions(n_clicks):
    regions = df.REGION_.unique()
    regions.sort()
    return [{'label': region, 'value': region} for region in regions], regions

@app.callback(
    [Output('comp_regions_dd', 'options'), Output('comp_regions_dd', 'value')],
    [Input('btn_comp_region_update', 'n_clicks')]
)
def update_comp_regions(n_clicks):
    regions = df.REGION_.unique()
    regions.sort()
    return [{'label': region, 'value': region} for region in regions], regions

@app.callback(
    [Output('table', 'figure'), Output('graph', 'figure')],
    [Input('active_loans_dd', 'value'), Input('products_dd', 'value'), Input('months_dd', 'value'),
     Input('regions_dd', 'value'), Input('analysis_dd', 'value'), Input('analysis_form_dd', 'value')]
)
def update_table_and_graph(active_loans, products, months, regions, analysis_type, analysis_form):
    df2 = df
    months_corr = []

    if months:
        for month in months:
            months_corr.append(chg_word_to_month(month))
    if active_loans:
        df2 = df2[df2.FLAG_ACTIVE_LOAN.isin(active_loans)]
    if products:
        df2 = df2[df2.PRODUCT.isin(products)]
    if months_corr:
        df2 = df2[df2.MONTH_SIGN_CTR.isin(months_corr)]
    if regions:
        df2 = df2[df2.REGION_.isin(regions)]

    #FPD_SPD_TPD table and graphs by share of amount
    if analysis_type == 'FPD SPD TPD с просрочкой больше дня' and analysis_form == 'Доля по сумме выдачи':
        df_tab1 = tables.fpd_spd_tpd_0(df2)[1]
        df_tab2 = tables.fpd_spd_tpd_0(df2)[0]
        return graphs.table_fpd_spd_tpd(df_tab1), graphs.graph_fpd_spd_tpd(df_tab2)

    if analysis_type == 'FPD SPD TPD с просрочкой больше 5 дней' and analysis_form == 'Доля по сумме выдачи':
        df_tab1 = tables.fpd_spd_tpd_5(df2)[1]
        df_tab2 = tables.fpd_spd_tpd_5(df2)[0]
        return graphs.table_fpd_spd_tpd(df_tab1), graphs.graph_fpd_spd_tpd(df_tab2)

    if analysis_type == 'FPD SPD TPD с просрочкой больше 15 дней' and analysis_form == 'Доля по сумме выдачи':
        df_tab1 = tables.fpd_spd_tpd_15(df2)[1]
        df_tab2 = tables.fpd_spd_tpd_15(df2)[0]
        return graphs.table_fpd_spd_tpd(df_tab1), graphs.graph_fpd_spd_tpd(df_tab2)

    if analysis_type == 'FPD SPD TPD с просрочкой больше 30 дней' and analysis_form == 'Доля по сумме выдачи':
        df_tab1 = tables.fpd_spd_tpd_30(df2)[1]
        df_tab2 = tables.fpd_spd_tpd_30(df2)[0]
        return graphs.table_fpd_spd_tpd(df_tab1), graphs.graph_fpd_spd_tpd(df_tab2)

    if analysis_type == 'FPD SPD TPD с просрочкой больше 45 дней' and analysis_form == 'Доля по сумме выдачи':
        df_tab1 = tables.fpd_spd_tpd_45(df2)[1]
        df_tab2 = tables.fpd_spd_tpd_45(df2)[0]
        return graphs.table_fpd_spd_tpd(df_tab1), graphs.graph_fpd_spd_tpd(df_tab2)

    if analysis_type == 'FPD SPD TPD с просрочкой больше 60 дней' and analysis_form == 'Доля по сумме выдачи':
        df_tab1 = tables.fpd_spd_tpd_60(df2)[1]
        df_tab2 = tables.fpd_spd_tpd_60(df2)[0]
        return graphs.table_fpd_spd_tpd(df_tab1), graphs.graph_fpd_spd_tpd(df_tab2)

    if analysis_type == 'FPD SPD TPD с просрочкой больше 90 дней' and analysis_form == 'Доля по сумме выдачи':
        df_tab1 = tables.fpd_spd_tpd_90(df2)[1]
        df_tab2 = tables.fpd_spd_tpd_90(df2)[0]
        return graphs.table_fpd_spd_tpd(df_tab1), graphs.graph_fpd_spd_tpd(df_tab2)

    if analysis_type == 'Действующие FPD SPD TPD' and analysis_form == 'Доля по сумме выдачи':
        df_tab1 = tables.fpd_spd_tpd_active(df2)[1]
        df_tab2 = tables.fpd_spd_tpd_active(df2)[0]
        return graphs.table_fpd_spd_tpd(df_tab1), graphs.graph_fpd_spd_tpd(df_tab2)

    #FPD_SPD_TPD table and graphs by share of count
    if analysis_type == 'FPD SPD TPD с просрочкой больше дня' and analysis_form == 'Доля по количеству выдачи':
        df_tab1 = tables.fpd_spd_tpd_0_sc(df2)[1]
        df_tab2 = tables.fpd_spd_tpd_0_sc(df2)[0]
        return graphs.table_fpd_spd_tpd_c(df_tab1), graphs.graph_fpd_spd_tpd_c(df_tab2)

    if analysis_type == 'FPD SPD TPD с просрочкой больше 5 дней' and analysis_form == 'Доля по количеству выдачи':
        df_tab1 = tables.fpd_spd_tpd_5_sc(df2)[1]
        df_tab2 = tables.fpd_spd_tpd_5_sc(df2)[0]
        return graphs.table_fpd_spd_tpd_c(df_tab1), graphs.graph_fpd_spd_tpd_c(df_tab2)

    if analysis_type == 'FPD SPD TPD с просрочкой больше 15 дней' and analysis_form == 'Доля по количеству выдачи':
        df_tab1 = tables.fpd_spd_tpd_15_sc(df2)[1]
        df_tab2 = tables.fpd_spd_tpd_15_sc(df2)[0]
        return graphs.table_fpd_spd_tpd_c(df_tab1), graphs.graph_fpd_spd_tpd_c(df_tab2)

    if analysis_type == 'FPD SPD TPD с просрочкой больше 30 дней' and analysis_form == 'Доля по количеству выдачи':
        df_tab1 = tables.fpd_spd_tpd_30_sc(df2)[1]
        df_tab2 = tables.fpd_spd_tpd_30_sc(df2)[0]
        return graphs.table_fpd_spd_tpd_c(df_tab1), graphs.graph_fpd_spd_tpd_c(df_tab2)

    if analysis_type == 'FPD SPD TPD с просрочкой больше 45 дней' and analysis_form == 'Доля по количеству выдачи':
        df_tab1 = tables.fpd_spd_tpd_45_sc(df2)[1]
        df_tab2 = tables.fpd_spd_tpd_45_sc(df2)[0]
        return graphs.table_fpd_spd_tpd_c(df_tab1), graphs.graph_fpd_spd_tpd_c(df_tab2)

    if analysis_type == 'FPD SPD TPD с просрочкой больше 60 дней' and analysis_form == 'Доля по количеству выдачи':
        df_tab1 = tables.fpd_spd_tpd_60_sc(df2)[1]
        df_tab2 = tables.fpd_spd_tpd_60_sc(df2)[0]
        return graphs.table_fpd_spd_tpd_c(df_tab1), graphs.graph_fpd_spd_tpd_c(df_tab2)

    if analysis_type == 'FPD SPD TPD с просрочкой больше 90 дней' and analysis_form == 'Доля по количеству выдачи':
        df_tab1 = tables.fpd_spd_tpd_90_sc(df2)[1]
        df_tab2 = tables.fpd_spd_tpd_90_sc(df2)[0]
        return graphs.table_fpd_spd_tpd_c(df_tab1), graphs.graph_fpd_spd_tpd_c(df_tab2)

    if analysis_type == 'Действующие FPD SPD TPD' and analysis_form == 'Доля по количеству выдачи':
        df_tab1 = tables.fpd_spd_tpd_active_sc(df2)[1]
        df_tab2 = tables.fpd_spd_tpd_active_sc(df2)[0]
        return graphs.table_fpd_spd_tpd_c(df_tab1), graphs.graph_fpd_spd_tpd_c(df_tab2)

@app.callback(
    Output('download-fpd', 'data'), [Input('btn_download_fpd', 'n_clicks')],
    [State('active_loans_dd', 'value'), State('products_dd', 'value'), State('months_dd', 'value'),
     State('regions_dd', 'value'), State('analysis_dd', 'value'), State('analysis_form_dd', 'value')]
)
def download_file_fpd(n_clicks, active_loans, products, months, regions, analysis_type, analysis_form):
    df2 = df
    months_corr = []

    if months:
        for month in months:
            months_corr.append(chg_word_to_month(month))
    if active_loans:
        df2 = df2[df2.FLAG_ACTIVE_LOAN.isin(active_loans)]
    if products:
        df2 = df2[df2.PRODUCT.isin(products)]
    if months_corr:
        df2 = df2[df2.MONTH_SIGN_CTR.isin(months_corr)]
    if regions:
        df2 = df2[df2.REGION_.isin(regions)]

    # FPD_SPD_TPD table and graphs by share of amount
    if analysis_type == 'FPD SPD TPD с просрочкой больше дня' and analysis_form == 'Доля по сумме выдачи':
        df_tab1 = tables.fpd_spd_tpd_0(df2)[1]

    if analysis_type == 'FPD SPD TPD с просрочкой больше 5 дней' and analysis_form == 'Доля по сумме выдачи':
        df_tab1 = tables.fpd_spd_tpd_5(df2)[1]

    if analysis_type == 'FPD SPD TPD с просрочкой больше 15 дней' and analysis_form == 'Доля по сумме выдачи':
        df_tab1 = tables.fpd_spd_tpd_15(df2)[1]

    if analysis_type == 'FPD SPD TPD с просрочкой больше 30 дней' and analysis_form == 'Доля по сумме выдачи':
        df_tab1 = tables.fpd_spd_tpd_30(df2)[1]

    if analysis_type == 'FPD SPD TPD с просрочкой больше 45 дней' and analysis_form == 'Доля по сумме выдачи':
        df_tab1 = tables.fpd_spd_tpd_45(df2)[1]

    if analysis_type == 'FPD SPD TPD с просрочкой больше 60 дней' and analysis_form == 'Доля по сумме выдачи':
        df_tab1 = tables.fpd_spd_tpd_60(df2)[1]

    if analysis_type == 'FPD SPD TPD с просрочкой больше 90 дней' and analysis_form == 'Доля по сумме выдачи':
        df_tab1 = tables.fpd_spd_tpd_90(df2)[1]

    if analysis_type == 'Действующие FPD SPD TPD' and analysis_form == 'Доля по сумме выдачи':
        df_tab1 = tables.fpd_spd_tpd_active(df2)[1]

    # FPD_SPD_TPD table and graphs by share of count
    if analysis_type == 'FPD SPD TPD с просрочкой больше дня' and analysis_form == 'Доля по количеству выдачи':
        df_tab1 = tables.fpd_spd_tpd_0_sc(df2)[1]

    if analysis_type == 'FPD SPD TPD с просрочкой больше 5 дней' and analysis_form == 'Доля по количеству выдачи':
        df_tab1 = tables.fpd_spd_tpd_5_sc(df2)[1]

    if analysis_type == 'FPD SPD TPD с просрочкой больше 15 дней' and analysis_form == 'Доля по количеству выдачи':
        df_tab1 = tables.fpd_spd_tpd_15_sc(df2)[1]

    if analysis_type == 'FPD SPD TPD с просрочкой больше 30 дней' and analysis_form == 'Доля по количеству выдачи':
        df_tab1 = tables.fpd_spd_tpd_30_sc(df2)[1]

    if analysis_type == 'FPD SPD TPD с просрочкой больше 45 дней' and analysis_form == 'Доля по количеству выдачи':
        df_tab1 = tables.fpd_spd_tpd_45_sc(df2)[1]

    if analysis_type == 'FPD SPD TPD с просрочкой больше 60 дней' and analysis_form == 'Доля по количеству выдачи':
        df_tab1 = tables.fpd_spd_tpd_60_sc(df2)[1]

    if analysis_type == 'FPD SPD TPD с просрочкой больше 90 дней' and analysis_form == 'Доля по количеству выдачи':
        df_tab1 = tables.fpd_spd_tpd_90_sc(df2)[1]

    if analysis_type == 'Действующие FPD SPD TPD' and analysis_form == 'Доля по количеству выдачи':
        df_tab1 = tables.fpd_spd_tpd_active_sc(df2)[1]

    if n_clicks > 0:
        return send_data_frame(df_tab1.to_excel, filename="fpd_spd_tpd.xlsx")

@app.callback(
    Output('fpd_spd_tpd_title', 'children'), [Input('analysis_dd', 'value'), Input('analysis_form_dd', 'value')]
)
def update_fpd_spd_tpd_title(analysis_type, analysis_form):
    #Updating of title by share amount
    if analysis_type == 'FPD SPD TPD с просрочкой больше дня' and analysis_form == 'Доля по сумме выдачи':
        return html.H2('Показатель долей по сумме выдачи с просрочкой больше дня (%)')

    if analysis_type == 'FPD SPD TPD с просрочкой больше 5 дней' and analysis_form == 'Доля по сумме выдачи':
        return html.H2('Показатель долей по сумме выдачи с просрочкой больше 5 дней (%)')

    if analysis_type == 'FPD SPD TPD с просрочкой больше 15 дней' and analysis_form == 'Доля по сумме выдачи':
        return html.H2('Показатель долей по сумме выдачи с просрочкой больше 15 дней (%)')

    if analysis_type == 'FPD SPD TPD с просрочкой больше 30 дней' and analysis_form == 'Доля по сумме выдачи':
        return html.H2('Показатель долей по сумме выдачи с просрочкой больше 30 дней (%)')

    if analysis_type == 'FPD SPD TPD с просрочкой больше 45 дней' and analysis_form == 'Доля по сумме выдачи':
        return html.H2('Показатель долей по сумме выдачи с просрочкой больше 45 дней (%)')

    if analysis_type == 'FPD SPD TPD с просрочкой больше 60 дней' and analysis_form == 'Доля по сумме выдачи':
        return html.H2('Показатель долей по сумме выдачи с просрочкой больше 60 дней (%)')

    if analysis_type == 'FPD SPD TPD с просрочкой больше 90 дней' and analysis_form == 'Доля по сумме выдачи':
        return html.H2('Показатель долей по сумме выдачи с просрочкой больше 90 дней (%)')

    if analysis_type == 'Действующие FPD SPD TPD' and analysis_form == 'Доля по сумме выдачи':
        return html.H2('Показатель долей по сумме выдачи действующих риск индикаторов (%)')

    #Updating of title by share count
    if analysis_type == 'FPD SPD TPD с просрочкой больше дня' and analysis_form == 'Доля по количеству выдачи':
        return html.H2('Показатель долей по количеству выдачи с просрочкой больше дня (%)')

    if analysis_type == 'FPD SPD TPD с просрочкой больше 5 дней' and analysis_form == 'Доля по количеству выдачи':
        return html.H2('Показатель долей по количеству выдачи с просрочкой больше 5 дней (%)')

    if analysis_type == 'FPD SPD TPD с просрочкой больше 15 дней' and analysis_form == 'Доля по количеству выдачи':
        return html.H2('Показатель долей по количеству выдачи с просрочкой больше 15 дней (%)')

    if analysis_type == 'FPD SPD TPD с просрочкой больше 30 дней' and analysis_form == 'Доля по количеству выдачи':
        return html.H2('Показатель долей по количеству выдачи с просрочкой больше 30 дней (%)')

    if analysis_type == 'FPD SPD TPD с просрочкой больше 45 дней' and analysis_form == 'Доля по количеству выдачи':
        return html.H2('Показатель долей по количеству выдачи с просрочкой больше 45 дней (%)')

    if analysis_type == 'FPD SPD TPD с просрочкой больше 60 дней' and analysis_form == 'Доля по количеству выдачи':
        return html.H2('Показатель долей по количеству выдачи с просрочкой больше 60 дней (%)')

    if analysis_type == 'FPD SPD TPD с просрочкой больше 90 дней' and analysis_form == 'Доля по количеству выдачи':
        return html.H2('Показатель долей по количеству выдачи с просрочкой больше 90 дней (%)')

    if analysis_type == 'Действующие FPD SPD TPD' and analysis_form == 'Доля по количеству выдачи':
        return html.H2('Показатель долей по количеству выдачи действующих риск индикаторов (%)')

@app.callback(
    [Output('comp_table', 'figure'), Output('comp_graph', 'figure')],
    [Input('btn_add_to_comp', 'n_clicks'), Input('active_loans_dd', 'value'), Input('products_dd', 'value'),
     Input('months_dd', 'value'), Input('comp_regions_dd', 'value'), Input('analysis_dd', 'value'), Input('analysis_form_dd', 'value')]
)
def update_comp_table_and_graph(n_clicks, active_loans, products, months, regions, analysis_type, analysis_form):
    if n_clicks % 2 == 1:
        df2 = df
        months_corr = []

        if months:
            for month in months:
                months_corr.append(chg_word_to_month(month))
        if active_loans:
            df2 = df2[df2.FLAG_ACTIVE_LOAN.isin(active_loans)]
        if products:
            df2 = df2[df2.PRODUCT.isin(products)]
        if months_corr:
            df2 = df2[df2.MONTH_SIGN_CTR.isin(months_corr)]
        if regions:
            df2 = df2[df2.REGION_.isin(regions)]

        # FPD_SPD_TPD table and graphs by share of amount
        if analysis_type == 'FPD SPD TPD с просрочкой больше дня' and analysis_form == 'Доля по сумме выдачи':
            df_tab1 = tables.fpd_spd_tpd_0(df2)[1]
            df_tab2 = tables.fpd_spd_tpd_0(df2)[0]
            return graphs.table_fpd_spd_tpd(df_tab1), graphs.graph_fpd_spd_tpd(df_tab2)

        if analysis_type == 'FPD SPD TPD с просрочкой больше 5 дней' and analysis_form == 'Доля по сумме выдачи':
            df_tab1 = tables.fpd_spd_tpd_5(df2)[1]
            df_tab2 = tables.fpd_spd_tpd_5(df2)[0]
            return graphs.table_fpd_spd_tpd(df_tab1), graphs.graph_fpd_spd_tpd(df_tab2)

        if analysis_type == 'FPD SPD TPD с просрочкой больше 15 дней' and analysis_form == 'Доля по сумме выдачи':
            df_tab1 = tables.fpd_spd_tpd_15(df2)[1]
            df_tab2 = tables.fpd_spd_tpd_15(df2)[0]
            return graphs.table_fpd_spd_tpd(df_tab1), graphs.graph_fpd_spd_tpd(df_tab2)

        if analysis_type == 'FPD SPD TPD с просрочкой больше 30 дней' and analysis_form == 'Доля по сумме выдачи':
            df_tab1 = tables.fpd_spd_tpd_30(df2)[1]
            df_tab2 = tables.fpd_spd_tpd_30(df2)[0]
            return graphs.table_fpd_spd_tpd(df_tab1), graphs.graph_fpd_spd_tpd(df_tab2)

        if analysis_type == 'FPD SPD TPD с просрочкой больше 45 дней' and analysis_form == 'Доля по сумме выдачи':
            df_tab1 = tables.fpd_spd_tpd_45(df2)[1]
            df_tab2 = tables.fpd_spd_tpd_45(df2)[0]
            return graphs.table_fpd_spd_tpd(df_tab1), graphs.graph_fpd_spd_tpd(df_tab2)

        if analysis_type == 'FPD SPD TPD с просрочкой больше 60 дней' and analysis_form == 'Доля по сумме выдачи':
            df_tab1 = tables.fpd_spd_tpd_60(df2)[1]
            df_tab2 = tables.fpd_spd_tpd_60(df2)[0]
            return graphs.table_fpd_spd_tpd(df_tab1), graphs.graph_fpd_spd_tpd(df_tab2)

        if analysis_type == 'FPD SPD TPD с просрочкой больше 90 дней' and analysis_form == 'Доля по сумме выдачи':
            df_tab1 = tables.fpd_spd_tpd_90(df2)[1]
            df_tab2 = tables.fpd_spd_tpd_90(df2)[0]
            return graphs.table_fpd_spd_tpd(df_tab1), graphs.graph_fpd_spd_tpd(df_tab2)

        if analysis_type == 'Действующие FPD SPD TPD' and analysis_form == 'Доля по сумме выдачи':
            df_tab1 = tables.fpd_spd_tpd_active(df2)[1]
            df_tab2 = tables.fpd_spd_tpd_active(df2)[0]
            return graphs.table_fpd_spd_tpd(df_tab1), graphs.graph_fpd_spd_tpd(df_tab2)

        # FPD_SPD_TPD table and graphs by share of count
        if analysis_type == 'FPD SPD TPD с просрочкой больше дня' and analysis_form == 'Доля по количеству выдачи':
            df_tab1 = tables.fpd_spd_tpd_0_sc(df2)[1]
            df_tab2 = tables.fpd_spd_tpd_0_sc(df2)[0]
            return graphs.table_fpd_spd_tpd_c(df_tab1), graphs.graph_fpd_spd_tpd_c(df_tab2)

        if analysis_type == 'FPD SPD TPD с просрочкой больше 5 дней' and analysis_form == 'Доля по количеству выдачи':
            df_tab1 = tables.fpd_spd_tpd_5_sc(df2)[1]
            df_tab2 = tables.fpd_spd_tpd_5_sc(df2)[0]
            return graphs.table_fpd_spd_tpd_c(df_tab1), graphs.graph_fpd_spd_tpd_c(df_tab2)

        if analysis_type == 'FPD SPD TPD с просрочкой больше 15 дней' and analysis_form == 'Доля по количеству выдачи':
            df_tab1 = tables.fpd_spd_tpd_15_sc(df2)[1]
            df_tab2 = tables.fpd_spd_tpd_15_sc(df2)[0]
            return graphs.table_fpd_spd_tpd_c(df_tab1), graphs.graph_fpd_spd_tpd_c(df_tab2)

        if analysis_type == 'FPD SPD TPD с просрочкой больше 30 дней' and analysis_form == 'Доля по количеству выдачи':
            df_tab1 = tables.fpd_spd_tpd_30_sc(df2)[1]
            df_tab2 = tables.fpd_spd_tpd_30_sc(df2)[0]
            return graphs.table_fpd_spd_tpd_c(df_tab1), graphs.graph_fpd_spd_tpd_c(df_tab2)

        if analysis_type == 'FPD SPD TPD с просрочкой больше 45 дней' and analysis_form == 'Доля по количеству выдачи':
            df_tab1 = tables.fpd_spd_tpd_45_sc(df2)[1]
            df_tab2 = tables.fpd_spd_tpd_45_sc(df2)[0]
            return graphs.table_fpd_spd_tpd_c(df_tab1), graphs.graph_fpd_spd_tpd_c(df_tab2)

        if analysis_type == 'FPD SPD TPD с просрочкой больше 60 дней' and analysis_form == 'Доля по количеству выдачи':
            df_tab1 = tables.fpd_spd_tpd_60_sc(df2)[1]
            df_tab2 = tables.fpd_spd_tpd_60_sc(df2)[0]
            return graphs.table_fpd_spd_tpd_c(df_tab1), graphs.graph_fpd_spd_tpd_c(df_tab2)

        if analysis_type == 'FPD SPD TPD с просрочкой больше 90 дней' and analysis_form == 'Доля по количеству выдачи':
            df_tab1 = tables.fpd_spd_tpd_90_sc(df2)[1]
            df_tab2 = tables.fpd_spd_tpd_90_sc(df2)[0]
            return graphs.table_fpd_spd_tpd_c(df_tab1), graphs.graph_fpd_spd_tpd_c(df_tab2)

        if analysis_type == 'Действующие FPD SPD TPD' and analysis_form == 'Доля по количеству выдачи':
            df_tab1 = tables.fpd_spd_tpd_active_sc(df2)[1]
            df_tab2 = tables.fpd_spd_tpd_active_sc(df2)[0]
            return graphs.table_fpd_spd_tpd_c(df_tab1), graphs.graph_fpd_spd_tpd_c(df_tab2)

####################################
#  Callbacks of approval rate
####################################

@app.callback(
    [Output('ar-group-product-dd', 'options'), Output('ar-group-product-dd', 'value')],
    [Input('btn_ar_groups', 'n_clicks')]
)
def update_ar_groups(n_clicks):
    group_of_products = df_ar.GROUPOFPRODUCT.unique()
    group_of_products.sort()
    return [{'label': product, 'value': product} for product in group_of_products], group_of_products

@app.callback(
    [Output('ar-products-dd', 'options'), Output('ar-products-dd', 'value')],
    [Input('btn_ar_products', 'n_clicks'), Input('ar-group-product-dd', 'value')]
)
def update_ar_products(n_clicks, group_of_products):
    if group_of_products:
        ar_products = df_ar[df_ar.GROUPOFPRODUCT.isin(group_of_products)].PRODUCT.unique()
    else:
        ar_products = df_ar.PRODUCT.unique()
    ar_products.sort()
    return [{'label': product, 'value': product} for product in ar_products], ar_products

@app.callback(
    [Output('ar-cities-dd', 'options'), Output('ar-cities-dd', 'value')],
    [Input('btn_ar_regions', 'n_clicks')]
)
def update_ar_cities(n_clicks):
    ar_cities = df_ar.CITY.unique()
    ar_cities.sort()
    return [{'label': city, 'value': city} for city in ar_cities], ar_cities

@app.callback(
    [Output('ar-segments-dd', 'options'), Output('ar-segments-dd', 'value')],
    [Input('btn_ar_segments', 'n_clicks')]
)
def update_ar_segments(n_clicks):
    ar_segments = df_ar.SEGMENT.unique()
    ar_segments.sort()
    return [{'label': segment, 'value': segment} for segment in ar_segments], ar_segments

@app.callback(
    [Output('ar-clienttype-dd', 'options'), Output('ar-clienttype-dd', 'value')],
    [Input('btn_ar_clienttype', 'n_clicks')]
)
def update_ar_clienttype(n_clicks):
    client_types = df_ar.TYPEOFCLIENTS.unique()
    client_types.sort()
    return [{'label': client, 'value': client} for client in client_types], client_types

@app.callback(
    [Output('ar-otdels-dd', 'options'), Output('ar-otdels-dd', 'value')],
    [Input('btn_ar_otdels', 'n_clicks'), Input('ar-cities-dd', 'value')]
)
def update_ar_otdels(n_clicks, cities):
    if cities:
        otdels = df_ar[df_ar.CITY.isin(cities)].LONGNAME.unique()
    else:
        otdels = df_ar.LONGNAME.unique()

    return [{'label': otdel, 'value': otdel} for otdel in otdels], otdels

@app.callback(
    [Output('ar-strategies-dd', 'options'), Output('ar-strategies-dd', 'value')],
    [Input('btn_ar_strategies', 'n_clicks')]
)
def update_ar_strategies(n_clicks):
    ar_strategies = df_ar.STRATEGY.unique()
    ar_strategies.sort()
    return [{'label': strategy, 'value': strategy} for strategy in ar_strategies], ar_strategies

@app.callback(
    [Output('ar-cors-dd', 'options'), Output('ar-cors-dd', 'value')],
    [Input('btn_ar_cors', 'n_clicks')]
)
def update_ar_cors(n_clicks):
    ar_cors = df_ar.COR.unique()
    ar_cors.sort()
    return [{'label': cor, 'value': cor} for cor in ar_cors], ar_cors

@app.callback(
    [Output('ar-challengers-dd', 'options'), Output('ar-challengers-dd', 'value')],
    [Input('btn_ar_challengers', 'n_clicks')]
)
def update_ar_challengers(n_clicks):
    ar_challengers = df_ar.CHALLENGER.unique()
    ar_challengers.sort()
    return [{'label': challenger, 'value': challenger} for challenger in ar_challengers], ar_challengers

@app.callback(
    [Output('ar-scorenames-dd', 'options'), Output('ar-scorenames-dd', 'value')],
    [Input('btn_ar_scorenames', 'n_clicks')]
)
def update_ar_score_names(n_clicks):
    ar_score_names = df_ar.SCORE_CARD_NAME.unique()
    ar_score_names.sort()
    return [{'label': score, 'value': score} for score in ar_score_names], ar_score_names

@app.callback(
    Output('download-ar', 'data'), [Input('btn_download_ar', 'n_clicks')],
    [State('ar-date-picker', 'start_date'), State('ar-date-picker', 'end_date'), State('ar-products-dd', 'value'), State('ar-cities-dd', 'value'),
     State('ar-otdels-dd', 'value'), State('ar-clienttype-dd', 'value'), State('ar-segments-dd', 'value'), State('ar-periodtype-dd', 'value'),
     State('ar-strategies-dd', 'value'), State('ar-cors-dd', 'value'), State('ar-challengers-dd', 'value'), State('ar-scorenames-dd', 'value')]
)
def download_file_ar(n_clicks, start_date, end_date, ar_products, ar_cities, ar_otdels, ar_clienttype, ar_segments, period_type, ar_strategies,
                     ar_cors, ar_challengers, ar_score_names):
    start_date = chg_str_to_date(start_date)
    end_date = chg_str_to_date(end_date)
    df_ar2 = df_ar
    df_ar2 = df_ar2[(df_ar2.DREG >= start_date) & (df_ar2.DREG <= end_date)]
    if ar_products:
        df_ar2 = df_ar2[df_ar2.PRODUCT.isin(ar_products)]
    if ar_cities:
        df_ar2 = df_ar2[df_ar2.CITY.isin(ar_cities)]
    if ar_otdels:
        df_ar2 = df_ar2[df_ar2.LONGNAME.isin(ar_otdels)]
    if ar_clienttype:
        df_ar2 = df_ar2[df_ar2.TYPEOFCLIENTS.isin(ar_clienttype)]
    if ar_segments:
        df_ar2 = df_ar2[df_ar2.SEGMENT.isin(ar_segments)]
    if ar_strategies:
        df_ar2 = df_ar2[df_ar2.STRATEGY.isin(ar_strategies)]
    if ar_cors:
        df_ar2 = df_ar2[df_ar2.COR.isin(ar_cors)]
    if ar_challengers:
        df_ar2 = df_ar2[df_ar2.CHALLENGER.isin(ar_challengers)]
    if ar_score_names:
        df_ar2 = df_ar2[df_ar2.SCORE_CARD_NAME.isin(ar_score_names)]

    if period_type == 'По дням':
        df_tab = tables.appr_table(df_ar2)

    if period_type == 'По неделям':
        df_tab = tables.appr_table_week(df_ar2)

    if period_type == 'По месяцам':
        df_tab = tables.appr_table_month(df_ar2)

    if n_clicks > 0:
        return send_data_frame(df_tab.to_excel, filename="ar_table.xlsx")


@app.callback(
    [Output('ar-table', 'figure'), Output('ar-graph', 'figure')],
    [Input('ar-date-picker', 'start_date'), Input('ar-date-picker', 'end_date'), Input('ar-products-dd', 'value'), Input('ar-cities-dd', 'value'),
     Input('ar-otdels-dd', 'value'), Input('ar-clienttype-dd', 'value'), Input('ar-segments-dd', 'value'), Input('ar-periodtype-dd', 'value'),
     Input('ar-strategies-dd', 'value'), Input('ar-cors-dd', 'value'), Input('ar-challengers-dd', 'value'), Input('ar-scorenames-dd', 'value')]
)
def update_ar_table_graph(start_date, end_date, ar_products, ar_cities, ar_otdels, ar_clienttype, ar_segments, period_type, ar_strategies,
                          ar_cors, ar_challengers, ar_score_names):
    start_date = chg_str_to_date(start_date)
    end_date = chg_str_to_date(end_date)
    df_ar2 = df_ar
    df_ar2 = df_ar2[(df_ar2.DREG >= start_date) & (df_ar2.DREG <= end_date)]
    if ar_products:
        df_ar2 = df_ar2[df_ar2.PRODUCT.isin(ar_products)]
    if ar_cities:
        df_ar2 = df_ar2[df_ar2.CITY.isin(ar_cities)]
    if ar_otdels:
        df_ar2 = df_ar2[df_ar2.LONGNAME.isin(ar_otdels)]
    if ar_clienttype:
        df_ar2 = df_ar2[df_ar2.TYPEOFCLIENTS.isin(ar_clienttype)]
    if ar_segments:
        df_ar2 = df_ar2[df_ar2.SEGMENT.isin(ar_segments)]
    if ar_strategies:
        df_ar2 = df_ar2[df_ar2.STRATEGY.isin(ar_strategies)]
    if ar_cors:
        df_ar2 = df_ar2[df_ar2.COR.isin(ar_cors)]
    if ar_challengers:
        df_ar2 = df_ar2[df_ar2.CHALLENGER.isin(ar_challengers)]
    if ar_score_names:
        df_ar2 = df_ar2[df_ar2.SCORE_CARD_NAME.isin(ar_score_names)]

    if period_type == 'По дням':
        return graphs.table_appr(tables.appr_table(df_ar2)), graphs.graph_appr(tables.appr_table(df_ar2))

    if period_type == 'По неделям':
        return graphs.table_appr(tables.appr_table_week(df_ar2)), graphs.graph_appr(tables.appr_table_week(df_ar2))

    if period_type == 'По месяцам':
        return graphs.table_appr(tables.appr_table_month(df_ar2)), graphs.graph_appr(tables.appr_table_month(df_ar2))

@app.callback(
    [Output('pivot-layout', 'children'), Output('btn_add_pivot', 'children')],
    [Input('btn_add_pivot', 'n_clicks')]
)
def show_hide_pivot_layout(n_clicks):
    if n_clicks % 2 != 0:
        return pivot_layout, 'Удалить сводную таблицу'
    return html.Div([]), 'Добавить сводную таблицу'

@app.callback(
    Output('pivot-table', 'children'),
    [Input('btn_create_pivot', 'n_clicks')],
    [State('pivot-columns-dd', 'value'), State('pivot-rows-dd', 'value'), State('pivot-value-dd', 'value'), State('pivot-type-dd', 'value'),
     State('first-svod-column-name', 'value'), State('first-svod-column-formula', 'value'), State('first-svod-column-operation', 'value'), State('first-svod-column-addit', 'value'),
     State('second-svod-column-name', 'value'), State('second-svod-column-formula', 'value'), State('second-svod-column-operation', 'value'), State('second-svod-column-addit', 'value'),
     State('third-svod-column-name', 'value'), State('third-svod-column-formula', 'value'), State('third-svod-column-operation', 'value'), State('third-svod-column-addit', 'value'),
     State('fourth-svod-column-name', 'value'), State('fourth-svod-column-formula', 'value'), State('fourth-svod-column-operation', 'value'), State('fourth-svod-column-addit', 'value'),
     State('fifth-svod-column-name', 'value'), State('fifth-svod-column-formula', 'value'), State('fifth-svod-column-operation', 'value'), State('fifth-svod-column-addit', 'value'),
     State('first-svod-column-other', 'value'), State('second-svod-column-other', 'value'), State('third-svod-column-other', 'value'), State('fourth-svod-column-other', 'value'),
     State('fifth-svod-column-other', 'value'), State('ar-date-picker', 'start_date'), State('ar-date-picker', 'end_date'), State('ar-products-dd', 'value'),
     State('ar-cities-dd', 'value'), State('ar-otdels-dd', 'value'), State('ar-clienttype-dd', 'value'), State('ar-segments-dd', 'value'),
     State('ar-periodtype-dd', 'value'), State('ar-strategies-dd', 'value'), State('ar-cors-dd', 'value'), State('ar-challengers-dd', 'value'),
     State('ar-scorenames-dd', 'value'), State('pivot-addition-dd', 'value')]
)
def create_pivot_table(n_clicks, pivot_cols, pivot_rows, pivot_value, pivot_type, first_col_name, first_col_formula, first_col_oper, first_col_addit,
                       second_col_name, second_col_formula, second_col_oper, second_col_addit, third_col_name, third_col_formula, third_col_oper, third_col_addit,
                       fourth_col_name, fourth_col_formula, fourth_col_oper, fourth_col_addit, fifth_col_name, fifth_col_formula, fifth_col_oper, fifth_col_addit,
                       first_col_other, second_col_other, third_col_other, fourth_col_other, fifth_col_other, start_date, end_date, ar_products, ar_cities, ar_otdels,
                       ar_clienttype, ar_segments, period_type, ar_strategies, ar_cors, ar_challengers, ar_score_names, pivot_addition):
    if n_clicks > 0:
        start_date = chg_str_to_date(start_date)
        end_date = chg_str_to_date(end_date)
        df_ar2 = df_ar
        df_ar2 = df_ar2[(df_ar2.DREG >= start_date) & (df_ar2.DREG <= end_date)]
        if ar_products:
            df_ar2 = df_ar2[df_ar2.PRODUCT.isin(ar_products)]
        if ar_cities:
            df_ar2 = df_ar2[df_ar2.CITY.isin(ar_cities)]
        if ar_otdels:
            df_ar2 = df_ar2[df_ar2.LONGNAME.isin(ar_otdels)]
        if ar_clienttype:
            df_ar2 = df_ar2[df_ar2.TYPEOFCLIENTS.isin(ar_clienttype)]
        if ar_segments:
            df_ar2 = df_ar2[df_ar2.SEGMENT.isin(ar_segments)]
        if ar_strategies:
            df_ar2 = df_ar2[df_ar2.STRATEGY.isin(ar_strategies)]
        if ar_cors:
            df_ar2 = df_ar2[df_ar2.COR.isin(ar_cors)]
        if ar_challengers:
            df_ar2 = df_ar2[df_ar2.CHALLENGER.isin(ar_challengers)]
        if ar_score_names:
            df_ar2 = df_ar2[df_ar2.SCORE_CARD_NAME.isin(ar_score_names)]

        isArbitrary = False
        if first_col_name or first_col_formula or second_col_name or second_col_formula or third_col_name or third_col_formula or fourth_col_name or fourth_col_formula or fifth_col_name or fifth_col_formula:
            isArbitrary = True
        if pivot_cols and pivot_rows and pivot_value and pivot_type and isArbitrary is False:
            if pivot_type == 'Сумма':
                agg = np.sum
            if pivot_type == 'Среднее':
                agg = np.mean
            if pivot_type == 'Медиана':
                agg = np.median
            if pivot_type == 'Максимум':
                agg = np.max
            if pivot_type == 'Минимум':
                agg = np.min

            return html.Div([
                dcc.Graph(
                    figure=graphs.table_pivot(tables.create_pivot(df_ar2, pivot_cols, pivot_rows, pivot_value, agg, pivot_addition))
                )
            ])
        if isArbitrary and pivot_rows:
            values = []
            if first_col_name and first_col_formula:
                values.append([first_col_name, first_col_formula, first_col_oper, first_col_addit, first_col_other])
            if second_col_name and second_col_formula:
                values.append([second_col_name, second_col_formula, second_col_oper, second_col_addit, second_col_other])
            if third_col_name and third_col_formula:
                values.append([third_col_name, third_col_formula, third_col_oper, third_col_addit, third_col_other])
            if fourth_col_name and fourth_col_formula:
                values.append([fourth_col_name, fourth_col_formula, fourth_col_oper, fourth_col_addit, fourth_col_other])
            if fifth_col_name and fifth_col_formula:
                values.append([fifth_col_name, first_col_formula, fifth_col_oper, fifth_col_addit, fifth_col_other])

            return html.Div([
                dcc.Graph(
                    figure=graphs.table_pivot(tables.arbitrary_pivot(df_ar2, values, pivot_rows))
                )
            ])
    return html.Div([])

#######################################
#  Callbacks of rejections
#######################################

@app.callback(
    [Output('reason-group-product-dd', 'options'), Output('reason-group-product-dd', 'value')],
    [Input('btn_reason_groups', 'n_clicks')]
)
def update_reason_groups(n_clicks):
    group_of_products = df_ar.GROUPOFPRODUCT.unique()
    group_of_products.sort()
    return [{'label': product, 'value': product} for product in group_of_products], group_of_products

@app.callback(
    [Output('reason-products-dd', 'options'), Output('reason-products-dd', 'value')],
    [Input('btn_reason_products', 'n_clicks'), Input('reason-group-product-dd', 'value')]
)
def update_reason_products(n_clicks, group_of_products):
    if group_of_products:
        products = df_ar[df_ar.GROUPOFPRODUCT.isin(group_of_products)].PRODUCT.unique()
    else:
        products = df_ar.PRODUCT.unique()
    products.sort()
    return [{'label': product, 'value': product} for product in products], products

@app.callback(
    [Output('reason-cities-dd', 'options'), Output('reason-cities-dd', 'value')],
    [Input('btn_reason_regions', 'n_clicks')]
)
def update_reason_cities(n_clicks):
    cities = df_ar.CITY.unique()
    cities.sort()
    return [{'label': city, 'value': city} for city in cities], cities

@app.callback(
    [Output('reason-segments-dd', 'options'), Output('reason-segments-dd', 'value')],
    [Input('btn_reason_segments', 'n_clicks')]
)
def update_reason_segments(n_clicks):
    segments = df_ar.SEGMENT.unique()
    segments.sort()
    return [{'label': segment, 'value': segment} for segment in segments], segments

@app.callback(
    [Output('reason-clienttype-dd', 'options'), Output('reason-clienttype-dd', 'value')],
    [Input('btn_reason_clienttype', 'n_clicks')]
)
def update_reason_clienttype(n_clicks):
    client_types = df_ar.TYPEOFCLIENTS.unique()
    client_types.sort()
    return [{'label': client, 'value': client} for client in client_types], client_types

@app.callback(
    [Output('reason-otdels-dd', 'options'), Output('reason-otdels-dd', 'value')],
    [Input('btn_reason_otdels', 'n_clicks'), Input('reason-cities-dd', 'value')]
)
def update_reason_otdels(n_clicks, cities):
    if cities:
        otdels = df_ar[df_ar.CITY.isin(cities)].LONGNAME.unique()
    else:
        otdels = df_ar.LONGNAME.unique()

    return [{'label': otdel, 'value': otdel} for otdel in otdels], otdels

@app.callback(
    [Output('reason-strategies-dd', 'options'), Output('reason-strategies-dd', 'value')],
    [Input('btn_reason_strategies', 'n_clicks')]
)
def update_reason_strategies(n_clicks):
    strategies = df_ar.STRATEGY.unique()
    strategies.sort()
    return [{'label': strategy, 'value': strategy} for strategy in strategies], strategies

@app.callback(
    [Output('reason-cors-dd', 'options'), Output('reason-cors-dd', 'value')],
    [Input('btn_reason_cors', 'n_clicks')]
)
def update_reason_cors(n_clicks):
    ar_cors = df_ar.COR.unique()
    ar_cors.sort()
    return [{'label': cor, 'value': cor} for cor in ar_cors], ar_cors

@app.callback(
    [Output('reason-challengers-dd', 'options'), Output('reason-challengers-dd', 'value')],
    [Input('btn_reason_challengers', 'n_clicks')]
)
def update_reason_challengers(n_clicks):
    ar_challengers = df_ar.CHALLENGER.unique()
    ar_challengers.sort()
    return [{'label': challenger, 'value': challenger} for challenger in ar_challengers], ar_challengers

@app.callback(
    [Output('reason-scorenames-dd', 'options'), Output('reason-scorenames-dd', 'value')],
    [Input('btn_reason_scorenames', 'n_clicks')]
)
def update_reason_score_names(n_clicks):
    ar_score_names = df_ar.SCORE_CARD_NAME.unique()
    ar_score_names.sort()
    return [{'label': score, 'value': score} for score in ar_score_names], ar_score_names

@app.callback(
    Output('download-rg', 'data'), [Input('btn_download_rg', 'n_clicks')],
    [State('reason-date-picker', 'start_date'), State('reason-date-picker', 'end_date'), State('reason-products-dd', 'value'), State('reason-cities-dd', 'value'),
     State('reason-otdels-dd', 'value'), State('reason-clienttype-dd', 'value'), State('reason-segments-dd', 'value'), State('reason-strategies-dd', 'value'),
     State('reason-cors-dd', 'value'), State('reason-challengers-dd', 'value'), State('reason-scorenames-dd', 'value')]
)
def download_reason_groups(n_clicks, start_date, end_date, products, cities, otdels, clienttype, segments, strategies, ar_cors, ar_challengers, ar_score_names):
    start_date = chg_str_to_date(start_date)
    end_date = chg_str_to_date(end_date)
    df_ar2 = df_ar
    df_ar2 = df_ar2[(df_ar2.DREG >= start_date) & (df_ar2.DREG <= end_date)]
    if products:
        df_ar2 = df_ar2[df_ar2.PRODUCT.isin(products)]
    if cities:
        df_ar2 = df_ar2[df_ar2.CITY.isin(cities)]
    if otdels:
        df_ar2 = df_ar2[df_ar2.LONGNAME.isin(otdels)]
    if clienttype:
        df_ar2 = df_ar2[df_ar2.TYPEOFCLIENTS.isin(clienttype)]
    if segments:
        df_ar2 = df_ar2[df_ar2.SEGMENT.isin(segments)]
    if strategies:
        df_ar2 = df_ar2[df_ar2.STRATEGY.isin(strategies)]
    if ar_cors:
        df_ar2 = df_ar2[df_ar2.COR.isin(ar_cors)]
    if ar_challengers:
        df_ar2 = df_ar2[df_ar2.CHALLENGER.isin(ar_challengers)]
    if ar_score_names:
        df_ar2 = df_ar2[df_ar2.SCORE_CARD_NAME.isin(ar_score_names)]

    df_tab = tables.reason_table(df_ar2)
    if n_clicks > 0:
        return send_data_frame(df_tab.to_excel, filename="reason_groups.xlsx")

@app.callback(
    Output('download-ra', 'data'), [Input('btn_download_ra', 'n_clicks')],
    [State('reason-date-picker', 'start_date'), State('reason-date-picker', 'end_date'), State('reason-products-dd', 'value'), State('reason-cities-dd', 'value'),
     State('reason-otdels-dd', 'value'), State('reason-clienttype-dd', 'value'), State('reason-segments-dd', 'value'), State('reason-strategies-dd', 'value'),
     State('reason-cors-dd', 'value'), State('reason-challengers-dd', 'value'), State('reason-scorenames-dd', 'value')]
)
def download_reason_alerts(n_clicks, start_date, end_date, products, cities, otdels, clienttype, segments, strategies, ar_cors, ar_challengers, ar_score_names):
    start_date = chg_str_to_date(start_date)
    end_date = chg_str_to_date(end_date)
    df_ar2 = df_ar
    df_ar2 = df_ar2[(df_ar2.DREG >= start_date) & (df_ar2.DREG <= end_date)]
    if products:
        df_ar2 = df_ar2[df_ar2.PRODUCT.isin(products)]
    if cities:
        df_ar2 = df_ar2[df_ar2.CITY.isin(cities)]
    if otdels:
        df_ar2 = df_ar2[df_ar2.LONGNAME.isin(otdels)]
    if clienttype:
        df_ar2 = df_ar2[df_ar2.TYPEOFCLIENTS.isin(clienttype)]
    if segments:
        df_ar2 = df_ar2[df_ar2.SEGMENT.isin(segments)]
    if strategies:
        df_ar2 = df_ar2[df_ar2.STRATEGY.isin(strategies)]
    if ar_cors:
        df_ar2 = df_ar2[df_ar2.COR.isin(ar_cors)]
    if ar_challengers:
        df_ar2 = df_ar2[df_ar2.CHALLENGER.isin(ar_challengers)]
    if ar_score_names:
        df_ar2 = df_ar2[df_ar2.SCORE_CARD_NAME.isin(ar_score_names)]

    df_tab = tables.reason_alerts_table(df_ar2)
    if n_clicks > 0:
        return send_data_frame(df_tab.to_excel, filename="reason_alerts.xlsx")

@app.callback(
    [Output('reason-table', 'figure'), Output('reason-graph', 'figure'), Output('reason-alert-table', 'figure')],
    [Input('reason-date-picker', 'start_date'), Input('reason-date-picker', 'end_date'), Input('reason-products-dd', 'value'), Input('reason-cities-dd', 'value'),
     Input('reason-otdels-dd', 'value'), Input('reason-clienttype-dd', 'value'), Input('reason-segments-dd', 'value'), Input('reason-strategies-dd', 'value'),
     Input('reason-cors-dd', 'value'), Input('reason-challengers-dd', 'value'), Input('reason-scorenames-dd', 'value')]
)
def update_reason_table_graph(start_date, end_date, products, cities, otdels, clienttype, segments, strategies, ar_cors, ar_challengers, ar_score_names):
    start_date = chg_str_to_date(start_date)
    end_date = chg_str_to_date(end_date)
    df_ar2 = df_ar
    df_ar2 = df_ar2[(df_ar2.DREG >= start_date) & (df_ar2.DREG <= end_date)]
    if products:
        df_ar2 = df_ar2[df_ar2.PRODUCT.isin(products)]
    if cities:
        df_ar2 = df_ar2[df_ar2.CITY.isin(cities)]
    if otdels:
        df_ar2 = df_ar2[df_ar2.LONGNAME.isin(otdels)]
    if clienttype:
        df_ar2 = df_ar2[df_ar2.TYPEOFCLIENTS.isin(clienttype)]
    if segments:
        df_ar2 = df_ar2[df_ar2.SEGMENT.isin(segments)]
    if strategies:
        df_ar2 = df_ar2[df_ar2.STRATEGY.isin(strategies)]
    if ar_cors:
        df_ar2 = df_ar2[df_ar2.COR.isin(ar_cors)]
    if ar_challengers:
        df_ar2 = df_ar2[df_ar2.CHALLENGER.isin(ar_challengers)]
    if ar_score_names:
        df_ar2 = df_ar2[df_ar2.SCORE_CARD_NAME.isin(ar_score_names)]

    return graphs.table_reason(tables.reason_table(df_ar2)), graphs.graph_reason(tables.reason_graph_table(df_ar2)), graphs.table_reason_alert(tables.reason_alerts_table(df_ar2))

#########################################
#   Callbacks of vintage
#########################################

@app.callback(
    [Output('dcc-vintage-products', 'options'), Output('dcc-vintage-products', 'value')],
    [Input('btn_v_products', 'n_clicks')]
)
def update_vintage_products(n_clicks):
    v_products = dfv.PRODUCTS.unique()
    v_products.sort()
    return [{'label': v_product, 'value': v_product} for v_product in v_products], v_products

@app.callback(
    [Output('dcc-vintage-programs', 'options'), Output('dcc-vintage-programs', 'value')],
    [Input('btn_v_programs', 'n_clicks'), Input('dcc-vintage-products', 'value')]
)
def update_vintage_programs(n_clicks, v_products):
    if len(v_products) > 0:
        v_programs = dfv[dfv.PRODUCTS.isin(v_products)].PROGRAMM.unique()
    else:
        v_programs = dfv.PROGRAMM.unique()

    v_programs.sort()

    return [{'label': v_program, 'value': v_program} for v_program in v_programs], v_programs

@app.callback(
    [Output('dcc-vintage-cities', 'options'), Output('dcc-vintage-cities', 'value')],
    [Input('btn_v_cities', 'n_clicks')]
)
def update_vintage_cities(n_clicks):
    v_cities = dfv.CITY2.unique()
    v_cities.sort()
    return [{'label': v_city, 'value': v_city} for v_city in v_cities], v_cities

@app.callback(
    [Output('dcc-vintage-segments', 'options'), Output('dcc-vintage-segments', 'value')],
    [Input('btn_v_segments', 'n_clicks')]
)
def update_vintage_cities(n_clicks):
    v_segments = dfv.SEGMENT.unique()
    v_segments.sort()
    return [{'label': v_segment, 'value': v_segment} for v_segment in v_segments], v_segments

@app.callback(
    [Output('dcc-vintage-ages', 'options'), Output('dcc-vintage-ages', 'value')],
    [Input('btn_v_ages', 'n_clicks')]
)
def update_vintage_cities(n_clicks):
    v_ages = dfv.AGE.unique()
    v_ages.sort()
    return [{'label': v_age, 'value': v_age} for v_age in v_ages], v_ages

@app.callback(
    Output('download-vintage', 'data'), [Input('btn_download_vintage', 'n_clicks')],
    [State('dcc-vintage-products', 'value'), State('dcc-vintage-programs', 'value'), State('dcc-vintage-cities', 'value'),
     State('dcc-vintage-segments', 'value'), State('dcc-vintage-ages', 'value'), State('dcc-vintage-groups', 'value')]
)
def download_vintage(n_clicks, v_products, v_programs, v_cities, v_segments, v_ages, v_group):
    dfv2 = dfv
    if v_products:
        dfv2 = dfv2[dfv2.PRODUCTS.isin(v_products)]
    if v_programs:
        dfv2 = dfv2[dfv2.PROGRAMM.isin(v_programs)]
    if v_cities:
        dfv2 = dfv2[dfv2.CITY2.isin(v_cities)]
    if v_segments:
        dfv2 = dfv2[dfv2.SEGMENT.isin(v_segments)]
    if v_ages:
        dfv2 = dfv2[dfv2.AGE.isin(v_ages)]

    if v_group == 'Просрочка 5+':
        df_tab = tables.vintage_table_5(dfv2)

    if v_group == 'Просрочка 30+':
        df_tab = tables.vintage_table_30(dfv2)

    if v_group == 'Просрочка 60+':
        df_tab = tables.vintage_table_60(dfv2)

    if v_group == 'Просрочка 90+':
        df_tab = tables.vintage_table_90(dfv2)

    if n_clicks > 0:
        return send_data_frame(df_tab.to_excel, filename='vintage.xlsx')

@app.callback(
    Output('vintage-table', 'figure'),
    [Input('dcc-vintage-products', 'value'), Input('dcc-vintage-programs', 'value'), Input('dcc-vintage-cities', 'value'),
     Input('dcc-vintage-segments', 'value'), Input('dcc-vintage-ages', 'value'), Input('dcc-vintage-groups', 'value')]
)
def update_vintage_table(v_products, v_programs, v_cities, v_segments, v_ages, v_group):
    dfv2 = dfv
    if v_products:
        dfv2 = dfv2[dfv2.PRODUCTS.isin(v_products)]
    if v_programs:
        dfv2 = dfv2[dfv2.PROGRAMM.isin(v_programs)]
    if v_cities:
        dfv2 = dfv2[dfv2.CITY2.isin(v_cities)]
    if v_segments:
        dfv2 = dfv2[dfv2.SEGMENT.isin(v_segments)]
    if v_ages:
        dfv2 = dfv2[dfv2.AGE.isin(v_ages)]

    if v_group == 'Просрочка 5+':
        return graphs.table_vintage(tables.vintage_table_5(dfv2))

    if v_group == 'Просрочка 30+':
        return graphs.table_vintage(tables.vintage_table_30(dfv2))

    if v_group == 'Просрочка 60+':
        return graphs.table_vintage(tables.vintage_table_60(dfv2))

    if v_group == 'Просрочка 90+':
        return graphs.table_vintage(tables.vintage_table_90(dfv2))

#####################################################
#  Callbacks of saved pattern
#####################################################

@app.callback(
    [Output('pattern-group-product-dd', 'options'), Output('pattern-group-product-dd', 'value')],
    [Input('btn_pattern_groups', 'n_clicks')]
)
def update_pattern_groups(n_clicks):
    group_of_products = df_ar.GROUPOFPRODUCT.unique()
    group_of_products.sort()
    return [{'label': product, 'value': product} for product in group_of_products], group_of_products

@app.callback(
    [Output('pattern-products-dd', 'options'), Output('pattern-products-dd', 'value')],
    [Input('btn_pattern_products', 'n_clicks'), Input('pattern-group-product-dd', 'value')]
)
def update_pattern_products(n_clicks, group_of_products):
    if group_of_products:
        products = df_ar[df_ar.GROUPOFPRODUCT.isin(group_of_products)].PRODUCT.unique()
    else:
        products = df_ar.PRODUCT.unique()
    products.sort()
    return [{'label': product, 'value': product} for product in products], products

@app.callback(
    [Output('pattern-cities-dd', 'options'), Output('pattern-cities-dd', 'value')],
    [Input('btn_pattern_regions', 'n_clicks')]
)
def update_pattern_cities(n_clicks):
    cities = df_ar.CITY.unique()
    cities.sort()
    return [{'label': city, 'value': city} for city in cities], cities

@app.callback(
    [Output('pattern-segments-dd', 'options'), Output('pattern-segments-dd', 'value')],
    [Input('btn_pattern_segments', 'n_clicks')]
)
def update_pattern_segments(n_clicks):
    segments = df_ar.SEGMENT.unique()
    segments.sort()
    return [{'label': segment, 'value': segment} for segment in segments], segments

@app.callback(
    [Output('pattern-clienttype-dd', 'options'), Output('pattern-clienttype-dd', 'value')],
    [Input('btn_pattern_clienttype', 'n_clicks')]
)
def update_pattern_clienttype(n_clicks):
    client_types = df_ar.TYPEOFCLIENTS.unique()
    client_types.sort()
    return [{'label': client, 'value': client} for client in client_types], client_types

@app.callback(
    [Output('pattern-otdels-dd', 'options'), Output('pattern-otdels-dd', 'value')],
    [Input('btn_pattern_otdels', 'n_clicks'), Input('pattern-cities-dd', 'value')]
)
def update_pattern_otdels(n_clicks, cities):
    if cities:
        otdels = df_ar[df_ar.CITY.isin(cities)].LONGNAME.unique()
    else:
        otdels = df_ar.LONGNAME.unique()

    return [{'label': otdel, 'value': otdel} for otdel in otdels], otdels

@app.callback(
    [Output('pattern-strategies-dd', 'options'), Output('pattern-strategies-dd', 'value')],
    [Input('btn_pattern_strategies', 'n_clicks')]
)
def update_pattern_strategies(n_clicks):
    strategies = df_ar.STRATEGY.unique()
    strategies.sort()
    return [{'label': strategy, 'value': strategy} for strategy in strategies], strategies

@app.callback(
    [Output('pattern-cors-dd', 'options'), Output('pattern-cors-dd', 'value')],
    [Input('btn_pattern_cors', 'n_clicks')]
)
def update_pattern_cors(n_clicks):
    ar_cors = df_ar.COR.unique()
    ar_cors.sort()
    return [{'label': cor, 'value': cor} for cor in ar_cors], ar_cors

@app.callback(
    [Output('pattern-challengers-dd', 'options'), Output('pattern-challengers-dd', 'value')],
    [Input('btn_pattern_challengers', 'n_clicks')]
)
def update_pattern_challengers(n_clicks):
    ar_challengers = df_ar.CHALLENGER.unique()
    ar_challengers.sort()
    return [{'label': challenger, 'value': challenger} for challenger in ar_challengers], ar_challengers

@app.callback(
    [Output('pattern-scorenames-dd', 'options'), Output('pattern-scorenames-dd', 'value')],
    [Input('btn_pattern_scorenames', 'n_clicks')]
)
def update_pattern_score_names(n_clicks):
    ar_score_names = df_ar.SCORE_CARD_NAME.unique()
    ar_score_names.sort()
    return [{'label': score, 'value': score} for score in ar_score_names], ar_score_names

@app.callback(
    Output('download-pattern', 'data'), [Input('btn_download_pattern', 'n_clicks')],
    [State('pattern-group-product-dd', 'value'), State('pattern-products-dd', 'value'), State('pattern-cities-dd', 'value'), State('pattern-segments-dd', 'value'),
     State('pattern-clienttype-dd', 'value'), State('pattern-otdels-dd', 'value'), State('pattern-strategies-dd', 'value'), State('pattern-cors-dd', 'value'),
     State('pattern-challengers-dd', 'value'), State('pattern-scorenames-dd', 'value'), State('pattern-list-dd', 'value'), State('pattern-date-picker', 'start_date'),
     State('pattern-date-picker', 'end_date')]
)
def download_pattern(n_clicks, pattern_group_products, pattern_products, pattern_cities, pattern_segments, pattern_clientype, pattern_otdels, pattern_strategies,
                 pattern_cors, pattern_challengers, pattern_scorenames, pattern_list, start_date, end_date):
    try:
        with open(client_path + 'patterns.json', 'r', encoding='utf-8') as file:
            patterns = json.load(file)
    except FileNotFoundError:
        with open(server_path + 'patterns.json', 'r', encoding='utf-8') as file:
            patterns = json.load(file)

    df_ar2 = df_ar
    start_date = chg_str_to_date(start_date)
    end_date = chg_str_to_date(end_date)
    df_ar2 = df_ar2[(df_ar2.DREG >= start_date) & (df_ar2.DREG <= end_date)]
    if pattern_group_products:
        df_ar2 = df_ar2[df_ar2.GROUPOFPRODUCT.isin(pattern_group_products)]
    if pattern_products:
        df_ar2 = df_ar2[df_ar2.PRODUCT.isin(pattern_products)]
    if pattern_cities:
        df_ar2 = df_ar2[df_ar2.CITY.isin(pattern_cities)]
    if pattern_segments:
        df_ar2 = df_ar2[df_ar2.SEGMENT.isin(pattern_segments)]
    if pattern_clientype:
        df_ar2 = df_ar2[df_ar2.TYPEOFCLIENTS.isin(pattern_clientype)]
    if pattern_otdels:
        df_ar2 = df_ar2[df_ar2.LONGNAME.isin(pattern_otdels)]
    if pattern_strategies:
        df_ar2 = df_ar2[df_ar2.STRATEGY.isin(pattern_strategies)]
    if pattern_cors:
        df_ar2 = df_ar2[df_ar2.COR.isin(pattern_cors)]
    if pattern_challengers:
        df_ar2 = df_ar2[df_ar2.CHALLENGER.isin(pattern_challengers)]
    if pattern_scorenames:
        df_ar2 = df_ar2[df_ar2.SCORE_CARD_NAME.isin(pattern_scorenames)]

    params = patterns[pattern_list]
    pivot_columns = params['pivot_columns']
    pivot_rows = params['pivot_rows']
    pivot_value = params['pivot_value']
    pivot_type = params['pivot_type']
    pivot_addition = params['pivot_addition']
    first_col_name = params['first_col_name']
    first_col_formula = params['first_col_formula']
    first_col_operation = params['first_col_operation']
    first_col_addit = params['first_col_addit']
    second_col_name = params['second_col_name']
    second_col_formula = params['second_col_formula']
    second_col_operation = params['second_col_operation']
    second_col_addit = params['second_col_addit']
    third_col_name = params['third_col_name']
    third_col_formula = params['third_col_formula']
    third_col_operation = params['third_col_operation']
    third_col_addit = params['third_col_addit']
    fourth_col_name = params['fourth_col_name']
    fourth_col_formula = params['fourth_col_formula']
    fourth_col_operation = params['fourth_col_operation']
    fourth_col_addit = params['fourth_col_addit']
    fifth_col_name = params['fifth_col_name']
    fifth_col_formula = params['fifth_col_formula']
    fifth_col_operation = params['fifth_col_operation']
    fifth_col_addit = params['fifth_col_addit']
    first_col_other = params['first_col_other']
    second_col_other = params['second_col_other']
    third_col_other = params['third_col_other']
    fourth_col_other = params['fourth_col_other']
    fifth_col_other = params['fifth_col_other']

    isArbitrary = False
    if first_col_name or first_col_formula or second_col_name or second_col_formula or third_col_name or third_col_formula or fourth_col_name or fourth_col_formula or fifth_col_name or fifth_col_formula:
        isArbitrary = True
    if pivot_columns and pivot_rows and pivot_value and pivot_type and isArbitrary is False:
        if pivot_type == 'Сумма':
            agg = np.sum
        if pivot_type == 'Среднее':
            agg = np.mean
        if pivot_type == 'Медиана':
            agg = np.median
        if pivot_type == 'Максимум':
            agg = np.max
        if pivot_type == 'Минимум':
            agg = np.min

        df_tab = tables.create_pivot(df_ar2, pivot_columns, pivot_rows, pivot_value, agg, pivot_addition)
        if n_clicks > 0:
            return send_data_frame(df_tab.to_excel, filename="pivot_table.xlsx")

    if isArbitrary and pivot_rows:
        values = []
        if first_col_name and first_col_formula:
            values.append([first_col_name, first_col_formula, first_col_operation, first_col_addit, first_col_other])
        if second_col_name and second_col_formula:
            values.append([second_col_name, second_col_formula, second_col_operation, second_col_addit, second_col_other])
        if third_col_name and third_col_formula:
            values.append([third_col_name, third_col_formula, third_col_operation, third_col_addit, third_col_other])
        if fourth_col_name and fourth_col_formula:
            values.append([fourth_col_name, fourth_col_formula, fourth_col_operation, fourth_col_addit, fourth_col_other])
        if fifth_col_name and fifth_col_formula:
            values.append([fifth_col_name, first_col_formula, fifth_col_operation, fifth_col_addit, fifth_col_other])

        df_tab = tables.arbitrary_pivot(df_ar2, values, pivot_rows)
        if n_clicks > 0:
            return send_data_frame(df_tab.to_excel, filename="pivot_table.xlsx")


@app.callback(
    Output('save-pattern-label', 'children'), [Input('btn_save_pattern', 'n_clicks')],
    [State('pivot-columns-dd', 'value'), State('pivot-rows-dd', 'value'), State('pivot-value-dd', 'value'), State('pivot-type-dd', 'value'), State('pivot-addition-dd', 'value'),
     State('first-svod-column-name', 'value'), State('first-svod-column-formula', 'value'), State('first-svod-column-operation', 'value'), State('first-svod-column-addit', 'value'),
     State('second-svod-column-name', 'value'), State('second-svod-column-formula', 'value'), State('second-svod-column-operation', 'value'), State('second-svod-column-addit', 'value'),
     State('third-svod-column-name', 'value'), State('third-svod-column-formula', 'value'), State('third-svod-column-operation', 'value'), State('third-svod-column-addit', 'value'),
     State('fourth-svod-column-name', 'value'), State('fourth-svod-column-formula', 'value'), State('fourth-svod-column-operation', 'value'), State('fourth-svod-column-addit', 'value'),
     State('fifth-svod-column-name', 'value'), State('fifth-svod-column-formula', 'value'), State('fifth-svod-column-operation', 'value'), State('fifth-svod-column-addit', 'value'),
     State('first-svod-column-other', 'value'), State('second-svod-column-other', 'value'), State('third-svod-column-other', 'value'), State('fourth-svod-column-other', 'value'),
     State('fifth-svod-column-other', 'value'), State('save-pattern-input', 'value')]
)
def save_pattern_parameters(n_clicks, pivot_columns, pivot_rows, pivot_value, pivot_type, pivot_addition, first_col_name, first_col_formula, first_col_operation,
                            first_col_addit, second_col_name, second_col_formula, second_col_operation, second_col_addit, third_col_name, third_col_formula, third_col_operation,
                            third_col_addit, fourth_col_name, fourth_col_formula, fourth_col_operation, fourth_col_addit, fifth_col_name, fifth_col_formula, fifth_col_operation,
                            fifth_col_addit, first_col_other, second_col_other, third_col_other, fourth_col_other, fifth_col_other, input_pattern_name):
    if n_clicks > 0:
        if input_pattern_name == "" or input_pattern_name.strip() == "":
            return html.Label("Введите наименование шаблона")
        else:
            try:
                with open(client_path + 'patterns.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open(server_path + 'patterns.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)

            if input_pattern_name in data.keys():
                return html.Label("Шаблон с данным именем уже существует")
            else:
                pat = {'pivot_columns': pivot_columns, 'pivot_rows': pivot_rows, 'pivot_value': pivot_value, 'pivot_type': pivot_type, 'pivot_addition': pivot_addition,
                       'first_col_name': first_col_name, 'first_col_formula': first_col_formula, 'first_col_operation': first_col_operation,
                       'first_col_addit': first_col_addit, 'second_col_name': second_col_name, 'second_col_formula': second_col_formula,
                       'second_col_operation': second_col_operation, 'second_col_addit': second_col_addit, 'third_col_name': third_col_name,
                       'third_col_formula': third_col_formula, 'third_col_operation': third_col_operation, 'third_col_addit': third_col_addit,
                       'fourth_col_name': fourth_col_name, 'fourth_col_formula': fourth_col_formula, 'fourth_col_operation': fourth_col_operation,
                       'fourth_col_addit': fourth_col_addit, 'fifth_col_name': fifth_col_name, 'fifth_col_formula': fifth_col_formula, 'fifth_col_operation': fifth_col_operation,
                       'fifth_col_addit': fifth_col_addit, 'first_col_other': first_col_other, 'second_col_other': second_col_other, 'third_col_other': third_col_other,
                       'fourth_col_other': fourth_col_other, 'fifth_col_other': fifth_col_other}
                data[input_pattern_name] = pat
                try:
                    with open(client_path + 'patterns.json', 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False)
                except FileNotFoundError:
                    with open(server_path + 'patterns.json', 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False)

                #os.execl(sys.executable, sys.executable, *sys.argv)

                return html.Label('Сохранено')

@app.callback(
    Output('pattern-table', 'children'),
    [Input('pattern-group-product-dd', 'value'), Input('pattern-products-dd', 'value'), Input('pattern-cities-dd', 'value'), Input('pattern-segments-dd', 'value'),
     Input('pattern-clienttype-dd', 'value'), Input('pattern-otdels-dd', 'value'), Input('pattern-strategies-dd', 'value'), Input('pattern-cors-dd', 'value'),
     Input('pattern-challengers-dd', 'value'), Input('pattern-scorenames-dd', 'value'), Input('pattern-list-dd', 'value'), Input('pattern-date-picker', 'start_date'),
     Input('pattern-date-picker', 'end_date')]
)
def show_pattern(pattern_group_products, pattern_products, pattern_cities, pattern_segments, pattern_clientype, pattern_otdels, pattern_strategies,
                 pattern_cors, pattern_challengers, pattern_scorenames, pattern_list, start_date, end_date):
    try:
        with open(client_path + 'patterns.json', 'r', encoding='utf-8') as file:
            patterns = json.load(file)
    except FileNotFoundError:
        with open(server_path + 'patterns.json', 'r', encoding='utf-8') as file:
            patterns = json.load(file)

    df_ar2 = df_ar
    start_date = chg_str_to_date(start_date)
    end_date = chg_str_to_date(end_date)
    df_ar2 = df_ar2[(df_ar2.DREG >= start_date) & (df_ar2.DREG <= end_date)]
    if pattern_group_products:
        df_ar2 = df_ar2[df_ar2.GROUPOFPRODUCT.isin(pattern_group_products)]
    if pattern_products:
        df_ar2 = df_ar2[df_ar2.PRODUCT.isin(pattern_products)]
    if pattern_cities:
        df_ar2 = df_ar2[df_ar2.CITY.isin(pattern_cities)]
    if pattern_segments:
        df_ar2 = df_ar2[df_ar2.SEGMENT.isin(pattern_segments)]
    if pattern_clientype:
        df_ar2 = df_ar2[df_ar2.TYPEOFCLIENTS.isin(pattern_clientype)]
    if pattern_otdels:
        df_ar2 = df_ar2[df_ar2.LONGNAME.isin(pattern_otdels)]
    if pattern_strategies:
        df_ar2 = df_ar2[df_ar2.STRATEGY.isin(pattern_strategies)]
    if pattern_cors:
        df_ar2 = df_ar2[df_ar2.COR.isin(pattern_cors)]
    if pattern_challengers:
        df_ar2 = df_ar2[df_ar2.CHALLENGER.isin(pattern_challengers)]
    if pattern_scorenames:
        df_ar2 = df_ar2[df_ar2.SCORE_CARD_NAME.isin(pattern_scorenames)]

    params = patterns[pattern_list]
    pivot_columns = params['pivot_columns']
    pivot_rows = params['pivot_rows']
    pivot_value = params['pivot_value']
    pivot_type = params['pivot_type']
    pivot_addition = params['pivot_addition']
    first_col_name = params['first_col_name']
    first_col_formula = params['first_col_formula']
    first_col_operation = params['first_col_operation']
    first_col_addit = params['first_col_addit']
    second_col_name = params['second_col_name']
    second_col_formula = params['second_col_formula']
    second_col_operation = params['second_col_operation']
    second_col_addit = params['second_col_addit']
    third_col_name = params['third_col_name']
    third_col_formula = params['third_col_formula']
    third_col_operation = params['third_col_operation']
    third_col_addit = params['third_col_addit']
    fourth_col_name = params['fourth_col_name']
    fourth_col_formula = params['fourth_col_formula']
    fourth_col_operation = params['fourth_col_operation']
    fourth_col_addit = params['fourth_col_addit']
    fifth_col_name = params['fifth_col_name']
    fifth_col_formula = params['fifth_col_formula']
    fifth_col_operation = params['fifth_col_operation']
    fifth_col_addit = params['fifth_col_addit']
    first_col_other = params['first_col_other']
    second_col_other = params['second_col_other']
    third_col_other = params['third_col_other']
    fourth_col_other = params['fourth_col_other']
    fifth_col_other = params['fifth_col_other']

    isArbitrary = False
    if first_col_name or first_col_formula or second_col_name or second_col_formula or third_col_name or third_col_formula or fourth_col_name or fourth_col_formula or fifth_col_name or fifth_col_formula:
        isArbitrary = True
    if pivot_columns and pivot_rows and pivot_value and pivot_type and isArbitrary is False:
        if pivot_type == 'Сумма':
            agg = np.sum
        if pivot_type == 'Среднее':
            agg = np.mean
        if pivot_type == 'Медиана':
            agg = np.median
        if pivot_type == 'Максимум':
            agg = np.max
        if pivot_type == 'Минимум':
            agg = np.min

        return html.Div([
            dcc.Graph(
                figure=graphs.table_pivot(
                    tables.create_pivot(df_ar2, pivot_columns, pivot_rows, pivot_value, agg, pivot_addition))
            )
        ])
    if isArbitrary and pivot_rows:
        values = []
        if first_col_name and first_col_formula:
            values.append([first_col_name, first_col_formula, first_col_operation, first_col_addit, first_col_other])
        if second_col_name and second_col_formula:
            values.append([second_col_name, second_col_formula, second_col_operation, second_col_addit, second_col_other])
        if third_col_name and third_col_formula:
            values.append([third_col_name, third_col_formula, third_col_operation, third_col_addit, third_col_other])
        if fourth_col_name and fourth_col_formula:
            values.append([fourth_col_name, fourth_col_formula, fourth_col_operation, fourth_col_addit, fourth_col_other])
        if fifth_col_name and fifth_col_formula:
            values.append([fifth_col_name, first_col_formula, fifth_col_operation, fifth_col_addit, fifth_col_other])

        return html.Div([
            dcc.Graph(
                figure=graphs.table_pivot(tables.arbitrary_pivot(df_ar2, values, pivot_rows))
            )
        ])

@app.callback(
    Output('text_save_settings', 'children'), [Input('btn_save_settings', 'n_clicks')],
    [State('rri_table_name_input', 'value'), State('rri_amount_input', 'value'), State('rri_month_input', 'value'), State('rri_fpd0_hist_input', 'value'),
     State('rri_spd0_hist_input', 'value'), State('rri_tpd0_hist_input', 'value'), State('rri_fpd5_hist_input', 'value'), State('rri_spd5_hist_input', 'value'),
     State('rri_tpd5_hist_input', 'value'), State('rri_fpd15_hist_input', 'value'), State('rri_spd15_hist_input', 'value'), State('rri_tpd15_hist_input', 'value'),
     State('rri_fpd30_hist_input', 'value'), State('rri_spd30_hist_input', 'value'), State('rri_tpd30_hist_input', 'value'), State('rri_fpd45_hist_input', 'value'),
     State('rri_spd45_hist_input', 'value'), State('rri_tpd45_hist_input', 'value'), State('rri_fpd60_hist_input', 'value'), State('rri_spd60_hist_input', 'value'),
     State('rri_tpd60_hist_input', 'value'), State('rri_fpd90_hist_input', 'value'), State('rri_spd90_hist_input', 'value'), State('rri_tpd90_hist_input', 'value'),
     State('rri_fpd_active_input', 'value'), State('rri_spd_active_input', 'value'), State('rri_tpd_active_input', 'value'), State('ar_table_input', 'value'),
     State('ar_date_input', 'value'), State('ar_cancel_input', 'value'), State('ar_cnt_input', 'value'), State('ar_acc_input', 'value'),
     State('ar_acc2_input', 'value'), State('ar_loan_s_min_input', 'value'), State('ar_acc_amt_input', 'value'), State('ar_acc_loan_input', 'value'),
     State('ar_loan_amt_input', 'value'), State('ar_group_reject_input', 'value'), State('ar_group_alert_input', 'value'), State('ar_week_input', 'value'),
     State('v_table_name_input', 'value'), State('v_given_month_input', 'value'), State('v_report_month_input', 'value'), State('v_loan_sum_input', 'value'),
     State('v_debt_5_input', 'value'), State('v_debt_30_input', 'value'), State('v_debt_60_input', 'value'), State('v_debt_90_input', 'value'),
     State('v_age_input', 'value'), State('v_products_input', 'value'), State('v_programs_input', 'value'), State('v_city_input', 'value'),
     State('v_segment_input', 'value'), State('main_user_input', 'value'), State('main_password_input', 'value'), State('main_host_input', 'value'),
     State('main_service_input', 'value'), State('main_port_input', 'value')]
)
def save_settings(n_clicks, rri_table_name, rri_amount, rri_month, fpd0_hist, spd0_hist, tpd0_hist, fpd5_hist, spd5_hist, tpd5_hist,
                  fpd15_hist, spd15_hist, tpd15_hist, fpd30_hist, spd30_hist, tpd30_hist, fpd45_hist, spd45_hist, tpd45_hist,
                  fpd60_hist, spd60_hist, tpd60_hist, fpd90_hist, spd90_hist, tpd90_hist, fpd_active, spd_active, tpd_active, ar_table,
                  ar_date, ar_cancel, ar_cnt, ar_acc, ar_acc2, ar_loan_s_min, ar_acc_amt, ar_acc_loan, ar_loan_amt, ar_group_reject,
                  ar_group_alert, ar_week, v_table_name, v_given_month, v_report_month, v_loan_sum, v_debt_5, v_debt_30, v_debt_60,
                  v_debt_90, v_age, v_products, v_programs, v_city, v_segment, main_user, main_password, main_host, main_service,
                  main_port):

    if n_clicks > 0:
        with open('/home/user/PycharmProjects/retail_risk/settings.json', 'r') as file:
            settings = json.load(file)

        settings['rri_table_name'] = rri_table_name
        settings['rri_amount'] = rri_amount
        settings['rri_month'] = rri_month
        settings['rri_fpd_0'] = fpd0_hist
        settings['rri_spd_0'] = spd0_hist
        settings['rri_tpd_0'] = tpd0_hist
        settings['rri_fpd_5'] = fpd5_hist
        settings['rri_spd_5'] = spd5_hist
        settings['rri_tpd_5'] = tpd5_hist
        settings['rri_fpd_15'] = fpd15_hist
        settings['rri_spd_15'] = spd15_hist
        settings['rri_tpd_15'] = tpd15_hist
        settings['rri_fpd_30'] = fpd30_hist
        settings['rri_spd_30'] = spd30_hist
        settings['rri_tpd_30'] = tpd30_hist
        settings['rri_fpd_45'] = fpd45_hist
        settings['rri_spd_45'] = spd45_hist
        settings['rri_tpd_45'] = tpd45_hist
        settings['rri_fpd_60'] = fpd60_hist
        settings['rri_spd_60'] = spd60_hist
        settings['rri_tpd_60'] = tpd60_hist
        settings['rri_fpd_90'] = fpd90_hist
        settings['rri_spd_90'] = spd90_hist
        settings['rri_tpd_90'] = tpd90_hist
        settings['rri_fpd_active'] = fpd_active
        settings['rri_spd_active'] = spd_active
        settings['rri_tpd_active'] = tpd_active
        settings['ar_table_name'] = ar_table
        settings['ar_date'] = ar_date
        settings['ar_cancel'] = ar_cancel
        settings['ar_cnt'] = ar_cnt
        settings['ar_acc'] = ar_acc
        settings['ar_acc2'] = ar_acc2
        settings['ar_loan_s_min'] = ar_loan_s_min
        settings['ar_acc_amt'] = ar_acc_amt
        settings['ar_acc_loan'] = ar_acc_loan
        settings['ar_loan_amt'] = ar_loan_amt
        settings['ar_groupofreject'] = ar_group_reject
        settings['ar_groupofalerts'] = ar_group_alert
        settings['ar_week'] = ar_week
        settings['v_table_name'] = v_table_name
        settings['v_given_month'] = v_given_month
        settings['v_report_month'] = v_report_month
        settings['v_loan_sum'] = v_loan_sum
        settings['v_debt_5'] = v_debt_5
        settings['v_debt_30']  = v_debt_30
        settings['v_debt_60'] = v_debt_60
        settings['v_debt_90'] = v_debt_90
        settings['v_age'] = v_age
        settings['v_products'] = v_products
        settings['v_program'] = v_programs
        settings['v_city'] = v_city
        settings['v_segment'] = v_segment
        settings['user'] = main_user
        settings['password'] = main_password
        settings['host'] = main_host
        settings['port'] = main_port
        settings['db'] = main_service

        try:
            with open(client_path + 'settings.json', 'w') as file:
                json.dump(settings, file)
        except FileNotFoundError:
            with open(server_path + 'settings.json', 'w') as file:
                json.dump(settings, file)

        #os.execl(sys.executable, sys.executable, *sys.argv)

    return html.Label('')

@app.callback(
    Output('text_restart_system', 'children'),
    [Input('btn_restart_system', 'n_clicks')]
)
def restart_system(n_clicks):
    if n_clicks > 0:
        os.system("sudo -S systemctl restart apache2")

        return html.Label('')

if __name__ == '__main__':
    app.run_server(debug=True)