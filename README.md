## Sudoku solver

This is a toy proof-of-concept project that I
used to play around with simple image parsing.

The task is to solve a standard Sudoku puzzle given
a reasonable-quality image of its initial 9x9 grid
with some of the digits filled.
See https://en.wikipedia.org/wiki/Sudoku for
details on the puzzle.

The system is implemented in Python and
follows these steps:

* Converting input image to a monochrome 
  bitmap - a Numpy 2d array, for simplicity
* Grid detection: identify horizontal and vertical
  "black" lines that are likely to define a
  9x9 grid of "white-ish" cells in the image.
  This is done heuristically using a few
  fine-tuned parameteters. See src/grid.py
* For each non-empty cell identified in the grid,
  apply a classifier to determine which of the 
  digits 1, 2,..., 9 it contains. The classifier
  is a simple kNN model trained on the digits
  subset of [Chars74K dataset](http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/).
  I used 420 instances per digit (removing
  examples from a few eccentric fonts). I used 
  a quick N-fold cross-validation to select
  reasonable parameters of the classifier.
  See src/digit.py. The trained model is included
  in the repository (src/model.dat)
* After digits in the cells are determined, a
  straightforward Sudoku solver finds the
  final solution using search with backtracking.
  See src/sudoku.py
* The system is deployed to AWS Lambda using SAM 
  and exposed as arestful API. See src/app.py,
  template.yaml and samconfig.toml
* There is a simple frontend page to try out
  the system: frontend/index.html. You can open
  it in your browser to check out the system
  in action.
