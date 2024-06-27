from pathlib import Path
from PIL import Image


ALLOW_IMAGE_EXT = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']


def get_dir_files(dir_path: str, ext: str) -> list[str]:
    path = Path(dir_path)
    files = [str(file) for file in path.rglob(ext, case_sensitive=False) if file.is_file()]
    return files


def get_all_files(dirs: list[str]) -> list[str]:
    all_files = []
    for dir_path in dirs:
        for ext in ALLOW_IMAGE_EXT:
            files = get_dir_files(dir_path, ext)
            all_files.extend(files)
    return all_files


def get_image_size(image_path: str) -> tuple[int, int]:
    with Image.open(image_path) as img:
        return img.size


def is_valid_image(image_path: str) -> bool:
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception as e:
        print('Invalid image: ', image_path)
        return False


def filter_valid_images(files: list[str]) -> list[str]:
    return [file for file in files if is_valid_image(file)]
