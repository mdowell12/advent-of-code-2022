from solutions.get_inputs import read_inputs


def run_1(inputs):
    result = 0
    for line in inputs:
        ((left_low, left_high), (right_low, right_high)) = parse(line)
        if is_contained(left_low, left_high, right_low, right_high):
            result += 1
    return result


def run_2(inputs):
    result = 0
    for line in inputs:
        ((left_low, left_high), (right_low, right_high)) = parse(line)
        if overlaps(left_low, left_high, right_low, right_high):
            result += 1
    return result


def is_contained(left_low, left_high, right_low, right_high):
    if left_low >= right_low and left_high <= right_high:
        return True
    elif right_low >= left_low and right_high <= left_high:
        return True
    else:
        return False


def overlaps(left_low, left_high, right_low, right_high):

    if is_contained(left_low, left_high, right_low, right_high):
        return True
    if left_high >= right_low and left_low <= right_high:
        return True
    if right_high >= left_low and right_low <= left_high:
        return True
    return False


def parse(line):
    parts = line.strip().split(',')
    return tuple(tuple(int(i) for i in part.strip().split('-')) for part in parts)


def run_tests():
    test_inputs = """
    2-4,6-8
    2-3,4-5
    5-7,7-9
    2-8,3-7
    6-6,4-6
    2-6,4-8
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 2:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 4:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(4)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
