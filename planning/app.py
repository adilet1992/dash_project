import pandas as pd
from sqlalchemy import create_engine
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import planning.table as table
import planning.graph as graph
from server import server

def vintage_product2(x):
    autos = ['Авто в производстве через автосалон', 'Авто кредитование', 'Автокредитование', 'Автокредитование через Астана Моторс  к 30 летию Банка',
             'Автосалон для партнеров Банка', 'Автосалон для партнеров Банка (для удаленки)', 'Автосалон для сотрудников Банка',
             'Автосалоны Астана Моторс', 'Автосалоны Астана Моторс (для удаленки)', 'Автосалоны льготное автокредитование',
             'Автотранспорт с пробегом через автосалоны', 'Льготное автокредитование отечественного производства',
             'Льготное кредитование автотранспорта отечественного производства', 'Льготное кредитование отечественного производства (для удаленки)',
             'Льготное кредитование через Автосалоны при оплате расходов по займу за счет кредита']
    goods = ['Товарный кредит', 'Товарный кредит BI']
    cashes = ['Кредит наличными', 'Рефинансирование беззалоговых займов с добором']
    mortgages = ['Ипотека "7-20-25"', 'Ипотека "7-20-25" (РД)', 'Ипотека "7-20-25" Скоринг', 'Ипотека "Баспана-Хит"', 'Ипотека "Баспана-Хит" РД']

    res = "Другие"
    if x in autos:
        res = 'Автокредитование'
    elif x in goods:
        res = 'Товарный кредит'
    elif x in cashes:
        res = 'Кредит наличными'
    elif x in mortgages:
        res = 'Ипотека'

    return res

def eri_products(x):
    autos = ['Автокредитование']
    goods = ['Товарный кредит']
    cashes = ['Беззалоговые займы под зарплату', 'Рефинансирование беззалоговых займов с добором ФЛ']
    mortgages = ['Баспана-Хит', 'Ипотека 7-20-25']

    res = 'Другие'
    if x in autos:
        res = 'Автокредитование'
    elif x in goods:
        res = 'Товарный кредит'
    elif x in cashes:
        res = 'Кредит наличными'
    elif x in mortgages:
        res = 'Ипотека'

    return res

con = create_engine("oracle+cx_oracle://MOLDAADI:b52$rtpu4@10.15.28.28:1521/?service_name=edwprod")

df_ar = pd.read_sql("SELECT * FROM RSK_BCC.DR_LREQDEA_AR WHERE DREG >= TO_DATE('01.08.2020', 'DD.MM.YYYY')", con=con)
df_ar.columns =[col.upper() for col in df_ar.columns]
df_ar.DREG = df_ar.DREG.apply(lambda x: datetime.date(x.year, x.month, x.day))
df_ar.WEEK = df_ar.WEEK.apply(lambda x: datetime.date(x.year, x.month, x.day))
df_ar = df_ar[['WEEK', 'CNT', 'CANCEL', 'ACC', 'ACC2', 'ACC_LOAN', 'PRODUCT2']]
for i in range(len(df_ar)):
    if df_ar['CANCEL'].iloc[i] == 1 and df_ar['ACC'].iloc[i] == 1:
        df_ar.at[i, 'CANCEL'] = 0

dfv = pd.read_sql("SELECT * FROM RSK_BCC.DRI_FINAL_VINTAGE WHERE GIVEN_MONTH >= TO_DATE('01.01.2019', 'DD.MM.YYYY')", con=con)
dfv.columns = [col.upper() for col in dfv.columns]
dfv.GIVEN_MONTH = dfv.GIVEN_MONTH.apply(lambda x: datetime.date(x.year, x.month, x.day))
dfv['PRODUCT2'] = dfv.PRODUCT_NAME.apply(lambda x: vintage_product2(x))
dfv = dfv[dfv.PRODUCT2 != 'Другие']

df_eri = pd.read_sql("SELECT * FROM RSK_BCC.DRI_ALL_CTR_ERI_HIST WHERE MONTH_SIGN_CTR >= TO_DATE('01.01.2019', 'DD.MM.YYYY')", con=con)
df_eri.columns = [col.upper() for col in df_eri.columns]
df_eri.MONTH_SIGN_CTR = df_eri.MONTH_SIGN_CTR.apply(lambda x: datetime.date(x.year, x.month, x.day))
df_eri['PRODUCT2'] = df_eri.PRODUCT.apply(lambda x: eri_products(x))
df_eri = df_eri[df_eri.PRODUCT2 != 'Другие']

df_del = pd.read_sql("SELECT * FROM RSK_BCC.T_CONTRACT_DEL WHERE CTRC_BGIN_YMD >= '20190101'", con=con)
df_del.columns = [x.upper() for x in df_del.columns]
df_del.CTRC_BGIN_YMD = df_del.CTRC_BGIN_YMD.apply(lambda x: datetime.date(int(x[:4]), int(x[4:6]), int(x[6:])))
df_del['MONTH_SIGN_CTR'] = df_del.CTRC_BGIN_YMD.apply(lambda x: datetime.date(x.year, x.month, 1))
df_del['FLAG_30_MOB'] = df_del.OVRDU_DPD_ACT.apply(lambda x: 1 if x > 30 else 0)
df_del['FLAG_60_MOB'] = df_del.OVRDU_DPD_ACT.apply(lambda x: 1 if x > 60 else 0)
df_del['FLAG_90_MOB'] = df_del.OVRDU_DPD_ACT.apply(lambda x: 1 if x > 90 else 0)
df_del['PRODUCT2'] = df_del.PROGRAMM.apply(lambda x: vintage_product2(x))
df_del = df_del[df_del.PRODUCT2 != 'Другие']

