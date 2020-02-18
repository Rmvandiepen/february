import os

from common import Direction, ChainUnsolved


class Connection:
    cell1 = None
    cell2 = None
    min_bridges = None
    max_bridges = None
    bridges = None
    intersections = None
    grid = None

    def __init__(self, cell1, cell2, grid):
        self.cell1 = cell1
        self.cell2 = cell2
        self.min_bridges = 0
        self.max_bridges = 2
        self.intersections = []
        self.grid = grid

    def solve(self, bridges, cascade=True):
        if self.solved:
            return

        self.min_bridges = bridges
        self.max_bridges = bridges
        self.bridges = bridges

        if bridges > 0 and self.grid.solve_slowly:
            os.system('clear')
            print(self.grid)
            input('Press return for the next step.')

        if cascade:
            if bridges > 0:
                for intersection in self.intersections:
                    intersection.solve(0)

            for connection in self.cell1.connections + self.cell2.connections:
                connection.calculate_min_and_max()

    @property
    def direction(self):
        if self.cell1.x == self.cell2.x:
            return Direction.VERTICAL
        else:
            return Direction.HORIZONTAL

    @property
    def solved(self):
        return self.bridges is not None

    @property
    def has_bridges(self):
        return self.min_bridges > 1

    def calculate_min_and_max(self):
        if self.solved:
            return

        min_c1 = sum([c.min_bridges for c in self.cell1.connections if c != self])
        max_c1 = sum([c.max_bridges for c in self.cell1.connections if c != self])
        min_c2 = sum([c.min_bridges for c in self.cell2.connections if c != self])
        max_c2 = sum([c.max_bridges for c in self.cell2.connections if c != self])
        min_f_c1 = self.cell1.value - max_c1
        max_f_c1 = self.cell1.value - min_c1
        min_f_c2 = self.cell2.value - max_c2
        max_f_c2 = self.cell2.value - min_c2
        min_t = max(min_f_c1, min_f_c2)
        max_t = min(max_f_c1, max_f_c2)
        self.min_bridges = max(self.min_bridges, min_t)
        self.max_bridges = min(self.max_bridges, max_t)

        if self.min_bridges == self.max_bridges:
            self.solve(self.min_bridges)

        if self.min_bridges > 0:
            for intersection in self.intersections:
                intersection.solve(0)

        # if self.min_bridges > 2:
        #     import pdb
        #     pdb.set_trace()

        self.ensure_single_chain()

    def ensure_single_chain(self):
        if not self.grid.advanced:
            return

        if not self.solved and self.max_bridges > 0:
            before_min = self.min_bridges
            before_max = self.max_bridges

            self.bridges = self.max_bridges
            if not self.cell1.solved or not self.cell2.solved:
                self.bridges = None
                return
            all_cells_if_connected = {self.cell1, self.cell2}
            try:
                all_cells_if_connected = set(
                    list(self.cell1.get_connected_cells(all_cells_if_connected)) +
                    list(self.cell2.get_connected_cells(all_cells_if_connected))
                )
                if len(all_cells_if_connected) != len(self.grid.cells):
                    self._unsolve(before_min, before_max)
                    self.max_bridges -= 1
            except ChainUnsolved:
                self.bridges = None

    def _unsolve(self, bmin, bmax):
        self.min_bridges = bmin
        self.max_bridges = bmax
        self.bridges = None

    def __repr__(self):
        if self.solved:
            return f'Connection({self.cell1}, {self.cell2}, bridges={self.bridges})'
        else:
            return f'Connection({self.cell1}, {self.cell2})'
