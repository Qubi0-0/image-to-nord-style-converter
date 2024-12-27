import cvui
from pathlib import Path
import sys
import cv2 as cv
import numpy as np
from tkinter import Tk, filedialog

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
    frame = np.zeros((600, 800, 3), np.uint8)

    img_path = ""
    processed_image = None

    while True:
        frame[:] = (49, 52, 49)
        cvui.text(frame, 10, 15, 'Nord Image Converter')

        if cvui.button(frame, 10, 50, 'Select Image'):
            img_path = select_file()
            if img_path:
                original_image = cv.imread(img_path)
                original_image = cv.resize(original_image, (400, 300))
                cvui.image(frame, 10, 100, original_image)

        if img_path and cvui.button(frame, 10, 450, 'Process Image'):
            out_path = Path(".")
            make_nord(Path(img_path), out_path, 5, False)
            processed_image = cv.imread(f"{out_path}/nord-{Path(img_path).name}")
            processed_image = cv.resize(processed_image, (400, 300))
            cvui.image(frame, 420, 100, processed_image)

        if img_path:
            original_image = cv.imread(img_path)
            original_image = cv.resize(original_image, (400, 300))
            cvui.image(frame, 10, 100, original_image)

        if processed_image is not None:
            cvui.image(frame, 420, 100, processed_image)

        cvui.imshow(WINDOW_NAME, frame)

        if cv.waitKey(20) == 27:
            break

if __name__ == "__main__":
    main()