products = ['Товарный кредит', 'Автокредитование', 'Кредит наличными', 'Ипотека']
overdues = ['Просрочка 5+', 'Просрочка 30+', 'Просрочка 60+', 'Просрочка 90+']

df_ar = df_ar[df_ar.PRODUCT2.isin(products)]
weeks = list(df_ar.WEEK.unique())
weeks.sort()
last_weeks = weeks[len(weeks)-8:]
df_ar = df_ar[df_ar.WEEK.isin(last_weeks)]

app = dash.Dash(__name__, server=server, title='Планерка', url_base_pathname='/planning/')

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3('Продукты', style={'font-family': 'verdana'})
        ]),
        html.Div([
            dcc.Dropdown(
                multi=False,
                id='products-dropdown',
                clearable=False,
                value=products[0],
                options=[{'label': product, 'value': product} for product in products],
                style={'font-family': 'verdana', 'width': '400px'}
            )
        ])
    ], style={'marginLeft': '100px', 'marginTop': '100px', 'marginBottom': '50px'}),
    html.Div([
        html.Div([
            html.H1('Уровень одобрения', style={'font-family': 'verdana'})
        ], style={'textAlign': 'center'}, id='ar_header'),
        html.Div([
            dcc.Graph(
                id='ar-table'
            )
        ], style={'marginLeft': '350px'})
    ]),
    html.Div([
        html.Div([
            html.H1('Ранние риск-индикаторы', style={'font-family': 'verdana'})
        ], style={'textAlign': 'center'}, id='eri_header'),
        html.Div([
            dcc.Graph(
                id='eri-table'
            )
        ], style={'marginLeft': '350px'})
    ]),
    html.Div([
        html.Div([
            html.H1('Винтаж', style={'font-family': 'verdana'}),
        ], style={'textAlign': 'center'}, id='vintage_header'),
        html.Div([
            dcc.Dropdown(
                id='overdue-dropdown',
                multi=False,
                clearable=False,
                value=overdues[0],
                options=[{'label': overdue, 'value': overdue} for overdue in overdues],
                style={'font-family': 'verdana', 'width': '400px'}
            )
        ], style={'marginLeft': '100px', 'marginTop': '50px'}),
        html.Div([
            dcc.Graph(
                id='vintage-table'
            )
        ])
    ])
])

@app.callback(
    Output('ar-table', 'figure'), [Input('products-dropdown', 'value')]
)
def update_ar_table(product):
    return graph.plot_ar_table(table.create_ar_table(df_ar, product))

@app.callback(
    Output('eri-table', 'figure'), [Input('products-dropdown', 'value')]
)
def update_eri_table(product):
    df_eri2 = df_eri[df_eri.PRODUCT2 == product]
    df_del2 = df_del[df_del.PRODUCT2 == product]
    return graph.plot_eri_table(table.create_eri_table(df_eri2, df_del2))

@app.callback(
    Output('vintage-table', 'figure'), [Input('products-dropdown', 'value'), Input('overdue-dropdown', 'value')]
)
def update_vintage_table(product, overdue_type):
    dfv2 = dfv[dfv.PRODUCT2 == product]
    if overdue_type == 'Просрочка 5+':
        return graph.plot_vintage_table(table.vintage_5_plus(dfv2))
    if overdue_type == 'Просрочка 30+':
        return graph.plot_vintage_table(table.vintage_30_plus(dfv2))
    if overdue_type == 'Просрочка 60+':
        return graph.plot_vintage_table(table.vintage_60_plus(dfv2))
    if overdue_type == 'Просрочка 90+':
        return graph.plot_vintage_table(table.vintage_90_plus(dfv2))

@app.callback(
    Output('ar_header', 'children'), [Input('products-dropdown', 'value')]
)
def update_ar_header(product):
    return html.H1('Уровень одобрения по продукту "' + product + '"', style={'font-family': 'verdana'})

@app.callback(
    Output('eri_header', 'children'), [Input('products-dropdown', 'value')]
)
def update_eri_header(product):
    return html.H1('Ранние риск-индикаторы по продукту "' + product + '"', style={'font-family': 'verdana'})

@app.callback(
    Output('vintage_header', 'children'), [Input('overdue-dropdown', 'value'), Input('products-dropdown', 'value')]
)
def update_vintage_header(overdue_type, product):
    if overdue_type == 'Просрочка 5+':
        text = 'просрочек 5+'
    if overdue_type == 'Просрочка 30+':
        text = 'просрочек 30+'
    if overdue_type == 'Просрочка 60+':
        text = 'просрочек 60+'
    if overdue_type == 'Просрочка 90+':
        text = 'просрочек 90+'

    return html.H1('Винтаж ' + text + ' по продукту "' + product + '"', style={'font-family': 'verdana'})

if __name__ == '__main__':
    app.run_server(debug=True)