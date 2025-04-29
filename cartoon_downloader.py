import os
from tqdm import tqdm
import utils

# ----------------------- CONFIGURATION ----------------------- #
BASE_DIR = './safebooru'
CSV_FILE_PATH = os.path.join(BASE_DIR, 'all_data.csv')
PHOTO_DIR = os.path.join(BASE_DIR, 'photos')
ZIP_OUTPUT_PATH = os.path.join(BASE_DIR, 'safebooru.zip')

def main():
    if not os.path.exists(PHOTO_DIR):
        os.makedirs(PHOTO_DIR)

    if not os.path.exists(CSV_FILE_PATH):
        print(f"CSV file not found at: {CSV_FILE_PATH}")
        return

    with open(CSV_FILE_PATH, 'r') as file:
        file.readline()  # skip header
        count = utils.count_existing_images(PHOTO_DIR)

        with tqdm(total=utils.NUM_IMAGES_TO_DOWNLOAD, initial=count) as pbar:
            while count < utils.NUM_IMAGES_TO_DOWNLOAD:
                line = file.readline()
                if not line:
                    print("Ran out of lines in CSV.")
                    break

                try:
                    url = 'http:' + line.split(',')[4].replace('"', '')
                    if url.endswith('.jpg'):
                        filename = url.split('/')[-1]
                        filepath = os.path.join(PHOTO_DIR, filename)
                        if utils.download_image_if_not_exists(filepath, url):
                            count += 1
                            pbar.update(1)
                except IndexError:
                    continue

    utils.zip_folder(ZIP_OUTPUT_PATH, PHOTO_DIR)
    print(f"Downloaded {count} images and zipped them into: {ZIP_OUTPUT_PATH}")

if __name__ == '__main__':
    main()
