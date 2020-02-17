import os

default_input_file = 'february_hashi_puzzles.txt'


def get_input_file():
    input_files = ['february_hashi_puzzles.txt']

    for file in [file for file in os.listdir('submissions/Rob/output_files/') if file[-4:] == '.txt']:
        input_files.append(f'submissions/Rob/output_files/{file}')

    input_files = {str(i): file for i, file in enumerate(input_files)}

    while True:
        print('Input files')
        print('\n'.join([str(key) + ': ' + file for key, file in input_files.items()]))
        txt = input(f'Please select input file (0 - {len(input_files) - 1}): ') or '0'
        if txt not in input_files:
            print('Invalid input')
            continue

        return input_files[txt]


def select_puzzles(puzzles):
    puzzle_numbers = input_number_range('Select puzzles', default=f'0-{len(puzzles) - 1}')
    return puzzles[puzzle_numbers['min']:puzzle_numbers['max'] + 1]


def select_yes_no(title, default='no'):
    while True:
        txt = input(f'{title}: ({default})') or default
        return True if txt in ('yes', 'y', '1', 'true', 'True') else False


def input_number_range(title, default=None):
    description = title + f' ({default})' if default is not None else ''
    while True:
        txt = input(f'{description}: ') or str(default)

        split_txt = txt.split('-')
        if txt.isdigit():
            return {'min': int(txt), 'max': int(txt)}
        elif len(split_txt) == 2 and split_txt[0].isdigit() and split_txt[1].isdigit():
            return {'min': int(split_txt[0]), 'max': int(split_txt[1])}

        print('Invalid input')


def input_number(title, default=None):
    description = title + f' ({default})' if default is not None else ''
    while True:
        txt = input(f'{description}: ') or str(default)

        if txt.isdigit():
            return int(txt)

        print('Invalid input')


def input_string(title, default=None):
    description = title + f' ({default})' if default is not None else ''
    while True:
        return input(f'{description}: ') or str(default)
