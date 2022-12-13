from ast import literal_eval
from functools import cmp_to_key
from math import prod

from solutions.get_inputs import read_inputs


def run_1(inputs):
    pairs = parse_pairs(inputs)
    in_order = []
    for i, pair in enumerate(pairs):
        if get_ordering(pair) == Ordering.IN_ORDER:
            in_order.append(i+1)
    return sum(in_order)



def run_2(inputs):
    packets = parse_packets(inputs)
    packets = sorted(packets, key=cmp_to_key(get_pair_ordering), reverse=True)
    result = []
    for i, packet in enumerate(packets):
        if packet in ([[2]], [[6]]):
            result.append(i+1)
    return prod(result)


class Ordering:
    IN_ORDER = 1
    NOT_IN_ORDER = -1
    NOT_SURE = 0


def get_pair_ordering(left, right):
    return get_ordering((left, right))


def get_ordering(pair):
    left, right = pair
    left = [i for i in left]
    right = [i for i in right]

    while len(left) > 0 and len(right) > 0:
        left_element = left.pop(0)
        right_element = right.pop(0)
        if isinstance(left_element, int) and isinstance(right_element, int):
            if left_element < right_element:
                return Ordering.IN_ORDER
            elif left_element > right_element:
                return Ordering.NOT_IN_ORDER
            else:
                pass
        else:
            left_element = [left_element] if not isinstance(left_element, list) else left_element
            right_element = [right_element] if not isinstance(right_element, list) else right_element
            ordering = get_ordering((left_element, right_element))
            if ordering == Ordering.IN_ORDER or ordering == Ordering.NOT_IN_ORDER:
                return ordering

    if len(right) == 0 and len(left) == 0:
        return Ordering.NOT_SURE
    return Ordering.IN_ORDER if len(right) > 0 else Ordering.NOT_IN_ORDER


def parse_packets(inputs):
    pairs = parse_pairs(inputs)
    packets = [i for p in pairs for i in p]
    return packets + [[[2]], [[6]]]


def parse_pairs(inputs):
    pairs = []
    queue = [i for i in inputs]
    while queue:
        left = literal_eval(queue.pop(0).strip())
        right = literal_eval(queue.pop(0).strip())
        pairs.append((left, right))
        if queue:
            queue.pop(0)
    return pairs


def run_tests():
    test_inputs = """
    [1,1,3,1,1]
    [1,1,5,1,1]

    [[1],[2,3,4]]
    [[1],4]

    [9]
    [[8,7,6]]

    [[4,4],4,4]
    [[4,4],4,4,4]

    [7,7,7,7]
    [7,7,7]

    []
    [3]

    [[[]]]
    [[]]

    [1,[2,[3,[4,[5,6,7]]]],8,9]
    [1,[2,[3,[4,[5,6,0]]]],8,9]
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 13:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 140:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(13)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
