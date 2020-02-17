import time

import input_handling
from common import readfile
from grid import Grid


def solve():
    file_location = input_handling.get_input_file()

    before_read = time.time()
    puzzles = readfile(file_location)
    print('Time to read: ', time.time() - before_read)

    puzzles = input_handling.select_puzzles(puzzles)

    use_advanced_solving = input_handling.select_yes_no('Advanced techniques', 'yes')
    print_results = input_handling.select_yes_no('Print result', 'yes')
    slow_solve = input_handling.select_yes_no('Slow solve')
    show_min_bridges = input_handling.select_yes_no('Show min bridges')

    before_solve = time.time()
    for i, puzzle in enumerate(puzzles):
        grid = Grid(**puzzle, use_advanced=use_advanced_solving)
        if slow_solve:
            grid.solve_slowly = True
        if show_min_bridges:
            grid.show_min_bridges = True

        solved = grid.solve()
        if print_results:
            print('Cells: ', len(grid.cells))
            print(grid)
        if solved:
            print(f'Solved {i}' + (' (Required advanced techniques)' if grid.advanced else ''))
        else:
            print(f'Couldn\'t solve {i}')

    time_to_solve = time.time() - before_solve
    print('Time to solve: ', time_to_solve)
    print(f'Average of {int(time_to_solve / (len(puzzles))*1000)} ms per puzzle')
