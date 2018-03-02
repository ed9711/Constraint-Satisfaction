'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. kenken_csp_model (worth 20/100 marks)
    - A model built using your choice of (1) binary binary not-equal, or (2)
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''

from cspbase import *
import itertools


def binary_ne_grid(kenken_grid):
    csp = CSP("binary")
    dimension = kenken_grid[0][0]
    domains = []
    # set indices
    for i in range(1, dimension + 1):
        domains.append(i)
    vars = []
    for i in domains:
        row = []
        for j in domains:
            row.append(Variable("{}{}".format(i, j), domains))
        vars.append(row)
    cons = []
    for i in range(dimension):
        for j in range(dimension):
            for k in range(len(vars[i])):
                if k > j:
                    # row
                    var1 = vars[i][j]
                    var2 = vars[i][k]
                    con = Constraint("{}{},{}{}".format(i + 1, j + 1, i + 1, k + 1), [var1, var2])
                    satisfied = []

                    for x in var1.domain():
                        for y in var2.domain():
                            if x != y:
                                satisfied.append((x, y))
                    con.add_satisfying_tuples(satisfied)
                    cons.append(con)

                if k > i:
                    # colunm
                    var3 = vars[i][j]
                    var4 = vars[k][j]
                    con1 = Constraint("{}{},{}{})".format(i + 1, j + 1, k + 1, j + 1), [var3, var4])
                    satisfied1 = []
                    for x in var3.domain():
                        for y in var4.domain():
                            if x != y:
                                satisfied1.append((x, y))
                    con1.add_satisfying_tuples(satisfied1)
                    cons.append(con1)

    for row in vars:
        for var in row:
            csp.add_var(var)

    for c in cons:
        csp.add_constraint(c)

    return csp, vars


def nary_ad_grid(kenken_grid):
    csp = CSP("n-ary")
    dimension = kenken_grid[0][0]
    domains = []
    # set indices
    for i in range(1, dimension + 1):
        domains.append(i)
    vars = []
    for i in domains:
        row = []
        for j in domains:
            row.append(Variable("{}{}".format(i, j), domains))
        vars.append(row)
    cons = []

    for i in range(dimension):
        row_var = []
        col_var = []
        for j in range(dimension):
            row_var.append(vars[i][j])
            col_var.append(vars[j][i])
        con = Constraint("row{}".format(i), row_var)
        con1 = Constraint("col{}".format(i), col_var)

        if len(row_var) == len(set(row_var)):
            for t in itertools.product(row_var, repeat=2):
                con.add_satisfying_tuples(t)
        cons.append(con)

        if len(col_var) == len(set(col_var)):
            for t in itertools.product(col_var, repeat=2):
                con1.add_satisfying_tuples(t)
        cons.append(con1)

    for row in vars:
        for var in row:
            csp.add_var(var)

    for c in cons:
        csp.add_constraint(c)

    return csp, vars


def kenken_csp_model(kenken_grid):
    csp = CSP("kenken")
    dimension = kenken_grid[0][0]
    domains = []
    # set indices
    for i in range(1, dimension + 1):
        domains.append(i)
    vars = []
    for i in domains:
        row = []
        for j in domains:
            row.append(Variable("Var {}{}".format(i, j), domains))
        vars.append(row)
    cons = []
    # cage constraints
    for c in range(len(kenken_grid)):
        # only 1 cell
        if len(kenken_grid[c]) == 2:
            con = Constraint("cage{}".format(c), [kenken_grid[c][0]])
            i = (kenken_grid[c][0] // 10) - 1
            j = (kenken_grid[c][0] % 10) - 1
            vars[i][j] = Variable("{}{}".format(i, j), [kenken_grid[c][1]])
        elif len(kenken_grid[c]) > 2:
            target = kenken_grid[c][-2]
            operation = kenken_grid[c][-1]
            c_vars = []
            c_vars_domain = []
            for x in range(len(kenken_grid[c]) - 2):
                i = kenken_grid[c][x] // 10 - 1
                j = kenken_grid[c][x] % 10 - 1
                c_vars.append(vars[i][j])
                c_vars_domain.append(vars[i][j].domain())
            constraint = Constraint("cage {}".format(c), c_vars)

            satisfied2 = []

            for t in itertools.product(*c_vars_domain):
                # addition
                if operation == 0:
                    ans = 0
                    for n in t:
                        ans += n
                    if ans == target:
                        satisfied2.append(t)
                # subtraction
                elif operation == 1:
                    for perm in itertools.permutations(t):
                        result = perm[0]
                        i = 1
                        while i < len(t):
                            result -= perm[i]
                            i += 1
                        if result == target:
                            satisfied2.append(t)
                # division
                elif operation == 2:
                    for perm in itertools.permutations(t):
                        result = perm[0]
                        i = 1
                        while i < len(t):
                            result //= perm[i]
                            i += 1
                        if result == target:
                            satisfied2.append(t)
                # multiplication
                elif operation == 3:
                    ans = 1
                    for n in t:
                        ans *= n
                    if ans == target:
                        satisfied2.append(t)
            constraint.add_satisfying_tuples(satisfied2)
            cons.append(constraint)

    # col and row with binary not equal
    for i in range(dimension):
        for j in range(dimension):
            for k in range(len(vars[i])):
                if k > j:
                    # row
                    var1 = vars[i][j]
                    var2 = vars[i][k]
                    con = Constraint("Var {}{}, Var {}{}".format(i + 1, j + 1, i + 1, k + 1), [var1, var2])
                    satisfied = []

                    for x in var1.domain():
                        for y in var2.domain():
                            if x != y:
                                satisfied.append((x, y))
                    con.add_satisfying_tuples(satisfied)
                    cons.append(con)

                if k > i:
                    # colunm
                    var3 = vars[i][j]
                    var4 = vars[k][j]
                    con1 = Constraint("Var {}{}, Var {}{}".format(i + 1, j + 1, k + 1, j + 1), [var3, var4])
                    satisfied1 = []
                    for x in var3.domain():
                        for y in var4.domain():
                            if x != y:
                                satisfied1.append((x, y))
                    con1.add_satisfying_tuples(satisfied1)
                    cons.append(con1)

    for row in vars:
        for var in row:
            csp.add_var(var)

    for c in cons:
        csp.add_constraint(c)

    return csp, vars
