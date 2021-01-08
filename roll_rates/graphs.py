import plotly.graph_objects as go

def table_image(df):
    table = go.Figure(data=[
        go.Table(header=dict(values=df.columns, font=dict(size=11, color='white'), fill_color='green',
                             line_color='black'),
                 cells=dict(
                     values=[df[col] for col in df.columns],
                     font=dict(size=11), fill_color='white', line_color='black'))
    ])
    table.update_layout(
        autosize=False,
        width=900,
        height=320
    )
    return table

def roll_rate_graph(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.BASE_YMD, y=df.SHARE, mode='lines+text', text=[str(x) + ' %' for x in df.SHARE.tolist()], textposition='bottom center'))
    fig.update_layout(
        autosize=False,
        width=900,
        height=500
    )

    return fig