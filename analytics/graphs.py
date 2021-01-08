import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Tables and graphs of FPD SPD TPD share amount
def table_fpd_spd_tpd(df_tab):

    table = go.Figure(data=[
        go.Table(header=dict(values=df_tab.columns, font=dict(size=11, color='white'), fill_color='green', line_color='black'),
                 cells=dict(values=[df_tab['Месяц выдачи'], df_tab['Сумма выдачи (в млн.)'], df_tab['FPD'], df_tab['SPD'], df_tab['TPD']],
                            font=dict(size=11), fill_color='white', line_color='black'))
    ])
    table.update_layout(
        autosize=False,
        width=800,
        height=700
    )
    return table

def graph_fpd_spd_tpd(df_tab):
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df_tab['Месяц выдачи'], y=df_tab['Сумма выдачи (в млн.)'], name='Сумма выдачи (в млн.)', marker={'color': 'green'}), secondary_y=False)
    fig.add_trace(go.Scatter(x=df_tab['Месяц выдачи'], y=df_tab['FPD'], name='FPD', marker={'color': '#FA7E61'}), secondary_y=True)
    fig.add_trace(go.Scatter(x=df_tab['Месяц выдачи'], y=df_tab['SPD'], name='SPD', marker={'color': '#984447'}), secondary_y=True)
    fig.add_trace(go.Scatter(x=df_tab['Месяц выдачи'], y=df_tab['TPD'], name='TPD', marker={'color': '#462255'}), secondary_y=True)

    fig.update_layout(
        autosize=False,
        height=600,
        width=1000
    )
    return fig

#Tables and graphs of FPD SPD TPD share count
def table_fpd_spd_tpd_c(df_tab):

    table = go.Figure(data=[
        go.Table(header=dict(values=df_tab.columns, font=dict(size=11, color='white'), fill_color='green', line_color='black'),
                 cells=dict(values=[df_tab['Месяц выдачи'], df_tab['Кол-во выдачи'], df_tab['FPD'], df_tab['SPD'], df_tab['TPD']],
                            font=dict(size=11), fill_color='white', line_color='black'))
    ])
    table.update_layout(
        autosize=False,
        width=800,
        height=700
    )
    return table

def graph_fpd_spd_tpd_c(df_tab):
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df_tab['Месяц выдачи'], y=df_tab['Кол-во выдачи'], name='Кол-во выдачи', marker={'color': 'green'}), secondary_y=False)
    fig.add_trace(go.Scatter(x=df_tab['Месяц выдачи'], y=df_tab['FPD'], name='FPD', marker={'color': '#FA7E61'}), secondary_y=True)
    fig.add_trace(go.Scatter(x=df_tab['Месяц выдачи'], y=df_tab['SPD'], name='SPD', marker={'color': '#984447'}), secondary_y=True)
    fig.add_trace(go.Scatter(x=df_tab['Месяц выдачи'], y=df_tab['TPD'], name='TPD', marker={'color': '#462255'}), secondary_y=True)

    fig.update_layout(
        autosize=False,
        height=600,
        width=1000
    )
    return fig

#######Graphs and tables of Approval rate analytics
def table_appr(df_tab):
    table = go.Figure(data=[
        go.Table(header=dict(values=df_tab.columns, font=dict(size=11, color='white'), fill_color='green', line_color='black'),
                 cells=dict(values=[df_tab[col] for col in df_tab.columns], font=dict(size=11), fill_color='white', line_color='black'))
    ])

    table.update_layout(
        autosize=False,
        width=1800,
        height=800
    )
    return table

