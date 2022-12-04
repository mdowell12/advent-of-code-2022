import string

from solutions.get_inputs import read_inputs


LOWER_PRIORITIES = {l: i+1 for i, l in enumerate(string.ascii_lowercase)}
UPPER_PRIORITIES = {l: i+1+26 for i, l in enumerate(string.ascii_uppercase)}


def run_1(inputs):
    result = 0
    for line in inputs:
        element = get_common_element(line.strip())
        priority = get_priority(element)
        result += priority
    return result


def run_2(inputs):
    result = 0
    for i in range(0, len(inputs), 3):
        element = get_common_element_across_lines(inputs[i:i+3])
        priority = get_priority(element)
        result += priority
    return result


def get_common_element(line):
    midpoint = len(line) // 2
    lefts = set(i for i in line[:midpoint])
    rights = set(i for i in line[midpoint:])
    return lefts.intersection(rights).pop()


def get_common_element_across_lines(lines):
    sets = [set(l.strip()) for l in lines]
    return sets[0].intersection(sets[1]).intersection(sets[2]).pop()


def get_priority(element):
    return LOWER_PRIORITIES[element] if element.islower() else UPPER_PRIORITIES[element]


def run_tests():
    test_inputs = """
    vJrwpWtwJgWrhcsFMMfFFhFp
    jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    PmmdzqPrVvPwwTWBwg
    wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ttgJtRGJQctTZtZT
    CrZsJsPPZsGzwwsLwLmpwMDw
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 157:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 70:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(3)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
