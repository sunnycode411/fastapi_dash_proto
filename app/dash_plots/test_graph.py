from dash import html, Dash, Output, dcc
import plotly.express as px
import pandas as pd
import numpy as np


def update_graph():
    # Generate sample time series data
    np.random.seed(42)

    date_rng = pd.date_range(start='2023-11-01', end='2023-11-30', freq='D')
    data = {
        'Date': date_rng,
        'Variable1': np.random.rand(len(date_rng)),
        'Variable2': np.random.rand(len(date_rng)),
        'Variable3': np.random.rand(len(date_rng)),
        'Variable4': np.random.rand(len(date_rng)),
        'Variable5': np.random.rand(len(date_rng)),
    }

    df = pd.DataFrame(data)

    fig = px.line(df, x='Date', y=['Variable1', 'Variable2', 'Variable3', 'Variable4', 'Variable5'],
                  title='Sample Time Series Data with 5 Variables',
                  labels={'value': 'Variable Value', 'variable': 'Variables'},
                  line_shape='linear',
                  )

    return fig


def test_graph():
    app = Dash(__name__, requests_pathname_prefix="/test_graph/")

    app.layout = html.Div([
        html.H1('Sample Graph!'),
        dcc.Graph(id='sample-graph', figure=update_graph())
    ])

    @app.callback(
        Output('sample-graph', 'graph')
    )
    def update_components():
        return update_graph()

    return app
