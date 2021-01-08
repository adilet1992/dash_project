import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from server import server

df_kol = pd.read_csv('/home/user/Downloads/data.csv')

df_kol['BRAND'] = df_kol.header.apply(lambda x: x.split(';')[0] if type(x) == str else '')
df_kol['MODEL'] = df_kol.header.apply(lambda x: x.split(';')[1] if type(x) == str else '')
df_kol['YEAR'] = df_kol.header.apply(lambda x: x.split(';')[2] if type(x) == str else '')
df_kol['VOLUME'] = df_kol.volume.apply(lambda x: x.strip() if type(x) == str else '')
df_kol['PRICE'] = df_kol.price.apply(lambda x: x.strip() if type(x) == str else '')
df_kol['COLOR'] = df_kol.color.apply(lambda x: x.strip() if type(x) == str else '')
df_kol['PROBEG'] = df_kol.probeg.apply(lambda x: x.strip() if type(x) == str else '')
df_kol['PROBEG_INT'] = df_kol.PROBEG.apply(lambda x: x.split('км')[0] if x != '' else x)
df_kol['PROBEG_MAIN'] = df_kol.PROBEG_INT.apply(lambda x: int("".join(c for c in x.split())) if x != '' else np.nan)
df_kol['PRICE_INT'] = df_kol.PRICE.apply(lambda x: int("".join(c for c in x.split())) if x != '' else np.nan)
df_kol['RESOURCE'] = df_kol.VOLUME.apply(lambda x: x.split()[1] if x != '' else x)
df_kol['VOLUME_INT'] = df_kol.VOLUME.apply(lambda x: float(x.split()[0]) if x != '' else np.nan)
df_kol['RESOURCE'] = df_kol.RESOURCE.apply(lambda x: x.strip('(').strip(')'))
df_kol = df_kol[~df_kol.YEAR.str.contains('года')]
df_kol['YEAR'] = df_kol.YEAR.apply(lambda x: int(x.strip()) if x != '' else np.nan)

df_kol.columns = [x.upper() for x in df_kol.columns]
df_kol2 = df_kol[['URL', 'BRAND', 'MODEL', 'YEAR', 'VOLUME_INT', 'PRICE_INT', 'PROBEG_MAIN', 'RESOURCE', 'PRIVOD', 'KUZOV', 'RASST', 'KOROBKA', 'RULE']]
df_kol2 = df_kol2[df_kol2.BRAND.notnull()]
df_kol2 = df_kol2[df_kol2.MODEL.notnull()]
df_kol2 = df_kol2[df_kol2.YEAR.notnull()]
df_kol2 = df_kol2[df_kol2.VOLUME_INT.notnull()]
df_kol2 = df_kol2[df_kol2.PRICE_INT.notnull()]
df_kol2 = df_kol2[df_kol2.RESOURCE.notnull()]
df_kol2 = df_kol2[df_kol2.PRIVOD.notnull()]
df_kol2 = df_kol2[df_kol2.KUZOV.notnull()]
df_kol2 = df_kol2[df_kol2.KOROBKA.notnull()]
df_kol2 = df_kol2[df_kol2.RULE.notnull()]
df_kol2 = df_kol2[df_kol2.RASST.notnull()]

brands = df_kol2.BRAND.unique()
brands.sort()

models = df_kol2.MODEL.unique()
models.sort()

years = df_kol2.YEAR.unique()
years.sort()

volumes = df_kol2.VOLUME_INT.unique()
volumes.sort()

resources = df_kol2.RESOURCE.unique()
resources.sort()

kuzov = df_kol2.KUZOV.unique()
kuzov.sort()

privod = df_kol2.PRIVOD.unique()
privod.sort()

rasst = df_kol2.RASST.unique()
rasst.sort()

korobki = df_kol2.KOROBKA.unique()
korobki.sort()

rule = df_kol2.RULE.unique()
rule.sort()

