import numpy as np

from research_RegEx.dfa import TempDFA, DFA
from research_RegEx.ndfa import NDFA


# Parse

def grouping_by_epsilon(automata: NDFA, state: int):
    res = {state}
    if automata.epsilon_transitions[state] is not None:
        for next_state in automata.epsilon_transitions[state]:
            if next_state not in res:
                res.add(next_state)
                res = res.union(grouping_by_epsilon(automata, next_state))
    return res


def parse_dfa(automata: NDFA):
    dfa = TempDFA(automata.sz)
    dfa.grouped_states.append(grouping_by_epsilon(automata, 0))
    parse_dfa_node(dfa, automata, 0)
    return DFA(dfa)


def parse_dfa_node(dfa, ndfa, i):
    # stop
    if len(dfa.grouped_states) == i:
        return

    # Search all the transitions from the set
    for state in dfa.grouped_states[i]:
        for col in range(len(ndfa.transition_table[state])):
            if ndfa.transition_table[state][col] != -1:
                # update the transition table
                gs = grouping_by_epsilon(ndfa, ndfa.transition_table[state][col])
                dfa.transitions[i][col] = gs
                # add the set if it's a new one
                if gs not in dfa.grouped_states:
                    dfa.grouped_states.append(gs)
        # update accept
        dfa.apply[i] = dfa.apply[i] or ndfa.apply[state]
    parse_dfa_node(dfa, ndfa, i + 1)


# --------------------------------------------------------------


# Minimization

def grouping_minimization(min_table, state, res):
    res.add(state)
    # search on line number 'state'
    for col in range(state):
        if (not min_table[state][col]) and col not in res:
            grouping_minimization(min_table, col, res)

    # search on column number 'state'
    for line in range(state + 1, len(min_table)):
        if not min_table[line][state]:
            grouping_minimization(min_table, line, res)

    return res


def get_min_table(dfa: DFA):
    # min_table mark the not equivalent pairs
    min_table = np.full((dfa.size, dfa.size), False, dtype=bool)

    # Basis
    for i in range(dfa.size):
        # Check dead states
        dead_states = True
        for j in range(256):
            if dfa.transitions[i][j] != -1:
                dead_states = False
                break

        for j in range(i):
            if dfa.accept[i] != dfa.accept[j] or dead_states:
                min_table[i][j] = True

    # Induction
    can_mark = True
    while can_mark:
        can_mark = False
        for i in range(dfa.size):
            for j in range(i):
                # check the unmarked pairs
                if not min_table[i][j]:
                    for col in range(256):
                        if dfa.transitions[i][col] != -1:
                            # state i have a col-transition but state j doesn't have it
                            if dfa.transitions[j][col] == -1:
                                min_table[i][j] = True
                                can_mark = True
                            else:
                                i2 = dfa.transitions[i][col]
                                j2 = dfa.transitions[j][col]

                                if j2 < i2:
                                    tmp = j2
                                    j2 = i2
                                    i2 = tmp

                                if i2 != j2 and min_table[i2][j2]:
                                    min_table[i][j] = True
                                    can_mark = True

                        else:
                            # state j have a col-transition but state i doesn't have it
                            if dfa.transitions[j][col] != -1:
                                min_table[i][j] = True
                                can_mark = True
    return min_table


def minimize_dfa(dfa: DFA):
    min_table = get_min_table(dfa)
    # make the link between an old state and a group
    old_sets = np.full(dfa.size, None, dtype=set)
    # make the link between a new state and a group of old states
    new_sets = []
    # extract all the groups
    for i in range(dfa.size):
        if old_sets[i] is None:
            g = set()
            grouping_minimization(min_table, i, g)
            for j in g:
                old_sets[j] = g
            new_sets.append(g)

    sz = len(new_sets)
    if sz == old_sets.size:
        return

    accept_res = np.full(sz, False, dtype=bool)
    transitions_res = np.full((sz, 256), -1, dtype=int)
    i = 0
    for e in new_sets:
        line = e.pop()
        e.add(line)
        for col in range(256):
            if dfa.transitions[line][col] != -1:
                old_state = dfa.transitions[line][col]
                new_state = new_sets.index(old_sets[old_state])
                transitions_res[i][col] = new_state
        accept_res[i] = dfa.accept[line]
        i += 1
    dfa.size = sz
    dfa.accept = accept_res
    dfa.transitions = transitions_res
