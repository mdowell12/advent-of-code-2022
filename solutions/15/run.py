from solutions.get_inputs import read_inputs


def run_1(inputs, row):
    sensors = parse_inputs(inputs)
    invalid_beacon_points = invalid_beacon_points_for_row(sensors, row)
    return len(invalid_beacon_points)


def run_2(inputs, upper_bound):
    sensors = parse_inputs(inputs)
    closest_beacons = set(s.closest_beacon for s in sensors)
    sensor_positions = set(s.position for s in sensors)
    for y in range(upper_bound):
        invalid_intervals = invalid_beacon_intervals_for_row(sensors, y)
        if y % 10000 == 0:
            print(f'2 for y {y}')
        potential_positions = valid_positions_from_intervals(0, upper_bound, invalid_intervals)
        for x in potential_positions:
            if (x, y) in closest_beacons or (x, y) in sensor_positions:
                continue
            return x * 4000000 + y
    raise Exception('No solution found')


def valid_positions_from_intervals(left_bound, right_bound, invalid_intervals):
    result = []
    current_left = left_bound
    for i, interval in enumerate(invalid_intervals):
        for x in range(current_left, interval[0]):
            result.append(x)
            current_left = x
        next_right = invalid_intervals[i+1][0] if i + 1 < len(invalid_intervals) else right_bound
        for x in range(interval[1]+1, next_right):
            result.append(x)
    return result


def invalid_beacon_points_for_row(sensors, row):
    invalid_beacon_points = set()
    invalid_intervals = invalid_beacon_intervals_for_row(sensors, row)
    closest_beacons = set(s.closest_beacon for s in sensors)
    sensor_positions = set(s.position for s in sensors)
    for left, right in invalid_intervals:
        for x in range(left, right+1):
            point = (x, row)
            if point not in closest_beacons and point not in sensor_positions:
                invalid_beacon_points.add(point)

    return invalid_beacon_points


def invalid_beacon_intervals_for_row(sensors, row):
    intervals = []
    for s in sensors:
        y_dist = abs(s.position[1] - row)
        if y_dist > s.distance:
            continue
        left_bound = s.position[0] - (s.distance - y_dist)
        right_bound = s.position[0] + (s.distance - y_dist)
        intervals.append([left_bound, right_bound])
    intervals = collapse_intervals(intervals)
    return intervals


def collapse_intervals(intervals):
    if not intervals:
        return []
    intervals = sorted(intervals)
    current_i = 0
    result = [intervals[current_i]]
    for interval in intervals:
        current_interval = result[current_i]
        if interval[0] <= current_interval[1]:
            result[current_i] = (current_interval[0], max(interval[1], current_interval[1]))
        else:
            result.append(interval)
            current_i += 1

    return result


def parse_inputs(inputs):
    sensors = []
    for line in inputs:
        parts = [i for i in line.strip().split(' ') if 'x=' in i or 'y=' in i]
        parts = [int(i.strip().replace('x=', '').replace('y=', '').replace(',', '').replace(':', '')) for i in parts]
        sensors.append(Sensor((parts[0], parts[1]), (parts[2], parts[3])))
    return sensors


class Sensor:

    def __init__(self, position, closest_beacon):
        self.position = position
        self.closest_beacon = closest_beacon
        self.distance = manhattan_distance(position, closest_beacon)

    def is_invalid_beacon(self, other_position):
        distance_to_other = manhattan_distance(self.position, other_position)
        return distance_to_other <= self.distance

    def __repr__(self):
        return f'({self.position[0]},{self.position[1]})'


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def run_tests():
    test_inputs = """
    Sensor at x=2, y=18: closest beacon is at x=-2, y=15
    Sensor at x=9, y=16: closest beacon is at x=10, y=16
    Sensor at x=13, y=2: closest beacon is at x=15, y=3
    Sensor at x=12, y=14: closest beacon is at x=10, y=16
    Sensor at x=10, y=20: closest beacon is at x=10, y=16
    Sensor at x=14, y=17: closest beacon is at x=10, y=16
    Sensor at x=8, y=7: closest beacon is at x=2, y=10
    Sensor at x=2, y=0: closest beacon is at x=2, y=10
    Sensor at x=0, y=11: closest beacon is at x=2, y=10
    Sensor at x=20, y=14: closest beacon is at x=25, y=17
    Sensor at x=17, y=20: closest beacon is at x=21, y=22
    Sensor at x=16, y=7: closest beacon is at x=15, y=3
    Sensor at x=14, y=3: closest beacon is at x=15, y=3
    Sensor at x=20, y=1: closest beacon is at x=15, y=3
    """.strip().split('\n')

    result_1 = run_1(test_inputs, 10)
    if result_1 != 26:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs, 20)
    if result_2 != 56000011:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(15)

    result_1 = run_1(input, 2000000)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input, 4000000)
    print(f"Finished 2 with result {result_2}")