app = dash.Dash(__name__, title='Цены kolesa.kz', server=server, url_base_pathname='/kolesa_kz/')

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.H4('Выберите марку', style={'font-family': 'arial'})
            ]),
            html.Div([
                dcc.Dropdown(
                    id='brands-dropdown',
                    multi=False,
                    clearable=False,
                    value=brands[0],
                    options=[{'label': brand, 'value': brand} for brand in brands],
                    style={'width': '300px', 'font-family': 'arial', 'fontSize': '14px'}
                )
            ])
        ], style={'marginTop': '30px', 'marginLeft': '350px'}),
        html.Div([
            html.Div([
                html.H4('Выберите модель', style={'font-family': 'arial'})
            ]),
            html.Div([
                dcc.Dropdown(
                    id='models-dropdown',
                    multi=False,
                    clearable=False,
                    value=models[0],
                    options=[{'label': model, 'value': model} for model in models],
                    style={'width': '300px', 'font-family': 'arial', 'fontSize': '14px'}
                )
            ])
        ], style={'marginTop': '30px', 'marginLeft': '350px'}),
        html.Div([
            html.Div([
                html.H4('Год производства', style={'font-family': 'arial'})
            ]),
            html.Div([
                dcc.Dropdown(
                    id='years-dropdown',
                    multi=False,
                    clearable=False,
                    value=str(years[0]),
                    options=[{'label': str(int(year)), 'value': str(int(year))} for year in years],
                    style={'width': '300px', 'font-family': 'arial', 'fontSize': '14px'}
                )
            ])
        ], style={'marginTop': '30px', 'marginLeft': '350px'}),
        html.Div([
            html.Div([
                html.H4('Объем автомобиля', style={'font-family': 'arial'})
            ]),
            html.Div([
                dcc.Dropdown(
                    id='volumes-dropdown',
                    multi=False,
                    clearable=False,
                    value=str(volumes[0]) if volumes is not None else None,
                    options=[{'label': str(volume), 'value': str(volume)} for volume in volumes] if volumes is not None else None,
                    style={'width': '300px', 'font-family': 'arial', 'fontSize': '14px'}
                )
            ])
        ], style={'marginTop': '30px', 'marginLeft': '350px'}),
        html.Div([
            html.Div([
                html.H4('Тип топлива', style={'font-family': 'arial'})
            ]),
            html.Div([
                dcc.Dropdown(
                    id='resources-dropdown',
                    multi=False,
                    clearable=False,
                    value=resources[0],
                    options=[{'label': resource, 'value': resource} for resource in resources],
                    style={'width': '300px', 'font-family': 'arial', 'fontSize': '14px'}
                )
            ])
        ], style={'marginTop': '30px', 'marginLeft': '350px'})
    ], style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        html.Div([
            html.Div([
                html.H4('Тип кузова', style={'font-family': 'arial'})
            ]),
            html.Div([
                dcc.Dropdown(
                    id='kuzovs-dropdown',
                    multi=False,
                    clearable=False,
                    value=kuzov[0],
                    options=[{'label': kuz, 'value': kuz} for kuz in kuzov],
                    style={'width': '300px', 'font-family': 'arial', 'fontSize': '14px'}
                )
            ])
        ], style={'marginTop': '30px', 'marginLeft': '150px'}),
        html.Div([
            html.Div([
                html.H4('Тип привода', style={'font-family': 'arial'})
            ]),
            html.Div([
                dcc.Dropdown(
                    id='privods-dropdown',
                    multi=False,
                    clearable=False,
                    value=privod[0],
                    options=[{'label': priv, 'value': priv} for priv in privod],
                    style={'width': '300px', 'font-family': 'arial', 'fontSize': '14px'}
                )
            ])
        ], style={'marginTop': '30px', 'marginLeft': '150px'}),
        html.Div([
            html.Div([
                html.H4('Тип коробки', style={'font-family': 'arial'})
            ]),
            html.Div([
                dcc.Dropdown(
                    id='korobki-dropdown',
                    multi=False,
                    clearable=False,
                    value=korobki[0],
                    options=[{'label': korob, 'value': korob} for korob in korobki],
                    style={'width': '300px', 'font-family': 'arial', 'fontSize': '14px'}
                )
            ])
        ], style={'marginTop': '30px', 'marginLeft': '150px'}),
        html.Div([
            html.Div([
                html.H4('Расположение руля', style={'font-family': 'arial'})
            ]),
            html.Div([
                dcc.Dropdown(
                    id='rules-dropdown',
                    multi=False,
                    clearable=False,
                    value=rule[0],
                    options=[{'label': rul, 'value': rul} for rul in rule],
                    style={'width': '300px', 'font-family': 'arial', 'fontSize': '14px'}
                )
            ])
        ], style={'marginTop': '30px', 'marginLeft': '150px'}),
        html.Div([
            html.Div([
                html.H4('Расстаможен в Казахстане', style={'font-family': 'arial'})
            ]),
            html.Div([
                dcc.Dropdown(
                    id='rasst-dropdown',
                    multi=False,
                    clearable=False,
                    value=rasst[0],
                    options=[{'label': rass, 'value': rass} for rass in rasst],
                    style={'width': '300px', 'font-family': 'arial', 'fontSize': '14px'}
                )
            ])
        ], style={'marginTop': '30px', 'marginLeft': '150px'})
    ], style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        html.Div([

        ], id='price_label', style={'textAlign': 'center', 'marginTop': '50px'}),
        html.Div([
            html.H4('Схожие объявления')
        ], style={'marginLeft': '80px', 'marginTop': '30px', 'font-family': 'arial'}),
        html.Div([

        ], id='links', style={'marginLeft': '80px', 'marginTop': '30px'})
    ], )
])

