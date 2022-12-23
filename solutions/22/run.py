from math import sqrt

from solutions.get_inputs import read_inputs
from solutions.grid import Grid2D


def run_1(inputs):
    grid, moves = parse_inputs(inputs)
    final_position, final_direction = get_final_position(grid, moves)
    return 1000 * (final_position[1] + 1) + 4 * (final_position[0] + 1) + final_direction


def run_2(inputs):
    grid, moves = parse_inputs(inputs)
    final_position, final_direction = get_final_position(grid, moves, wrap_fn=get_wrap_with_cube)
    return 1000 * (final_position[1] + 1) + 4 * (final_position[0] + 1) + final_direction


def get_final_position(grid, moves, wrap_fn=None):
    start_x = min([p[0] for p, val in get_row(grid, 0) if p[1] == 0])
    position = (start_x, 0)
    direction = 0
    for move in moves:
        position, direction = do_move(grid, move, position, direction, wrap_fn)
        # if wrap_fn: print(f'{position} {direction} after {move}')
    return position, direction


def do_move(grid, move, position, direction, wrap_fn):
    if not isinstance(move, int):
        new_direction = turn(direction, move)
        return position, new_direction

    for i in range(move):
        next = next_position(position, direction)
        value = grid.value_at_position(next)
        if value == '#':
            return position, direction
        elif value == '.':
            position = next
        elif value == ' ':
            if wrap_fn is None:
                wrap_fn = get_wrap
            wrap_position, wrap_direction = wrap_fn(grid, position, direction)
            print(f'wrapped {position} {direction} to {wrap_position} {wrap_direction}')
            wrap_value = grid.value_at_position(wrap_position)
            if wrap_value == '.':
                position = wrap_position
                direction = wrap_direction
            elif wrap_value == '#':
                return position, direction
            else:
                raise Exception(f'invalid wrap for pos={position} dir={direction} new_pos={wrap_position} val={wrap_value}')
        else:
            Exception(f'unknown value {value} at position {next}')
    return position, direction


def get_wrap(grid, position, direction):
    if direction == 0:
        row = get_row(grid, position[1])
        return min([p for p, val in row if val in ('.', '#')]), direction
    elif direction == 1:
        col = get_col(grid, position[0])
        return min([p for p, val in col if val in ('.', '#')]), direction
    elif direction == 2:
        row = get_row(grid, position[1])
        return max([p for p, val in row if val in ('.', '#')]), direction
    elif direction == 3:
        col = get_col(grid, position[0])
        return max([p for p, val in col if val in ('.', '#')]), direction
    raise Exception(f'Bad direction {direction}')


