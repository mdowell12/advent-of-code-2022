from itertools import cycle

from solutions.get_inputs import read_inputs


ROCKS = [
    # Horizontal line
    {
        0: [0],
        1: [0],
        2: [0],
        3: [0],
    },
    # Cross
    {
        0: [1],
        1: [0, 2],
        2: [1],
        3: None,
    },
    # El
    {
        0: [0],
        1: [0],
        2: [0, 1, 2],
        3: None,
    },
    # Vertical line
    {
        0: [0, 1, 2, 3],
        1: None,
        2: None,
        3: None,
    },
    # Square
    {
        0: [0, 1],
        1: [0, 1],
        2: None,
        3: None,
    },

]


def run_1(inputs):
    return run(inputs, 2022)


def run_2(inputs):
    return run(inputs, 1_000_000_000)
    # return run(inputs, 1000000000000)


def run(inputs, num_rocks):
    gas_str = list(inputs[0].strip())
    gas_directions = cycle(gas_str)
    width = 7
    slot_heights = {i: [-1] for i in range(width)}
    max_height = 0
    num_gas_changes = 0
    rocks = cycle(ROCKS)

    from collections import defaultdict
    seen = defaultdict(lambda: set())
    # import pdb; pdb.set_trace()
    for i in range(num_rocks):
        rock = rocks.__next__()
        # if i % len(ROCKS) == 0 and num_gas_changes % len(gas_str) == 0 and all(max(slot_heights[i]) == max_height for i in slot_heights):
        #     import pdb; pdb.set_trace()
        # if all(max(slot_heights[i]) == max_height for i in slot_heights):
        #     import pdb; pdb.set_trace()
        # print(num_gas_changes)
        # if num_gas_changes % len(gas_str) == 0:
        #     import pdb; pdb.set_trace()
        # if i % len(ROCKS) == 0 and num_gas_changes % len(gas_str) == 0:
        #     # print_game(slot_heights, rock, None)
        #     import pdb; pdb.set_trace()
        #     key = (i, num_gas_changes)
        #     maxes = ','.join([str(max(v)) for v in slot_heights.values()])
        #     if key in SEEN and maxes in SEEN[key]:
        #         import pdb; pdb.set_trace()
        #     else:
        #         SEEN[key].add(maxes)
        # print(len(SEEN))

        slot_heights, gas_directions, num_gas_changes, seen = do_rock(rock, slot_heights, gas_directions, max_height, gas_str, num_gas_changes, seen, i % len(ROCKS) == 0)
        # num_gas_changes += this_num_gas_changes

        new_max_height = max(max(v) for v in slot_heights.values())
        increase = new_max_height - max_height
        max_height = new_max_height
        print(i, num_gas_changes)
    return max_height+1


def do_rock(rock, slot_heights, gas_directions, max_height, gas_str, num_gas_changes, seen, i_mod_zero):
    rock_positions = starting_rock_position(rock, max_height, slot_heights)
    down = False
    # num_gas_changes = 0

    while True:
        # move rock
        if down:
            next_rock_positions = next_positions_down(rock_positions)
            if intersects_with_other_rock(slot_heights, next_rock_positions):
                break
            else:
                rock_positions = next_rock_positions
        else:
            gas_direction = 1 if gas_directions.__next__() == '>' else -1
            num_gas_changes += 1
            # if i_mod_zero:
            #     import pdb; pdb.set_trace()
            if num_gas_changes % len(gas_str) == 0 and i_mod_zero:
                import pdb; pdb.set_trace()
            if gas_direction == 1 and rock_positions[6] is not None:
                pass
            elif gas_direction == -1 and rock_positions[0] is not None:
                pass
            else:
                next_rock_positions = next_positions_side(rock_positions, gas_direction)
                if intersects_with_other_rock(slot_heights, next_rock_positions):
                    pass
                else:
                    rock_positions = next_rock_positions

        # def get_move_str(down, gas_direction):
        #     if down:
        #         return 'down'
        #     return 'left' if gas_direction == -1 else 'right'
        # print_game(slot_heights, rock_positions, get_move_str(down, gas_direction))
        # import pdb; pdb.set_trace()
        down = False if down else True


    # Adjust slot heights with new rock
    for i, positions in rock_positions.items():
        if positions is not None:
            for height in positions:
                slot_heights[i].append(height)

    # Cap min vals for slot height at floor of game
    # min_height = min(max(j for j in i if j != -1) if len(i) > 1 else -1 for i in slot_heights.values())
    min_height = get_new_floor(slot_heights)
    # import pdb; pdb.set_trace()
    # print(min_height)
    if min_height is not None:
        for i in slot_heights:
            slot_heights[i] = [h for h in slot_heights[i] if h > min_height-2]

    # print_game(slot_heights, rock_positions, None)

    return slot_heights, gas_directions, num_gas_changes, seen


def get_new_floor(slot_heights):
    result = None
    for column in slot_heights.values():
        if column == [-1]:
            return None
        highest = max(column)
        if result is None or highest < result:
            result = highest
    return result


def print_game(slot_to_height, rock_positions, last_move):
    min_height = min(min(i) for i in slot_to_height.values())
    max_height = max(max(i) for i in rock_positions.values() if i is not None)
    print('.|.......|')
    for i in range(max_height, min_height, -1):
        row = []
        row.append(str(i))
        row.append('|')
        for col in slot_to_height:
            if i in slot_to_height[col]:
                row.append('X')
            elif rock_positions[col] is not None and i in range(rock_positions[col][0], rock_positions[col][-1]+1):
                row.append('@')
            else:
                row.append('.')
        row.append('|')
        print(''.join(row))
    print('.|.......|')
    print(last_move, max(max(v) for v in slot_to_height.values()))


def intersects_with_other_rock(slot_heights, rock_positions):
    for i, positions in rock_positions.items():
        if positions is None:
            continue
        rock_at_i = set(range(positions[0], positions[-1]+1))
        slot_at_i = set(slot_heights[i])
        if rock_at_i.intersection(slot_at_i):
            return True
    return False

def next_positions_down(rock_positions):
    result = {}
    for i, positions in rock_positions.items():
        if positions is None:
            result[i] = None
        else:
            result[i] = [p-1 for p in positions]
    return result


def next_positions_side(rock_positions, gas_direction):
    result = {i: None for i in rock_positions}
    for i, positions in rock_positions.items():
        if positions is not None:
            result[i+gas_direction] = positions
    return result


def starting_rock_position(rock, max_height, slot_heights):
    max_height = max(max(v) for v in slot_heights.values())
    result = {i: None for i in slot_heights}
    for i, positions in rock.items():
        result[i+2] = [max_height + p + 3 + 1 for p in positions] if positions else None
    return result


def invalid_rock_position(i, height, slot_to_height):
    if i not in slot_to_height:
        return True
    elif any(height == h for h in slot_to_height.values()):
        return True
    return False


def run_tests():
    test_inputs = """
    >>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 3068:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    # result_2 = run_2(test_inputs)
    # if result_2 != 1514285714288:
    #     raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(17)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