@app.callback(
    [Output('models-dropdown', 'value'), Output('models-dropdown', 'options')], [Input('brands-dropdown', 'value')]
)
def update_brands(brand):
    models = df_kol2[df_kol2.BRAND == brand].MODEL.unique()
    models.sort()
    return models[0], [{'label': model, 'value': model} for model in models]

@app.callback(
    [Output('years-dropdown', 'value'), Output('years-dropdown', 'options')], [Input('brands-dropdown', 'value'), Input('models-dropdown', 'value')]
)
def update_years(brand, model):
    years = df_kol2[(df_kol2.BRAND == brand) & (df_kol2.MODEL == model)].YEAR.unique()
    years.sort()
    return str(int(years[0])), [{'label': str(int(year)), 'value': str(int(year))} for year in years]

@app.callback(
    [Output('volumes-dropdown', 'value'), Output('volumes-dropdown', 'options')],
    [Input('brands-dropdown', 'value'), Input('models-dropdown', 'value'), Input('years-dropdown', 'value')]
)
def update_volumes(brand, model, year):
    volumes = df_kol2[(df_kol2.BRAND == brand) & (df_kol2.MODEL == model) & (df_kol2.YEAR == int(year))].VOLUME_INT.unique()
    if volumes is not None:
        volumes.sort()
        return str(volumes[0]), [{'label': str(volume), 'value': str(volume)} for volume in volumes]
    return None, None

@app.callback(
    [Output('resources-dropdown', 'value'), Output('resources-dropdown', 'options')],
    [Input('brands-dropdown', 'value'), Input('models-dropdown', 'value'), Input('years-dropdown', 'value'), Input('volumes-dropdown', 'value')]
)
def update_resources(brand, model, year, volume):
    resources = df_kol2[(df_kol2.BRAND == brand) & (df_kol2.MODEL == model) & (df_kol2.YEAR == int(year)) & (df_kol2.VOLUME_INT == float(volume))].RESOURCE.unique()
    resources.sort()
    return resources[0], [{'label': resource, 'value': resource} for resource in resources]

@app.callback(
    [Output('kuzovs-dropdown', 'value'), Output('kuzovs-dropdown', 'options')],
    [Input('brands-dropdown', 'value'), Input('models-dropdown', 'value'), Input('years-dropdown', 'value'), Input('volumes-dropdown', 'value'),
     Input('resources-dropdown', 'value')]
)
def update_kuzov(brand, model, year, volume, resource):
    kuzov = df_kol2[(df_kol2.BRAND == brand) & (df_kol2.MODEL == model) & (df_kol2.YEAR == int(year)) & (df_kol2.VOLUME_INT == float(volume)) & (df_kol2.RESOURCE == resource)].KUZOV.unique()
    kuzov.sort()
    return kuzov[0], [{'label': kuz, 'value': kuz} for kuz in kuzov]

@app.callback(
    [Output('privods-dropdown', 'value'), Output('privods-dropdown', 'options')],
    [Input('brands-dropdown', 'value'), Input('models-dropdown', 'value'), Input('years-dropdown', 'value'), Input('volumes-dropdown', 'value'),
     Input('resources-dropdown', 'value'), Input('kuzovs-dropdown', 'value')]
)
def update_privods(brand, model, year, volume, resource, kuzov):
    temp = df_kol2[(df_kol2.BRAND == brand) & (df_kol2.MODEL == model) & (df_kol2.YEAR == int(year)) & (df_kol2.VOLUME_INT == float(volume)) & (df_kol2.RESOURCE == resource)]
    temp = temp[temp.KUZOV == kuzov]
    privods = temp.PRIVOD.unique()
    privods.sort()

    return privods[0], [{'label': privod, 'value': privod} for privod in privods]

