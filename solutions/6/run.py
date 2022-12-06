from solutions.get_inputs import read_inputs


def run_1(inputs):
    return find_marker(inputs[0])


def run_2(inputs):
    return find_marker(inputs[0], num_chars=14)


def find_marker(stream, num_chars=4):
    stream = stream.strip()
    for i in range(num_chars, len(stream)):
        if len(set(stream[i-num_chars:i])) == num_chars:
            return i
    raise Exception()


def run_tests():

    result_1 = find_marker('mjqjpqmgbljsphdztnvjfqwrcgsmlb')
    if result_1 != 7:
        raise Exception(f"Test did not pass, got {result_1}")

    result_1 = find_marker('bvwbjplbgvbhsrlpgdmjqwftvncz')
    if result_1 != 5:
        raise Exception(f"Test did not pass, got {result_1}")

    result_1 = find_marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg')
    if result_1 != 10:
        raise Exception(f"Test did not pass, got {result_1}")

    result_1 = find_marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw')
    if result_1 != 11:
        raise Exception(f"Test did not pass, got {result_1}")

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(6)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
