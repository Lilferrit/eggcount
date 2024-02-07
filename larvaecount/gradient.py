from typing import Tuple, Dict, Optional

import numpy as np
import cv2

def component_filter_thresh(
    img: np.ndarray,
    color_thresh: int = 75,
    avg_area: float = 800,
    kernal_size: tuple[int, int] = (3, 3),
    max_eggs: Optional[int] = None
) -> Dict:
    # Clone image, get grayscale, and masc for candidate egg pixels
    visualization_img = img.copy()
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    bin_mask = cv2.inRange(img_gray, 0, color_thresh)

    # Filter pixels not part of a elliptical region
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernal_size)
    opening = cv2.morphologyEx(bin_mask, cv2.MORPH_OPEN, kernel, iterations = 1)
    close =  cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations = 1)

    # Get connected components of filtered image
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        close,
    )

    num_eggs = 0

    # Iterate over stats, calculating the number of eggs in each connected component
    for curr_label, curr_stat in enumerate(stats):
        left_x = curr_stat[cv2.CC_STAT_LEFT]
        top_y = curr_stat[cv2.CC_STAT_TOP]
        area = curr_stat[cv2.CC_STAT_AREA]

        if (area < avg_area / 2) or curr_label == 0:
            continue

        # Calculate number of eggs
        curr_num_eggs = round(area / avg_area)

        if max_eggs and (curr_num_eggs > max_eggs):
            continue

        # Draw border around current component
        component_mask = (labels == curr_label).astype(np.uint8)
        contours, _ = cv2.findContours(component_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(visualization_img, contours, -1, (255, 0, 0), 2)

        # Label current component with number of eggs
        cv2.putText(
            visualization_img,
            str(curr_num_eggs),
            (left_x, top_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 0, 255),
            3
        )

        num_eggs += curr_num_eggs

    return {
        "stats": {
            "Num-Eggs": num_eggs
        },
        "vis": {
            "Gray-Scale": img_gray.astype(np.uint8),
            "Egg-Mask": bin_mask.astype(np.uint8),
            "Ellipse-Filter": close.astype(np.uint8),
            "Visualization": visualization_img.astype(np.uint8)
        }
    }

def component_thesh(
    img: np.ndarray,
    color_thresh: int = 75,
    avg_area: float = 800,
    max_eggs: Optional[int] = None
) -> Dict:
    # Clone image
    visualization_img = img.copy()

    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Mask out egg pixels
    bin_mask = cv2.inRange(img_gray, 0, color_thresh)

    # Get connected components
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        bin_mask,
    )

    num_eggs = 0

    # Iterate over stats, calculating the number of eggs in each connected component
    for curr_label, curr_stat in enumerate(stats):
        left_x = curr_stat[cv2.CC_STAT_LEFT]
        top_y = curr_stat[cv2.CC_STAT_TOP]
        area = curr_stat[cv2.CC_STAT_AREA]

        if (area < avg_area / 2) or curr_label == 0:
            continue

        # Calculate number of eggs
        curr_num_eggs = round(area / avg_area)

        if max_eggs and (curr_num_eggs > max_eggs):
            continue

        # Draw border around current component
        component_mask = (labels == curr_label).astype(np.uint8)
        contours, _ = cv2.findContours(component_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(visualization_img, contours, -1, (255, 0, 0), 2)

        # Label current component with number of eggs
        cv2.putText(
            visualization_img,
            str(curr_num_eggs),
            (left_x, top_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 0, 255),
            3
        )

        num_eggs += curr_num_eggs

    return {
        "stats": {
            "Num-Eggs": num_eggs
        },
        "vis": {
            "Gray-Scale": img_gray.astype(np.uint8),
            "Egg-Mask": bin_mask.astype(np.uint8),
            "Visualization": visualization_img.astype(np.uint8)
        }
    }

def contour_thresh(
    img: np.ndarray,
    color_thresh: int = 75,
    avg_area: float = 800,
    kernal_size: tuple[int, int] = (3, 3),
    max_eggs: Optional[int] = None
) -> Dict:
    visualization_img = img.copy()
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    bin_mask = cv2.inRange(img_gray, 0, color_thresh)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernal_size)
    opening = cv2.morphologyEx(bin_mask, cv2.MORPH_OPEN, kernel, iterations = 1)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations = 2)

    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    num = 0

    for cnt in cnts:
        area = cv2.contourArea(cnt)

        if area > avg_area / 2:
            curr_num = round(area / avg_area)

            if max_eggs and (curr_num > max_eggs):
                continue

            cv2.drawContours(visualization_img, [cnt], -1, (255, 0, 0), 2)
            curr_num = round(area / avg_area)
            num += curr_num

            cv2.putText(
                visualization_img,
                str(curr_num),
                cnt[0, 0],
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 0, 255),
                3
            )

    return {
        "stats": {
            "Num-Eggs": num
        },
        "vis": {
            "Gray-Scale": img_gray.astype(np.uint8),
            "Egg-Mask": bin_mask.astype(np.uint8),
            "Ellipse-Filter": close.astype(np.uint8),
            "Visualization": visualization_img.astype(np.uint8)
        }
    }
