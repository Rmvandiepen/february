import os

import input_handling
from common import readfile, Direction, Quiting, BackToMenu
from grid import Grid
from key_poller import KeyPoller


class Next(Exception):
    pass


def process_input(grid, input_val):
    if input_val == ' ':
        grid.creating_bridges = not grid.creating_bridges
    elif input_val == 'r':
        for connection in grid._connections:
            connection._unsolve(0, 2)
    elif input_val == 'q':
        raise Quiting()
    elif input_val == 'm':
        raise BackToMenu()
    elif input_val == 'n':
        raise Next()
    elif input_val in ('w', 'a', 's', 'd'):
        if grid.creating_bridges:
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


def update_screen(grid):
    os.system('clear')
    print(grid)
    print('Use WASD to move around or to place bridges. ')
    print('Space to toggle between building bridges and moving around')
    print('(r) to reset puzzle, (n) for next puzzle, (m) back to menu, (q) to quit')


def play_puzzles():
    file_location = input_handling.get_input_file()
    puzzles = readfile(file_location)
    puzzles = input_handling.select_puzzles(puzzles)

    for puzzle in puzzles:
        grid = Grid(**puzzle)
        grid.make_connections()
        grid.show_cursor = True
        grid.color_solved_cells = True

        update_screen(grid)

        with KeyPoller() as key_poller:
            while True:
                i = key_poller.poll()
                if i is not None:
                    try:
                        process_input(grid, i)
                    except Next:
                        print('Going to the next puzzle')
                        break
                    update_screen(grid)

                    if grid.solved:
                        print('Well done! Puzzle solved')
                        input('Press return to continue. \n')
                        break
