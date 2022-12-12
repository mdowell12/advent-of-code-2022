from string import ascii_lowercase

from solutions.get_inputs import read_inputs
from solutions.grid import Grid2D


LETTER_TO_HEIGHT = {l: i for i, l in enumerate(ascii_lowercase)}
LETTER_TO_HEIGHT['S'] = 0
LETTER_TO_HEIGHT['E'] = 26


def run_1(inputs):
    grid = Grid2D([i.strip() for i in inputs])
    start = grid.positions_from_value('S')[0]
    return shortest_from_starting_positions(grid, start)


def run_2(inputs):
    grid = Grid2D([i.strip() for i in inputs])
    starting_positions = grid.positions_from_value('a')
    starting_positions += grid.positions_from_value('S')
    shortest_from_positions = []
    for position in starting_positions:
        shortest_from_here = shortest_from_starting_positions(grid, position)
        if shortest_from_here:
            shortest_from_positions.append(shortest_from_here)
    return sorted(shortest_from_positions)[0]


def shortest_from_starting_positions(grid, starting_position):
    queue = [[starting_position]]
    shortest_to_position_so_far = {}
    valid_paths_to_destination = []
    while queue:
        path = queue.pop(0)
        next_positions = get_potential_next_positions(path, grid)
        for position in next_positions:
            if grid.value_at_position(position) == 'E':
                valid_paths_to_destination.append(path + [position])
                break
        else:
            for position in next_positions:
                if position not in shortest_to_position_so_far or len(path) < shortest_to_position_so_far[position]:
                    queue.append(path + [position])
                    shortest_to_position_so_far[position] = len(path)

    path_lengths = sorted([len(p)-1 for p in valid_paths_to_destination])
    return path_lengths[0] if path_lengths else None


def get_potential_next_positions(path, grid):
    last_position = path[-1]
    neighbors = [
        (last_position[0]-1, last_position[1]),
        (last_position[0]+1, last_position[1]),
        (last_position[0], last_position[1]-1),
        (last_position[0], last_position[1]+1),
    ]
    result = []
    for neighbor in neighbors:
        if neighbor in path:
            continue
        value_at_neighbor = grid.value_at_position(neighbor)
        if not value_at_neighbor:
            continue
        my_height = LETTER_TO_HEIGHT[grid.value_at_position(last_position)]
        neighbor_height = LETTER_TO_HEIGHT[value_at_neighbor]
        if neighbor_height <= my_height + 1:
            result.append(neighbor)
    return result


def run_tests():
    test_inputs = """
    Sabqponm
    abcryxxl
    accszExk
    acctuvwj
    abdefghi
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 31:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 29:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(12)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
