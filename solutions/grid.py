

class Grid2D:
    """
    Two dimensional grid where (0, 0), (0, 1), (0, 2) is moving rightward on
    the "top" row and (0, 0), (1, 0), (2, 0) is moving downward on the "left" col.

    print_window: example print_window=((500-20, 500+20), (0, overall_max_y + 3))
    """

    def __init__(self, rows, map_fn=None, default_if_missing=None, print_window=None):
        self.items, self.max_x, self.max_y = self.parse_rows(rows, map_fn)
        self.current_position = None
        self.default_if_missing = default_if_missing
        self.print_window = print_window

    def parse_rows(self, rows, map_fn):
        items = {}
        max_y = len(rows) - 1
        max_x = 0
        for y, row in enumerate(rows):
            for x, item in enumerate(row):
                if x > max_x:
                    max_x = x
                if map_fn:
                    item = map_fn(item)
                items[(x, y)] = item
        return items, max_x, max_y

    def value_at_position(self, position, default=None):
        if default is None and self.default_if_missing is not None:
            default = self.default_if_missing
        return self.items.get(position, default)

    def set_value_at_position(self, position, new_value):
        self.items[position] = new_value
        if position[0] > self.max_x:
            self.max_x = position[0]
        if position[1] > self.max_y:
            self.max_y = position[1]

    def positions_from_value(self, value):
        result = []
        for (x, y), this_value in self:
            if this_value == value:
                result.append((x,y))
        return result

    def position_is_in_grid(self, position):
        x, y = position
        return x >= 0 and y >= 0 and x <= self.max_x and y <= self.max_y

    def get_max_x(self):
        return self.max_x

    def get_max_y(self):
        return self.max_y

    def __repr__(self):
        lines = []
        x_min, x_max = (0, self.max_x) if self.print_window is None else self.print_window[0]
        y_min, y_max = (0, self.max_y) if self.print_window is None else self.print_window[1]
        for y in range(y_min, y_max+1):
            line = [str(self.value_at_position((x, y))) for x in range(x_min, x_max+1)]
            lines.append(' '.join(line))
        return '\n'.join(lines)

    def __iter__(self):
        self.current_position = (-1, 0)
        return self

    def __next__(self):
        if not self.current_position:
            raise Exception()
        curr_x, curr_y = self.current_position

        # End of grid
        if curr_x == self.max_x and curr_y == self.max_y:
            raise StopIteration()

        # Not end of row, return next in row
        if curr_x < self.max_x:
            self.current_position = (curr_x + 1, curr_y)
            return self.current_position, self.items.get(self.current_position)

        # End of row, go to next row
        self.current_position = (0, curr_y + 1)
        return self.current_position, self.items.get(self.current_position)
