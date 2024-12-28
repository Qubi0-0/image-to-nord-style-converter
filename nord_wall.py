import cvui
from pathlib import Path
import sys
import cv2 as cv
import numpy as np
from tkinter import Tk, filedialog
import os

sys.path.append(str(Path(__file__).resolve().parent / 'scripts'))

from make_nord import make_nord

colors = [
    (47, 37, 29),  # #1D252F → (29, 37, 47)
    (64, 52, 46),  # #2e3440 → (46, 52, 64)
    (82, 66, 59),  # #3b4252 → (59, 66, 82)
    (94, 76, 67),  # #434c5e → (67, 76, 94)
    (106, 86, 76), # #4c566a → (76, 86, 106)
    (193, 161, 129), # #81A1C1 → (129, 161, 193)
    (244, 239, 236)  # #ECEFF4 → (236, 239, 244)
]



def select_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()
    return file_path

def main():
    WINDOW_NAME = 'Nord Image Converter'

    # Initialize cvui and create/open a OpenCV window.
    cvui.init(WINDOW_NAME)
    # Create a frame to render components to.
    frame = np.zeros((600, 1000, 3), np.uint8)

    processed_proxy_image = None
    processed_image = None
    blurr = [False]
    trackbarValue = [int(0)]

    color_centers = None

    img_path = ""
    out_path = ""
    proxy_img_dir = ""
    proxy_in_path = ""
    proxy_out_path = ""

    picker_x = 200
    picker_y = 450
    color_checks = [[True], [True], [True], [True], [True], [True], [True]]

    while True:
        frame[:] = (49, 52, 49)
        cvui.text(frame, 10, 15, 'Nord Image Converter')

        if cvui.button(frame, 10, 50, 'Select Image'):
            img_path = select_file()
            if img_path:
                original_image = cv.imread(img_path)
                proxy_image = cv.resize(original_image, (400, 300))
                proxy_in_path = Path(f"./proxy-{os.path.basename(img_path)}")
                cv.imwrite(proxy_in_path, proxy_image)

        if proxy_out_path and cvui.button(frame, 150, 50, 'Save Image'):
            out_path = Path(".")
            _ = make_nord(img_path, out_path, color_checks, blurr[0])
            os.remove(proxy_img_dir)
            proxy_img_dir = ""
            os.remove(proxy_in_path)
            proxy_in_path = ""
            proxy_out_path = ""
            img_path = ""

        cvui.text(frame, picker_x, picker_y - 30, 'Pick the colors (Minimum 2!)')

        for i, color in enumerate(colors):
                    color_img = np.zeros((20, 20, 3), np.uint8)
                    color_img[:] = color
                    cvui.image(frame, picker_x + i * 30, picker_y, color_img)
                    cvui.checkbox(frame, picker_x + i * 31, picker_y + 25, '', color_checks[i])
                    k = sum(checked[0] for checked in color_checks)
                    

        cvui.checkbox(frame, 290, 50, 'Blurr', blurr)

        # cvui.trackbar(frame, 360, 50, 150, trackbarValue, int(1), int(5))

        if img_path and cvui.button(frame, 10, picker_y, 'Process Image') and k >= 2:
            proxy_out_path = Path(".")
            proxy_img_dir = make_nord(proxy_in_path, proxy_out_path, color_checks, blurr[0], proxy = True)
    
        if proxy_out_path:
            processed_proxy_image = cv.imread(proxy_img_dir)
            cvui.image(frame, 500, 100, processed_proxy_image)

        if img_path:
            original_image = cv.imread(img_path)
            proxy_image = cv.resize(original_image, (400, 300))
            cvui.image(frame, 10, 100, proxy_image)

        if processed_image is not None:
            cvui.image(frame, 420, 100, processed_image)

        if cvui.button(frame, 420, picker_y, 'Exit'):
            os.remove(proxy_in_path)
            os.remove(proxy_img_dir)
            break

        cvui.imshow(WINDOW_NAME, frame)

        if cv.waitKey(20) == 27 :
            break


if __name__ == "__main__":
    main()
    