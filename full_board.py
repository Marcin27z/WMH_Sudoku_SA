from sudoku_grid import SudokuGrid
from random import shuffle


class FullBoard(SudokuGrid):

    def __init__(self, grid=None):
        super().__init__(grid)
        self.numberList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self._counter = 0
        if grid is None:
            self.generate_full()

    @classmethod
    def from_grid(cls, grid):
        return cls(grid)

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
        self._counter = 0
        self._calculate_possible_solutions(FullBoard.from_grid(SudokuGrid.copy_grid(self.grid)))
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