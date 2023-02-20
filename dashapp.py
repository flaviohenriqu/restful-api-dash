import os
from uuid import UUID

import dash
import flask
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
from sqlmodel import select

from models import Visualization
from settings import get_settings


def create_dash_app(requests_pathname_prefix: str = None) -> dash.Dash:
    """
    Sample Dash application from Plotly
    """
    server = flask.Flask(__name__)
    server.secret_key = os.environ.get('secret_key', 'secret')

    app = dash.Dash(__name__, server=server, requests_pathname_prefix=requests_pathname_prefix)

    app.scripts.config.serve_locally = False
    dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

    app.layout = html.Div([
        html.H1('Visualizations Athenian API'),
        dcc.Input(
            id="input_uid",
            type="text",
            placeholder="visualization uid",
        ),
        dcc.Graph(id="athenian-graph")
    ])

    @app.callback(Output('athenian-graph', 'figure'),
                  [Input('input_uid', 'value')])
    def update_graph(uid):
        dsn_url = get_settings().dsn_sync_url
        stmt = select(Visualization).filter(Visualization.data != None)
        df = pd.read_sql(stmt, con=dsn_url)
        dff = df[df["uid"] == UUID(uid)]

        return dff.iloc[0]["data"]


    return app