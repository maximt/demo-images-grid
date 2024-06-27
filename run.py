from PIL import Image

from files import get_all_files
from draw import draw_grid


def run():
    dirs = [
        '../data/1388_6_Наклейки 3-D_2',
        '../data/1388_2_Наклейки 3-D_1',
        '../data/1388_12_Наклейки 3-D_3',
        '../data/1369_12_Наклейки 3-D_3',
    ]

    files = get_all_files(dirs)
    draw_grid(files, '../output.tiff')


if __name__ == "__main__":
    run()
