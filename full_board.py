from sudoku_grid import SudokuGrid
from random import shuffle
import os


## Klasa tworząca pełne oraz częściowe, poprawnie wypełnione plansze sudoku.
#
#
class FullBoard(SudokuGrid):

    def __init__(self, grid=None):
        super().__init__(grid)
        self._numberList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self._counter = 0
        if grid is None:
            self.generate_full()

    ## Stworzenie planszy na podstawie tablicy dwuwymiarowej.
    #
    #  @param grid Tablica dwuwymiarowa, z której utworzyć obiekt.
    @classmethod
    def from_grid(cls, grid):
        return cls(grid)

    ## Funkcja wczytująca planszę z pliku.
    #
    #  Możliwe jest wybranie konkretnej instancji lub losowej instancji spośród dostępnych.
    #  @param level Liczba wypełnionych pól na planszy.
    #  @param instance Liczba porządkowa zapisanej instancji.
    @classmethod
    def from_cache(cls, level: int, instance=-1):
        if instance == -1:
            cached = os.listdir(f'sudoku/{level}')
            shuffle(cached)
            index = cached[0]
        else:
            index = instance
        try:
            with open(f'sudoku/{level}/{index}') as file:
                print("open(f'sudoku/{level}/{index}')")
                return cls(eval(file.readline(), {}))
        except FileNotFoundError:
            print("FileNotFoundError")
            full_board = cls()
            full_board.reduce_fields(81 - level)
            return full_board

    ## Funkcja generująca pełną planszę od zera
    #
    #  Tworzenie planszy polega na wstawianiu po kolei wartości z zachowaniem poprawności planszy.
    #  Jeżeli algorytm napotka konflikt to się wycofuje z wyboru liczby i próbuje inną wartość.
    def generate_full(self):
        for i in range(0, 81):
            row = i // 9
            column = i % 9
            if self.is_field_empty(row, column):
                shuffle(self._numberList)
                for number in self._numberList:
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
                shuffle(sudoku_grid._numberList)
                for number in sudoku_grid._numberList:
                    if sudoku_grid.put_with_check(row, column, number):
                        if sudoku_grid.is_grid_full:
                            self._counter += 1
                        else:
                            if self._calculate_possible_solutions(sudoku_grid):
                                return True
                break
        sudoku_grid.put(row, column, 0)

    ## Funkcja zwracająca współrzędne losowego niezerowego pola planszy.
    #
    #  Funkcja sprawdza, które pola zawierają niezerowe wartości i zwraca losowo jedno z nich.
    #  Zwraca -1, -1 w przypadku, gdy nie ma takiego pola.
    def _get_random_not_empty_cell(self) -> tuple:
        not_zeroes = list(
            filter(lambda x: x != -1, [(i, j) if self._grid[i][j] != 0 else -1 for i in range(9) for j in range(9)])
        )
        if len(not_zeroes) == 0:
            return -1, -1
        shuffle(not_zeroes)
        return not_zeroes[0]

    ## Property obliczeniowe zwracające liczbę możliwych rozwiązań sudoku
    #
    #  Property zwraca liczbę możliwych rozwiązań sudoku. Sprawdzanie polega na próbie rozwiązania sudoku i policzeniu
    #  poprawnych możliwości.
    @property
    def _possible_solutions(self) -> int:
        self._counter = 0
        self._calculate_possible_solutions(FullBoard.from_grid(SudokuGrid.copy_grid(self._grid)))
        return self._counter

    ## Funkcja usuwająca określoną liczbę pól z planszy z zachowaniem warunku, że sudoku ma jedno rozwiązanie. Wygenerowana plansza może być zapisana do pliku.
    #
    #  Funkcja zaczynając od pełnej planszy usuwa losowe pola pojedynczo sprawdzając warunek,
    #  żeby powstałe sudoku zawierało tylko jedno rozwiązanie.
    #  @param number Liczba pól do zredukowania.
    #  @param save_to_cache Zmienna mówiąca, czy zapisać zredukowaną planszę.
    def reduce_fields(self, number: int, save_to_cache=False):
        if number > 81 - 17:
            raise Exception
        i = number
        while i > 0:
            row, column = self._get_random_not_empty_cell()
            backup = self.get(row, column)
            self.delete(row, column)
            if self._possible_solutions != 1:
                self.put(row, column, backup)
            else:
                i -= 1

        if save_to_cache:
            if not os.path.exists('sudoku'):
                os.makedirs('sudoku')
            if not os.path.exists(f'sudoku/{81 - number}'):
                os.makedirs(f'sudoku/{81 - number}')
            count = len(os.listdir(f'sudoku/{81 - number}'))
            with open(f'sudoku/{81 - number}/{count}', mode='w') as file:
                file.write(str(self._grid))
