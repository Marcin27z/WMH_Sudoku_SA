from random import shuffle


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
        self.numberList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self._counter = 0

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

    def generate_full(self):
        for i in range(0, 81):
            row = i // 9
            column = i % 9
            if self.is_field_empty(row, column):
                shuffle(self.numberList)
                for number in self.numberList:
                    if self.put_with_check(row, column, number):
                        if self.is_grid_full:
                            return True
                        else:
                            if self.generate_full():
                                return True
                break
        self.put(row, column, 0)

    @valid_coords
    def delete(self, row: int, column: int):
        self.put(row, column, 0)

    def _calculate_possible_solutions(self, sudoku_grid):
        for i in range(0, 81):
            row = i // 9
            column = i % 9
            if sudoku_grid.is_field_empty(row, column):
                shuffle(sudoku_grid.numberList)
                for number in sudoku_grid.numberList:
                    if sudoku_grid.put_with_check(row, column, number):
                        if sudoku_grid.is_grid_full:
                            self._counter += 1
                        else:
                            if self._calculate_possible_solutions(sudoku_grid):
                                return True
                break
        sudoku_grid.put(row, column, 0)

    def get_random_not_empty_cell(self) -> tuple:
        not_zeroes = list(
            filter(lambda x: x != -1, [(i, j) if self.grid[i][j] != 0 else -1 for i in range(9) for j in range(9)])
        )
        if len(not_zeroes) == 0:
            return -1, -1
        shuffle(not_zeroes)
        return not_zeroes[0]

    @property
    def possible_solutions(self) -> int:
        def copy_grid(grid):
            copy = []
            for r in range(0, 9):
                copy.append([])
                for c in range(0, 9):
                    copy[r].append(grid[r][c])
            return copy

        self._counter = 0
        self._calculate_possible_solutions(SudokuGrid.from_grid(copy_grid(self.grid)))
        return self._counter

    def reduce_fields(self, number):
        if number > 81 - 17:
            raise Exception
        while number > 0:
            row, column = self.get_random_not_empty_cell()
            backup = self.get(row, column)
            self.delete(row, column)
            if self.possible_solutions != 1:
                self.put(row, column, backup)
            else:
                number -= 1


if __name__ == '__main__':
    sudokuGrid = SudokuGrid()
    sudokuGrid.generate_full()
    sudokuGrid.reduce_fields(50)  # zajmuje trochę czasu
    print(sudokuGrid)
