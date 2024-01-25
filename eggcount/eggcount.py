from typing import Tuple

import numpy as np
import cv2
import fire

def contour_thresh(
    img: np.ndarray,
    color_thresh: int = 75,
    avg_area: float = 800
) -> Tuple[int, np.ndarray]:
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    bin_mask = cv2.inRange(img_gray, 0, color_thresh)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    opening = cv2.morphologyEx(bin_mask, cv2.MORPH_OPEN, kernel, iterations = 1)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations = 2)

    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    num = 0

    for cnt in cnts:
        area = cv2.contourArea(cnt)

        if area > avg_area / 2:
            cv2.drawContours(img, [cnt], -1, (255, 0, 0), 2)
            curr_num = round(area / avg_area)
            num += curr_num

            cv2.putText(
                img,
                str(curr_num),
                cnt[0, 0],
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 0, 255),
                3
            )

    return num, img

if __name__ == "__main__":
    fire.Fire()
