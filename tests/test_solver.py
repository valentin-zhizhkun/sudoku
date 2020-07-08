from solver import solve

def test_solve():
    t = [[9,0,0, 0,1,8, 5,4,0],
         [0,0,5, 6,0,0, 0,9,2],
         [0,1,0, 0,0,0, 6,0,0],

         [6,0,9, 4,0,7, 0,0,1],
         [5,2,0, 0,0,0, 0,7,3],
         [8,0,0, 9,0,2, 4,0,5],

         [0,0,8, 0,0,0, 0,1,1],
         [7,4,0, 0,0,6, 2,0,0],
         [0,9,6, 5,2,0, 0,0,4]]

    assert solve(t) is True
    assert t == [
         [9,6,2, 3,1,8, 5,4,7],
         [3,8,5, 6,7,4, 1,9,2],
         [4,1,7, 2,9,5, 6,3,8],

         [6,3,9, 4,5,7, 8,2,1],
         [5,2,4, 8,6,1, 9,7,3],
         [8,7,1, 9,3,2, 4,6,5],

         [2,5,8, 7,4,9, 3,1,1],
         [7,4,3, 1,8,6, 2,5,9],
         [1,9,6, 5,2,3, 7,8,4]]


def test_no_solution():
    # Same grid, but with impossible "7" in position (0, 1)
    t = [[9,7,0, 0,1,8, 5,4,0],
         [0,0,5, 6,0,0, 0,9,2],
         [0,1,0, 0,0,0, 6,0,0],

         [6,0,9, 4,0,7, 0,0,1],
         [5,2,0, 0,0,0, 0,7,3],
         [8,0,0, 9,0,2, 4,0,5],

         [0,0,8, 0,0,0, 0,1,1],
         [7,4,0, 0,0,6, 2,0,0],
         [0,9,6, 5,2,0, 0,0,4]]

    assert solve(t) is False