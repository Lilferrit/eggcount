from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate
from typing import Tuple, Any, Dict
from io import BytesIO
from PIL import Image
from pillow_heif import register_heif_opener

import plotly.express as px
import base64
import dash
import dash_bootstrap_components as dbc
import numpy as np

register_heif_opener()
dash.register_page(__name__, path = "/")

UPLOAD_HEIGHT = "25vh"

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