@app.callback(
    [Output('korobki-dropdown', 'value'), Output('korobki-dropdown', 'options')],
    [Input('brands-dropdown', 'value'), Input('models-dropdown', 'value'), Input('years-dropdown', 'value'), Input('volumes-dropdown', 'value'),
     Input('resources-dropdown', 'value'), Input('kuzovs-dropdown', 'value'), Input('privods-dropdown', 'value')]
)
def update_korobki(brand, model, year, volume, resource, kuzov, privod):
    temp = df_kol2[(df_kol2.BRAND == brand) & (df_kol2.MODEL == model) & (df_kol2.YEAR == int(year)) & (df_kol2.VOLUME_INT == float(volume)) & (df_kol2.RESOURCE == resource)]
    temp = temp[(temp.KUZOV == kuzov) & (temp.PRIVOD == privod)]
    korobki = temp.KOROBKA.unique()
    korobki.sort()

    return korobki[0], [{'label': korob, 'value': korob} for korob in korobki]

@app.callback(
    [Output('rules-dropdown', 'value'), Output('rules-dropdown', 'options')],
    [Input('brands-dropdown', 'value'), Input('models-dropdown', 'value'), Input('years-dropdown', 'value'), Input('volumes-dropdown', 'value'),
     Input('resources-dropdown', 'value'), Input('kuzovs-dropdown', 'value'), Input('privods-dropdown', 'value'), Input('korobki-dropdown', 'value')]
)
def update_rules(brand, model, year, volume, resource, kuzov, privod, korobki):
    temp = df_kol2[(df_kol2.BRAND == brand) & (df_kol2.MODEL == model) & (df_kol2.YEAR == int(year)) & (df_kol2.VOLUME_INT == float(volume)) & (df_kol2.RESOURCE == resource)]
    temp = temp[(temp.KUZOV == kuzov) & (temp.PRIVOD == privod) & (temp.KOROBKA == korobki)]
    rules = temp.RULE.unique()
    rules.sort()

    return rules[0], [{'label': rule, 'value': rule} for rule in rules]

@app.callback(
    [Output('rasst-dropdown', 'value'), Output('rasst-dropdown', 'options')],
    [Input('brands-dropdown', 'value'), Input('models-dropdown', 'value'), Input('years-dropdown', 'value'), Input('volumes-dropdown', 'value'),
     Input('resources-dropdown', 'value'), Input('kuzovs-dropdown', 'value'), Input('privods-dropdown', 'value'), Input('korobki-dropdown', 'value'),
     Input('rules-dropdown', 'value')]
)
def update_rasst(brand, model, year, volume, resource, kuzov, privod, korobki, rule):
    temp = df_kol2[(df_kol2.BRAND == brand) & (df_kol2.MODEL == model) & (df_kol2.YEAR == int(year)) & (df_kol2.VOLUME_INT == float(volume)) & (df_kol2.RESOURCE == resource)]
    temp = temp[(temp.KUZOV == kuzov) & (temp.PRIVOD == privod) & (temp.KOROBKA == korobki) & (temp.RULE == rule)]
    rasst = temp.RASST.unique()
    rasst.sort()

    return rasst[0], [{'label': rass, 'value': rass} for rass in rasst]

@app.callback(
    [Output('price_label', 'children'), Output('links', 'children')],
    [Input('brands-dropdown', 'value'), Input('models-dropdown', 'value'), Input('years-dropdown', 'value'), Input('volumes-dropdown', 'value'),
     Input('resources-dropdown', 'value'), Input('kuzovs-dropdown', 'value'), Input('privods-dropdown', 'value'), Input('korobki-dropdown', 'value'),
     Input('rules-dropdown', 'value'), Input('rasst-dropdown', 'value')]
)
def update_price(brand, model, year, volume, resource, kuzov, privod, korobka, rule, rasst):
    temp = df_kol2[(df_kol2.BRAND == brand) & (df_kol2.MODEL == model) & (df_kol2.YEAR == int(year)) & (df_kol2.VOLUME_INT == float(volume)) & (df_kol2.RESOURCE == resource)]
    temp = temp[(temp.KUZOV == kuzov) & (temp.PRIVOD == privod) & (temp.KOROBKA == korobka) & (temp.RULE == rule) & (temp.RASST == rasst)]
    urls = temp.URL.unique()
    price = temp.PRICE_INT.mean()

    return html.H1('Средняя цена: ' + '{:,}'.format(int(price)).replace(',', ' ') + ' тг.', style={'font-family': 'arial'}),\
           [html.Div([dcc.Link(href=url)], style={'font-family': 'arial', 'fontSize': '14px'}) for url in urls]

if __name__ == '__main__':
    app.run_server(debug=True)