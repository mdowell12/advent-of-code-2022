from collections import defaultdict

from solutions.get_inputs import read_inputs


def run_1(inputs):
    stacks, moves = parse(inputs)
    for quantity, origin, destination in moves:
        origin_stack = stacks[origin]
        for _ in range(quantity):
            element = origin_stack.pop(0)
            stacks[destination] = [element] + stacks[destination]

    return get_top_crates(stacks)


def run_2(inputs):
    stacks, moves = parse(inputs)
    for quantity, origin, destination in moves:
        origin_stack = stacks[origin]

        elements = [i for i in origin_stack[:quantity]]
        stacks[origin] = origin_stack[quantity:]
        stacks[destination] = elements + stacks[destination]

    return get_top_crates(stacks)


def get_top_crates(stacks):
    top_elements = []
    for i in range(20):
        if stacks[i]:
            top_elements.append(stacks[i][0])
    return ''.join(top_elements)


def parse(inputs):
    stacks, moves = defaultdict(lambda: []), []
    for line in inputs:
        if 'move' in line:
            parts = line.strip().split(' ')
            moves.append((int(parts[1]), int(parts[3]), int(parts[5])))
        elif '[' in line:
            stack_i = 1
            for i in range(1, 99, 4):
                if len(line) > i and line[i].isalpha():
                    stack = stacks[stack_i]
                    stack.append(line[i])
                stack_i += 1
    return stacks, moves


def run_tests():
    test_inputs = """
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
    """.split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 'CMZ':
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 'MCD':
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(5, strip=False)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
