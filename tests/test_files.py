import pytest
from PIL import Image

from ..files import get_image_size, get_dir_files, get_all_files


def create_image(path, size):
    with Image.new('RGB', size, (255, 255, 255)) as image:
        image.save(path)


@pytest.fixture(scope='module')
def setup_images(tmpdir_factory):
    tmpdir1 = tmpdir_factory.mktemp('dir1')
    tmpdir2 = tmpdir_factory.mktemp('dir2')

    images = [
        {
            'path': tmpdir1,
            'files': {
                '1.png': (tmpdir1 / '1.png', (100, 100)),
                '2.jpg': (tmpdir1 / '2.jpg', (500, 500)),
                '3.png': (tmpdir1 / '3.png', (800, 800)),
            }
        },
        {
            'path': tmpdir2,
            'files': {
                '4.png': (tmpdir2 / '4.png', (100, 100)),
                '5.png': (tmpdir2 / '5.png', (500, 500)),
                '6.ico': (tmpdir2 / '6.ico', (800, 800)),
            }
        }
    ]

    [create_image(filename, size) for dir in images for filename, size in dir['files'].values()]

    return images


@pytest.mark.parametrize('expected_files', [
    ('1.png', '3.png')
])
def test_get_dir_files(setup_images, expected_files):
    path = setup_images[0]['path']
    expected_files_ = [path / filename for filename in expected_files]

    files = get_dir_files(path, '*.png')

    assert set(files) == set(expected_files_)


@pytest.mark.parametrize('expected_files', [
    (('1.png', '2.jpg', '3.png'), ('4.png', '5.png'))
])
def test_get_all_files(setup_images, expected_files):
    dirs = [dir['path'] for dir in setup_images]
    expected_files_ = [
        str(setup['path'] / filename)
        for index, setup in enumerate(setup_images)
        for filename in expected_files[index]
    ]

    files = get_all_files(dirs)
    
    assert set(files) == set(expected_files_)


@pytest.mark.parametrize('filename, expected_size', [
    ('1.png', (100, 100)),
    ('2.jpg', (500, 500)),
    ('3.png', (800, 800))
])
def test_get_image_size(setup_images, filename, expected_size):
    image_path, _ = setup_images[0]['files'][filename]
    assert get_image_size(image_path) == expected_size
