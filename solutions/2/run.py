from solutions.get_inputs import read_inputs


class Types:
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


LETTER_TO_TYPE = {
    'A': Types.ROCK,
    'B': Types.PAPER,
    'C': Types.SCISSORS,
    'X': Types.ROCK,
    'Y': Types.PAPER,
    'Z': Types.SCISSORS,
}

LETTER_TO_RESULT_TYPE = {
    'X': 0,
    'Y': 3,
    'Z': 6,
}


def run_1(inputs):
    result = 0
    for line in inputs:
        left, right = [i for i in line.strip().split(' ')]
        left_type, right_type = [LETTER_TO_TYPE[letter] for letter in (left, right)]
        game_result = play(left_type, right_type)
        result += game_result
        result += right_type
    return result


def run_2(inputs):
    result = 0
    for line in inputs:
        left, right = [i for i in line.strip().split(' ')]
        left_type = LETTER_TO_TYPE[left]
        game_result = LETTER_TO_RESULT_TYPE[right]
        right_type = find_type_for_result(left_type, game_result)
        result += game_result
        result += right_type
    return result


def find_type_for_result(left_type, game_result):
    if game_result == 3:
        return left_type
    elif game_result == 0:
        if left_type == Types.PAPER:
            return Types.ROCK
        elif left_type == Types.ROCK:
            return Types.SCISSORS
        if left_type == Types.SCISSORS:
            return Types.PAPER
    elif game_result == 6:
        if left_type == Types.PAPER:
            return Types.SCISSORS
        elif left_type == Types.ROCK:
            return Types.PAPER
        if left_type == Types.SCISSORS:
            return Types.ROCK
    raise Exception()


def play(left, right):
    if left == right:
        return 3
    elif left == Types.ROCK:
        if right == Types.PAPER:
            return 6
        else:
            return 0
    elif left == Types.PAPER:
        if right == Types.SCISSORS:
            return 6
        else:
            return 0
    elif left == Types.SCISSORS:
        if right == Types.ROCK:
            return 6
        else:
            return 0
    raise Exception()


def run_tests():
    test_inputs = """
    A Y
    B X
    C Z
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 15:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 12:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(2)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
