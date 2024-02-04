import dash_bootstrap_components as dbc
import dash
import fire

from eggcount.ui.ui_utils import (
    get_navbar
)
from dash import Dash, html, dcc

app = Dash(
    __name__,
    use_pages = True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = dbc.Container(
    children = [
        get_navbar(),
        dash.page_container
    ],
    class_name = "m-0 p-0 w-100 mw-100",
    id = "content-container"
)

def main(
    debug: bool = False,
    port: str = "8080",
    host: str = "127.0.0.1"
) -> None:
    app.run(
        debug = debug,
        host = host,
        port = port
    )

if __name__ == '__main__':
    fire.Fire(main)
