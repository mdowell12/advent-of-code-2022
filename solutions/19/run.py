from collections import defaultdict
from math import prod

from solutions.get_inputs import read_inputs


def run_1(inputs):
    blueprints = [Blueprint(line) for line in inputs]
    return sum(b.quality() for b in blueprints)


def run_2(inputs):
    blueprints = [Blueprint(line) for line in inputs[:3]]
    return prod(b.max_geodes(32) for b in blueprints)


class Blueprint:

    def __init__(self, line):
        self.name, self.prices = self._parse(line)

    def _parse(self, line):
        name = line.strip().split(":")[0].split(' ')[1]
        prices = {}
        sentences = line.strip().split(':')[1].split('.')
        prices['ore'] = int(sentences[0].strip().split(' ')[4])
        prices['clay'] = int(sentences[1].strip().split(' ')[4])
        prices['obsidian'] = (int(sentences[2].strip().split(' ')[4]), int(sentences[2].strip().split(' ')[7]))
        prices['geode'] = (int(sentences[3].strip().split(' ')[4]), int(sentences[3].strip().split(' ')[7]))
        return name, prices

    def max_geodes(self, num_minutes):
        games = [self.new_game()]
        for i in range(1, num_minutes+1):

            next_games = []
            for game in games:
                other_games = self.play(game)
                next_games += other_games
            # if i == 8:
                # for g in next_games:
                #     print(g)
                # import pdb; pdb.set_trace()
            # games = self.dedupe(next_games)
            games = next_games

            # def get_keys(game):
            #     result = ['ore']
            #     if game['obsidian'][0] > 0 or game['obsidian'][1] > 0:
            #         result.append('clay')
            #     if game['geode'][0] > 0 or game['geode'][1] > 0:
            #         result.append('obsidian')
            #     return result
            #
            # # Normal way
            # to_add = self.dedupe(games, get_keys, lambda g: (g['ore'], g['clay'], g['obsidian'], g['geode']))
            # games = to_add
            #
            # # Other way
            # def get_keys_2(game):
            #     return ['ore', 'obsidian', 'geode']
            # to_add = self.dedupe(games, get_keys_2, lambda g: (g['ore'], g['obsidian'], g['geode'], g['clay']))
            # games = to_add
            #
            # # Other way
            # def get_keys_3(game):
            #     return ['ore', 'clay', 'geode']
            # to_add = self.dedupe(games, get_keys_3, lambda g: (g['ore'], g['clay'], g['geode'], g['obsidian']))
            # games = to_add
            #
            # # Other way
            # def get_keys_4(game):
            #     return ['obsidian', 'geode', 'clay']
            # to_add = self.dedupe(games, get_keys_4, lambda g: (g['obsidian'], g['geode'], g['clay'], g['ore']))
            # games = to_add

            # for game in games:
            #     print(game)
            print(self.name, i, len(games))

            # if i > 28:
            #     import pdb; pdb.set_trace()

        max_geodes = None
        for game in games:
            geodes = self.num_rocks(game, 'geode')
            if max_geodes is None or geodes > max_geodes:
                print(game)
                max_geodes = geodes

        print('max_geodes', self.name, max_geodes)
        # print('max_geode_crackers', self.name, max_geode_crackers)
        return max_geodes

    # def dedupe(self, games, get_key_fn, sort_key_fn):
    #     to_add = []
    #     sorted_games = sorted(games, key=sort_key_fn)
    #
    #     if len(sorted_games) == 1:
    #         to_add = sorted_games
    #     else:
    #         previous = sorted_games[0]
    #         for j in range(1, len(sorted_games)):
    #             current = sorted_games[j]
    #             keys = get_key_fn(previous)
    #             if all(previous[k] == current[k] for k in keys):
    #                 previous = current
    #             else:
    #                 if all(v[1] < 50 for k, v in previous.items()):
    #                     to_add.append(previous)
    #                 previous = current
    #         to_add.append(previous)
    #     return to_add

    def dedupe(self, games):
        rocks = ['ore', 'clay', 'obsidian', 'geode']
        # games = [g for g in games]
        # import pdb; pdb.set_trace()
        for rock in rocks:
            other_rocks = [r for r in rocks if r != rock]
            sort_keys = other_rocks + [rock]
            to_add = []
            sorted_games = sorted(games, key=lambda g: tuple([g[r] for r in sort_keys]))

            if len(sorted_games) == 1:
                to_add = sorted_games
            else:
                previous = sorted_games[0]
                for j in range(1, len(sorted_games)):
                    current = sorted_games[j]
                    # keys = get_key_fn(previous)
                    if all(previous[k] == current[k] for k in other_rocks):
                        previous = current
                    else:
                        if all(v[1] < 50 for k, v in previous.items()):
                            to_add.append(previous)
                        previous = current
                to_add.append(previous)
            games = to_add
        return games

    def num_rocks(self, game, rock):
        return game[rock][1]

    def play(self, game):
        games = [(game, [])]
        # Make new game for every combination of purchases we could make, keeping track of what the new robots WILL be
        new_robot_batches = self.possible_purchases(game)
        for new_robots in new_robot_batches:
            new_game = self.new_game(parent_game=game)
            games.append((new_game, new_robots))
        # For each of those games, collect an ore for every robot that existed before this turn
        for game, _ in games:
            self.collect(game)
        # For each of those games, add the new robots from the first step to the game's robot counts
        result = []
        for game, new_robots in games:
            valid, game = self.add_robots(game, new_robots)
            if valid:
                result.append(game)
        return result

    def add_robots(self, game, new_robots):
        # if len(new_robots) > 1:
        #     import pdb; pdb.set_trace()
        for robot in new_robots:
            if robot == 'ore':
                game['ore'] = (game['ore'][0]+1, game['ore'][1]-self.prices['ore'])
            elif robot == 'clay':
                game['clay'] = (game['clay'][0]+1, game['clay'][1])
                game['ore'] = (game['ore'][0], game['ore'][1]-self.prices['clay'])
            elif robot == 'obsidian':
                game['obsidian'] = (game['obsidian'][0]+1, game['obsidian'][1])
                game['ore'] = (game['ore'][0], game['ore'][1]-self.prices['obsidian'][0])
                game['clay'] = (game['clay'][0], game['clay'][1]-self.prices['obsidian'][1])
            elif robot == 'geode':
                game['geode'] = (game['geode'][0]+1, game['geode'][1])
                game['ore'] = (game['ore'][0], game['ore'][1]-self.prices['geode'][0])
                game['obsidian'] = (game['obsidian'][0], game['obsidian'][1]-self.prices['geode'][1])
            else:
                raise Exception(robot)
        valid = all(v[1] >= 0 for v in game.values())
        return valid, game

    def possible_purchases(self, game):
        from itertools import combinations
        can_afford = set()
        if game['ore'][1] >= self.prices['ore']:
            can_afford.add('ore')
        if game['ore'][1] >= self.prices['clay']:
            can_afford.add('clay')
        if game['ore'][1] >= self.prices['obsidian'][0] and game['clay'][1] >= self.prices['obsidian'][1]:
            can_afford.add('obsidian')
        if game['ore'][1] >= self.prices['geode'][0] and game['obsidian'][1] >= self.prices['geode'][1]:
            can_afford = {'geode',}
            # can_afford.add('geode')
        # result = [i for i in combinations(can_afford, 1)]
        # dub = [i for i in combinations(can_afford, 2)]
        # if dub:
        #     # import pdb; pdb.set_trace()
        #     result += dub

        # result += [i for i in combinations(can_afford, 3)]
        # import pdb; pdb.set_trace()
        return list([i] for i in can_afford if not self.not_needed_because_have_enough(i, game))
        # return list([i] for i in can_afford)
        # return result

    def not_needed_because_have_enough(self, rock, game):
        if rock == 'geode':
            return False
        prices_using_rock = {
            'ore': [self.prices['ore'], self.prices['clay'], self.prices['obsidian'][0], self.prices['geode'][0]],
            'clay': [self.prices['obsidian'][1]],
            'obsidian': [self.prices['geode'][1]]
        }
        # import pdb; pdb.set_trace()
        num_rock = game[rock][1]
        max_needed = max(prices_using_rock[rock])
        return num_rock > max_needed

    def collect(self, game):
        for rock in ['ore', 'clay', 'obsidian', 'geode']:
            num_robots = game[rock][0]
            game[rock] = (game[rock][0], game[rock][1] + num_robots)

    def new_game(self, parent_game=None):
        if parent_game is None:
            parent_game = {}

        ore = parent_game.get('ore', (1, 0))
        clay = parent_game.get('clay', (0, 0))
        obsidian = parent_game.get('obsidian', (0, 0))
        geode = parent_game.get('geode', (0, 0))
        return {
            'ore': ore,
            'clay': clay,
            'obsidian': obsidian,
            'geode': geode,
        }

    def quality(self):
        max_geodes = self.max_geodes(24)
        return int(self.name) * max_geodes

    def __repr__(self):
        return f'{self.name} {self.prices}'

def run_tests():
    test_inputs = """
    Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
    Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 33:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 56 * 62:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(19)

    # result_1 = run_1(input)
    # print(f"Finished 1 with result {result_1}")

    # result_2 = run_2(input)
    # # 16380 too low
    # # 20580 is not correct
    # print(f"Finished 2 with result {result_2}")
