from PIL import Image

from grid import get_tile_size, get_grid_size


IMAGE_PAD_PX = 10


def draw_tile(canvas: Image, image_path: str, x: int, y: int):
    img_x = x + IMAGE_PAD_PX
    img_y = y + IMAGE_PAD_PX
    image = Image.open(image_path)
    canvas.paste(image, (img_x, img_y))


def draw_grid(files: list[str], output_file: str = 'output.tiff'):
    tile_width, tile_height = get_tile_size(files)
    tiles_x, tiles_y = get_grid_size(len(files))

    canvas_size = \
        (tile_width + IMAGE_PAD_PX * 2) * tiles_x, \
        (tile_height + IMAGE_PAD_PX * 2) * tiles_y

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
