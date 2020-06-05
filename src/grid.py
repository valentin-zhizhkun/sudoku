"""Sudoku grid recognition"""
import numpy as np

import image

def get_lines_brightness(a):
    br = [
        sum(map(int, line)) / len(line)  # Line brightness
        for line in a
    ]
    return br, sorted(br)

def detect_horizontal_lines(a, brightness, num):
    """Find dark lines, assuming there are at least num"""
    # Take num darkest lines, and report all that are at least as dark (allow 10%)
    darkest = max(brightness[1][:num])
    return [w <= darkest * 1.1 for w in brightness[0]]


def detect_vertical_segments(a, num_segments=9):
    height = a.shape[0]
    # At least 4% of horizontal lines should define grid boundary
    num_lines = max(height // 25, num_segments - 1)
    # But not too many lines
    max_num_lines = max(height // 10, num_segments + 1)
    brightness = get_lines_brightness(a)
    while num_lines <= max_num_lines:
        h_lines = detect_horizontal_lines(a, brightness, num_lines)
        # Grid cells cannot be too small or too big
        min_segment_h, max_segment_h = height / 12, height / 7
        res = []
        i = 0
        # Skip top all-white lines
        while i < len(a) and all(a[i]):
            i += 1
        while i < height - min_segment_h:
            if h_lines[i]:
                # Skip dark lines
                i += 1
                continue
            j = i
            while j < height and not h_lines[j]:
                # Extend current segment
                j += 1
            if i + min_segment_h < j < i + max_segment_h:
                # Found an acceptable segment
                res.append((i, j - 1))
            i = j + 1
        if len(res) >= num_segments:
            # Ignore all but first 9 segments (e.g. image footer etc.)
            return res[:num_segments]
        # Not enough segments found: try with more lines that we detected just now
        num_lines = sum(h_lines) + 1

    return []  # Nothing found


def detect_filled_cells(a):
    """Return list of cells: [(bitmap, top-left-coords, position-in-grid), ... ]"""
    v_segments = detect_vertical_segments(a)
    h_segments = detect_vertical_segments(np.transpose(a))

    cells = []
    # Cells are at intersections of vertical and horizontal segments
    for vi, v in enumerate(v_segments):
        for hi, h in enumerate(h_segments):
            c = a[v[0]:v[1], h[0]:h[1]]
            pos = v[0], h[0]
            c, pos = image.shrink(c, pos)
            if c.shape > (0, 0):
                cells.append((c, pos, (vi, hi)))
    return cells