def get_wrap_with_cube(grid, position, direction):
    square_size = int(sqrt(sum(1 for p, v in grid if v in ('.', '#')) // 6))
    x, y = position
    if y == 0 and 50 <= x < 100 and direction == 3:
        # Top mid to bottom left
        diff = x - 50
        return (0, 150 + diff), 0
    elif x == 49 and 150 <= y and direction == 0:
        # bottom right to middle bottom
        diff = y - 150
        return (50 + diff, 149), 3
    elif x == 99 and 100 <= y < 150 and direction == 0:
        # middlebottom right to top right
        diff = y - 100
        return (149, 50 - diff - 1), 2
    elif y == 49 and 100 <= x < 150 and direction == 1:
        # right bottom to middletop right
        diff = x - 100
        return (99, 50 + diff), 2
    elif y == 0 and x > 100 and direction == 3:
        # top right to left bottom
        diff = x - 100
        return (diff, 199), 3
    elif y == 149 and 50 <= x < 100 and direction == 1:
        # middle bottom to bottom right
        diff = x - 50
        return (49, 150 + diff), 2
    elif x == 99 and 50 <= y < 100 and direction == 0:
        # middletop right to right bottom
        diff = y - 50
        return (100 + diff, 49), 3
    elif x == 149 and 0 <= y < 50 and direction == 0:
        # top right to middlebottom right
        diff = y
        return (99, 150 - diff - 1), 2
    elif x == 0 and 150 <= y < 200 and direction == 2:
        # bottom left to top top
        diff = y - 150
        return (50 + diff, 0), 1
    elif x == 50 and y < 50 and direction == 2:
        # top left to left left mid
        diff = y
        return (0, 3 * square_size - diff - 1), 0
    elif y == 2 * square_size and x < 1 * square_size and direction == 3:
        # left left top to middletop left
        diff = x
        return (50, 50 + diff), 0
    elif y == 199 and x < 50 and direction == 1:
        # left left bottom to right top
        diff = x
        return (100 + diff, 0), 1
    elif x == 0 and 100 <= y < 150 and direction == 2:
        # left left left to top left
        diff = y - 100
        return (50, 1 * square_size - diff - 1), 0
    elif x == 50 and 1 * square_size <= y < 2 * square_size and direction == 2:
        diff = y - 50
        return (diff, 100), 1

    raise Exception(f'Bad position {position} {direction}')


def next_position(position, direction):
    if direction == 0:
        return (position[0] + 1, position[1])
    elif direction == 1:
        return (position[0], position[1] + 1)
    elif direction == 2:
        return (position[0] - 1, position[1])
    elif direction == 3:
        return (position[0], position[1] - 1)
    raise Exception(f'Bad direction {direction}')


def turn(direction, move):
    val = 1 if move == 'R' else -1
    result = direction + val
    if result == 4:
        result = 0
    if result == -1:
        result = 3
    return result


def get_row(grid, row):
    return [(p, val) for p, val in grid if p[1] == row and val != ' ']


def get_col(grid, col):
    return [(p, val) for p, val in grid if p[0] == col and val != ' ']


def parse_inputs(inputs):
    inputs = [i for i in inputs if i]
    grid = Grid2D([i for i in inputs if '.' in i or '#' in i], default_if_missing=' ')
    moves = []
    move_string = inputs[-1].strip()
    i = 0
    current = ''
    for i in range(len(move_string)):
        if not move_string[i].isdigit():
            moves.append(int(current))
            current = ''
            moves.append(move_string[i])
        else:
            current = current + move_string[i]
    if current:
        moves.append(int(current))
    return grid, moves


def test_cube_wrap(test_inputs, source, to, direction):
    grid, _ = parse_inputs(test_inputs)
    result, _ = get_wrap_with_cube(grid, source, direction)
    if result != to:
        raise Exception(f"Cube wrap did not pass for src {source} dir {direction}. Actual {result} expected {to}")


def run_tests():
    test_inputs = """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5""".split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 6032:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    test_inputs = read_inputs(22, strip=False)
    test_cube_wrap(test_inputs, (64, 0), (0, 164), 3)
    test_cube_wrap(test_inputs, (49, 179), (79, 149), 0)
    test_cube_wrap(test_inputs, (99, 125), (149, 24), 0)
    test_cube_wrap(test_inputs, (99, 102), (149, 47), 0)
    test_cube_wrap(test_inputs, (134, 49), (99, 84), 1)
    test_cube_wrap(test_inputs, (102, 0), (2, 199), 3)
    test_cube_wrap(test_inputs, (64, 149), (49, 164), 1)
    test_cube_wrap(test_inputs, (99, 97), (147, 49), 0)
    test_cube_wrap(test_inputs, (149, 49), (99, 100), 0)
    test_cube_wrap(test_inputs, (0, 167), (67, 0), 2)
    test_cube_wrap(test_inputs, (50, 24), (0, 125), 2)
    test_cube_wrap(test_inputs, (10, 100), (50, 60), 3)
    test_cube_wrap(test_inputs, (42, 199), (142, 0), 1)
    test_cube_wrap(test_inputs, (0, 132), (50, 17), 2)
    test_cube_wrap(test_inputs, (50, 99), (49, 100), 2)

    # result_2 = run_2(test_inputs)
    # if result_2 != 5031:
    #     raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(22, strip=False)

    # result_1 = run_1(input)
    # print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    # 146103 too high
    # 40599 too high
    print(f"Finished 2 with result {result_2}")
