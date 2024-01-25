from dash import html, dcc, callback, Input, Output

import dash
import dash_bootstrap_components as dbc

dash.register_page(__name__, path = "/")

UPLOAD_HEIGHT = "25vh"

layout = dbc.Container(
    children = dcc.Upload(
        id = 'upload-data',
        children = dbc.Container(
            "Upload Image Here",
            class_name = "w-100 border border-dark",
            style = {
                "height": UPLOAD_HEIGHT
            }
        )
    ),
    class_name = "text-center mt-3"
)
