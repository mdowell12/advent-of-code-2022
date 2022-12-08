

class Grid2D:
    """
    Two dimensional grid where (0, 0), (0, 1), (0, 2) is moving rightward on
    the "top" row and (0, 0), (1, 0), (2, 0) is moving downward on the "left" col.
    """

    def __init__(self, rows, map_fn=None):
        self.items, self.max_x, self.max_y = self.parse_rows(rows, map_fn)
        self.current_position = None

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
        return self.items.get(position, default)

    def position_is_in_grid(self, position):
        x, y = position
        return x >= 0 and y >= 0 and x <= self.max_x and y <= self.max_y

    def get_max_x(self):
        return self.max_x

    def get_max_y(self):
        return self.max_y

    def __repr__(self):
        lines = []
        for y in range(self.max_y+1):
            line = [str(self.items.get((x, y))) for x in range(self.max_x+1)]
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
