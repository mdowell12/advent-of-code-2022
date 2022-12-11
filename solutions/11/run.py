from collections import defaultdict

from solutions.get_inputs import read_inputs


def run_1(inputs):
    monkeys = parse_input(inputs)
    monkeys_by_id = {m.id: m for m in monkeys}

    for _ in range(20):
        do_round(monkeys_by_id)

    items_inspected_counts = sorted([m.items_inspected for m in monkeys])
    return items_inspected_counts[-1] * items_inspected_counts[-2]


def run_2(inputs):
    monkeys = parse_input(inputs, divide_by_three=False)
    monkeys_by_id = {m.id: m for m in monkeys}

    mod_by = 1
    for m in monkeys:
        mod_by *= m.throw_instructions.divisor

    for i in range(10_000):
        do_round(monkeys_by_id, mod_by=mod_by)
        counts = ', '.join([str(m.items_inspected) for m in monkeys])

    items_inspected_counts = sorted([m.items_inspected for m in monkeys])
    return items_inspected_counts[-1] * items_inspected_counts[-2]


def do_round(monkeys_by_id, mod_by=None):
    for i in range(len(monkeys_by_id)):
        monkey = monkeys_by_id[i]
        items_for_others = monkey.do_turn(mod_by=mod_by)
        for monkey_id, new_items in items_for_others.items():
            monkeys_by_id[monkey_id].add_items(new_items)


def parse_input(inputs, divide_by_three=True):
    monkeys = []

    i = 0
    while i < len(inputs):
        line = inputs[i]
        if 'Monkey' in line:
            monkeys.append(parse_monkey(inputs[i:i+6], divide_by_three))
            i += 6
        else:
            i += 1

    return monkeys


def parse_monkey(monkey_lines, divide_by_three):
    id = int(monkey_lines[0].strip().split(' ')[-1].replace(':', '').strip())
    items = [int(i) for i in monkey_lines[1].replace('Starting items: ', '').split(',')]
    operation = Operation(monkey_lines[2])
    divisor = int(monkey_lines[3].strip().split('by')[-1])
    true_monkey_id = monkey_lines[4].strip().split('monkey')[-1].strip()
    false_monkey_id = monkey_lines[5].strip().split('monkey')[-1].strip()
    throw_instructions = ThrowInstructions(divisor, true_monkey_id, false_monkey_id)
    return Monkey(id, items, operation, throw_instructions, divide_by_three)


class Monkey:

    DEBUG = False

    def __init__(self, id, items, operation, throw_instructions, divide_by_three):
        self.id = id
        self.items = [i for i in items]
        self.operation = operation
        self.throw_instructions = throw_instructions
        self.items_inspected = 0
        self.divide_by_three = divide_by_three

    def do_turn(self, mod_by=None):
        result = defaultdict(lambda: [])
        while self.items:
            item = self.items.pop(0)
            if self.DEBUG: print(f"Monkey {self.id} inspects item with level {item}")
            item = self.operation.apply(item)
            if self.DEBUG: print(f"  Worry level after operation is {item}")
            if self.divide_by_three:
                item = item // 3
                if self.DEBUG: print(f"  Worry level divided by 3 to {item}")
            elif mod_by is not None:
                item = item % mod_by
                if self.DEBUG: print(f"  Worry level moduloed by {mod_by} to {item}")
            next_monkey = self.throw_instructions.find_monkey(item)
            if self.DEBUG: print(f"  Next monkey is {next_monkey}")
            result[next_monkey].append(item)
            self.items_inspected += 1
        return result

    def add_items(self, new_items):
        self.items += new_items

    def __repr__(self):
        return f"Monkey[ id={self.id} items={self.items} ]"



class Operation:

    VALUE = 'old'

    def __init__(self, line):
        self.is_add, self.parts = self.parse(line)

    def parse(self, line):
        is_add = '+' in line
        parts = line.split('=')[-1].strip().split(' ')
        left, right = parts[0], parts[2]
        return is_add, list(map(lambda x: int(x) if 'old' not in x else self.VALUE, [left, right]))

    def apply(self, old):
        elements = [old if i == self.VALUE else i for i in self.parts]
        if self.is_add:
            return sum(elements)
        else:
            result = 1
            for i in elements:
                result *= i
            return result



class ThrowInstructions:

    def __init__(self, divisor, true_monkey_id, false_monkey_id):
        self.divisor = divisor
        self.true_monkey_id = int(true_monkey_id)
        self.false_monkey_id = int(false_monkey_id)

    def find_monkey(self, value):
        return self.true_monkey_id if value % self.divisor == 0 else self.false_monkey_id


def run_tests():
    test_inputs = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 10605:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 2713310158:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(11)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
