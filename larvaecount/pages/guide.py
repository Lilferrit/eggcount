from dash import html, dcc, callback, Input, Output, State
from larvaecount.ui.ui_utils import read_md_file

import dash
import dash_bootstrap_components as dbc
import os

dash.register_page(__name__, path = "/guide")

USER_GUIDE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        "docs",
        "user_guide.md"
    )
)

layout = dbc.Container(
    children = dcc.Markdown(
        children = read_md_file(USER_GUIDE_PATH),
        className = "wiki"
    ),
    class_name = "text-center mt-3"
)

