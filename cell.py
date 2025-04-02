from geometry import Line, Point


class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

        self.visited = False

        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None

        self._win = win


    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        def draw_wall(condition, p1, p2):
            color = "black" if condition else "#d9d9d9"
            line = Line(p1, p2)
            self._win.draw_line(line, color)

        draw_wall(self.has_left_wall,  Point(x1, y1), Point(x1, y2))
        draw_wall(self.has_top_wall,   Point(x1, y1), Point(x2, y1))
        draw_wall(self.has_right_wall, Point(x2, y1), Point(x2, y2))
        draw_wall(self.has_bottom_wall,Point(x1, y2), Point(x2, y2))


    def draw_move(self, to_cell, undo=False):
        x_center = (self._x1 + self._x2) // 2
        y_center = (self._y1 + self._y2) // 2
        x_center2 = (to_cell._x1 + to_cell._x2) // 2
        y_center2 = (to_cell._y1 + to_cell._y2) // 2

        color = "red" if undo else "grey"

        line = Line(Point(x_center, y_center), Point(x_center2, y_center2))
        self._win.draw_line(line, color)
