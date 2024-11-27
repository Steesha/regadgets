from z3 import sat, Z3Exception, Z3_UNINTERPRETED_SORT, is_array, Or, Solver
from copy import deepcopy
def z3_get_models(s: Solver):
    s = deepcopy(s)
    while s.check() == sat:
        m = s.model()
        # Create a new constraint the blocks the current model
        block = []
        for d in m:
            # d is a declaration
            if d.arity() > 0:
                raise Z3Exception("uninterpreted functions are not supported")
            # create a constant from declaration
            c = d()
            if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
                raise Z3Exception("arrays and uninterpreted sorts are not supported")
            block.append(c != m[d])
        s.add(Or(block))
        yield m
    return