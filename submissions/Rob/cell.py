from common import ChainUnsolved, Direction


class Cell:
    x = None
    y = None
    value = None
    connections = None
    grid = None

    def __init__(self, x, y, value, grid):
        self.x = x
        self.y = y
        self.value = int(value)
        self.connections = []
        self.grid = grid

    def add_connection(self, connection):
        self.connections.append(connection)

    def try_connections(self):
        for connection in self.connections:
            connection.calculate_min_and_max()

    @property
    def solved(self):
        return sum([connection.bridges or 0 for connection in self.connections]) == self.value

    def get_connected_cells(self, cells=None):
        cells = cells or set()
        for connection in self.connections:
            if not connection.solved or connection.bridges == 0:
                continue
            other_cell = connection.cell1 if connection.cell1 is not self else connection.cell2
            if other_cell in cells:
                continue

            if not other_cell.solved:
                raise ChainUnsolved()

            cells.add(other_cell)
            for other in other_cell.get_connected_cells(cells):
                cells.add(other)
        return cells

    def get_connection(self, direction, positive):
        for connection in self.connections:
            other_cell = connection.cell1 if connection.cell1 is not self else connection.cell2
            if direction == Direction.HORIZONTAL and connection.direction == Direction.HORIZONTAL and positive and other_cell.x > self.x:
                return connection
            elif direction == Direction.HORIZONTAL and connection.direction == Direction.HORIZONTAL and not positive and other_cell.x < self.x:
                return connection
            elif direction == Direction.VERTICAL and connection.direction == Direction.VERTICAL and positive and other_cell.y > self.y:
                return connection
            elif direction == Direction.VERTICAL and connection.direction == Direction.VERTICAL and not positive and other_cell.y < self.y:
                return connection
        return None

    def value_left(self):
        return self.value - sum(connection.bridges or 0 for connection in self.connections)

    def __hash__(self):
        return self.x + self.y * self.grid.width

    def __repr__(self):
        return f'Cell(x={self.x}, y={self.y}, value={self.value})'
