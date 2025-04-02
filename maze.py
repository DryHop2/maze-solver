import time, random
from cell import Cell


class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed is not None:
            random.seed(seed)

        self._cells = []

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()


    def _create_cells(self):
        # self._cells = []

        for col in range(self._num_cols):
            column = []
            for row in range(self._num_rows):
                cell = Cell(self._win)
                column.append(cell)
            self._cells.append(column)

        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._draw_cell(col, row)


    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y

        cell = self._cells[i][j]
        cell.draw(x1, y1, x2, y2)
        self._animate()


    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)


    def _break_entrance_and_exit(self):
        top_left = self._cells[0][0]
        top_left.has_top_wall = False
        self._draw_cell(0, 0)

        bottom_right_col = self._num_cols - 1
        bottom_right_row = self._num_rows - 1
        bottom_right = self._cells[bottom_right_col][bottom_right_row]
        bottom_right.has_bottom_wall = False
        self._draw_cell(bottom_right_col, bottom_right_row)


    def _break_walls_r(self, i, j):
        current = self._cells[i][j]
        current.visited = True

        while True:
            neighbors = []

            if i > 0 and not self._cells[i - 1][j].visited:
                neighbors.append(("W", i - 1, j))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                neighbors.append(("E", i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                neighbors.append(("N", i, j - 1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                neighbors.append(("S", i, j + 1))

            if not neighbors:
                self._draw_cell(i, j)
                return
            
            direction, ni, nj = random.choice(neighbors)
            neighbor = self._cells[ni][nj]

            if direction == "N":
                current.has_top_wall = False
                neighbor.has_bottom_wall = False
            elif direction == "S":
                current.has_bottom_wall = False
                neighbor.has_top_wall = False
            elif direction == "E":
                current.has_right_wall = False
                neighbor.has_left_wall = False
            elif direction == "W":
                current.has_left_wall = False
                neighbor.has_right_wall = False

            self._break_walls_r(ni, nj)


    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False


    def solve(self):
        return self._solve_r(0, 0)
    

    def _solve_r(self, i, j):
        self._animate()

        current = self._cells[i][j]
        current.visited = True
        
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        
        directions = [("E", i + 1, j), ("S", i, j + 1), ("W", i - 1, j), ("N", i, j - 1)]

        for direction, ni, nj in directions:
            if 0 <= ni < self._num_cols and 0 <= nj < self._num_rows:
                neighbor = self._cells[ni][nj]

                if not neighbor.visited:
                    if direction == "E" and not current.has_right_wall:
                        current.draw_move(neighbor)
                        if self._solve_r(ni, nj):
                            return True
                        current.draw_move(neighbor, undo=True)

                    elif direction == "S" and not current.has_bottom_wall:
                        current.draw_move(neighbor)
                        if self._solve_r(ni, nj):
                            return True
                        current.draw_move(neighbor, undo=True)

                    elif direction == "W" and not current.has_left_wall:
                        current.draw_move(neighbor)
                        if self._solve_r(ni, nj):
                            return True
                        current.draw_move(neighbor, undo=True)

                    elif direction == "N" and not current.has_top_wall:
                        current.draw_move(neighbor)
                        if self._solve_r(ni, nj):
                            return True
                        current.draw_move(neighbor, undo=True)

        return False