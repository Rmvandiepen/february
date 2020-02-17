from datetime import date

import input_handling
from generator import generate_puzzles, Settings

REQUEST_INPUT = True

width = 10
height = 10
amount_of_cells = 14
amount_of_puzzles = 1
output_file = 'auto_' + date.today().strftime("%Y%m%d")
settings = None

if REQUEST_INPUT:
    print('Please fill in the following values.')
    width = input_handling.input_number('Width', default=width)
    height = input_handling.input_number('Height', default=height)
    amount_of_cells = input_handling.input_number_range('Amount of cells', default=amount_of_cells)
    amount_of_puzzles = input_handling.input_number('Amount of puzzles', default=amount_of_puzzles)
    output_file = input_handling.input_string('Output file', output_file)

    modify_settings = input_handling.select_yes_no('Want to change settings?', default='no')
    if modify_settings:
        settings = Settings()
        settings.change_settings()

generate_puzzles(width, height, amount_of_cells, amount_of_puzzles, output_file, use_settings=settings)
