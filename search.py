from BirdsOfAFeatherNode import BirdsOfAFeatherNode

closed = set()
node_count = 0
goal_node = None


def reset_depth_first_search_no_repeats():
    global closed, node_count, goal_node
    closed = set()
    node_count = 0
    goal_node = None


def depth_first_search_no_repeats(node):
    global closed, node_count, goal_node
    node_count += 1
    if node.is_goal():
        goal_node = node
        return True
    node_str = repr(node)
    if node_str in closed:
        return False
    for child in node.expand():
        if depth_first_search_no_repeats(child):
            return True
    closed.add(node_str)
    return False


def test_random_solve():
    reset_depth_first_search_no_repeats()
    root = BirdsOfAFeatherNode.create_initial()  # (367297990)
    print(root)
    if root.has_separated_flock():
        print('Separated flock - search is futile.')
    elif depth_first_search_no_repeats(root):
        # successful search
        print('Goal node found in {} nodes.'.format(node_count))
        print('Solution string:', goal_node.solution_string())
    else:
        # unsuccessful search
        print('Goal node not found in {} nodes.'.format(node_count))


def experiment1():
    start_seed = 0
    num_seeds = 100
    num_solved = 0
    unsolvable = []
    for seed in range(start_seed, start_seed + num_seeds):
        print('Seed {}: '.format(seed), end='')
        node = BirdsOfAFeatherNode.create_initial(seed)
        solvable = False if node.has_separated_flock() else depth_first_search_no_repeats(node)
        if solvable:
            print('solved.')
            num_solved += 1
        else:
            unsolvable.append(seed)
            print('unsolvable seed {}.'.format(seed))
            print(node)
    print('Seeds {}-{}: {} solved, {} not solvable'.format(start_seed, start_seed + num_seeds - 1, num_solved,
                                                           num_seeds - num_solved))
    print('          Unsolvable: ', unsolvable)


def experiment2():
    start_seed = int(input('Start seed? '))
    num_seeds = int(input('How many seeds? '))
    num_solved = 0
    unsolvable = []
    odd_birds = []
    separated_flocks = []
    for seed in range(start_seed, start_seed + num_seeds):
        print('Seed {}: '.format(seed), end='')
        node = BirdsOfAFeatherNode.create_initial(seed)
        if node.has_odd_bird():
            solvable = False
            odd_birds.append(seed)
        elif node.has_separated_flock():
            solvable = False
            separated_flocks.append(seed)
        else:
            solvable = depth_first_search_no_repeats(node)
        if solvable:
            print('solved.')
            num_solved += 1
        else:
            unsolvable.append(seed)
            print('unsolvable seed {}.'.format(seed))
            print(node)
    print('Seeds {}-{}: {} solved, {} not solvable'.format(start_seed, start_seed + num_seeds - 1, num_solved,
                                                           num_seeds - num_solved))
    print('Unsolvable odd birds: ', odd_birds)
    print('    Separated flocks: ', separated_flocks)
    print('          Unsolvable: ', unsolvable)


if __name__ == '__main__':
    # test_random_solve()
    experiment1()  # TWN: ran on my laptop in 1m27.726s, whereas original distributed Java version ran in 31.553s
    # experiment2()
