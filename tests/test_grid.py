import numpy as np

import grid

# Helper to generate bitmaps
def _bitmap(rows):
    return np.array([
        [False if p == '.' else True for p in row]
        for row in rows
    ])


def test_detect_vertical_segments():
    a = _bitmap([
        '..................',
        ' .   .   .   .   .',
        '..................',
        ' .   .   .   .   .',
        '..................',
        ' .   .   .   .   .',
        '..................',
        '        ..       .',

    ])
    assert grid.detect_vertical_segments(a, num_segments=4) \
           == [(1, 1), (3, 3), (5, 5), (7, 7)]
