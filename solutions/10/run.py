from solutions.get_inputs import read_inputs


def run_1(inputs):
    register = 1
    cycle = 0
    measurements = []
    
    for line in inputs:
        command, value = parse_line(line)
        new_measurement, cycle, register = process(command, value, cycle, register)
        if new_measurement is not None:
            measurements.append(new_measurement)

    return sum(measurements)


def run_2(inputs):
    register = 1
    cycle = 0
    pixels = {}
    
    for line in inputs:
        command, value = parse_line(line)
        new_pixels, cycle, register = process_2(command, value, cycle, register)
        pixels.update(new_pixels)

    row = []
    for i in range(1, cycle+1):
        if i > 1 and (i-1) % 40 == 0:
            print(''.join(row))
            row = []
        row.append(pixels[i])
    print(''.join(row))



def process(command, value, cycle, register):
    measurement = None
    if command == 'noop':
        if cycle + 1 >= 20 and (cycle + 1 - 20) % 40 == 0:
            measurement = register * (cycle + 1)
        return measurement, cycle + 1, register
    elif command == 'addx':
        for i in [1, 2]:
            if cycle + i >= 20 and (cycle + i - 20) % 40 == 0:
                measurement = register * (cycle + i)
        return measurement, cycle + 2, register + value
    else:
        raise Exception()


def process_2(command, value, cycle, register):
    new_pixels = {}
    num_cycles = 2 if command == 'addx' else 1
    
    for i in range(1, num_cycles+1):
        crt_position = (cycle + i) % 40
        if crt_position in [register, register+1, register+2]:
            new_pixels[cycle + i] = 'X'
        else:
            new_pixels[cycle + i] = '.'

    if command == 'addx':
        register += value

    return new_pixels, cycle + num_cycles, register


def parse_line(line):
    parts = line.strip().split(' ')
    command = parts[0]
    value = int(parts[1]) if len(parts) > 1 else None
    return command, value


def run_tests():
    test_inputs = """
    addx 15
    addx -11
    addx 6
    addx -3
    addx 5
    addx -1
    addx -8
    addx 13
    addx 4
    noop
    addx -1
    addx 5
    addx -1
    addx 5
    addx -1
    addx 5
    addx -1
    addx 5
    addx -1
    addx -35
    addx 1
    addx 24
    addx -19
    addx 1
    addx 16
    addx -11
    noop
    noop
    addx 21
    addx -15
    noop
    noop
    addx -3
    addx 9
    addx 1
    addx -3
    addx 8
    addx 1
    addx 5
    noop
    noop
    noop
    noop
    noop
    addx -36
    noop
    addx 1
    addx 7
    noop
    noop
    noop
    addx 2
    addx 6
    noop
    noop
    noop
    noop
    noop
    addx 1
    noop
    noop
    addx 7
    addx 1
    noop
    addx -13
    addx 13
    addx 7
    noop
    addx 1
    addx -33
    noop
    noop
    noop
    addx 2
    noop
    noop
    noop
    addx 8
    noop
    addx -1
    addx 2
    addx 1
    noop
    addx 17
    addx -9
    addx 1
    addx 1
    addx -3
    addx 11
    noop
    noop
    addx 1
    noop
    addx 1
    noop
    noop
    addx -13
    addx -19
    addx 1
    addx 3
    addx 26
    addx -30
    addx 12
    addx -1
    addx 3
    addx 1
    noop
    noop
    noop
    addx -9
    addx 18
    addx 1
    addx 2
    noop
    noop
    addx 9
    noop
    noop
    noop
    addx -1
    addx 2
    addx -37
    addx 1
    addx 3
    noop
    addx 15
    addx -21
    addx 22
    addx -6
    addx 1
    noop
    addx 2
    addx 1
    noop
    addx -10
    noop
    noop
    addx 20
    addx 1
    addx 2
    addx 2
    addx -6
    addx -11
    noop
    noop
    noop
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 13140:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    run_2(test_inputs)


if __name__ == "__main__":
    run_tests()

    input = read_inputs(10)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
