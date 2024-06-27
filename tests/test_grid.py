import pytest

from ..libs.grid import get_grid_size


@pytest.mark.parametrize("files_count, expected", [
    (1, (1, 1)),
    (2, (2, 1)),
    (3, (2, 2)),
    (4, (2, 2)),
    (5, (3, 2)),
    (6, (3, 2)),
    (7, (3, 3)),
    (8, (3, 3)),
    (9, (3, 3)),
    (10, (4, 3)),
    (15, (4, 4)),
    (16, (4, 4)),
])
def test_get_grid_size(files_count, expected):
    assert get_grid_size(files_count) == expected


def test_get_grid_size_capacity():
    for files_count in range(1, 1000):
        x, y = get_grid_size(files_count)
        grid_count = x * y
        assert grid_count >= files_count
