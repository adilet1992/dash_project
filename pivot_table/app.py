import pandas as pd
from sqlalchemy import create_engine
import dash
import dash_html_components as html
import dash_pivottable
import datetime
import dash_core_components as dcc
from dash.dependencies import Input, Output
import random
from server import server

con = create_engine("oracle+cx_oracle://MOLDAADI:b52$rtpu4@10.15.28.28:1521/?service_name=edwprod")
df = pd.read_sql("SELECT * FROM RSK_BCC.DR_LREQDEA_AR WHERE DREG >= TO_DATE('01.01.2020', 'DD.MM.YYYY')", con=con)
df = df[['dreg', 'week', 'segment', 'typeofclients', 'product', 'groupofproduct', 'longname', 'city', 'groupofalerts', 'groupofreject', 'strategy', 'score_card_name', 'cor', 'challenger', 'cnt', 'acc', 'acc_loan', 'cancel', 'loan_s_min', 'loan_amt', 'acc_amt', 'acc2']]
df.columns = [x.upper() for x in df.columns]
df.DREG = df.DREG.apply(lambda x: datetime.date(x.year, x.month, x.day))
df.WEEK = df.WEEK.apply(lambda x: datetime.date(x.year, x.month, x.day))
df['REVIEW'] = df.CNT - df.CANCEL

data = [df.columns.tolist()] + df.values.tolist()

app = dash.Dash(__name__, server=server, title='Сводные таблицы', url_base_pathname='/pivots/')

app.layout = html.Div([
    html.Div([
        html.H4('Выберите период', style={'font-family': 'arial'})
    ], style={'marginLeft': '30px'}),
    html.Div([
        dcc.DatePickerRange(
            id='date_picker',
            start_date=df.DREG.max() - datetime.timedelta(days=30),
            end_date=df.DREG.max(),
            min_date_allowed=df.DREG.min(),
            max_date_allowed=df.DREG.max() + datetime.timedelta(days=1),
            display_format='DD.MM.YYYY',
            style={'font-family': 'arial'}
        )
    ], style={'marginLeft': '30px', 'marginTop': '10px', 'marginBottom': '10px'}),
    dcc.Loading(
        id='loading',
        type='circle',
        children=[
            html.Div([

            ], style={'marginLeft': '30px'}, id='pivot-div')
        ]
    )
])

@app.callback(
    Output('pivot-div', 'children'), [Input('date_picker', 'start_date'), Input('date_picker', 'end_date')]
)
def update_data(start_date, end_date):
    start_date = datetime.date(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    end_date = datetime.date(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2]))
    df2 = df[(df.DREG >= start_date) & (df.DREG <= end_date)]
    data2 = [df2.columns.tolist()] + df2.values.tolist()
    idd = str(random.randint(10000, 99999))
    layout = [
        dash_pivottable.PivotTable(
            id=idd,
            data=data2,
            cols=['SEGMENT'],
            rows=['TYPEOFCLIENTS'],
            vals=['CNT']
        )]

    return layout


if __name__ == '__main__':
    app.run_server(debug=True)