class Grid:
    def __init__(self, grid=None):
        self.grid = [[0 for _ in range(9)] for _ in range(9)] if grid is None else grid

    def __str__(self) -> str:
        return "\n".join([" ".join(map(lambda x: str(x), self.grid[i])) for i in range(9)])