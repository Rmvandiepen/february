import pdb
import copy
import time
from datetime import date
from random import randint

import input_handling
from cell import Cell
from common import Direction, Quiting, BackToMenu
from grid import Grid


class CannotMakeException(Exception):
    pass


class RecreateCells(Exception):
    pass


class RecreateConnecions(Exception):
    pass


settings = None


class Settings:
    request_input_during = False
    request_input_after = False
    print_grid_after_solve = True
    verbose = False
    create_connections_tries = 100
    create_cells_tries = 100

    def __init__(self):
        pass

    def change_settings(self):
        self.request_input_during = input_handling.select_yes_no('Request input during')
        self.request_input_after = input_handling.select_yes_no('Request input after')
        self.print_grid_after_solve = input_handling.select_yes_no('Print grid after solve', 'yes')
        self.verbose = input_handling.select_yes_no('Verbose')
        self.create_connections_tries = input_handling.input_number('Create connection tries', default=self.create_connections_tries)
        self.create_cells_tries = input_handling.input_number('Create cells tries', default=self.create_cells_tries)


def printt(*args, **kwargs):
    if settings.verbose:
        print(*args, **kwargs)


def init_generate_puzzles():
    width = 10
    height = 10
    amount_of_cells = 14
    amount_of_puzzles = 1
    output_file = 'auto_' + date.today().strftime("%Y%m%d")
    settings = None

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


def generate_puzzles(width, height, num_of_cells, amount_of_puzzles, output_file, use_settings=None):
    global settings
    settings = use_settings or Settings()
    amount_generated = 0
    while True:
        try:
            final_cells = do_generation(width, height, num_of_cells)
        except RecreateCells:
            continue

        grid = Grid(width, height, final_cells, use_advanced=True)
        if not grid.solve():
            printt('Still failed to solve!!')
            continue

        if settings.print_grid_after_solve:
            print(grid)

        with open(f'submissions/Rob/output_files/{output_file}.txt', 'a') as file:
            file.write(grid.export() + '\n')

        if settings.request_input_after:
            if not settings.print_grid_after_solve:
                print(grid)

            if grid.advanced:
                print(f'Required advanced solving!!!!!!!')

            txt = input('Want to (c)ontinue, (s)olve slowly, (m)enu or (q)uit?')
            if txt == 'm':
                raise BackToMenu()
            if txt == 'q':
                raise Quiting()
            elif txt == 's':
                grid = Grid(width, height, final_cells, use_advanced=True)
                grid.solve_slowly = True
                grid.solve()

        amount_generated += 1
        if amount_generated == amount_of_puzzles:
            print('Done generating puzzles!')
            return


def do_generation(width, height, num_of_cells):
    global settings

    num_of_cells = randint(num_of_cells['min'], num_of_cells['max'])
    tries2 = 0
    while True:
        tries2 += 1
        try:
            generated_cells = generate_cells(width, height, num_of_cells)
            printt(f'Try: {tries2} with {len(generated_cells)} cells')

            tries = 0
            while tries < settings.create_connections_tries:
                tries += 1
                try:
                    final_cells = generate_connections(width, height, generated_cells)
                except RecreateConnecions:
                    printt(f'Failed, restarting creation of connections. tries: {tries}')
                    continue

                grid = Grid(width, height, final_cells, use_advanced=True)
                if grid.solve():
                    printt('Succeeded after {tries} tries')
                    return final_cells
            printt(f'Failed to create connections {settings.create_connections_tries} times.')
        except RecreateCells:
            pass
        printt('Recreating cells')


def generate_cells(width, height, num_of_cells):
    global settings
    cells = []
    init_cell = {
        'x': randint(1, width - 2),
        'y': randint(1, height - 2),
        'value': 0
    }
    cells.append(init_cell)
    for _ in range(num_of_cells - 1):
        new_cell = None
        iteration = 0
        grid = Grid(width, height, cells, use_advanced=False)
        while new_cell is None:
            iteration += 1
            if iteration > settings.create_cells_tries:
                printt(f'Failed to create cells {settings.create_cells_tries} times.')
                raise RecreateCells()

            cell_data = cells[randint(0, len(cells) - 1)]
            cell = grid.get_cell_at(cell_data['x'], cell_data['y'])

            direction = Direction(randint(0, 1))
            positive = randint(0, 1)

            grid.make_connections()
            connection = cell.get_connection(direction, positive)
            if connection is not None:
                continue

            new_cell = make_new_cell(width, height, cell_data['x'], cell_data['y'], direction, positive)
            if new_cell:
                for cell in cells:
                    if abs(new_cell['x'] - cell['x']) + abs(new_cell['y'] - cell['y']) <= 1:
                        new_cell = None
                        break

        cells.append(new_cell)
        printt(f'New cell created, {new_cell}\n')
    return cells


