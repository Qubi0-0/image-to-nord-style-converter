import os
import cv2 as cv
import numpy as np
from argparse import ArgumentParser
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
            
            

def make_nord(img_path: Path, out_path: Path, K_val: int, blurr: bool):
    global done 
    image = cv.imread(img_path)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)



    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    
    k = min(max(K_val, 2), 5)
    
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

    new_values = [np.array([29, 37, 47]), np.array([46, 52, 64]), np.array([76, 86, 106]), np.array([129, 161, 193]), np.array([236, 239, 244])]

    replacement_map = {i: new_values[idx] for idx, i in enumerate(np.argsort([np.mean(c) for c in sorted_centers]))}

    new_image = np.array([replacement_map[label] for label in labels.flatten()])
    new_image = new_image.reshape(image.shape).astype(np.uint8)

    if blurr:
        new_image = cv.GaussianBlur(new_image,(3,3),0)

    file_name = os.path.basename(img_path)
    print("Saving image!")
    new_image = cv.cvtColor(new_image, cv.COLOR_RGB2BGR)
    cv.imwrite(f"{out_path}/nord-{file_name}", new_image)
    

def main():
    aparser = ArgumentParser(description=(
        "This script allows you to convert any picture to a nord style. "
        "Choose k (from 2 to 5), and specify the input image and output path."
        " Since the image is quantized, blurr helps to soften edges of the output image."
    ))
    aparser.add_argument(
        "img_path", 
        type=Path,
        help="Path to the input image file."
    )
    aparser.add_argument(
        "--out", 
        type=Path, 
        default=Path(""),
        help="Path to save the output image. Default dir is '/.'."
    )
    aparser.add_argument(
        "--k", 
        type=int, 
        default=5, 
        choices=range(2, 6),
        help="Choose a value for k (from 2 to 5). Default is 5."
    )
    aparser.add_argument(
        "--b", 
        action="store_true", 
        help="Enable blur. If not specified, blur will be disabled."
    )
    args = aparser.parse_args()

    print(f"Processing image: {args.img_path}")
    print(f"Saving output to: {args.out}/nord-{os.path.basename(args.img_path)}")
    print(f"Using k = {args.k}")
    if args.b:
        print(f"Using blurr")
    make_nord(img_path=args.img_path, out_path=args.out, K_val=args.k, blurr=args.b)


if __name__ == "__main__":
    main()