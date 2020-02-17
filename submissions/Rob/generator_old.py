from random import randint

from cell import Cell
from common import Direction
from generator import CannotMakeException, make_new_cell
from grid import Grid


def generate_puzzle_old(width, height, num_of_cells):
    unsolvable = 0
    cannot_make = 0
    too_many_bridges = 0
    cells = []
    init_cell = {
        'x': randint(1, width - 2),
        'y': randint(1, height - 2),
        'value': 0
    }
    cells.append(init_cell)
    while len(cells) != num_of_cells:
        # print(len(cells), unsolvable, cannot_make, too_many_bridges)
        # print(cells)
        grid = Grid(width, height, cells, use_advanced=False)
        grid.solve()

        cell_data = cells[randint(0, len(cells) - 1)]
        cell = grid.get_cell_at(cell_data['x'], cell_data['y'])

        direction = Direction(randint(0, 1))
        positive = randint(0, 1)

        connection = cell.get_connection(direction, positive)
        if not connection:
            try:
                new_cell = Cell(**make_new_cell(width, height, cell.x, cell.y, direction, positive), grid=None)
                if grid.get_cell_at(new_cell.x - 1, new_cell.y) \
                        or grid.get_cell_at(new_cell.x + 1, new_cell.y) \
                        or grid.get_cell_at(new_cell.x, new_cell.y - 1) \
                        or grid.get_cell_at(new_cell.x, new_cell.y + 1):
                    raise CannotMakeException()
                # print('new cell', new_cell)
            except CannotMakeException:
                cannot_make += 1
                if cannot_make > 50:
                    print('Cannot make, removing last one. len: ', len(cells))
                    print(grid)
                    cells = cells[:-1]
                    unsolvable = 0
                    too_many_bridges = 0
                    cannot_make = 0
                continue
            grid.cells.append(new_cell)
            grid.make_connections()

            connection = grid.get_connection(cell, new_cell)

        if connection.bridges == 2:
            too_many_bridges += 1
            if too_many_bridges > 50:
                print('Too many bridges, removing last one. len: ', len(cells))
                print(grid)
                cells = cells[:-1]
                unsolvable = 0
                too_many_bridges = 0
                cannot_make = 0
            continue

        # print('connection', connection)
        connection.cell1.value += 1
        connection.cell2.value += 1

        new_cells = [{
            'x': cell.x,
            'y': cell.y,
            'value': cell.value
        } for cell in grid.cells]

        grid = Grid(width, height, new_cells, use_advanced=True)
        # print(grid.export())
        if not grid.solve():
            unsolvable += 1
            # print('cannot solve!')
            # print(grid.cells)
            # print(grid._connections)
            # print(grid)
            if unsolvable > 50:
                print('Cannot solve 3, removing last one. len: ', len(new_cells))
                print(grid)
                # print(grid)
                cells = cells[:-1]
                unsolvable = 0
                too_many_bridges = 0
                cannot_make = 0
                connection.cell1.value -= 1
                connection.cell2.value -= 1
            continue

        unsolvable = 0
        too_many_bridges = 0
        cannot_make = 0
        cells = new_cells
        print(grid)

    grid = Grid(width, height, cells, use_advanced=True)
    print(grid.export())
    print(grid)
    solved = grid.solve()
    print(grid)
    print('Solved: ', solved)
    print(f'Advanced: {grid.advanced}')
