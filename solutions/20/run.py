from solutions.get_inputs import read_inputs


def run_1(inputs):
    numbers = Numbers(inputs)
    numbers.mix()
    # import pdb; pdb.set_trace()
    return numbers.get(1000) + numbers.get(2000) + numbers.get(3000)


def run_2(inputs):
    pass


class Numbers:

    def __init__(self, inputs):
        self.numbers = [int(i) for i in inputs]
        self.original_order = [i for i in self.numbers]

    def get(self, index):
        i = self.numbers.index(0) + index
        return self.numbers[i % len(self.numbers)]

    def mix(self):
        for number in self.original_order:
            self.mix_one(number)
            # print(self.numbers)

    def mix_one(self, number):
        i = self.numbers.index(number)
        if number >= 0:
            inc = (number % len(self.numbers))
            next_i = i + inc
            if next_i >= len(self.numbers):
                next_i = (next_i % len(self.numbers)) + 1
            # next_i = (i + number) % len(self.numbers)
        else:
            # inc = (number % len(self.numbers)) - 1
            inc = (number * -1) % len(self.numbers)
            if i - inc >= 0:
                next_i = i - inc
            else:
                next_i = len(self.numbers) - (inc - i + 1)
            if next_i == 0:
                next_i = len(self.numbers) - 2
                # next_i = (i + inc) % len(self.numbers)

        print(f'num {number} from {i} to {next_i}')
        if i == next_i:
            return
        elif i < next_i:
            self.numbers = self.numbers[:i] + self.numbers[i+1:next_i+1] + [number] + self.numbers[next_i+1:]
        else:
            # import pdb; pdb.set_trace()
            self.numbers = self.numbers[:next_i] + [number] + self.numbers[next_i:i] + self.numbers[i+1:]



def run_tests():
    test_inputs = """
    1
    2
    -3
    3
    -2
    0
    4
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 3:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    test_inputs = """
    -1
    0
    -3
    """.strip().split('\n')

    numbers = Numbers(test_inputs)
    numbers.mix_one(-1)
    if numbers.numbers != [0, -1, -3]:
        raise Exception(f"Test 1.2 did not pass, got {numbers.numbers}")

    test_inputs = """
    -2
    0
    -3
    """.strip().split('\n')

    numbers = Numbers(test_inputs)
    numbers.mix_one(-2)
    if numbers.numbers != [-2, 0, -3]:
        raise Exception(f"Test 1.3 did not pass, got {numbers.numbers}")

    test_inputs = """
    -3
    0
    4
    """.strip().split('\n')

    numbers = Numbers(test_inputs)
    import pdb; pdb.set_trace()
    numbers.mix_one(-3)
    if numbers.numbers != [0, -3, 4]:
        raise Exception(f"Test 1.4 did not pass, got {numbers.numbers}")

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(20)

    result_1 = run_1(input)
    # -128 not correct
    print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
