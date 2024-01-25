from eggcount.gradient import (
    contour_thresh,
    component_thesh,
    component_filter_thresh
)
from os import PathLike
from PIL import Image
from pillow_heif import register_heif_opener
from typing import Optional

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import fire

register_heif_opener()

def filter_connected_components(
    img_dir: PathLike,
    color_thresh: int = 75,
    avg_area: float = 800,
    vis: bool = False,
    save_loc: PathLike = "",
    kernal_size: tuple[int, int] = (3, 3),
    max_eggs: Optional[int] = None
) -> None:
    # Open image, supports apple HEIC format
    pil_img = Image.open(img_dir)

    # Convert to standard RGB Image
    img = np.array(pil_img)
    res = component_filter_thresh(
        img,
        color_thresh = color_thresh,
        avg_area = avg_area,
        kernal_size = kernal_size,
        max_eggs = max_eggs
    )

    res_vis = res["vis"]
    res_stats = res["stats"]

    for label, stat in res_stats.items():
        print(f"{label.replace('-', ' ')}: {stat}")

    if vis:
        for label, curr_img in res_vis.items():
            plt.imshow(curr_img)
            plt.show()

    if save_loc:
        for label, curr_img in res_vis.items():
            save_path = os.path.join(save_loc, label + ".png")
            plt.imsave(save_path, curr_img)
    

def connected_components(
    img_dir: PathLike,
    color_thresh: int = 75,
    avg_area: float = 800,
    vis: bool = False,
    save_loc: PathLike = "",
    max_eggs: Optional[int] = None
) -> None:
    # Open Image
    pil_img = Image.open(img_dir)

    # Convert to standard RGB Image
    img = np.array(pil_img)

    res = component_thesh(
        img,
        color_thresh = color_thresh,
        avg_area = avg_area,
        max_eggs = max_eggs
    )
    res_vis = res["vis"]
    res_stats = res["stats"]

    for label, stat in res_stats.items():
        print(f"{label.replace('-', ' ')}: {stat}")

    if vis:
        for label, curr_img in res_vis.items():
            plt.imshow(curr_img)
            plt.show()

    if save_loc:
        for label, curr_img in res_vis.items():
            save_path = os.path.join(save_loc, label + ".png")
            plt.imsave(save_path, curr_img)

def contour(
    img_dir: PathLike,
    color_thresh: int = 75,
    avg_area: float = 800,
    vis: bool = False,
    save_loc: PathLike = "",
    kernal_size: tuple[int, int] = (3, 3)
) -> None:
    # Open image, supports apple HEIC format
    pil_img = Image.open(img_dir)

    # Convert to standard RGB Image
    img = np.array(pil_img)
    res = contour_thresh(
        img,
        color_thresh = color_thresh,
        avg_area = avg_area,
        kernal_size = kernal_size
    )

    res_vis = res["vis"]
    res_stats = res["stats"]

    for label, stat in res_stats.items():
        print(f"{label.replace('-', ' ')}: {stat}")

    if vis:
        for label, curr_img in res_vis.items():
            plt.imshow(curr_img)
            plt.show()

    if save_loc:
        for label, curr_img in res_vis.items():
            save_path = os.path.join(save_loc, label + ".png")
            plt.imsave(save_path, curr_img)

if __name__ == "__main__":
    fire.Fire()
