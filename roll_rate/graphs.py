import plotly.graph_objects as go

def total_debt_graph_2(df):
    operdates = df.columns[1:]
    data = []
    for i in range(len(df.values)-1):
        data.append(go.Bar(name=df.values[i][0], x=operdates, y=df.values[i][1:]))
    fig = go.Figure(data=data)
    fig.update_layout(barmode='stack', autosize=False, width=1500, height=600)

    return fig

def total_debt_graph(df):
    operdates = df.columns[1:]
    data = []
    for i in range(len(df.values)):
        data.append(go.Bar(name=df.values[i][0], x=operdates, y=df.values[i][1:]))
    fig = go.Figure(data=data)
    fig.update_layout(barmode='stack', autosize=False, width=1500, height=600)

    return fig

def scatter_graph(df):
    operdates = df.columns[1:]
    fig = go.Figure()
    for i in range(len(df.values)):
        fig.add_trace(go.Scatter(x=operdates, y=df.values[i][1:], name=df.values[i][0], mode='lines+markers'))

    fig.update_layout(autosize=False, width=1500, height=600)

    return fig