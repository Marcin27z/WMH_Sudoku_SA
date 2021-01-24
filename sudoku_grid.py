from __future__ import annotations

# to nie jest potrzebne, dodałem dla zabawy
from grid import Grid


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


## Klasa reprezentująca planszę sudoku
#
#
class SudokuGrid(Grid):

    def __init__(self, grid=None):
        super().__init__(grid)

    @classmethod
    ## Tworzenie planszy na podstawie dwuwymiarowej tablicy
    #
    #  @param grid Tablica dwuwymiarowan, na której podstawie zostanie stworzony obiekt.
    def from_grid(cls, grid):
        return cls(grid)

    @valid_coord
    ## Funkcja sprawdzająca, czy dana kolumna zawiera podaną liczbę
    #
    #  @param column Numer kolumny liczony od 0 od lewej.
    #  @param number Liczba do sprawdzenia.
    def column_contains(self, column: int, number: int) -> bool:
        return any([number if self._grid[i][column] == number else None for i in range(9)])

    @valid_coord
    ## Funkcja sprawdzająca, czy dany wiersz zawiera podaną liczbę
    #
    #  @param row Numer wiersza liczony od 0 od góry.
    #  @param number Liczba do sprawdzenia.
    def row_contains(self, row: int, number: int) -> bool:
        return number in self._grid[row]

    ## Funkcja zwracająca wiersz planszy
    #
    #  @param row Numer wiersza liczony od 0 od góry.
    def get_row(self, row: int) -> list:
        return self._grid[row]

    ## Funkcja zwracająca kolumnę planszy
    #
    #  @param column Numer kolumny liczony od 0 od lewej.
    def get_column(self, column: int) -> list:
        return [self._grid[i][column] for i in range(9)]

    ## Funkcja umieszczająca liczbę na planszy na podanych współrzędnych
    #
    #  @param row Numer wiersza liczony od 0 od góry.
    #  @param column Numer kolumny liczony od 0 od lewej.
    #  @param number Liczba do umieszczenia.
    @valid_coords
    def put(self, row: int, column: int, number: int):
        self._grid[row][column] = number

    ## Funkcja zwracająca liczbę z planszy na podanych współrzędnych
    #
    #  @param row Numer wiersza liczony od 0 od góry.
    #  @param column Numer kolumny liczony od 0 od lewej.
    @valid_coords
    def get(self, row: int, column: int) -> int:
        return self._grid[row][column]

    ## Funkcja umieszczająca liczbę na planszy na podanych współrzędnych jeżeli nie wprowadza to konfliktu. Zwraca wynik operacji.
    #
    #  @param row Numer wiersza liczony od 0 od góry.
    #  @param column Numer kolumny liczony od 0 od lewej.
    #  @param number Liczba do umieszczenia.
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
    ## Funkcja sprawdzająca, czy kwadrat 3x3 zawierający punkt o podanych współrzędnych zawiera podaną liczbę.
    #
    #  @param row Numer wiersza liczony od 0 od góry.
    #  @param column Numer kolumny liczony od 0 od lewej.
    #  @param number Liczba do sprawdzenia.
    def region_contains(self, row: int, column: int, number: int) -> bool:
        row_region_id = (row % 9 // 3) * 3
        column_region_id = (column % 9 // 3) * 3
        column_region_range = range(column_region_id, column_region_id + 3)
        row_region_range = range(row_region_id, row_region_id + 3)
        # print([self.grid[i][j] for i in row_region_range for j in column_region_range])
        return number in [self._grid[i][j] for i in row_region_range for j in column_region_range]

    ## Funkcja sprawdzająca, czy pole jest puste
    #
    #  @param row Numer wiersza liczony od 0 od góry.
    #  @param column Numer kolumny liczony od 0 od lewej.
    @valid_coords
    def is_field_empty(self, row: int, column: int) -> bool:
        return self._grid[row][column] == 0

    ## Funkcja sprawdzająca, czy plansza jest pełna
    #
    #  Funkcja sprawdza, czy wszystkie pola planszy są zapełnione, czyli czy nie posiadają zerowych wawrtości.
    @property
    def is_grid_full(self) -> bool:
        return 0 not in [self._grid[i][j] for i in range(9) for j in range(9)]

    ## Funkcja usuwająca liczbę z planszy na podanych współrzędnych
    #
    #  @param row Numer wiersza liczony od 0 od góry.
    #  @param column Numer kolumny liczony od 0 od lewej.
    @valid_coords
    def delete(self, row: int, column: int):
        self.put(row, column, 0)

