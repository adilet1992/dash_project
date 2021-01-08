import plotly.graph_objects as go

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
            go.Scatter(x=df_tab.columns[2:], y=df_tab.loc[i].tolist()[2:], name=df_tab.loc[i].tolist()[0]))
    figure.update_layout(
        autosize=False,
        width=1900,
        height=700
    )
    return figure