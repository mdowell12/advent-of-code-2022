from itertools import cycle

from solutions.get_inputs import read_inputs


ROCKS = [
    # Horizontal line
    {
        0: [0, 1, 2, 3],
        1: [],
        2: [],
        3: [],
    },
    # Cross
    {
        0: [1],
        1: [0, 1, 2],
        2: [1],
        3: [],
    },
    # El
    {
        0: [0, 1, 2],
        1: [2],
        2: [2],
        3: [],
    },
    # Vertical line
    {
        0: [1],
        1: [1],
        2: [1],
        3: [1],
    },
    # Square
    {
        0: [0, 1],
        1: [0, 1],
        2: [],
        3: [],
    },

]


def run_1(inputs):
    gas_directions = cycle(list(inputs[0].strip()))
    width = 7
    slot_to_height = {i: -1 for i in range(width)}
    max_height = 0
    rocks = cycle(ROCKS)

    for i in range(2022):
        rock = rocks.__next__()
        slot_to_height, gas_directions = do_rock(rock, slot_to_height, gas_directions, max_height)
        max_height = max(v for v in slot_to_height.values())
        print(i)

    return max_height


def do_rock(rock, slot_to_height, gas_directions, max_height):
    rock_positions = starting_rock_position(rock, max_height, slot_to_height)
    down = False
    left = min(i for i in rock_positions if rock_positions[i] is not None)
    
    while True:
        # import pdb; pdb.set_trace()
        # move rock
        if down:
            # import pdb; pdb.set_trace()
            next_rock_positions = {i: rock_positions[i] - 1 if rock_positions[i] is not None else None for i in slot_to_height}
            if any(height == slot_to_height[i] for i, height in next_rock_positions.items()):
                break
            else:
                rock_positions = next_rock_positions
        else:
            
            gas_direction = 1 if gas_directions.__next__() == '>' else -1
            # if gas_direction != 1:
            #     import pdb; pdb.set_trace()
            # next_rock_positions = {i: rock_positions.get(i-gas_direction) for i in slot_to_height}
            next_rock_positions = {i+gas_direction: height for i, height in rock_positions.items() if height is not None}
            for i in slot_to_height:
                if i not in next_rock_positions:
                    next_rock_positions[i] = None
            if any(invalid_rock_position(i, height, slot_to_height) for i, height in next_rock_positions.items()):
                pass
            else:
                left += gas_direction
                rock_positions = next_rock_positions
        # print(list(rock_positions[i] for i in sorted(slot_to_height)))
        down = False if down else True

    # Adjust slot to height with new rock
    
    # for i in slot_to_height:
    #     import pdb; pdb.set_trace()
    #     current_height = slot_to_height[i]
    #     rock_height = max(rock.get(i-left)) if rock.get(i-left, []) else None
    #     print(i, rock_height)
    #     if rock_height:
    #         slot_to_height[i] = current_height + rock_height
    to_add = {}
    for height, i_with_this_height in rock.items():
        for i in i_with_this_height:
            to_add[left + i] = height+1
    for i, height in to_add.items():
        slot_to_height[i] += height

    # import pdb; pdb.set_trace()
    return slot_to_height, gas_directions


def starting_rock_position(rock, max_height, slot_to_height):
    result = {i: None for i in slot_to_height}
    for i in rock[0]:
        result[i+2] = max_height + 3
    return result


def invalid_rock_position(i, height, slot_to_height):
    if i not in slot_to_height:
        return True
    elif any(height == h for h in slot_to_height.values()):
        return True
    return False


def rock_is_stopped(rock, rock_bottom_left, slot_to_height):
    return True


def run_2(inputs):
    pass


def run_tests():
    test_inputs = """
    >>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 3068:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(17)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
