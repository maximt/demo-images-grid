from pathlib import Path
import math
from PIL import Image


ALLOW_IMAGE_EXT = ['*.png', '*.jpg', '*.jpeg', '*.gif']
IMAGE_PAD_PX = 10


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
        width, height = img.size
    return width, height


def get_grid_size(files_count: int) -> tuple[int, int]:
    tiles_x = math.ceil(math.sqrt(files_count))
    tiles_y = math.ceil(files_count / tiles_x)
    return tiles_x, tiles_y


def get_tile_size(files: list[str]) -> tuple[int, int]:
    max_width = 0
    max_height = 0
    for file in files:
        width, height = get_image_size(file)
        max_width = max(max_width, width)
        max_height = max(max_height, height)
    return max_width, max_height


def draw_tile(canvas: Image, image_path: str, x: int, y: int):
    img_x = x + IMAGE_PAD_PX
    img_y = y + IMAGE_PAD_PX
    image = Image.open(image_path)
    canvas.paste(image, (img_x, img_y))


def draw_mosaic(files: list[str], output_file: str = 'output.tiff'):
    tile_width, tile_height = get_tile_size(files)
    tiles_x, tiles_y = get_grid_size(len(files))

    canvas_size = \
        (tile_width + IMAGE_PAD_PX * 2) * tiles_x, \
        (tile_height + IMAGE_PAD_PX * 2) * tiles_y

    canvas_size = (image_width, image_height)
    canvas = Image.new('RGB', canvas_size, (255, 255, 255))

    tile_x = 0
    tile_y = 0
    for file in files:
        x = tile_x * (tile_width + IMAGE_PAD_PX * 2)
        y = tile_y * (tile_height + IMAGE_PAD_PX * 2)

        draw_tile(canvas, file, x, y)

        tile_x += 1
        if tile_x >= tiles_x:
            tile_x = 0
            tile_y += 1

    canvas.save(output_file, 'TIFF')


def run():
    dirs = [
        '../data/1388_6_Наклейки 3-D_2',
        '../data/1388_2_Наклейки 3-D_1',
        '../data/1388_12_Наклейки 3-D_3',
        '../data/1369_12_Наклейки 3-D_3',
    ]

    files = get_all_files(dirs)
    draw_mosaic(files, 'output.tiff')



if __name__ == "__main__":
    run()
