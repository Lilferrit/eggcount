from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate
from typing import Tuple, Any, Dict, Optional
from functools import partial
from io import BytesIO
from PIL import Image
from pillow_heif import register_heif_opener
from eggcount.gradient import (
    component_thesh,
    component_filter_thresh,
    contour_thresh
)
from eggcount.ui.ui_utils import (
    get_cc_ui,
    get_cc_filter_ui,
    get_contour_ui,
    display_slider_value,
    get_results_container
)

import plotly.express as px
import base64
import dash
import dash_bootstrap_components as dbc
import numpy as np

register_heif_opener()
dash.register_page(__name__, path = "/")

UPLOAD_HEIGHT = "25vh"

COUNT_FUNCS = {
    "Gradient CC": get_cc_ui,
    "Gradient CC w/ filter": get_cc_filter_ui,
    "Contour": get_contour_ui
}

DEFAULT_STRATEGY = "Gradient CC"

def get_initial_upload_container() -> dbc.Container:
    return dcc.Upload(
        id = "upload-data",
        children = dbc.Container(
            children = [
                html.Img(
                    src = "assets/camera.png",
                    alt = "camera-image",
                    className = "h-50"
                ),
                html.H2("Drag and Drop or Select Image File")
            ],
            class_name = "w-100 d-flex flex-column justify-content-center align-items-center",
            style = {
                "height": UPLOAD_HEIGHT
            }
        )
    )

def get_new_upload_container(
    image_b64: str,
    file_name: str
) -> dbc.Container:
    decoded_bytes = base64.b64decode(image_b64)
    image_data = BytesIO(decoded_bytes)
    pil_img = Image.open(image_data)
    img = np.array(pil_img)
    image_fig = px.imshow(img)

    return dbc.Container(
        children = [
            html.H3(
                children = file_name,
                className = "p-2 text-start",
            ),
            dcc.Graph(figure = image_fig),
            dbc.Container(
                children = dcc.Upload(
                    children = dbc.Button(
                        children = "Upload New Image",
                        color = "secondary"
                    ),
                    id = "upload-data"
                ),
                class_name = "w-100 pb-4 d-flex flex-row justify-content-center align-items-center"
            )
        ]
    )

layout = dbc.Container(
    children = [
        dbc.Container(
            children = get_initial_upload_container(),
            id = "image-upload-container",
            class_name = "m-0 p-0 border border-dark"
        ),
        dcc.Store(
            id = "img-data-store",
            storage_type = "memory"
        ),
        dbc.Modal(
            children = [
                dbc.ModalHeader(
                    dbc.ModalTitle("Error Processing Image File")
                ),
                dbc.ModalBody(
                    children = "",
                    id = "upload-modal-content"
                ),
            ],
            is_open = False,
            id = "upload-modal"
        ),
        html.H4("Select Counting Strategy", className = "text-start mt-3"),
        dcc.Dropdown(
            options = [name for name in COUNT_FUNCS],
            value = DEFAULT_STRATEGY,
            id = "strat-picker",
            className = "my-2 w-100"
        ),
        dbc.Container(
            id = "count-ui-container",
            className = "mt-1 mx-0 px-0" 
        ),
        dcc.Loading(
            children = dbc.Container(
                id = "count-res-container",
                className = "mt-4 mx-0 px-0" 
            ),
            type = "default",
            color = "black"
        )
    ],
    class_name = "text-center mt-3"
)