def graph_appr(df_tab):
    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=df_tab['Дата'], y=df_tab['Заявки нерассмотренные скоринговой системой'] + df_tab['Заявки рассмотренные скоринговой системой'], name='Общее кол-во заявок', marker={'color': '#057044'}), secondary_y=False)
    fig.add_trace(go.Bar(x=df_tab['Дата'], y=df_tab['Одобренные заявки с учетом альтернативных предложений'], name='Одобренные заявки с учетом альтернативных предложений', marker={'color': '#c6a26e'}), secondary_y=False)
    fig.add_trace(go.Bar(x=df_tab['Дата'], y=df_tab['Одобренные заявки без учета альтернативных предложений'], name='Одобренные заявки без учета альтернативных предложений', marker={'color': 'blue'}), secondary_y=False)
    fig.add_trace(go.Scatter(x=df_tab['Дата'], y=df_tab['Уровень одобрения с учетом альтернативных предложений, %'], name='Уровень одобрения с учетом альтернативных предложений, %'), secondary_y=True)
    fig.add_trace(go.Scatter(x=df_tab['Дата'], y=df_tab['Уровень одобрения без учета альтернативных предложений, %'], name='Уровень одобрения без учета альтернативных предложений, %'), secondary_y=True)
    fig.add_trace(go.Scatter(x=df_tab['Дата'], y=df_tab['Конверсия в выдачу с учетом альтернативных предложений'], name='Конверсия в выдачу с учетом альтернативных предложений'), secondary_y=True)
    fig.add_trace(go.Scatter(x=df_tab['Дата'], y=df_tab['Конверсия в выдачу без учета альтернативных предложений'], name='Конверсия в выдачу без учета альтернативных предложений'), secondary_y=True)
    fig.update_layout(
        autosize=False,
        width=1800,
        height=700
    )
    return fig

def table_reason(df_tab):
    table = go.Figure(data=[
        go.Table(header=dict(values=df_tab.columns, font=dict(size=11, color='white'), fill_color='green', line_color='black'),
                 cells=dict(values=[df_tab[col] for col in df_tab.columns], font=dict(size=11), fill_color='white', line_color='black'),
                 columnorder=[i+1 for i in range(len(df_tab.columns))],
                 columnwidth=[150] + [80 for i in range(len(df_tab.columns)-1)])
    ])

    table.update_layout(
        autosize=False,
        width=1000,
        height=600
    )
    return table

def graph_reason(df_tab):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_tab['Месяц выдачи'], y=df_tab['Одобрено'], name='Одобрено', marker={'color': '#057044'}))
    fig.add_trace(go.Bar(x=df_tab['Месяц выдачи'], y=df_tab['Отказано'], name='Отказано', marker={'color': '#c6a26e'}))

    fig.update_layout(
        autosize=False,
        width=800,
        height=600,
        barmode='stack'
    )
    return fig

def table_reason_alert(df_tab):
    table = go.Figure(data=[
        go.Table(header=dict(values=df_tab.columns, font=dict(size=11, color='white'), fill_color='green', line_color='black'),
                 cells=dict(values=[df_tab[col] for col in df_tab.columns], font=dict(size=11), fill_color='white', line_color='black'),
                 columnorder=[i + 1 for i in range(len(df_tab.columns))],
                 columnwidth=[300] + [80 for i in range(len(df_tab.columns) - 1)])
    ])

    table.update_layout(
        autosize=False,
        width=1500,
        height=800
    )
    return table

def table_reason_name(df_tab):
    table = go.Figure(data=[
        go.Table(header=dict(values=df_tab.columns),
                 cells=dict(values=[df_tab[col] for col in df_tab.columns]),
                 columnorder=[i + 1 for i in range(len(df_tab.columns))],
                 columnwidth=[500] + [80 for i in range(len(df_tab.columns) - 1)])
    ])

    table.update_layout(
        autosize=False,
        width=1500,
        height=800
    )
    return table

def table_pivot(df_tab):
    table = go.Figure(data=[
        go.Table(header=dict(values=df_tab.columns, font=dict(size=11, color='white'), fill_color='green', line_color='black'),
                 cells=dict(values=[df_tab[col] for col in df_tab.columns], font=dict(size=11), fill_color='white', line_color='black'))
    ])
    table.update_layout(
        autosize=False,
        width=1200,
        height=700
    )
    return table

def table_vintage(df_tab):
    table = go.Figure(data=[
        go.Table(header=dict(values=df_tab.columns, font=dict(size=11, color='white'), fill_color='green', line_color='black'),
                 cells=dict(values=[df_tab[col] for col in df_tab.columns], font=dict(size=11), fill_color='white', line_color='black'))
    ])
    table.update_layout(
        autosize=False,
        width=1900,
        height=1000
    )
    return table

def graph_vintage(df_tab):
    figure = go.Figure()
    for i in df_tab.index:
        figure.add_trace(
            go.Scatter(x=df_tab.columns[1:], y=df_tab.loc[i].tolist()[1:], name=df_tab.loc[i].tolist()[0]))
    figure.update_layout(
        autosize=False,
        width=1900,
        height=1000
    )
    return figure