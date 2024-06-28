import pytest
from PIL import Image
from pathlib import Path

from ..libs.draw import draw_tile, draw_tiles, draw_big_image, \
    IMAGE_PAD_PX, X, Y


@pytest.fixture
def setup_images(tmpdir_factory):
    sizes = [(50, 50), (50, 50), (50, 50), (50, 50)]

    image_paths = []
    tmpdir = tmpdir_factory.mktemp('dir1')
    for i, size in enumerate(sizes):
        img_path = str(tmpdir / f"img_{i}.png")
        color = (i * 50, i * 50, i * 50)  # dummy color
        with Image.new('RGB', size, color) as img:
            img.save(img_path)
        image_paths.append(img_path)
    return image_paths


def test_draw_tile():
    """
        draw black and red tiles on grid[1, 2] with white background
        check pixel's color in expected positions
    """
    img_size = (20, 20)
    tile_size = (40, 40)

    color_white = (255, 255, 255)
    color_black = (0, 0, 0)
    color_red = (255, 0, 0)

    canvas = Image.new('RGB', (120, 60), color_white)
    image1 = Image.new('RGB', img_size, color_black)
    image2 = Image.new('RGB', img_size, color_red)

    pos1 = (0, 0)
    draw_tile(canvas, image1, pos1, tile_size)

    pos2 = (tile_size[X] + IMAGE_PAD_PX*2, 0)
    draw_tile(canvas, image2, pos2, tile_size)

    offset = \
        (tile_size[X] - img_size[X]) // 2, \
        (tile_size[Y] - img_size[Y]) // 2

    # pad + tile1 + pad | pad + tile2 + pad

    # tile 1
    test_pos1 = (IMAGE_PAD_PX + offset[X], IMAGE_PAD_PX + offset[Y])
    assert canvas.getpixel(test_pos1) == color_black

    # tile 2
    test_pos2 = (IMAGE_PAD_PX + tile_size[X] + IMAGE_PAD_PX + IMAGE_PAD_PX + offset[X], IMAGE_PAD_PX + offset[Y])  # for readability
    assert canvas.getpixel(test_pos2) == color_red


def test_draw_tiles(setup_images):
    """
        draw tiles on grid[2, 2] with white background
        check pixel's color is not white in expected positions
    """
    tile_size = (50, 50)
    grid_size = (2, 2)

    color_white = (255, 255, 255)

    canvas_size = (
        (tile_size[X] + IMAGE_PAD_PX * 2) * grid_size[X],
        (tile_size[Y] + IMAGE_PAD_PX * 2) * grid_size[Y]
    )
    canvas = Image.new('RGB', canvas_size, color_white)

    draw_tiles(canvas, setup_images, tile_size, grid_size)

    for tile_x in range(grid_size[X]):
        for tile_y in range(grid_size[Y]):
            pos_x = tile_x * (tile_size[X] + IMAGE_PAD_PX * 2) + IMAGE_PAD_PX
            pos_y = tile_y * (tile_size[Y] + IMAGE_PAD_PX * 2) + IMAGE_PAD_PX
            assert canvas.getpixel((pos_x, pos_y)) != color_white


def test_draw_big_image(setup_images, tmpdir):
    output_file = tmpdir / "output.tiff"
    draw_big_image(setup_images, output_file=output_file)

    assert Path(output_file).exists()
    with Image.open(output_file) as img:
        assert img.format == 'TIFF'
