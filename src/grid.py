"""Sudoku grid recognition"""


def detect_horizontal_lines(a, num):
    """Find all horizontal dark lines in a bitmap, assuming there are at least num"""
    weights = [
        sum(map(int, line)) / len(line)  # Line brightness
        for line in a
    ]
    # Take num darkest lines, and report all that are at least as dark
    darkest = max(sorted(weights)[:num])
    return [w <= darkest for w in weights]


def detect_vertical_segments(a, num_segments=9):
    # There should be at least 8 horizontal lines in a Sudoku image
    num_lines = num_segments - 1
    height = a.shape[0]
    while num_lines <= max(height // 20, num_segments):  # Not too many lines
        h_lines = detect_horizontal_lines(a, num_lines)
        # Grid cells cannot be too small or too big
        min_segment_h, max_segment_h = height / 12, height / 7
        res = []
        i = 0
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
        # Not enough segments found: try with more lines
        num_lines += 2

    return []  # Nothing found

