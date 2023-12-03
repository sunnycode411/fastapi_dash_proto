import json
from pathlib import Path
from dateutil.relativedelta import relativedelta
from datetime import datetime

import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash
from dash.dependencies import Output, Input

app_path = Path(__file__).parent.parent
data_path = app_path / 'datasets'


def get_data(start_date: pd.Timestamp, end_date: pd.Timestamp):
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
    df["state_id"] = df["State or union territory"].apply(lambda x: state_id_map[x])  # Change the column name to "state_id"
    df["lat"] = 20.5937  # Add latitude column (you can customize this based on your data)
    df["lon"] = 78.9629  # Add longitude column (you can customize this based on your data)
    return df, india_states


def india_map():
    # Create the Dash app
    app = Dash(__name__, requests_pathname_prefix='/animated_india_map/')

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

        fig = px.scatter_geo(
            df,
            lat="lat",  # Column name for latitude
            lon="lon",  # Column name for longitude
            color="Density",
            hover_name="State or union territory",
            hover_data=["Density"],
            title="India Population Density",
            scope="asia",  # You can customize the scope as needed
        )

        return fig

    return app


animated_india_map_dash_app = india_map()
