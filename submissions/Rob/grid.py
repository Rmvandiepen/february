from cell import Cell
from common import Direction, between, drawing_map, ChainUnsolved
from connection import Connection


class Grid:
    height = None
    width = None
    cells = None
    _connections = None
    use_advanced = None
    advanced = None

    solve_slowly = False

    show_cursor = None
    cursor_x = 0
    cursor_y = 0
    creating_bridges = False
    color_solved_cells = False
    show_min_bridges = False
    remove_output_spaces = False

    def __init__(self, width, height, cells, use_advanced=False):
        self.height = height
        self.width = width
        self.cells = []
        for cell in cells:
            if isinstance(cell, Cell):
                self.cells.append(Cell(x=cell.x, y=cell.y, value=cell.value, grid=self))
            else:
                self.cells.append(Cell(**cell, grid=self))

        self.use_advanced = use_advanced

    def get_cell_at(self, x, y):
        for cell in self.cells:
            if cell.x == x and cell.y == y:
                return cell
        return None

    def make_connections(self):
        self._connections = []
        for cell in self.cells:
            cell.connections = []
        for cell in self.cells:
            for x in range(cell.x + 1, self.width):
                cell_at = self.get_cell_at(x, cell.y)
                if cell_at is not None:
                    connection = Connection(cell, cell_at, grid=self)
                    cell.add_connection(connection)
                    cell_at.add_connection(connection)
                    self._connections.append(connection)
                    break
            for y in range(cell.y + 1, self.height):
                cell_at = self.get_cell_at(cell.x, y)
                if cell_at is not None:
                    connection = Connection(cell, cell_at, grid=self)
                    cell.add_connection(connection)
                    cell_at.add_connection(connection)
                    self._connections.append(connection)
                    break

    def make_intersections(self):
        for connection1 in self._connections:
            for connection2 in self._connections:
                if connection1 == connection2 \
                        or connection1.direction == connection2.direction \
                        or connection1.direction != Direction.HORIZONTAL:
                    continue

                if between(connection1.cell1.x, connection1.cell2.x, connection2.cell1.x) \
                        and between(connection2.cell1.y, connection2.cell2.y, connection1.cell1.y):
                    connection1.intersections.append(connection2)
                    connection2.intersections.append(connection1)

    def get_connection(self, cell1, cell2):
        for connection in self._connections:
            if connection.cell1 == cell1 and connection.cell2 == cell2 \
                    or connection.cell1 == cell2 and connection.cell2 == cell1:
                return connection
        return None

    @property
    def solved_connections(self):
        return len([connection for connection in self._connections if connection.solved])

    @property
    def solved(self):
        all_cells_solved = all([cell.solved for cell in self.cells])
        if not all_cells_solved:
            return False

        try:
            cells_in_chain = list(self.cells[0].get_connected_cells({}))
        except ChainUnsolved:
            return False
        one_big_chain = len(cells_in_chain) == len(self.cells)
        return all_cells_solved and one_big_chain

    def solve(self):
        self.make_connections()
        self.make_intersections()

        for cell in self.cells:
            cell.try_connections()

        if not self.solved and self.use_advanced and not self.advanced:
            self.advanced = True
            for cell in self.cells:
                cell.try_connections()

        return self.solved

    def backtracking(self):
        self.make_connections()

        def do(offset):
            for i, connection in enumerate(self._connections[offset:]):
                if connection.bridges is None:
                    for bridges in range(0, min(2, connection.cell1.value_left(), connection.cell2.value_left()) + 1):
                        connection.bridges = bridges
                        do(offset + i + 1)
                        connection.bridges = None

            if self.solved:
                raise Exception()

        try:
            do(0)
        except Exception:
            return True
        return False

    def __repr__(self):
        result = []
        for _ in range(self.height):
            result.append([' '] * self.width)

        for cell in self.cells:
            result[cell.y][cell.x] = str(cell.value)
            if self.color_solved_cells:
                if cell.solved:
                    result[cell.y][cell.x] = f'\u001b[32m' + result[cell.y][cell.x] + "\u001b[0m"
                elif cell.value_left() < 0:
                    result[cell.y][cell.x] = f'\u001b[31m' + result[cell.y][cell.x] + "\u001b[0m"

        for connection in self._connections:
            colored = False
            if connection.solved and connection.bridges > 0:
                bridges_to_draw = connection.bridges
            elif self.show_min_bridges and connection.min_bridges > 0:
                bridges_to_draw = connection.min_bridges
                colored = True
            else:
                continue

            if connection.direction == Direction.HORIZONTAL:
                for x in range(connection.cell1.x + 1, connection.cell2.x):
                    result[connection.cell1.y][x] = drawing_map[Direction.HORIZONTAL][bridges_to_draw]
                    if colored:
                        result[connection.cell1.y][x] = u"\u001b[37m" + result[connection.cell1.y][x] + u"\u001b[0m"
            else:
                for y in range(connection.cell1.y + 1, connection.cell2.y):
                    result[y][connection.cell1.x] = drawing_map[Direction.VERTICAL][bridges_to_draw]
                    if colored:
                        result[y][connection.cell1.x] = u"\u001b[37m" + result[y][connection.cell1.x] + u"\u001b[0m"

        if self.show_cursor and 0 <= self.cursor_y < self.height and 0 <= self.cursor_x < self.width:
            if self.creating_bridges:
                result[self.cursor_y][self.cursor_x] = "\u001b[41m" + result[self.cursor_y][self.cursor_x] + "\u001b[0m"
            else:
                result[self.cursor_y][self.cursor_x] = "\u001b[44m" + result[self.cursor_y][self.cursor_x] + "\u001b[0m"

        result = '+' + '-' * (self.width * 2 + 1) + '+\n' \
                 + '| ' + ' |\n| '.join([u' '.join(cell) for cell in result]) + ' |\n' \
                 + '+' + '-' * (self.width * 2 + 1) + '+'

        if self.remove_output_spaces:
            result = result.replace(' ' + drawing_map[Direction.HORIZONTAL][1],
                                    drawing_map[Direction.HORIZONTAL][1] * 2)
            result = result.replace(drawing_map[Direction.HORIZONTAL][1] + ' ',
                                    drawing_map[Direction.HORIZONTAL][1] * 2)
            result = result.replace(' ' + drawing_map[Direction.HORIZONTAL][2],
                                    drawing_map[Direction.HORIZONTAL][2] * 2)
            result = result.replace(drawing_map[Direction.HORIZONTAL][2] + ' ',
                                    drawing_map[Direction.HORIZONTAL][2] * 2)
        return result

    def export(self):
        size = f'{self.width}x{self.height}'
        rest = ''
        for y in range(self.height):
            for x in range(self.width):
                cell_at = self.get_cell_at(x, y)
                if cell_at is not None:
                    rest += str(cell_at.value)
                else:
                    rest += '0'
        return size + 'S' + rest
