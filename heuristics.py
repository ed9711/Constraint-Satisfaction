'''
This file will contain different variable ordering heuristics to be used within
bt_search.

1. ord_dh(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the DH heuristic.
2. ord_mrv(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the MRV heuristic.
3. val_lcv(csp, var)
    - Takes in a CSP object (csp), and a Variable object (var)
    - Returns a list of all of var's potential values, ordered from best value 
      choice to worst value choice according to the LCV heuristic.

The heuristics can use the csp argument (CSP object) to get access to the 
variables and constraints of the problem. The assigned variables and values can 
be accessed via methods.
'''

import random
from copy import deepcopy


def ord_dh(csp):
    highest_degree = 0
    dh_var = None
    for var in csp.get_all_unasgn_vars():
        cons = csp.get_cons_with_var(var)
        count = 0
        for c in cons:
            count += len(c.get_scope()) - 1
        if count > highest_degree:
            highest_degree = count
            dh_var = var
    return dh_var


def ord_mrv(csp):
    min_var = None
    min_domain = 999999
    for var in csp.get_all_unasgn_vars():
        if min_domain > var.cur_domain_size():
            min_domain = var.cur_domain_size()
            min_var = var
    return min_var


def val_lcv(csp, var):
    # TODO! IMPLEMENT THIS!
    pass
