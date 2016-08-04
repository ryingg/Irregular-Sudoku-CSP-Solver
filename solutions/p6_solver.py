# -*- coding: utf-8 -*-

from p1_is_complete import *
from p2_is_consistent import *
from p5_ordering import *
from collections import deque


def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.

    For P6, *you do not need to modify this method.*
    """
    return ac3(csp, csp.constraints[variable].arcs())


def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.

    For P6, *you do not need to modify this method.*
    """
    if backtrack(csp):
        return csp.assignment
    else:
        return None

def backtrack(csp):
    """Performs the backtracking search for the given csp.

    If there is a solution, this method returns True; otherwise, it returns False.
    """
    if is_complete(csp): # return assignment if complete
        return True
    var = select_unassigned_variable(csp) # select unassigned var
    for value in order_domain_values(csp, var): # look through domain
        if is_consistent(csp, var, value): # if value is consistent w assignment
            csp.variables.begin_transaction() # begin to make changes
            csp.assignment[var] = value # add to assignment
            if inference(csp, var):    # uses inference(csp, variable)
                if backtrack(csp): # complete csp
                    return True
            csp.variables.rollback() # roll back changes
    return False # failure


def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.

    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.

    Note that the current domain of each variable can be retrieved by 'variable.domains'.

    This method returns True if the arc consistency check succeeds, and False otherwise."""

    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())
    while queue_arcs: # while queue is not empty
        xi, xj = queue_arcs.popleft() # remove first
        if revise(csp, xi, xj):
            if len(xi.domain) == 0: #if size of domain = 0
                return False
            for (xk, neighbor) in csp.constraints[xi].arcs():
                if neighbor != xj: 
                    queue_arcs.append((xk, neighbor))
    return True

def revise(csp, xi, xj):
    # You may additionally want to implement the 'revise' method.
    revised = False
    for x in xi.domain:
        if no_satisfy(csp, x, xi, xj): # if no value satisfied constraint between xi xj
            xi.domain.remove(x) # delete x from domain
            revised = True
    return revised

def no_satisfy(csp, x, xi, xj):
    for c in csp.constraints[xi]:
        if c.var2 == xj: # if xj
            if c.var2.is_assigned():
                if c.is_satisfied(x, c.var2.value): # satisfies constraint
                    return False
            else:
                for y in c.var2.domain: # look through xj
                    if c.is_satisfied(x,y): # satisfies
                        return False
    return True