"""Sudoku solver implementation"""

def can_put(t, i, j, v):
    """Tell whether we can put digit v in position (i, j) in grid t"""
    for x in range(9):
        if t[x][j] == v:
            return False
        if t[i][x] == v:
            return False
    i0 = (i // 3) * 3
    j0 = (j // 3) * 3
    for x in range(i0, i0 + 3):
        for y in range(j0, j0 + 3):
            if t[x][y] == v:
                return False
    return True


def solve(t):
    """Fill Sudoku grid t and return True; otherwise, return False"""
    for i in range(9):
        for j in range(9):
            if t[i][j] == 0:
                for v in range(1, 10):
                    if can_put(t, i, j, v):
                        t[i][j] = v
                        if solve(t):
                            return True
                        # Try another value
                        t[i][j] = 0
                # No suitable value for position (i, j)
                return False
    # Filled all positions
    return True
