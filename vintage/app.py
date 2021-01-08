import pandas as pd
from sqlalchemy import create_engine
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import datetime
import vintage.table as table
import vintage.graph as graph
from server import server

con = create_engine("oracle+cx_oracle://MOLDAADI:b52$rtpu4@10.15.28.28:1521/?service_name=edwprod")
df = pd.read_sql("select * from RSK_BCC.DRI_FINAL_VINTAGE where given_month >= to_date('01.01.2019', 'dd.mm.yyyy')", con=con)
df.columns = [col.upper() for col in df.columns]
df.GIVEN_MONTH = df.GIVEN_MONTH.apply(lambda x: datetime.date(x.year, x.month, x.day))
df.REPORT_MONTH = df.REPORT_MONTH.apply(lambda x: datetime.date(x.year, x.month, x.day))

products = df.PRODUCT.unique()
products.sort()

product_names = df.PRODUCT_NAME.unique()
product_names.sort()

overdue_types = ['Просрочка 5+', 'Просрочка 30+', 'Просрочка 60+', 'Просрочка 90+']

app = dash.Dash(__name__, server=server, title='Винтаж', url_base_pathname='/vintage/')

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H4('Выберите продукт', style={'font-family': 'arial'})
        ]),
        html.Div([
            dcc.Dropdown(
                id='products_dropdown',
                value=products,
                options=[{'label': product, 'value': product} for product in products],
                multi=True,
                style={'width': '600px', 'fontSize': '14px', 'font-family': 'arial'}
            )
        ])
    ], style={'marginLeft': '100px', 'marginTop': '20px'}),
    html.Div([
        html.Div([
            html.H4('Выберите наименование продукта', style={'font-family': 'arial'})
        ]),
        html.Div([
            dcc.Dropdown(
                id='product_names_dropdown',
                value=product_names,
                options=[{'label': product_name, 'value': product_name} for product_name in product_names],
                multi=True,
                style={'width': '600px', 'fontSize': '14px', 'font-family': 'arial', 'height': '200px', 'display': 'inline-block', 'overflowY': 'scroll'}
            )
        ])
    ], style={'marginLeft': '100px', 'marginTop': '60px'}),
    html.Div([
        html.Div([
            html.H4('Выберите тип просрочки', style={'font-family': 'arial'})
        ]),
        html.Div([
            dcc.Dropdown(
                id='overdue_type_dropdown',
                value=overdue_types[0],
                multi=False,
                clearable=False,
                options=[{'label': overdue_type, 'value': overdue_type} for overdue_type in overdue_types],
                style={'width': '600px', 'fontSize': '14px', 'font-family': 'arial'}
            )
        ])
    ], style={'marginLeft': '100px', 'marginTop': '60px'}),
    html.Div([
        html.Div([
            dcc.Graph(
                id='vintage_table'
            )
        ])
    ]),
    html.Div([
        html.Div([
            dcc.Graph(
                id='vintage_graph'
            )
        ])
    ])
])

@app.callback(
    [Output('product_names_dropdown', 'value'), Output('product_names_dropdown', 'options')],
    [Input('products_dropdown', 'value')]
)
def update_product_names_list(products):
    df2 = df
    if products:
        df2 = df2[df2.PRODUCT.isin(products)]
    product_names = df2.PRODUCT_NAME.unique()
    product_names.sort()

    return product_names, [{'label': product_name, 'value': product_name} for product_name in product_names]

@app.callback(
    [Output('vintage_table', 'figure'), Output('vintage_graph', 'figure')],
    [Input('products_dropdown', 'value'), Input('product_names_dropdown', 'value'), Input('overdue_type_dropdown', 'value')]
)
def update_vintage_table(products, product_names, overdue_type):
    df2 = df
    if products:
        df2 = df2[df2.PRODUCT.isin(products)]
    if product_names:
        df2 = df2[df2.PRODUCT_NAME.isin(product_names)]

    if overdue_type == 'Просрочка 5+':
        return graph.table_vintage(table.vintage_5_plus(df2)), graph.graph_vintage(table.vintage_5_plus(df2))
    if overdue_type == 'Просрочка 30+':
        return graph.table_vintage(table.vintage_30_plus(df2)), graph.graph_vintage(table.vintage_30_plus(df2))
    if overdue_type == 'Просрочка 60+':
        return graph.table_vintage(table.vintage_60_plus(df2)), graph.graph_vintage(table.vintage_60_plus(df2))
    if overdue_type == 'Просрочка 90+':
        return graph.table_vintage(table.vintage_90_plus(df2)), graph.graph_vintage(table.vintage_90_plus(df2))

if __name__ == '__main__':
    app.run_server(debug=True)