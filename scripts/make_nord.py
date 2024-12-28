import os
import cv2 as cv
import numpy as np
from pathlib import Path
import threading
import time

"""
Used colors for the script
#2e3440 → (46, 52, 64)
#3b4252 → (59, 66, 82)
#434c5e → (67, 76, 94)
#4c566a → (76, 86, 106) 
#1D252F → (29, 37, 47)
#81A1C1 → (129, 161, 193)
#ECEFF4 → (236, 239, 244)
"""

done = False

def animate_dots():
    while not done:
        for dots in ['.', '..', '...']:
            print(f'\rProcessing{dots}', end='', flush=True)
            time.sleep(0.5)
            
def make_nord(img_path: Path, out_path: Path, color_checks, blurr: bool, proxy = False):
    global done 
    image = cv.imread(img_path)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)



    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    
    k = sum(checked[0] for checked in color_checks)

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 300, 0.1)
    print("Processing image")
    animation_thread = threading.Thread(target=animate_dots)
    animation_thread.start()
    _, labels, centers = cv.kmeans(pixel_values, k, None, criteria, 10, cv.KMEANS_PP_CENTERS)
    done = True
    animation_thread.join()
    print("\nProcessing done!")
    centers = np.uint8(centers)
    sorted_centers = sorted(centers, key=lambda x: np.mean(x)) # type: ignore

    all_new_values = [np.array([29, 37, 47]), np.array([46, 52, 64]), np.array([59, 66, 82]) , np.array([76, 86, 106]), np.array([67, 76, 94]), np.array([129, 161, 193]), np.array([236, 239, 244])]
    new_values = [color for color, check in zip(all_new_values, color_checks) if check[0]]
    replacement_map = {
    i: new_values[idx] if idx < len(new_values) else new_values[-1]
    for idx, i in enumerate(np.argsort([np.mean(c) for c in sorted_centers]))
    }


    new_image = np.array([replacement_map[label] for label in labels.flatten()])
    new_image = new_image.reshape(image.shape).astype(np.uint8)



    if blurr:
        new_image = cv.GaussianBlur(new_image,(3,3),0)

    file_name = os.path.basename(img_path)
    print("Saving image!")
    new_image_rgb = cv.cvtColor(new_image, cv.COLOR_RGB2BGR)
    

    if proxy:
        out_file_dir = f"{out_path}/proxy-nord-{file_name}"
    else:
        out_file_dir = f"{out_path}/nord-{file_name}"

    cv.imwrite(out_file_dir, new_image_rgb)

    return out_file_dir


if __name__ == "__main__":
    img_path = Path("images/proxy-ubuntu.jpg")
    out_path = Path(".")
    K_val = 5
    blurr = False
    color_checks = [[True], [True], [True], [True], [True], [True], [True]]  # Wszystkie kolory wybrane

    out = make_nord(img_path, out_path, color_checks, blurr)

    cv.imshow("img", cv.imread(out))
