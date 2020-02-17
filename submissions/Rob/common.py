import enum


class Direction(enum.Enum):
    VERTICAL = 0
    HORIZONTAL = 1


drawing_map = {
    Direction.HORIZONTAL: {
        1: u'\u2500',
        2: u'\u2550'
    },
    Direction.VERTICAL: {
        1: u'\u2502',
        2: u'\u2551'
    }
}


def readfile(file_location):
    puzzles = []
    with open(file_location) as f:
        line = f.readline()
        while line:
            dimensions, puzzle = line.split('S')
            puzzle = puzzle[:-1]
            width, height = dimensions.split('x')
            width = int(width)
            height = int(height)
            cells = []
            for i, value in enumerate(puzzle):
                if value == '0':
                    continue
                i = int(i)
                cells.append({
                    'x': i % width,
                    'y': int(i / width),
                    'value': value
                })
            puzzles.append({
                'width': width,
                'height': height,
                # 'puzzle': puzzle,
                'cells': cells
            })
            line = f.readline()
    return puzzles


class ChainUnsolved(Exception):
    pass


def between(val1, val2, value):
    low_value = min(val1, val2)
    high_value = max(val1, val2)
    return low_value < value < high_value
