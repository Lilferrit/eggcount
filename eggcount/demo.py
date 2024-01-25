from eggcount.eggcount import (
    count_eggs_contour_thresh
)
from os import PathLike
from PIL import Image
from pillow_heif import register_heif_opener

import numpy as np
import matplotlib.pyplot as plt
import fire

register_heif_opener()

def demo(
    img_dir: PathLike,
    color_thresh: int = 75,
    avg_area: float = 800
) -> None:
    # Open image, suppoorts apple HEIC format
    pil_img = Image.open(img_dir)

    # Convert to standard RGB Image
    img = np.array(pil_img)

    num, processed_image = count_eggs_contour_thresh(
        img,
        color_thresh = color_thresh,
        avg_area = avg_area
    )

    print(num)
    plt.imshow(processed_image)
    plt.show()

if __name__ == "__main__":
    fire.Fire(demo)

