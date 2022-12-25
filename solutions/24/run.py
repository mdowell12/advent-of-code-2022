from collections import defaultdict

from solutions.get_inputs import read_inputs
from solutions.grid import Grid2D


def run_1(inputs):
    grid = Grid2D(inputs)
    position = (1, 0)
    destination = (grid.get_max_x() - 1, grid.get_max_y())
    min_x, min_y, max_x, max_y = 0, 0, grid.get_max_x(), grid.get_max_y()
    all_blizzards = {}
    blizzards = [(p, v) for p, v in grid if v not in {'.', '#'}]
    queue = [(position, 0, 0)]

    index_to_next_blizzard = {}
    best_at_position_with_blizzard = {}
    blizzard_to_index = defaultdict(lambda: max(v for v in blizzard_to_index.values()) + 1)
    blizzard_to_index[hash_bliz(blizzards)] = 0

    # queue = [([position], [blizzards])]
    # queue = [([position], blizzards)]
    # return get_steps_to_finish(grid, blizzards, position, destination, {})
    best = None
    i = 0
    # import pdb; pdb.set_trace()
    while queue and i < 1_000_000:
        i += 1
        # print('start')
        # last, blizzards, steps = queue.pop(0)
        last, blizzard_index, steps = queue.pop(0)
        x, y = last
        next_positions = {(x, y), (x, y-1), (x+1, y), (x, y+1), (x-1, y)}
        if destination in next_positions:
            # if best is None or len(path) < best:
            if best is None or steps + 1 < best:
                # print(path)
                # best = len(path)
                best = steps + 1
        else:
            # grid, blizzards = move_blizzards(grid, blizzards)
            # print('before', blizzard_index)
            # import pdb; pdb.set_trace()
            if blizzard_index in index_to_next_blizzard:
                blizzards = index_to_next_blizzard[blizzard_index]
                next_index = blizzard_to_index[hash_bliz(blizzards)]
            else:
                # previous_blizzards = blizzards
                blizzards = move_blizzards(blizzards, min_x, max_x, min_y, max_y)
                index_to_next_blizzard[blizzard_index] = blizzards
                next_index = blizzard_to_index[hash_bliz(blizzards)]


            # blizzards = move_blizzards(blizzards, min_x, max_x, min_y, max_y)
            # all_blizzards[hash_bliz(previous_blizzards)] = hash_bliz(blizzards)

            blizzard_positions = [b for b, _ in blizzards]
            # print('loop')
            for next_position in next_positions:
                # if grid.value_at_position(next_position) == '.':
                # print('hey')
                if (next_position not in blizzard_positions and min_x < next_position[0] < max_x and min_y < next_position[1] < max_y) or next_position == (1, 0):

                    # new_path = path + [next_position]
                    # if best is None or len(new_path) < best:
                    if best is None or steps + 1 < best:
                        key = f'{next_position}{hash_bliz(blizzards)}'
                        if key in best_at_position_with_blizzard and best_at_position_with_blizzard[key] <= steps:
                            continue
                        best_at_position_with_blizzard[key] = steps + 1
                        # queue.append((new_path, blizzards, grids + [grid]))
                        # queue.append((new_path, blizzards))
                        # queue.append((next_position, blizzards, steps + 1))
                        # print(next_position, next_index)
                        queue.append((next_position, next_index, steps + 1))
        print(i, len(queue), queue[-1] if queue else None, len(blizzard_to_index), len(index_to_next_blizzard), len(best_at_position_with_blizzard), best)
        # print(queue)
    return best


def hash_bliz(blizzards):
    return ','.join(f'{p}.{d}' for p, d in sorted(blizzards))


def unhash_bliz(bliz_hash):
    return [tuple(j for j in i.split('.')) for i in bliz_hash.split(',')]


def get_steps_to_finish(grid, blizzards, position, destination, best_so_far, so_far=0):
    x, y = position
    next_positions = {(x, y), (x, y-1), (x+1, y), (x, y+1), (x-1, y)}
    if destination in next_positions:
        return so_far + 1

    if so_far > 20:
        return None

    grid, blizzards = move_blizzards(grid, blizzards)
    results = []
    for next_position in next_positions:
        if grid.value_at_position(next_position) == '.':
            # i = so_far % ((grid.get_max_x()-2) * (grid.get_max_y()-2))
            # key = (i, next_position)
            # if key not in best_so_far or best_so_far[key] > so_far:
            result = get_steps_to_finish(grid, blizzards, position, destination, best_so_far, so_far=so_far+1)
            if result is not None:
                results.append(result)
                # best_so_far[key] = so_far
    return min(results) if results else None


def move_blizzards(blizzards, min_x, max_x, min_y, max_y):
    new_blizzards = []
    for point, direction in blizzards:
        next_point = move_blizzard(point, direction, min_x, max_x, min_y, max_y)
        new_blizzards.append((next_point, direction))
    return new_blizzards


# def move_blizzards(grid, blizzards):
#     new_blizzards = []
#     new_grid = grid.copy()
#     for point, direction in blizzards:
#         next_point = move_blizzard(new_grid, point, direction)
#         new_blizzards.append((next_point, direction))
#     for point, _ in blizzards:
#         new_grid.set_value_at_position(point, '.')
#     for next_point, direction in new_blizzards:
#         new_grid.set_value_at_position(next_point, direction)
#     return new_grid, new_blizzards


# def move_blizzard(grid, point, direction):
#     x, y = point
#     new_x, new_y = point
#     if direction == '^':
#         new_y = y - 1 if y != grid.get_min_y() + 1 else grid.get_max_y() - 1
#     elif direction == '>':
#         new_x = x + 1 if x != grid.get_max_x() - 1 else grid.get_min_x() + 1
#     elif direction == '<':
#         new_x = x - 1 if x != grid.get_min_x() + 1 else grid.get_max_x() - 1
#     elif direction == 'v':
#         new_y = y + 1 if y != grid.get_max_y() - 1 else grid.get_min_y() + 1
#     else:
#         raise Exception()
#     return (new_x, new_y)


def move_blizzard(point, direction, min_x, max_x, min_y, max_y):
    x, y = point
    new_x, new_y = point
    if direction == '^':
        new_y = y - 1 if y != min_y + 1 else max_y - 1
    elif direction == '>':
        new_x = x + 1 if x != max_x - 1 else min_x + 1
    elif direction == '<':
        new_x = x - 1 if x != min_x + 1 else max_x - 1
    elif direction == 'v':
        new_y = y + 1 if y != max_y - 1 else min_y + 1
    else:
        raise Exception()
    return (new_x, new_y)


def run_2(inputs):
    pass


def run_tests():
#     test_inputs = """
# #.#####
# #.....#
# #>....#
# #.....#
# #...v.#
# #.....#
# #####.#
#     """.strip().split('\n')
#     grid = Grid2D(test_inputs)
#     blizzards = [(p, v)for p, v in grid if v not in {'.', '#'}]
#     print(grid)
#     grid, blizzards = move_blizzards(grid, blizzards)
#     print(grid)
#     grid, blizzards = move_blizzards(grid, blizzards)
#     print(grid)
#     grid, blizzards = move_blizzards(grid, blizzards)
#     print(grid)
#     grid, blizzards = move_blizzards(grid, blizzards)
#     print(grid)
#     grid, blizzards = move_blizzards(grid, blizzards)
#     print(grid)

    test_inputs = """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 18:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(24)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
