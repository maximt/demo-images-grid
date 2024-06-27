import math

from files import get_image_size


def get_tile_size(files: list[str]) -> tuple[int, int]:
    max_width = 0
    max_height = 0
    for file in files:
        width, height = get_image_size(file)
        max_width = max(max_width, width)
        max_height = max(max_height, height)
    return max_width, max_height


def get_grid_size(files_count: int) -> tuple[int, int]:
    tiles_x = math.ceil(math.sqrt(files_count))
    tiles_y = math.ceil(files_count / tiles_x)
    return tiles_x, tiles_y
