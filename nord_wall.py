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
    frame = np.zeros((1200, 1600, 3), np.uint8)

    img_path = ""
    processed_proxy_image = None
    processed_image = None
    blurr = [False]
    trackbarValue = [int(0)]
    processed = False


    while True:
        frame[:] = (49, 52, 49)
        cvui.text(frame, 10, 15, 'Nord Image Converter')

        if cvui.button(frame, 10, 50, 'Select Image'):
            img_path = select_file()
            if img_path:
                original_image = cv.imread(img_path)
                proxy_image = cv.resize(original_image, (400, 300))
                cvui.image(frame, 10, 100, proxy_image)

        if cvui.button(frame, 120, 50, 'Save Image'):
            processed_image = make_nord(original_image, k, blurr[0])
            file_name = os.path.basename(img_path)
            print("Saving image!")
            new_image_rgb = cv.cvtColor(processed_image, cv.COLOR_RGB2BGR)
            cv.imwrite(f"{Path(".")}/nord-{file_name}", new_image_rgb)


        cvui.checkbox(frame, 500, 160, 'Blurr', blurr)

        cvui.trackbar(frame, 500, 110, 150, trackbarValue, int(1), int(5))

        if img_path and cvui.button(frame, 10, 450, 'Process Image'):
            k = int(trackbarValue[0])
            processed_proxy_image = make_nord(proxy_image, k, blurr[0])
            processed = True
            if processed:
                processed_proxy_image = cv.cvtColor(processed_proxy_image, cv.COLOR_RGB2BGR)
                cvui.image(frame, 2 * 420 + 100, 100, processed_proxy_image)

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