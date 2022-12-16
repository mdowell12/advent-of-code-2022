from datetime import datetime
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
    valves_with_nonzero_flow = [v for v in valves if v[1] != 0]
    valve_to_pressure = {v[0]: v[1] for v in valves}
    valve_name_to_valve = {v[0]: v for v in valves}
    total_release = sum(valve_name_to_valve[v[0]][1] for v in valves_with_nonzero_flow)
    starting_valve = [v for v in valves if v[0] == 'AA'][0]
    max_at_valve = defaultdict(lambda: 0)

    best_score = 0

    paths = [Path(starting_valve, elephant_last_valve=starting_valve)]
    for i in range(26):
        next_paths = []
        path_start = datetime.now()
        for path in paths:

            if path.all_valves_open(valves_with_nonzero_flow):
                final_score = calc_score_for_finished_path(path, i, 26, total_release)
                max_at_valve[path.names_and_opened()] = final_score
                if final_score > best_score:
                    best_score = final_score
                continue

            path.release_pressure(valve_to_pressure)

            neighbors = path.neighbors(valve_name_to_valve)
            for neighbor in neighbors:
                if neighbor.pressure_released >= max_at_valve[neighbor.names_and_opened()]:
                    max_at_valve[neighbor.names_and_opened()] = neighbor.pressure_released
                    next_paths.append(neighbor)
        path_end = datetime.now()

        dedupe_start = datetime.now()
        next_paths_deduped = {}
        for path in next_paths:
            if path.names_and_opened() not in next_paths_deduped or path.pressure_released > next_paths_deduped[path.names_and_opened()].pressure_released:
                next_paths_deduped[path.names_and_opened()] = path
        paths = [path for path in sorted([p for p in next_paths_deduped.values()], key=lambda p: p.pressure_released)][-100000:]

        dedupe_end = datetime.now()
        path_elapsed = (path_end-path_start).seconds
        dedupe_elapsed = (dedupe_end-dedupe_start).seconds
        print(f'min {i+1} with {len(paths)} paths deduped from a possible {len(next_paths)}. Path took {path_elapsed} dedupe took {dedupe_elapsed}')

        if paths[-1].pressure_released > best_score:
            best_score = paths[-1].pressure_released

    return best_score


def calc_score_for_finished_path(finished_path, current_minute, total_minutes, total_release_on_map):
    minutes_remaining = total_minutes - current_minute
    return finished_path.pressure_released + minutes_remaining * total_release_on_map



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

    def names(self):
        return f'{self.last_valve[0]},{self.elephant_last_valve[0]}'

    def names_and_opened(self):
        opened = ','.join(sorted([i for i in self.opened_valves]))
        return f'{self.last_valve[0]},{self.elephant_last_valve[0]},{opened}'

    def neighbors(self, valve_name_to_valve):
        result = []

        if self.elephant_last_valve is None:
            for valve_name in self.last_valve[2]:
                valve = valve_name_to_valve[valve_name]
                result.append(self.copy(last_valve=valve))
        else:
            valve_name_combos = product(self.last_valve[2], self.elephant_last_valve[2]) if self.last_valve[0] != self.elephant_last_valve[0] else combinations(set(self.last_valve[2]).union(self.elephant_last_valve[2]), 2)
            for valve_name, elephant_valve_name in valve_name_combos:
                valve = valve_name_to_valve[valve_name]
                elephant_valve = valve_name_to_valve[elephant_valve_name]
                copy = self.copy(last_valve=valve, elephant_last_valve=elephant_valve)
                result.append(copy)

            if self.current_valve_is_closed() and self.last_valve[1] != 0:
                with_current_opened = self.open_current_valve()
                for valve_name in with_current_opened.elephant_last_valve[2]:
                    valve = valve_name_to_valve[valve_name]
                    result.append(with_current_opened.copy(elephant_last_valve=valve))
                if with_current_opened.elephant_valve_is_closed() and with_current_opened.elephant_last_valve[1] != 0:
                    with_elephant_opened = with_current_opened.open_elephant_valve()
                    result.append(with_elephant_opened)
            if self.elephant_valve_is_closed() and self.elephant_last_valve[1] != 0:
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
        opened = sorted([i for i in self.opened_valves])
        return f'me={self.last_valve[0]} elephant={self.elephant_last_valve[0]} opened={opened} released={self.pressure_released}'


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
