from solutions.get_inputs import read_inputs
from solutions.grid import Grid2D


def run_1(inputs):
    starting_point = (500, 0)
    grid = parse_inputs(inputs, starting_point)
    units = 0
    while units <= 100000:
        units += 1
        resting_point = drop_sand(grid, starting_point)
        if resting_point is None:
            break
        else:
            grid.set_value_at_position(resting_point, 'o')
    return units - 1


def run_2(inputs):
    starting_point = (500, 0)
    grid = parse_inputs(inputs, starting_point)
    floor = grid.get_max_y() + 2
    units = 0
    while units <= 100000:
        units += 1
        resting_point = drop_sand_2(grid, starting_point, floor)
        if resting_point == starting_point:
            break
        else:
            grid.set_value_at_position(resting_point, 'o')
    return units


def drop_sand(grid, starting_point):
    point = starting_point

    while point[1] < grid.get_max_y():
        x, y = point
        if grid.value_at_position((x, y+1)) == '.':
            point = (x, y+1)
        elif grid.value_at_position((x-1, y+1)) == '.':
            point = (x-1, y+1)
        elif grid.value_at_position((x+1, y+1)) == '.':
            point = (x+1, y+1)
        else:
            return point
    return None


def drop_sand_2(grid, starting_point, floor):
    point = starting_point
    while True:
        x, y = point
        if y == floor - 1:
            return point
        elif grid.value_at_position((x, y+1)) == '.':
            point = (x, y+1)
        elif grid.value_at_position((x-1, y+1)) == '.':
            point = (x-1, y+1)
        elif grid.value_at_position((x+1, y+1)) == '.':
            point = (x+1, y+1)
        else:
            return point
    raise Exception()


def parse_inputs(inputs, starting_point):
    points = set()
    for line in inputs:
        parts = [(int(p.split(',')[0]), int(p.split(',')[1])) for p in line.strip().split(' -> ')]
        for i in range(len(parts)-1):
            left, right = parts[i], parts[i+1]
            if left[0] == right[0]:
                for y in range(min(left[1], right[1]), max(left[1], right[1])+1):
                    points.add((left[0], y))
            elif left[1] == right[1]:
                for x in range(min(left[0], right[0]), max(left[0], right[0])+1):
                    points.add((x, left[1]))
            else:
                raise Exception()
    points.add(starting_point)
    overall_min_x, overall_max_x = min(p[0] for p in points), max(p[0] for p in points)
    overall_min_y, overall_max_y = min(p[1] for p in points), max(p[1] for p in points)

    rows = []
    for y in range(0, overall_max_y + 1):
        row = []
        for x in range(0, overall_max_x + 1):
            row.append('X' if (x,y) in points else '.')
        rows.append(row)

    return Grid2D(rows, default_if_missing='.', print_window=((500-20, 500+20), (0, overall_max_y + 3)))


def run_tests():
    test_inputs = """
    498,4 -> 498,6 -> 496,6
    503,4 -> 502,4 -> 502,9 -> 494,9
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 24:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 93:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(14)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
