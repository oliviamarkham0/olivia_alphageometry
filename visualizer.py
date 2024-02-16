from problem import Problem, Definition, Theorem, EmptyDependency
from graph import Graph
import graph as gh
from timeout_decorator import timeout, TimeoutError


defs_file = 'defs.txt'
theorems_file = 'rules.txt'
input_str = "a b c = triangle a b c; d = eq_triangle d b a; e = midpoint e a d; f = on_bline f b a; g = midpoint g b c; h = midpoint h c g; i = on_bline i e b; j = eq_triangle j a d; k = on_tline k i h b; l = on_tline l e h b; m = midpoint m l b; n = angle_bisector n k g c; o = eq_triangle o n h"
@timeout(5)  # Timeout in seconds (1 seconds)
def process_problem(input_str, defs_file, theorems_file):
    problem = Problem.from_txt(input_str)
    definitions = Definition.from_txt_file(defs_file, to_dict=True)
    theorems = Theorem.from_txt_file(theorems_file, to_dict=True)
    graph, dependencies = Graph.build_problem(problem, definitions, verbose=False)
    return graph

g = process_problem(input_str, defs_file, theorems_file)
gh.nm.draw(
    g.type2nodes[gh.Point],
    g.type2nodes[gh.Line],
    g.type2nodes[gh.Circle],
    g.type2nodes[gh.Segment],
    display = True)
