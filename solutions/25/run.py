from solutions.get_inputs import read_inputs


def run_1(inputs):
    decimal_sum = 0
    for line in inputs:
        decimal_sum += to_decimal(line.strip())
    # need to convert 34182852926025
    return to_snafu(decimal_sum)


def run_2(inputs):
    pass


def to_decimal(number):
    multiplier = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
    result = 0
    for i, value in enumerate(reversed(number)):
        place = 5 ** i
        result += multiplier[value] * place
    return result


def to_snafu(number):
    # remainder_to_symbol = {0: '0', 1: '1', 2: '2', 3: '=', 4: '-'}
    multiplier = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
    multiplier = {v: k for k, v in multiplier.items()}
    # for s_1, mult_1 in multiplier.items():
    #     for s_2, mult_2 in multiplier.items():
    #         for s_3, mult_3 in multiplier.items():
    #             for s_4, mult_4 in multiplier.items():
    #                 for s_5, mult_5 in multiplier.items():
    #                     for s_6, mult_6 in multiplier.items():
    #                         value = 5**5 * mult_6 + 5**4 * mult_5 + 5**3 * mult_4 + 5**2 * mult_3 + 5**1 * mult_2 + 5**0 * mult_1
    #                         if value == number:
    #                             return s_6 + s_5 + s_4 + s_3 + s_2 + s_1
    # raise Exception(number)
    # import pdb; pdb.set_trace()
    quotient = number
    remainders = []
    while quotient > 0:
        quotient, remainder = divide_by_5(quotient)
        # remainders.append(remainder_to_symbol[remainder])
        remainders.append(remainder)

    # remainders = [i for i in reversed(remainders)]
    import pdb; pdb.set_trace()
    while not all(i <= 2 for i in remainders):
        # result = []
        for i in range(len(remainders)):
            if remainders[i] <= 2:
                # result.append(remainders[i])
                pass
            elif remainders[i] > 4:
                q, r = divide_by_5(remainders[i])
                remainders[i] = r
                if i + 1 == len(remainders):
                    remainders.append(q)
                else:
                    remainders[i+1] += q
            else:
                remainders[i] = -2 if remainders[i] == 3 else -1
                new_value = 2 if remainders[i] == 3 else 1
                if i + 1 == len(remainders):
                    remainders.append(new_value)
                else:
                    remainders[i+1] += new_value

    print(remainders)
    result = ''.join([multiplier[i] for i in reversed(remainders)])
    print(result)
    return result


def divide_by_5(number):
    return number // 5, number % 5


def run_tests():
    assert to_decimal('2=-01') == 976
    assert to_snafu(4890) == '2=-1=0'

    test_inputs = """
    1=-0-2
    12111
    2=0=
    21
    2=01
    111
    20012
    112
    1=-1=
    1-12
    12
    1=
    122
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != '2=-1=0':
        raise Exception(f"Test 1 did not pass, got {result_1}")

    # result_2 = run_2(test_inputs)
    # if result_2 != 0:
    #     raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(25)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # print(f"Finished 2 with result {result_2}")
