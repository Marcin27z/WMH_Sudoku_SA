# to nie jest potrzebne, dodałem dla zabawy
def valid_coords(func):
    def func_wrapper(*args, **kwargs):
        if args[1] in range(9) and args[2] in range(9):
            return func(*args, **kwargs)
        else:
            raise Exception

    return func_wrapper


def valid_coord(func):
    def func_wrapper(*args, **kwargs):
        if args[1] in range(9):
            return func(*args, **kwargs)
        else:
            raise Exception

    return func_wrapper


# generowanie sudoku, pełnej poprawnej planszy, a następnie usuwanie części pól z zachowaniem jednego rozwiązania
# na podstawie https://www.101computing.net/sudoku-generator-algorithm/

class SudokuGrid:

    def __init__(self, grid=None):
        self.grid = [[0 for _ in range(9)] for _ in range(9)] if grid is None else grid

    @classmethod
    def from_grid(cls, grid):
        return cls(grid)

    @valid_coord
    def column_contains(self, column: int, number: int) -> bool:
        return any([number if self.grid[i][column] == number else None for i in range(9)])

    @valid_coord
    def row_contains(self, row: int, number: int) -> bool:
        return number in self.grid[row]

    @valid_coords
    def put(self, row: int, column: int, number: int):
        self.grid[row][column] = number

    @valid_coords
    def get(self, row: int, column: int) -> int:
        return self.grid[row][column]

    @valid_coords
    def put_with_check(self, row: int, column: int, number: int) -> bool:
        if not (self.column_contains(column, number)
                or self.row_contains(row, number)
                or self.region_contains(row, column, number)):
            self.put(row, column, number)
            return True
        else:
            return False

    @valid_coords
    def region_contains(self, row: int, column: int, number: int) -> bool:
        row_region_id = (row % 9 // 3) * 3
        column_region_id = (column % 9 // 3) * 3
        column_region_range = range(column_region_id, column_region_id + 3)
        row_region_range = range(row_region_id, row_region_id + 3)
        # print([self.grid[i][j] for i in row_region_range for j in column_region_range])
        return number in [self.grid[i][j] for i in row_region_range for j in column_region_range]

    @valid_coords
    def is_field_empty(self, row: int, column: int) -> bool:
        return self.grid[row][column] == 0

    @property
    def is_grid_full(self) -> bool:
        return 0 not in [self.grid[i][j] for i in range(9) for j in range(9)]

    def __str__(self) -> str:
        return "\n".join([" ".join(map(lambda x: str(x), self.grid[i])) for i in range(9)])

    @valid_coords
    def delete(self, row: int, column: int):
        self.put(row, column, 0)

    @staticmethod
    def copy_grid(grid):
        copy = []
        for r in range(0, 9):
            copy.append([])
            for c in range(0, 9):
                copy[r].append(grid[r][c])
        return copy
