# from dfa import DFA

from research_RegEx.regex_parser import parse_expression
from research_RegEx.ndfa_parser import parse_ndfa
from research_RegEx.dfa_parser import parse_dfa, minimize_dfa


def generate_dfa(expression: str):
    rt = parse_expression(expression)
    #print('rt', rt)
    ndfa = parse_ndfa(rt)
    #print('ndfa', ndfa)
    dfa = parse_dfa(ndfa)
    #print('dfa', dfa)
    #minimize_dfa(dfa)
    #print('minimized dfa', dfa)
    return dfa

print(generate_dfa("baba|are").apply("bareknuckle"))