@callback(
    Output("image-upload-container", "children"),
    Output("img-data-store", "data"),
    Output("upload-modal-content", "children"),
    Output("upload-modal", "is_open"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("image-upload-container", "children"),
    State("img-data-store", "data")
)
def on_image_upload(
    upload_image_data: str,
    upload_image_name: str,
    curr_upload_chidren: Any,
    curr_img_store_data: Dict,
) -> Tuple[dbc.Container, Dict, str, bool]:
    if not upload_image_data:
        raise PreventUpdate
    
    try:
        content_type, content_string = upload_image_data.split(',')
        next_children = get_new_upload_container(content_string, upload_image_name)

        return (
            next_children,
            {"img": content_string},
            "",
            False
        )
    except Exception as e:
        return (
            curr_upload_chidren,
            curr_img_store_data,
            str(e),
            True
        )

@callback(
    Output("count-ui-container", "children"),
    Input("strat-picker", "value")
)
def on_select_strat(
    curr_strat: str
) -> Optional[dbc.Container]:
    if curr_strat not in COUNT_FUNCS:
        return None
    
    ui_fun = COUNT_FUNCS[curr_strat]
    return ui_fun()

@callback(
    Output("count-res-container", "children", allow_duplicate = True),
    Input("count-cc", "n_clicks"),
    State("select-cc-color-thresh", "value"),
    State("select-cc-avg-area", "value"),
    State("select-cc-max-eggs", "value"),
    State("img-data-store", "data"),
    allow_duplicate = True,
    prevent_initial_call = True
)
def on_count_cc(
    n_clicks: int,
    color_thresh: int,
    avg_area: int,
    max_eggs: Optional[int],
    image_store: Dict,
) -> dbc.Container:
    if not n_clicks:
        return None

    decoded_bytes = base64.b64decode(image_store["img"])
    image_data = BytesIO(decoded_bytes)
    pil_img = Image.open(image_data)
    img = np.array(pil_img)

    color_thresh = int(color_thresh)
    avg_area = int(avg_area)

    if max_eggs:
        max_eggs = int(max_eggs)

    results = component_thesh(
        img,
        color_thresh = color_thresh,
        avg_area = avg_area,
        max_eggs = max_eggs
    )

    return get_results_container(results)

@callback(
    Output("count-res-container", "children", allow_duplicate = True),
    Input("count-cc-filter", "n_clicks"),
    State("select-cc-filter-color-thresh", "value"),
    State("select-cc-filter-avg-area", "value"),
    State("select-cc-filter-max-eggs", "value"),
    State("select-cc-kernel-width", "value"),
    State("select-cc-kernel-height", "value"),
    State("img-data-store", "data"),
    prevent_initial_call = True
)
def on_count_cc(
    n_clicks: int,
    color_thresh: int,
    avg_area: int,
    max_eggs: Optional[int],
    kernel_width: int,
    kernel_height: int,
    image_store: Dict,
) -> dbc.Container:
    if not n_clicks:
        return None

    decoded_bytes = base64.b64decode(image_store["img"])
    image_data = BytesIO(decoded_bytes)
    pil_img = Image.open(image_data)
    img = np.array(pil_img)

    color_thresh = int(color_thresh)
    avg_area = int(avg_area)
    kernel_width = int(kernel_width)
    kernel_height = int(kernel_height)

    if max_eggs:
        max_eggs = int(max_eggs)

    results = component_filter_thresh(
        img,
        color_thresh = color_thresh,
        avg_area = avg_area,
        kernal_size = (kernel_width, kernel_height),
        max_eggs = max_eggs
    )

    return get_results_container(results)

@callback(
    Output("count-res-container", "children", allow_duplicate = True),
    Input("count-contour", "n_clicks"),
    State("select-contour-color-thresh", "value"),
    State("select-contour-avg-area", "value"),
    State("select-contour-max-eggs", "value"),
    State("select-contour-width", "value"),
    State("select-contour-height", "value"),
    State("img-data-store", "data"),
    prevent_initial_call = True
)
def on_count_contour(
    n_clicks: int,
    color_thresh: int,
    avg_area: int,
    max_eggs: Optional[int],
    kernel_width: int,
    kernel_height: int,
    image_store: Dict,
) -> dbc.Container:
    if not n_clicks:
        return None

    decoded_bytes = base64.b64decode(image_store["img"])
    image_data = BytesIO(decoded_bytes)
    pil_img = Image.open(image_data)
    img = np.array(pil_img)

    color_thresh = int(color_thresh)
    avg_area = int(avg_area)
    kernel_width = int(kernel_width)
    kernel_height = int(kernel_height)

    if max_eggs:
        max_eggs = int(max_eggs)

    results = contour_thresh(
        img,
        color_thresh = color_thresh,
        avg_area = avg_area,
        kernal_size = (kernel_width, kernel_height),
        max_eggs = max_eggs
    )

    return get_results_container(results)
    
callback(
    Output("display-cc-color-thresh", "children"),
    Input("select-cc-color-thresh", "value")
)(partial(display_slider_value, "Color Threshold"))

callback(
    Output("display-cc-filter-color-thresh", "children"),
    Input("select-cc-filter-color-thresh", "value")
)(partial(display_slider_value, "Color Threshold"))
