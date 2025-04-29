import os
import zipfile
import urllib.request
from pycocotools.coco import COCO
from tqdm import tqdm
import utils

# ----------------------- CONFIG ----------------------- #
BASE_DIR = './coco'
ANNOTATION_DIR = os.path.join(BASE_DIR, 'annotations')
ANNOTATION_FILE = os.path.join(ANNOTATION_DIR, 'instances_train2017.json')
ANNOTATION_ZIP_URL = 'http://images.cocodataset.org/annotations/annotations_trainval2017.zip'
ANNOTATION_ZIP_FILE = os.path.join(ANNOTATION_DIR, 'annotations_trainval2017.zip')

PHOTO_DIR = os.path.join(BASE_DIR, 'photos')
ZIP_OUTPUT_PATH = os.path.join(BASE_DIR, 'coco.zip')
CATEGORY_NAME = 'person'

# ----------------------- UTILS ----------------------- #
def download_and_extract_annotations():
    print("Annotation file not found. Downloading...")

    if not os.path.exists(ANNOTATION_DIR):
        os.makedirs(ANNOTATION_DIR)

    print("Downloading annotation zip...")
    urllib.request.urlretrieve(ANNOTATION_ZIP_URL, ANNOTATION_ZIP_FILE)
    print("Download complete.")

    print("Extracting annotations...")
    with zipfile.ZipFile(ANNOTATION_ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(BASE_DIR)
    print("Extraction complete.")

    os.remove(ANNOTATION_ZIP_FILE)
    print("Cleaned up zip file.")

# ----------------------- MAIN ----------------------- #
def main():
    if not os.path.exists(ANNOTATION_FILE):
        download_and_extract_annotations()

    if not os.path.exists(PHOTO_DIR):
        os.makedirs(PHOTO_DIR)

    coco = COCO(ANNOTATION_FILE)
    cat_ids = coco.getCatIds(catNms=[CATEGORY_NAME])
    img_ids = coco.getImgIds(catIds=cat_ids)
    img_data = coco.loadImgs(img_ids)
    iterator = iter(img_data)

    count = utils.count_existing_images(PHOTO_DIR)

    with tqdm(total=utils.NUM_IMAGES_TO_DOWNLOAD, initial=count) as pbar:
        while count < utils.NUM_IMAGES_TO_DOWNLOAD:
            try:
                data = next(iterator)
                url = data.get('coco_url')
                filename = os.path.join(PHOTO_DIR, data['file_name'])
                if url and utils.download_image_if_not_exists(filename, url):
                    count += 1
                    pbar.update(1)
            except StopIteration:
                print("Ran out of images to download.")
                break
            except Exception as e:
                print("Unexpected error:", e)
                continue

    utils.zip_folder(ZIP_OUTPUT_PATH, PHOTO_DIR)
    print(f"Downloaded {count} images and zipped them into {ZIP_OUTPUT_PATH}")

if __name__ == '__main__':
    main()
