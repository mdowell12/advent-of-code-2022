from solutions.get_inputs import read_inputs


def run_1(inputs):
    root = build_file_tree(inputs)
    # root.print_tree()
    directory_sizes = get_directory_sizes(root)
    result = 0
    for _, total_size in directory_sizes.items():
        if total_size <= 100000:
            result += total_size
    return result


def run_2(inputs):
    root = build_file_tree(inputs)
    directory_sizes = get_directory_sizes(root)    
    candidates = [d for d in directory_sizes.values() if directory_sizes['root'] - d <= 40000000]
    return sorted(candidates)[0]


def get_directory_sizes(directory, sizes=None):
    if sizes is None:
        sizes = {}

    if not directory.is_dir():
        return sizes

    total_size = 0
    for name, node in directory.children.items():
        if not node.is_dir():
            total_size += node.size
        else:
            sizes = get_directory_sizes(node, sizes=sizes)
            total_size += sizes[node.get_full_path()]
    if directory.get_full_path() in sizes:
        raise Exception(f'{sizes} {directory.get_full_path()}')
    sizes[directory.get_full_path()] = total_size

    return sizes


def build_file_tree(inputs):
    cur_dir = None
    root = Directory('root', None)
    is_directory_listing = False

    for line in inputs:
        line = line.strip()
        # print(f'directory={cur_dir} is_directory_listing={is_directory_listing} next_line={line}')
        if line[0] == '$':
            is_directory_listing = False
            parts = line.split(' ')
            command = parts[1]
            if command == 'cd':
                target = parts[2]
                if target == '/':
                    cur_dir = root
                elif target == '..':
                    cur_dir = cur_dir.parent
                else:
                    cur_dir = cur_dir.children[target]
            elif command == 'ls':
                is_directory_listing = True
            else:
                raise Exception(f'Unknown command {command}')
        elif is_directory_listing:
            if line[:3] == 'dir':
                cur_dir.add_child_directory(line.split(' ')[-1])
            else:
                size, name = line.split(' ')
                cur_dir.add_child_file(size, name)
        else:
            raise Exception(f'Unknown input {line}')

    return root



class Directory:

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = {}

    def is_dir(self):
        return True

    def add_child_directory(self, name):
        if name in self.children:
            raise Exception()
        self.children[name] = Directory(name, self)

    def add_child_file(self, size, name):
        if name in self.children:
            raise Exception()
        self.children[name] = File(name, int(size))

    def get_full_path(self):
        parts = [self.name]
        next = self.parent
        while next is not None:
            parts.append(next.name)
            next = next.parent
        return '/'.join(reversed(parts))

    def print_tree(self, depth=0):
        print(' '*depth + self.name)
        for name, node in self.children.items():
            if node.is_dir():
                node.print_tree(depth=depth+1)
            else:
                print(' '*depth + ' ' + node.name + ' ' + str(node.size))

    def __repr__(self):
        children = ','.join(c for c in self.children)
        return f'{self.get_full_path()}[{children}]'


class File:

    def __init__(self, name, size):
        self.name = name
        self.size = size

    def is_dir(self):
        return False


def run_tests():
    test_inputs = """
    $ cd /
    $ ls
    dir a
    14848514 b.txt
    8504156 c.dat
    dir d
    $ cd a
    $ ls
    dir e
    29116 f
    2557 g
    62596 h.lst
    $ cd e
    $ ls
    584 i
    $ cd ..
    $ cd ..
    $ cd d
    $ ls
    4060174 j
    8033020 d.log
    5626152 d.ext
    7214296 k
    """.strip().split('\n')

    result_1 = run_1(test_inputs)
    if result_1 != 95437:
        raise Exception(f"Test 1 did not pass, got {result_1}")

    result_2 = run_2(test_inputs)
    if result_2 != 24933642:
        raise Exception(f"Test 2 did not pass, got {result_2}")


if __name__ == "__main__":
    run_tests()

    input = read_inputs(7)

    result_1 = run_1(input)
    print(f"Finished 1 with result {result_1}")

    result_2 = run_2(input)
    # 30324496 too high
    # 5999 too low
    print(f"Finished 2 with result {result_2}")
