import json
from pathlib import Path
from dateutil.relativedelta import relativedelta
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash import dcc, html, Dash
from dash.dependencies import Output, Input

app_path = Path(__file__).parent.parent
data_path = app_path / 'datasets'


def get_data(start_date: pd.Timestamp, end_date: pd.Timestamp):
    pio.renderers.default = 'browser'

    # Load geojson file
    india_states = json.load(open(data_path / "states_india.geojson", "r"))

    # Create state_id_map
    state_id_map = {}
    for feature in india_states["features"]:
        feature["id"] = feature["properties"]["state_code"]
        state_id_map[feature["properties"]["st_nm"]] = feature["id"]

    # Read the data
    df = pd.read_csv(data_path / "india_census.csv")
    df["Density"] = df["Density[a]"].apply(lambda x: int(x.split("/")[0].replace(",", "")))
    df["id"] = df["State or union territory"].apply(lambda x: state_id_map[x])
    return df, india_states


def india_map():
    # Create the Dash app
    app = Dash(__name__, requests_pathname_prefix='/india_map_graph/')

    # Define the layout of the app
    app.layout = html.Div([
        dcc.DatePickerRange(
            id='datepicker',
            start_date=datetime.now().strftime('%Y-%m-%d'),
            end_date=(datetime.now() + relativedelta(days=1)).strftime('%Y-%m-%d')
        ),
        dcc.Graph(
            id='choropleth-map',
            style={'height': '100vh'}
        )
    ])

    @app.callback(
        Output('choropleth-map', 'figure'),
        [
            Input('datepicker', 'start_date'),
            Input('datepicker', 'end_date')
        ]
    )
    def update_map(start_date, end_date):
        df, geojson = get_data(start_date, end_date)
        fig = px.choropleth_mapbox(
                df,
                locations="id",
                geojson=geojson,
                color="Density",
                hover_name="State or union territory",
                hover_data=["Density"],
                title="India Population Density",
                # mapbox_style="carto-positron",
                mapbox_style="white-bg",
                center={"lat": 20.5937, "lon": 78.9629},  # Center coordinates for India
                zoom=3,
                # pitch=0,  # Set pitch to 0 to disable tilt and make the map 2D
                opacity=0.5,
        )
        return fig

    return app


india_map_dash_app = india_map()
