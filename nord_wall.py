import cvui
from pathlib import Path
import sys
import cv2 as cv
import numpy as np
from tkinter import Tk, filedialog
import os


sys.path.append(str(Path(__file__).resolve().parent / 'scripts'))

from make_nord import make_nord

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
    frame = np.zeros((600, 1200, 3), np.uint8)

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
                cvui.image(frame, 10, 100, proxy_image)

        if proxy_out_path and cvui.button(frame, 150, 50, 'Save Image'):
            k = int(trackbarValue[0])
            out_path = Path(".")
            _ = make_nord(img_path, out_path, k, blurr[0])
            os.remove(proxy_img_dir)
            proxy_img_dir = ""
            os.remove(proxy_in_path)
            proxy_in_path = ""
            proxy_out_path = ""
            img_path = ""


        cvui.checkbox(frame, 290, 50, 'Blurr', blurr)

        cvui.trackbar(frame, 360, 50, 150, trackbarValue, int(1), int(5))

        if img_path and cvui.button(frame, 10, 450, 'Process Image'):
            k = int(trackbarValue[0])
            proxy_out_path = Path(".")
            proxy_img_dir = make_nord(proxy_in_path, proxy_out_path, k, blurr[0], proxy = True)
    
        if proxy_out_path:
            processed_proxy_image = cv.imread(proxy_img_dir)
            cvui.image(frame, 500, 100, processed_proxy_image)

        if img_path:
            original_image = cv.imread(img_path)
            proxy_image = cv.resize(original_image, (400, 300))
            cvui.image(frame, 10, 100, proxy_image)

        if processed_image is not None:
            cvui.image(frame, 420, 100, processed_image)

        cvui.imshow(WINDOW_NAME, frame)

        if cv.waitKey(20) == 27:
            break

if __name__ == "__main__":
    main()
    