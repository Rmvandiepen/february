import os

import input_handling
from common import readfile, Direction
from grid import Grid
from key_poller import KeyPoller


def process_input(grid, input_val):
    if input_val == ' ':
        grid.creating_bridges = not grid.creating_bridges
    elif grid.creating_bridges:
        if input_val == 'w':
            direction = Direction.VERTICAL
            positive = 0
        elif input_val == 's':
            direction = Direction.VERTICAL
            positive = 1
        elif input_val == 'a':
            direction = Direction.HORIZONTAL
            positive = 0
        elif input_val == 'd':
            direction = Direction.HORIZONTAL
            positive = 1
        else:
            return

        cell = grid.get_cell_at(grid.cursor_x, grid.cursor_y)
        if not cell:
            return

        connection = cell.get_connection(direction, positive)
        if not connection:
            return

        current_bridges = connection.bridges or 0
        new_bridges = (current_bridges + 1) % 3
        connection.bridges = new_bridges
    else:
        if input_val == 'w':
            grid.cursor_y -= 1
            grid.cursor_y = grid.cursor_y % grid.height
        elif input_val == 's':
            grid.cursor_y += 1
            grid.cursor_y = grid.cursor_y % grid.height
        elif input_val == 'a':
            grid.cursor_x -= 1
            grid.cursor_x = grid.cursor_x % grid.width
        elif input_val == 'd':
            grid.cursor_x += 1
            grid.cursor_x = grid.cursor_x % grid.width

    os.system('clear')
    print(grid)


def play_puzzles():
    file_location = input_handling.get_input_file()
    puzzles = readfile(file_location)
    puzzles = input_handling.select_puzzles(puzzles)

    for puzzle in puzzles:
        grid = Grid(**puzzle)
        grid.make_connections()
        grid.show_cursor = True
        grid.color_solved_cells = True

        os.system('clear')
        print(grid)

        with KeyPoller() as key_poller:
            while not grid.solved:
                i = key_poller.poll()
                if i is not None:
                    process_input(grid, i)

            print('Well done! Puzzle solved')
            input('Press return to continue. \n')

