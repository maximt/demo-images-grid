from PIL import Image, ImageFile

from .grid import get_tile_size, get_grid_size


IMAGE_PAD_PX = 10
X = 0
Y = 1


def draw_tile(canvas: Image.Image, image: ImageFile.ImageFile, pos: tuple[int, int], tile_size: tuple[int, int]):
    # place image to center of tile
    img_size = image.size
    offset = \
        (tile_size[X] - img_size[X]) // 2, \
        (tile_size[Y] - img_size[Y]) // 2
    pos_ajusted = \
        pos[X] + offset[X] + IMAGE_PAD_PX, \
        pos[Y] + offset[Y] + IMAGE_PAD_PX
    canvas.paste(image, pos_ajusted)


def draw_tiles(canvas: Image.Image, files: list[str],
               tile_size: tuple[int, int], grid_size: tuple[int, int]):
    tile_x = 0
    tile_y = 0
    for file in files:
        pos = \
            tile_x * (tile_size[X] + IMAGE_PAD_PX * 2), \
            tile_y * (tile_size[Y] + IMAGE_PAD_PX * 2)

        with Image.open(file) as image:
            draw_tile(canvas, image, pos, tile_size)

        tile_x += 1
        if tile_x >= grid_size[0]:
            tile_x = 0
            tile_y += 1


def draw_big_image(files: list[str], output_file: str = 'output.tiff'):
    if not files:
        raise ValueError('Input files are required')

    tile_size = get_tile_size(files)

    if tile_size[X] == 0 or tile_size[Y] == 0:
        raise ValueError('Tile size is zero')

    grid_size = get_grid_size(len(files))

    canvas_size = \
        (tile_size[X] + IMAGE_PAD_PX * 2) * grid_size[X], \
        (tile_size[Y] + IMAGE_PAD_PX * 2) * grid_size[Y]

    with Image.new('RGB', canvas_size, (255, 255, 255)) as canvas:
        draw_tiles(canvas, files, tile_size, grid_size)
        canvas.save(output_file, 'TIFF')
