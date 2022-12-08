from solutions.get_inputs import read_inputs
from solutions.grid import Grid2D


def run_1(inputs):
    rows = [list(line.strip()) for line in inputs]
    grid = Grid2D(rows, map_fn=int)
    visible = []
    for position, height in grid:
        x, y = position
        if is_visible(grid, x, y, height):
            visible.append(position)
    return len(visible)


def run_2(inputs):
    rows = [list(line.strip()) for line in inputs]
    grid = Grid2D(rows, map_fn=int)
    best_score = 0
    for position, height in grid:
        scenic_score = get_scenic_score(grid, position, height)
        if scenic_score > best_score:
            best_score = scenic_score
    return best_score


def get_scenic_score(grid, position, height):
    scores = []
    x, y = position

    left = 0
    for other_x in range(x-1, -1, -1):
        if not grid.position_is_in_grid((other_x, y)):
            break
        left += 1
        if grid.value_at_position((other_x, y)) >= height:
            break
    scores.append(left)

    right = 0
    for other_x in range(x+1, grid.get_max_x()+1):
        if not grid.position_is_in_grid((other_x, y)):
            break
        right += 1
        if grid.value_at_position((other_x, y)) >= height:
            break
    scores.append(right)

    up = 0
    for other_y in range(y-1, -1, -1):
        if not grid.position_is_in_grid((x, other_y)):
            break
        up += 1
        if grid.value_at_position((x, other_y)) >= height:
            break
    scores.append(up)

    down = 0
    for other_y in range(y+1, grid.get_max_y()+1):
        if not grid.position_is_in_grid((x, other_y)):
            break
        down += 1
        if grid.value_at_position((x, other_y)) >= height:
            break
    scores.append(down)

    result = 1
    for score in scores:
        result *= score
    return result


def is_visible(grid, x, y, value):
    # Check if x,y is on the edge
    if x == 0 or y == 0 or x == grid.get_max_x() or y == grid.get_max_y():
        return True

    if all(grid.value_at_position((other_x, y)) < value for other_x in range(0, x)):
        return True

    if all(grid.value_at_position((other_x, y)) < value for other_x in range(x+1, grid.get_max_x()+1)):
        return True

    if all(grid.value_at_position((x, other_y)) < value for other_y in range(0, y)):
        return True

    if all(grid.value_at_position((x, other_y)) < value for other_y in range(y+1, grid.get_max_y()+1)):
        return True

    return False


def run_tests():
    test_inputs = """
    30373
    25512
    65332
    33549
    35390
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 21:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 8:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(8)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
