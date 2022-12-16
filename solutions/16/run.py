from collections import defaultdict
from itertools import product, combinations

from solutions.get_inputs import read_inputs


def run_1(inputs):
    valves = parse_inputs(inputs)
    valve_to_pressure = {v[0]: v[1] for v in valves}
    valve_name_to_valve = {v[0]: v for v in valves}
    starting_valve = [v for v in valves if v[0] == 'AA'][0]
    max_at_valve = defaultdict(lambda: 0)
    
    paths = [Path(starting_valve)]
    for i in range(30):
        next_paths = []
        for path in paths:
            path.release_pressure(valve_to_pressure)
            if path.all_valves_open(valves):
                next_paths.append(path)
                continue
            neighbors = path.neighbors(valve_name_to_valve)
            for neighbor_valve in neighbors:
                if neighbor_valve.pressure_released >= max_at_valve[neighbor_valve.last_valve[0]]:
                    max_at_valve[neighbor_valve.last_valve[0]] = neighbor_valve.pressure_released
                    next_paths.append(neighbor_valve)
            if path.current_valve_is_closed():
                next_paths.append(path.open_current_valve())
        paths = [p for p in next_paths]
        print(f'min {i} with {len(paths)} possible paths')
        

    best = sorted(paths, key=lambda p: p.pressure_released)[-1]
    return best.pressure_released


def run_2(inputs):
    valves = parse_inputs(inputs)
    valve_to_pressure = {v[0]: v[1] for v in valves}
    valve_name_to_valve = {v[0]: v for v in valves}
    starting_valve = [v for v in valves if v[0] == 'AA'][0]
    max_at_valve = defaultdict(lambda: 0)
    
    paths = [Path(starting_valve, elephant_last_valve=starting_valve)]
    for i in range(26):
        next_paths = []
        for path in paths:
            path.release_pressure(valve_to_pressure)
            # if path.all_valves_open(valves):
            #     next_paths.append(path)
            #     continue
            neighbors = path.neighbors(valve_name_to_valve)
            # import pdb; pdb.set_trace()
            for neighbor in neighbors:
                last_valve_name = neighbor.last_valve[0]
                elephant_last_valve_name = neighbor.elephant_last_valve[0]
                if neighbor.pressure_released >= max_at_valve[','.join(sorted([last_valve_name, elephant_last_valve_name]))]:
                    if not path.all_valves_open(valves):
                        max_at_valve[','.join(sorted([last_valve_name, elephant_last_valve_name]))] = neighbor.pressure_released
                        next_paths.append(neighbor)
                # else:
                #     print('visted')
                # # if neighbor.pressure_released >= max_at_valve[last_valve_name] >= max_at_valve[path.last_valve[0]]:

            # if path.current_valve_is_closed() and path.elephant_valve_is_closed():
            #     next_paths.append(path.open_current_valve().open_elephant_valve())
            # if path.elephant_valve_is_closed():
            #     next_paths.append(path.open_elephant_valve())
        paths = [p for p in next_paths]
        print(f'min {i} with {len(paths)} possible paths')
        

    best = sorted(paths, key=lambda p: p.pressure_released)[-1]
    return best.pressure_released


class Path:

    def __init__(self, last_valve, opened_valves=None, pressure_released=0, elephant_last_valve=None):
        self.opened_valves = set() if opened_valves is None else opened_valves
        self.last_valve = last_valve
        self.pressure_released = pressure_released
        self.elephant_last_valve = elephant_last_valve

    def all_valves_open(self, valves):
        return len(self.opened_valves) == len(valves)

    def release_pressure(self, valve_to_pressure):
        for valve_name in self.opened_valves:
            self.pressure_released += valve_to_pressure[valve_name]

    def current_valve_is_closed(self):
        return self.last_valve[0] not in self.opened_valves

    def elephant_valve_is_closed(self):
        if self.elephant_last_valve is None:
            raise Exception()
        return self.elephant_last_valve[0] not in self.opened_valves

    def open_current_valve(self):
        copy = self.copy()
        copy.opened_valves.add(copy.last_valve[0])
        return copy

    def open_elephant_valve(self):
        if self.elephant_last_valve is None:
            raise Exception()
        copy = self.copy()
        copy.opened_valves.add(copy.elephant_last_valve[0])
        return copy

    def neighbors(self, valve_name_to_valve):
        result = []
        
        if self.elephant_last_valve is None:
            for valve_name in self.last_valve[2]:
                valve = valve_name_to_valve[valve_name]
                result.append(self.copy(last_valve=valve))
        else:
            # import pdb; pdb.set_trace()
            valve_name_combos = combinations(set(self.last_valve[2]).union(self.elephant_last_valve[2]), 2)
            # valve_name_combos = product(self.last_valve[2], self.elephant_last_valve[2])
            for valve_name, elephant_valve_name in valve_name_combos:
                valve = valve_name_to_valve[valve_name]
                elephant_valve = valve_name_to_valve[elephant_valve_name]
                result.append(self.copy(last_valve=valve, elephant_last_valve=elephant_valve))

            if self.current_valve_is_closed():
                with_current_opened = self.open_current_valve()
                for valve_name in with_current_opened.elephant_last_valve[2]:
                    valve = valve_name_to_valve[valve_name]
                    result.append(with_current_opened.copy(elephant_last_valve=valve))
                if with_current_opened.elephant_valve_is_closed():
                    with_elephant_opened = with_current_opened.open_current_valve()
                    result.append(with_elephant_opened)
            elif self.elephant_valve_is_closed():
                with_elephant_opened = self.open_elephant_valve()
                for valve_name in with_elephant_opened.last_valve[2]:
                    valve = valve_name_to_valve[valve_name]
                    result.append(with_elephant_opened.copy(last_valve=valve))
        return result

    def copy(self, last_valve=None, elephant_last_valve=None):
        last_valve = self.last_valve if last_valve is None else last_valve
        elephant_last_valve = self.elephant_last_valve if elephant_last_valve is None else elephant_last_valve
        return Path(
            last_valve,
            opened_valves=set(i for i in self.opened_valves), 
            pressure_released=self.pressure_released, 
            elephant_last_valve=elephant_last_valve
        )

    def __repr__(self):
        return f'me={self.last_valve[0]} elephant={self.elephant_last_valve[0]} opened={self.opened_valves} released={self.pressure_released}'


def parse_inputs(inputs):
    valves = []
    for line in inputs:
        parts = line.strip().split(' ')
        name = parts[1]
        rate = int(parts[4].replace('rate=', '').replace(';', ''))
        other_valves = tuple(p.replace(',', '').strip() for p in parts[9:])
        valves.append((name, rate, other_valves))
    return valves


def run_tests():
    test_inputs = """
    Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    Valve BB has flow rate=13; tunnels lead to valves CC, AA
    Valve CC has flow rate=2; tunnels lead to valves DD, BB
    Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
    Valve EE has flow rate=3; tunnels lead to valves FF, DD
    Valve FF has flow rate=0; tunnels lead to valves EE, GG
    Valve GG has flow rate=0; tunnels lead to valves FF, HH
    Valve HH has flow rate=22; tunnel leads to valve GG
    Valve II has flow rate=0; tunnels lead to valves AA, JJ
    Valve JJ has flow rate=21; tunnel leads to valve II
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 1651:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 1707:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(16)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    print(f"Finished 2 with result {result_2}")