def generate_connections(width, height, from_cells):
    global settings

    from_cells = copy.deepcopy(from_cells)
    grid = Grid(width, height, from_cells)
    grid.make_connections()
    grid.make_intersections()

    while True:
        cells_to_process = [cell for cell in grid.cells if cell.value == 0 or not cell.solved]
        if len(cells_to_process) == 0:
            tmp_grid = Grid(width, height, [{
                'x': cell.x,
                'y': cell.y,
                'value': cell.value
            } for cell in grid.cells], use_advanced=True)
            if tmp_grid.solve():
                return [{
                    'x': cell.x,
                    'y': cell.y,
                    'value': cell.value
                } for cell in grid.cells]
            printt('No cells to process. Falling back cells with empty connections')
            cells_to_process = [cell for cell in grid.cells if len(empty_connections_for_cell(cell))]

        if len(cells_to_process) == 0:
            printt('Really no more cells to process!')
            raise RecreateConnecions()

        cells_to_process.sort(key=sort_cells_to_process)

        printt('Cells to process: ')
        for cell in cells_to_process:
            printt(cell, sort_cells_to_process(cell))

        cell_to_process = cells_to_process[0]
        printt(f'Processing cell: {cell_to_process}')

        free_connections = empty_connections_for_cell(cell_to_process)
        if len(free_connections) == 0:
            printt('No more free connections')
            raise RecreateConnecions()

        for i, connection in enumerate(free_connections):
            connection._unsolve(0, 2)
            bridges_on_connection = randint(0, 2)
            connection.cell1.value += bridges_on_connection
            connection.cell2.value += bridges_on_connection
            connection.solve(bridges_on_connection, cascade=False)
            printt(f'Created connection {connection}')
        printt(grid)

        if settings.request_input_during:
            txt = input('(c)ontinue, (d)ebug, (n)ew cells or (e)xit')
            if txt == 'd':
                pdb.set_trace()
            elif txt == 'n':
                raise RecreateCells()
            elif txt == 'e':
                exit()


def empty_connections_for_cell(cell):
    return [
        connection for connection in cell.connections if not connection.bridges and not any(
            [intersection.bridges for intersection in connection.intersections]
        )
    ]


def sort_cells_to_process(cell):
    return len(empty_connections_for_cell(cell))


def make_new_cell(width, height, x, y, direction, positive):
    if direction == Direction.HORIZONTAL:
        if positive:
            if x >= width - 2:
                return None
            from_x = x + 2
            to_x = width - 1
            distance = to_x - from_x
            random_num = randint(0, distance ** 2)
            from_the_end = int(random_num ** 0.5)
            x = to_x - from_the_end
            return {
                'x': x,
                'y': y,
                'value': 0
            }
        else:
            if x <= 1:
                return None
            from_x = 0
            to_x = x - 2
            distance = to_x - from_x
            random_num = randint(0, distance ** 2)
            from_the_start = int(random_num ** 0.5)
            x = from_x + from_the_start
            return {
                'x': x,
                'y': y,
                'value': 0
            }
    else:
        if positive:
            if y >= height - 2:
                return None
            from_y = y + 2
            to_y = height - 1
            distance = to_y - from_y
            random_num = randint(0, distance ** 2)
            from_the_end = int(random_num ** 0.5)
            y = to_y - from_the_end
            return {
                'x': x,
                'y': y,
                'value': 0
            }
        else:
            if y <= 1:
                return None
            from_y = 0
            to_y = y - 2
            distance = to_y - from_y
            random_num = randint(0, distance ** 2)
            from_the_start = int(random_num ** 0.5)
            y = from_y + from_the_start
            return {
                'x': x,
                'y': y,
                'value': 0
            }
