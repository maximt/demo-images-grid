import argparse
from PIL import Image

from libs.files import get_all_files, filter_valid_images
from libs.draw import draw_big_image


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('dirs', nargs='+', help='Input directories')
    parser.add_argument('-o', '--output', type=str, help='Output file')
    return parser.parse_args()


def run():
    args = parse_args()

    # dirs = [
    #     '../data/1388_6_Наклейки 3-D_2',
    #     '../data/1388_2_Наклейки 3-D_1',
    #     '../data/1388_12_Наклейки 3-D_3',
    #     '../data/1369_12_Наклейки 3-D_3',
    # ]

    if not args.dirs:
        print("Input directories are required")
        return
    output_file = args.output if args.output else 'output.tiff'

    try:
        files = get_all_files(args.dirs)
        valid_files = filter_valid_images(files)

        print("Total files:", len(files))
        print("Valid files:", len(valid_files))

        draw_big_image(valid_files, output_file)

        print("File saved:", output_file)
    except Exception as e:
        print("Image cannot be created")
        print('Error:', e)


if __name__ == "__main__":
    run()
