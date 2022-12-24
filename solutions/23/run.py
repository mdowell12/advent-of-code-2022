from collections import defaultdict

from solutions.get_inputs import read_inputs
from solutions.grid import Grid2D


def run_1(inputs):
    grid = Grid2D([i.strip() for i in inputs], default_if_missing='.')
    elves = {p for p, v in grid if v == '#'}
    direction = None
    for i in range(10):
        elves, grid, direction, _ = do_round(elves, grid, direction)
    return grid.size() - len(elves)


def run_2(inputs):
    grid = Grid2D([i.strip() for i in inputs], default_if_missing='.')
    elves = {p for p, v in grid if v == '#'}
    direction = None
    i = 0
    while i < 1_000_000:
        i += 1
        elves, grid, direction, did_move = do_round(elves, grid, direction)
        if not did_move:
            return i
    raise Exception()


def do_round(elves, grid, direction):
    direction = next_direction(direction)
    did_move = False
    # Position to elves who want to move here
    proposed_moves = defaultdict(lambda: [])

    for elf in elves:
        moves_to = find_move(elf, grid, direction)
        if moves_to is not None:
            proposed_moves[moves_to].append(elf)

    for position, moving_elves in proposed_moves.items():
        if len(moving_elves) == 1:
            did_move = True
            elf = moving_elves[0]
            elves.remove(elf)
            elves.add(position)
            grid.set_value_at_position(elf, '.')
            grid.set_value_at_position(position, '#')

    return elves, grid, direction, did_move


def find_move(elf, grid, start_direction):
    increments = {
        'N': [(0, -1), (-1, -1), (1, -1)],
        'E': [(1, 0), (1, -1), (1, 1)],
        'S': [(0, 1), (-1, 1), (1, 1)],
        'W': [(-1, 0), (-1, -1), (-1, 1)],
    }
    directions = [start_direction]
    for i in range(3):
        directions.append(next_direction(directions[-1]))
    unoccupied_directions = []
    for direction in directions:
        if any(is_occupied(elf, i, grid) for i in increments[direction]):
            continue
        move = increments[direction][0]
        next_position = (elf[0] + move[0], elf[1] + move[1])
        unoccupied_directions.append(next_position)
    return unoccupied_directions[0] if 0 < len(unoccupied_directions) < 4  else None


def is_occupied(elf, move, grid):
    new_position = (elf[0] + move[0], elf[1] + move[1])
    return grid.value_at_position(new_position) == '#'


def next_direction(direction):
    if direction is None:
        return 'N'
    elif direction == 'N':
        return 'S'
    elif direction == 'S':
        return 'W'
    elif direction == 'W':
        return 'E'
    elif direction == 'E':
        return 'N'
    raise Exception()


def run_tests():
#     test_inputs = """
# .....
# ..##.
# ..#..
# .....
# ..##.
# .....
#     """.strip().split('\n')
#
#     result_1 = run_1(test_inputs)
    # if result_1 != 110:
    #     raise Exception(f"Test 0 did not pass, got {result_1}")

    test_inputs = """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 110:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 20:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(23)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
