from solutions.get_inputs import read_inputs


def run_1(inputs):
    print(len(inputs))
    cubes = []
    for line in inputs:
        cube = Cube(tuple(int(i) for i in line.strip().split(',')))
        cubes = cube.place_cube(cubes)
    return sum(c.total_uncovered() for c in cubes)


def run_2(inputs):
    # return 58


class Cube:

    def __init__(self, position):
        self.position = position
        # self.faces_covered = {i: False for i in range(6)}
        self.faces_covered = 0

    def place_cube(self, other_cubes):
        for cube in other_cubes:
            if self.is_touching(cube):
                cube.faces_covered += 1
                self.faces_covered += 1
        other_cubes.append(self)
        return other_cubes

    def is_touching(self, other_cube):
        distance = abs(self.position[0] - other_cube.position[0]) + abs(self.position[1] - other_cube.position[1]) + abs(self.position[2] - other_cube.position[2])
        if distance == 0:
            raise Exception(f'duplicate cubes at {self.position}')
        return distance == 1

    def total_uncovered(self):
        # return sum(1 for is_covered in self.faces_covered.values() if not is_covered)
        return 6 - self.faces_covered

    def __repr__(self):
        return f'{self.position} {self.faces_covered}'


def run_tests():
    test_inputs = """
    2,1,1
    1,1,1
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 10:
        raise Exception(f"Test 1.0 did not pass, got {result_1}")

    test_inputs = """
    2,2,2
    1,2,2
    3,2,2
    2,1,2
    2,3,2
    2,2,1
    2,2,3
    2,2,4
    2,2,6
    1,2,5
    3,2,5
    2,1,5
    2,3,5
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 64:
        raise Exception(f"Test 1.1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 58:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(18)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
