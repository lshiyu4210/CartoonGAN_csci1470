import os
import cv2
import numpy as np
from tqdm import tqdm
from glob import glob
from utils import zip_folder

# ----------------------- HARDCODED CONFIG ----------------------- #
INPUT_DIR  = './safebooru/photos'
OUTPUT_DIR = './safebooru/safebooru_smoothed'
ZIP_PATH   = './safebooru/safebooru_smoothed.zip'
IMG_SIZE   = 256

# ----------------------- EDGE SMOOTHING ----------------------- #
def apply_edge_smoothing(input_dir, output_dir, img_size):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_list = glob(os.path.join(input_dir, '*.*'))

    kernel_size = 5
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    gauss = cv2.getGaussianKernel(kernel_size, 0)
    gauss = gauss @ gauss.T  # outer product

    for filepath in tqdm(file_list):
        file_name = os.path.basename(filepath)
        bgr_img = cv2.imread(filepath)
        gray_img = cv2.imread(filepath, 0)

        if bgr_img is None or gray_img is None:
            print(f"Skipping unreadable file: {filepath}")
            continue

        bgr_img = cv2.resize(bgr_img, (img_size, img_size))
        gray_img = cv2.resize(gray_img, (img_size, img_size))
        padded = np.pad(bgr_img, ((2, 2), (2, 2), (0, 0)), mode='reflect')

        edges = cv2.Canny(gray_img, 100, 200)
        dilated = cv2.dilate(edges, kernel)

        smoothed = np.copy(bgr_img)
        idx = np.where(dilated != 0)

        for y, x in zip(*idx):
            for c in range(3):
                region = padded[y:y+kernel_size, x:x+kernel_size, c]
                smoothed[y, x, c] = np.sum(region * gauss)

        cv2.imwrite(os.path.join(output_dir, file_name), smoothed)

# ----------------------- MAIN ----------------------- #
def main():
    apply_edge_smoothing(INPUT_DIR, OUTPUT_DIR, IMG_SIZE)
    zip_folder(ZIP_PATH, OUTPUT_DIR)
    print(f"Smoothed images saved to {OUTPUT_DIR} and zipped to {ZIP_PATH}")

if __name__ == '__main__':
    main()
