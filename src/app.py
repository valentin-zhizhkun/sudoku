"""AWS Lambda implementation for the Sudoku solver"""
import urllib.request
import copy
import json

import image
import grid
import digit
import solver


digit.initialize_predictor()


def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        url = body['url']
    except Exception as e:
        return {
            'statusCode': 400,
            'body': 'Cannot get url from request: %s' % e,
        }
    img_data = urllib.request.urlopen(url)

    img, bitmap = image.read_image(img_data)
    cells = grid.detect_filled_cells(bitmap)
    sudoku = [[0 for _ in range(9)] for _ in range(9)]
    for cell in cells:
        value = digit.predict(cell[0])
        pos = cell[2]
        sudoku[pos[0]][pos[1]] = int(value)
    result = copy.deepcopy(sudoku)
    if not solver.solve(result):
        result = None

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST',
        },
        'body': json.dumps({
            'input': sudoku,
            'solved': result,
        }),
    }