from solutions.get_inputs import read_inputs


def run_1(inputs):
    max_so_far = 0
    elf_total = 0
    for line in inputs:
        if line.strip():
            elf_total += int(line)
        else:
            if elf_total > max_so_far:
                max_so_far = elf_total
            elf_total = 0
    return max_so_far


def run_2(inputs):
    inputs.append("")
    totals = []
    elf_total = 0
    for line in inputs:
        if line.strip():
            elf_total += int(line)
        else:
            totals.append(elf_total)
            elf_total = 0
    return sum(sorted(totals)[-3:])


def run_tests():
    test_inputs = """
    1000
    2000
    3000

    4000

    5000
    6000

    7000
    8000
    9000

    10000
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 24000:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 45000:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(1)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
