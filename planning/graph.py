import plotly.graph_objects as go

def plot_ar_table(df_tab):
    table = go.Figure(data=[
        go.Table(header=dict(values=df_tab.columns, font=dict(size=11, color='white'), fill_color='green', line_color='black'),
                 cells=dict(values=[df_tab[col] for col in df_tab.columns], font=dict(size=11), fill_color='white', line_color='black'))
    ])

    table.update_layout(
        autosize=False,
        width=1200,
        height=400
    )
    return table

def plot_vintage_table(df_tab):
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

def plot_eri_table(df_tab):
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