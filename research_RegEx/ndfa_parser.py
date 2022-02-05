from research_RegEx.ndfa import NDFA
from research_RegEx.regex_tree import RegExTree
import research_RegEx.regex_symbol as rs


def finish(i: int, automata: NDFA):
    # check if the end already exist
    if automata.end == -1:
        # create the end
        automata.increment_size()
        automata.end = automata.sz
        automata.accept[automata.sz] = True
    if automata.epsilon_transitions[i] is None:
        automata.epsilon_transitions[i] = []
    automata.epsilon_transitions[i].append(automata.end)


def parse_ndfa(rg_tree: RegExTree):
    automaton = NDFA(rg_tree)
    parse_ndfa_node(rg_tree, automaton, True)
    return automaton


def parse_ndfa_node(rg_tree, automata, can_finish):
    # Leaf
    if rg_tree.sub_trees is None or len(rg_tree.sub_trees) == 0:
        process_leaf(rg_tree, automata, can_finish)

    # Operations
    if rg_tree.root == rs.ALTERN:
        process_altern(rg_tree, automata, can_finish)
    elif rg_tree.root == rs.ETOILE:
        process_etoile(rg_tree, automata, can_finish)
    elif rg_tree.root == rs.CONCAT:
        process_concat(rg_tree, automata, can_finish)
    return


def process_leaf(rg_tree: RegExTree, automata, can_finish):
    if not (chr(rg_tree.root).isalnum()):
        print("Error : A Leaf is not a Letter or a Digit", rg_tree.root)
    automata.epsilon_transitions[automata.sz] = []
    # the state have a transition with the end
    if can_finish:
        my_id = automata.sz
        if automata.end == -1:
            # create end
            automata.increment_size()
            automata.end = automata.sz
            automata.accept[automata.sz] = True
        automata.transition_table[my_id][rg_tree.root] = automata.end
    # create new state
    else:
        automata.transition_table[automata.sz][rg_tree.root] = automata.sz + 1
        automata.increment_size()
        automata.epsilon_transitions[automata.sz] = []


def process_altern(rg_tree, automata, can_finish):
    print("automata.sz", automata.sz)
    my_id = automata.sz
    automata.epsilon_transitions[my_id] = []

    join = []
    for node in rg_tree.sub_trees:
        # create and add new state
        automata.increment_size()
        automata.epsilon_transitions[my_id].append(automata.sz)
        # parse sub-trees
        parse_ndfa_node(node, automata, False)
        # add last state id to the join list
        join.append(automata.sz)

    # join branches
    for i in range(len(join)):
        if can_finish:
            finish(join[i], automata)
        else:
            if i == 0:
                # create new join state
                automata.increment_size()
                automata.epsilon_transitions[automata.sz] = []
            automata.epsilon_transitions[join[i]].append(automata.sz)
    return


def process_etoile(rg_tree, automata, can_finish):
    # can go to end or search the subTree
    first = automata.sz

    # search
    automata.increment_size()
    if automata.epsilon_transitions[first] is None:
        automata.epsilon_transitions[first] = []
    automata.epsilon_transitions[first].append(automata.sz)
    automata.epsilon_transitions[automata.sz] = []
    parse_ndfa_node(rg_tree, automata, can_finish)

    # loop
    automata.epsilon_transitions[automata.sz].append(first + 1)

    # end
    if can_finish:
        finish(automata.sz, automata)
        # skip the search
        automata.epsilon_transitions[first].append(automata.end)
    else:
        automata.epsilon_transitions[automata.sz].append(automata.sz + 1)
        automata.increment_size()
        automata.epsilon_transitions[automata.sz] = []
        # skip the search
        automata.epsilon_transitions[first].append(automata.sz)


def process_concat(rg_tree, automata, can_finish):
    # Left
    parse_ndfa_node(rg_tree.sub_trees[0], automata, False)
    # Join
    automata.epsilon_transitions[automata.sz].append(automata.sz + 1)
    automata.increment_size()
    automata.epsilon_transitions[automata.sz] = []
    # Right
    parse_ndfa_node(rg_tree.sub_trees[1], automata, can_finish)
