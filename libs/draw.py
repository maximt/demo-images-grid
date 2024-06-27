from PIL import Image

from .grid import get_tile_size, get_grid_size


IMAGE_PAD_PX = 10
X = 0
Y = 1


def draw_tile(canvas: Image, image: Image, x: int, y: int):
    img_x = x + IMAGE_PAD_PX
    img_y = y + IMAGE_PAD_PX
    canvas.paste(image, (img_x, img_y))


def draw_tiles(canvas: Image, files: list[str],
               tile_size: tuple[int, int], grid_size: tuple[int, int]):
    tile_x = 0
    tile_y = 0
    for file in files:
        pos = \
            tile_x * (tile_size[X] + IMAGE_PAD_PX * 2), \
            tile_y * (tile_size[Y] + IMAGE_PAD_PX * 2)

        with Image.open(file) as image:
            draw_tile(canvas, image, pos[X], pos[Y])

        tile_x += 1
        if tile_x >= grid_size[0]:
            tile_x = 0
            tile_y += 1


def draw_big_image(files: list[str], output_file: str = 'output.tiff'):
    tile_size = get_tile_size(files)
    grid_size = get_grid_size(len(files))

    canvas_size = \
        (tile_size[X] + IMAGE_PAD_PX * 2) * grid_size[X], \
        (tile_size[Y] + IMAGE_PAD_PX * 2) * grid_size[Y]

    with Image.new('RGB', canvas_size, (255, 255, 255)) as canvas:
        draw_tiles(canvas, files, tile_size, grid_size)
        canvas.save(output_file, 'TIFF')
