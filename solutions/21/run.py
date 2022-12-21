from solutions.get_inputs import read_inputs


def run_1(inputs):
    monkeys = get_monkeys(inputs)
    return monkeys['root'].find_value(monkeys)


def run_2(inputs):
    left_bound = 3_500_000_000_000
    right_bound = 4_000_000_000_000
    while True:
        candidate = next_candidate(left_bound, right_bound)
        monkeys = get_monkeys(inputs)
        monkeys['humn'].value = candidate

        root = monkeys['root']
        left = monkeys[root.left].find_value(monkeys)
        right = monkeys[root.right].find_value(monkeys)
        if left == right:
            print(f"{left} == {right} for {candidate}")
            return candidate
        elif left > right:
            left_bound, right_bound = candidate, right_bound
            print(f"{left} > {right} for {candidate}")
        else:
            left_bound, right_bound = left_bound, candidate
            print(f"{left} < {right} for {candidate}")
    return -1


def next_candidate(left_bound, right_bound):
    import time
    time.sleep(0.5)
    candidate = left_bound  + (right_bound - left_bound) // 2
    return candidate


def get_monkeys(inputs):
    monkeys = {}
    for line in inputs:
        monkey = Monkey(line)
        monkeys[monkey.name] = monkey
    return monkeys


class Monkey:

    def __init__(self, line):
        self.name, self.value, self.left, self.right, self.operation = self._parse(line)

    def _parse(self, line):
        name = line.split(':')[0].strip()
        right_side = line.split(':')[1]
        if right_side.strip().isdigit():
            value = int(right_side.strip())
            left, right, operation = None, None, None
        else:
            value = None
            left, operation, right = right_side.strip().split(' ')
        return name, value, left, right, operation

    def find_value(self, monkeys):
        if self.value is not None:
            return self.value
        left = monkeys[self.left].find_value(monkeys)
        right = monkeys[self.right].find_value(monkeys)
        if self.operation == '+':
            self.value = left + right
        elif self.operation == '-':
            self.value = left - right
        elif self.operation == '*':
            self.value = left * right
        elif self.operation == '/':
            self.value = left // right
        return self.value

    def __repr__(self):
        return f'{self.name}: {self.left} {self.operation} {self.right} : {self.value}'


def run_tests():
    test_inputs = """
    root: pppw + sjmn
    dbpl: 5
    cczh: sllz + lgvd
    zczc: 2
    ptdq: humn - dvpt
    dvpt: 3
    lfqf: 4
    humn: 5
    ljgn: 2
    sjmn: drzm * dbpl
    sllz: 4
    pppw: cczh / lfqf
    lgvd: ljgn * ptdq
    drzm: hmdt - zczc
    hmdt: 32
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 152:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    # result_2 = run_2(test_inputs)
    # if result_2 != 301:
    #     raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    inputs = read_inputs(21)

    result_1 = run_1(inputs)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(inputs)
    print(f"Finished 2 with result {result_2}")
