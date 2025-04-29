import os
import shutil
import urllib.request

NUM_IMAGES_TO_DOWNLOAD = 4500

def count_existing_images(directory_path):
    if not os.path.exists(directory_path):
        return 0
    else:
        existing = len(os.listdir(directory_path))
        print("Already downloaded files:", existing)
        return existing

def download_image_if_not_exists(filepath, url):
    if not os.path.exists(filepath):
        return download_image(url, filepath)
    else:
        print("Skipping file, already exists:", filepath)
        return False

def download_image(url, filepath):
    try:
        with urllib.request.urlopen(url) as response, open(filepath, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        return True
    except urllib.error.HTTPError as e:
        print("Download failed:", e)
        return False

def zip_folder(zip_name, folder_path):
    shutil.make_archive(zip_name.replace('.zip', ''), 'zip', folder_path)
