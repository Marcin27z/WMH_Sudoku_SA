from __future__ import annotations


## Klasa opakowująca tablicę dwywymiarową
#
#
class Grid:
    def __init__(self, grid=None):
        self._grid = [[0 for _ in range(9)] for _ in range(9)] if grid is None else grid

    def __str__(self) -> str:
        return "\n".join([" ".join(map(lambda x: str(x), self._grid[i])) for i in range(9)])

    ## Funkcja kopiująca podaną tablicę dwuwymiarową
    #
    #  @param grid Tablica do skopiowania.
    @staticmethod
    def copy_grid(grid):
        copy = []
        for r in range(0, 9):
            copy.append([])
            for c in range(0, 9):
                copy[r].append(grid[r][c])
        return copy

    ## Funkcja zwracająca planszę zawierające wartość 1 w miejscach, na których plansza się różni od podanej planszy
    #
    #  @param other Drugi obiekt typu Grid do porównania.
    def difference(self, other: Grid) -> Grid:
        return Grid([[1 if self._grid[i][j] != other._grid[i][j] else 0 for j in range(9)] for i in range(9)])