from dash import html, dcc
from typing import Dict

import plotly.express as px
import numpy as np
import dash_bootstrap_components as dbc

NAVBAR_MIN_HEIGHT = "4rem"

def get_navbar() -> dbc.Nav:
    return dbc.Nav(
        children = [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src = "/assets/mosquito-white.png", height = "30px")),
                    ],
                    align = "center",
                    className = "g-0 px-2",
                ),
                style = {"textDecoration": "none"},
            ),
            dbc.NavItem(
                children = dbc.NavLink(
                    children = "Home",
                    href = "/",
                    class_name = "text-light"
                )
            ),
            dbc.NavItem(
                children = dbc.NavLink(
                    children = "Usage Guide",
                    href = "/guide",
                    class_name = "text-light"
                )
            ),
            dbc.NavItem(
                children = dbc.NavLink(
                    children = "About",
                    href = "/about",
                    class_name = "text-light"
                )
            )
        ],
        className = "bg-dark d-flex flex-row justify-content-start align-items-center",
        style = {
            "min-height": NAVBAR_MIN_HEIGHT
        }
    )

def display_slider_value(name: str, value: int | float) -> str:
    return f"{name}: {value}"

def get_cc_ui() -> dbc.Container:
    return dbc.Container(
        children = [
            html.H5(
                children = "Color Threshold (0 - 255)",
                className = "text-start my-3"
            ),
            dcc.Slider(
                min = 0,
                max = 255,
                value = 75,
                id = "select-cc-color-thresh",
                className = "my-1"
            ),
            html.P(
                children = display_slider_value("Color Threshold", 75),
                id = "display-cc-color-thresh"
            ),
            html.H5(
                children = "Average Area",
                className = "text-start my-3"
            ),
            dcc.Input(
                value = 800,
                type = "number",
                id = "select-cc-avg-area",
                className = "w-50"
            ),
            html.H5(
                children = "Max Eggs Per Cluster (optional)",
                className = "text-start my-3 mt-3"
            ),
            dcc.Input(
                type = "number",
                id = "select-cc-max-eggs",
                className = "w-50"
            ),
            dbc.Button(
                children = "Count",
                color = "primary",
                className = "w-25 mt-4",
                id = "count-cc"
            )
        ],
        className = "p-3 m-0 border border-dark d-flex flex-column justify-content-center align-items-left"
    )

def get_cc_filter_ui() -> dbc.Container:
    return dbc.Container(
        children = [
            html.H5(
                children = "Color Threshold (0 - 255)",
                className = "text-start my-3"
            ),
            dcc.Slider(
                min = 0,
                max = 255,
                value = 75,
                id = "select-cc-filter-color-thresh",
                className = "my-1"
            ),
            html.P(
                children = display_slider_value("Color Threshold", 75),
                id = "display-cc-filter-color-thresh"
            ),
            html.H5(
                children = "Average Area",
                className = "text-start my-3"
            ),
            dcc.Input(
                value = 800,
                type = "number",
                id = "select-cc-filter-avg-area",
                className = "w-50"
            ),
            html.H5(
                children = "Max Eggs Per Cluster (optional)",
                className = "text-start my-3 mt-3"
            ),
            dcc.Input(
                type = "number",
                id = "select-cc-filter-max-eggs",
                className = "w-50"
            ),
            html.H5(
                children = "Filter Kernel Width (Pixels)",
                className = "text-start my-3"
            ),
            dcc.Input(
                value = 3,
                type = "number",
                id = "select-cc-kernel-width",
                className = "w-50"
            ),
            html.H5(
                children = "Filter Kernel Height (Pixels)",
                className = "text-start my-3"
            ),
            dcc.Input(
                value = 3,
                type = "number",
                id = "select-cc-kernel-height",
                className = "w-50"
            ),
            dbc.Button(
                children = "Count",
                color = "primary",
                className = "w-25 mt-4",
                id = "count-cc-filter"
            )
        ],
        className = "p-3 m-0 border border-dark d-flex flex-column justify-content-center align-items-left"
    )

def get_contour_ui() -> dbc.Container:
    return dbc.Container(
        children = [
            html.H5(
                children = "Color Threshold (0 - 255)",
                className = "text-start my-3"
            ),
            dcc.Slider(
                min = 0,
                max = 255,
                value = 75,
                id = "select-contour-color-thresh",
                className = "my-1"
            ),
            html.P(
                children = display_slider_value("Color Threshold", 75),
                id = "display-contour-color-thresh"
            ),
            html.H5(
                children = "Average Area",
                className = "text-start my-3"
            ),
            dcc.Input(
                value = 800,
                type = "number",
                id = "select-contour-avg-area",
                className = "w-50"
            ),
            html.H5(
                children = "Max Eggs Per Cluster (optional)",
                className = "text-start my-3 mt-3"
            ),
            dcc.Input(
                type = "number",
                id = "select-contour-max-eggs",
                className = "w-50"
            ),
            html.H5(
                children = "Filter Kernel Width (Pixels)",
                className = "text-start my-3"
            ),
            dcc.Input(
                value = 3,
                type = "number",
                id = "select-contour-width",
                className = "w-50"
            ),
            html.H5(
                children = "Filter Kernel Height (Pixels)",
                className = "text-start my-3"
            ),
            dcc.Input(
                value = 3,
                type = "number",
                id = "select-contour-height",
                className = "w-50"
            ),
            dbc.Button(
                children = "Count",
                color = "primary",
                className = "w-25 mt-4",
                id = "count-contour"
            )
        ],
        className = "p-3 m-0 border border-dark d-flex flex-column justify-content-center align-items-left"
    )

def get_results_container(result: Dict) -> dbc.Container:
    children = list()

    for stat_name, stat in result["stats"].items():
        children.append(
            html.H5(
                children = f"{stat_name.replace('-', ' ')}: {stat}",
                className = "text-start w-100"
            ),
        )

    children.append(html.Hr(className = "border border-dark"))

    for vis_name, vis_pic in result["vis"].items():
        children.append(html.H4(vis_name.replace("-", " ")))
        image_fig = px.imshow(vis_pic)
        children.append(
            dcc.Graph(
                figure = image_fig,
                className = "w-100"
            )
        )

    return dbc.Container(
        children = children,
        className = "p-3 m-0 border border-dark d-flex flex-column justify-content-center align-items-center"
    )
