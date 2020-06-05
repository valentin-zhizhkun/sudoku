import numpy as np
import pytest

import grid
import image

# Helper to generate bitmaps
def _bitmap(rows):
    return np.array([
        [False if p == '.' else True for p in row]
        for row in rows
    ])


def test_detect_vertical_segments():
    a = _bitmap([
        '.... .............',
        ' .   .   .   .   .',
        '....... ... ......',
        ' .   .   .   .   .',
        '... .... ..... ...',
        ' .   .   .   .   .',
        '..................',
        '        ..       .',

    ])
    # Four 1-pixel-high segments
    assert grid.detect_vertical_segments(a, num_segments=4) \
           == [(1, 1), (3, 3), (5, 5), (7, 7)]


@pytest.mark.parametrize('example,ext', [
    (1, 'jpg'),
    (2, 'png'),
    (3, 'jpg'),
    (4, 'jpg'),
    (5, 'png'),
])
def test_detection(example, ext):
    im, a = image.read_image(f'data/sudoku{example}.{ext}')
    expected_cells = eval(open(f'data/sudoku{example}.gold').read())
    cells = grid.detect_filled_cells(a)
    # Cell coordinates and positions should be as expected
    coords = [c[1] for c in cells]
    pos = [c[2] for c in cells]
    assert coords == expected_cells['coords']
    assert pos == expected_cells['pos']
    #image.show_cells(a, cells)
