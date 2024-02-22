from problem import Problem, Definition, Theorem
from graph import Graph
import graph as gh
from timeout_decorator import timeout


defs_file = 'defs.txt'
theorems_file = 'rules.txt'
input_str = "a b c = triangle a b c; d = incenter d a c b; e = on_pline e a d b; f = angle_mirror f e b d; g = angle_bisector g b d a; h = eqangle3 h b c e d f; i = angle_bisector i d h a; j = eqangle3 j i e b c d; k = circle k g h a; l = excenter2 l d f g k e a; m = angle_bisector m k c l; n = eqdistance n d f a; o = segment o k ? eqangle g h g k h k g h"
@timeout(10)
def process_problem(input_str, defs_file, theorems_file):
    problem = Problem.from_txt(input_str)
    definitions = Definition.from_txt_file(defs_file, to_dict=True)
    graph, dependencies = Graph.build_problem(problem, definitions, verbose=False)
    return graph

g = process_problem(input_str, defs_file, theorems_file)
gh.nm.draw(
    g.type2nodes[gh.Point],
    g.type2nodes[gh.Line],
    g.type2nodes[gh.Circle],
    g.type2nodes[gh.Segment],
    display = True)
