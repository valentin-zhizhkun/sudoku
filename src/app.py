"""AWS Lambda implementation for the Sudoku solver"""
import urllib.request

import image
import grid
import digit


digit.initialize_predictor()


def lambda_handler(event, context):
    url = event['queryStringParameters'].get('url')
    if not url:
        return {
            'statusCode': 400,
            'body': 'Missing url parameter'
        }
    req = urllib.request.urlopen(url)
    img, bitmap = image.read_image(req)
    cells = grid.detect_filled_cells(bitmap)
    sudoku = [[0 for _ in range(9)] for _ in range(9)]
    for cell in cells:
        value = digit.predict(cell[0])
        pos = cell[2]
        sudoku[pos[0]][pos[1]] = value
    return {
        'statusCode': 200,
        'body': str(sudoku)
    }