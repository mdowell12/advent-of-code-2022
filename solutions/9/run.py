from solutions.get_inputs import read_inputs


def run_1(inputs):
    head = (0, 0)
    tail = (0, 0)
    visited = set()

    for line in inputs:
        direction, magnitude = line.strip().split(' ')
        for _ in range(int(magnitude)):
            head, tail = move(direction, head, tail)
            visited.add(tail)

    return len(visited)


def run_2(inputs):
    positions = {i: (0, 0) for i in range(10)}
    visited = set()

    for line in inputs:
        direction, magnitude = line.strip().split(' ')
        for _ in range(int(magnitude)):
            positions = move_2(direction, positions)
            visited.add(positions[9])

    return len(visited)


def move_2(direction, positions):
    head_x, head_y = positions[0]

    # Move head
    if direction == 'R':
        positions[0] = head_x + 1, head_y
    elif direction == 'L':
        positions[0] = head_x - 1, head_y
    elif direction == 'U':
        positions[0] = head_x, head_y - 1
    elif direction == 'D':
        positions[0] = head_x, head_y + 1
    else:
        Exception()

    # Move other knots
    for i in range(1, 10):
        head_x, head_y = positions[i-1]
        tail_x, tail_y = positions[i]
        positions[i] = get_following_knot_position(head_x, head_y, tail_x, tail_y)

    return positions


def move(direction, head, tail):
    head_x, head_y = head
    tail_x, tail_y = tail

    # Move head
    if direction == 'R':
        head_x, head_y = head_x + 1, head_y
    elif direction == 'L':
        head_x, head_y = head_x - 1, head_y
    elif direction == 'U':
        head_x, head_y = head_x, head_y - 1
    elif direction == 'D':
        head_x, head_y = head_x, head_y + 1
    else:
        Exception()

    # Move tail
    tail_x, tail_y = get_following_knot_position(head_x, head_y, tail_x, tail_y)

    return (head_x, head_y), (tail_x, tail_y)


def get_following_knot_position(head_x, head_y, tail_x, tail_y):
    diff_x = head_x - tail_x
    diff_y = head_y - tail_y
    if abs(diff_x) > 1 or abs(diff_y) > 1:
        tail_x = tail_x + get_tail_move_magnitude(diff_x)
        tail_y = tail_y + get_tail_move_magnitude(diff_y)
    return (tail_x, tail_y)


def get_tail_move_magnitude(diff):
    if diff == 0:
        return 0
    else:
        return 1 if diff > 0 else -1


def run_tests():
    test_inputs = """
    R 4
    U 4
    L 3
    D 1
    R 4
    D 1
    L 5
    R 2
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 13:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 1:
        raise Exception(f"Test 2.1 did not pass, got {result_2}")

    test_inputs = """
    R 5
    U 8
    L 8
    D 3
    R 17
    D 10
    L 25
    U 20
    """.strip().split('\n')

    result_2 = run_2(test_inputs)
    if result_2 != 36:
        raise Exception(f"Test 2.2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(9)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
