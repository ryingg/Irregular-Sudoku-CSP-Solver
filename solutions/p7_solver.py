# -*- coding: utf-8 -*-

from p1_is_complete import *
from p2_is_consistent import *
from collections import deque
from Queue import PriorityQueue

def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    This method implements the minimum-remaining-values (MRV) and degree heuristic. That is,
    the variable with the smallest number of values left in its available domain.  If MRV ties,
    then it picks the variable that is involved in the largest number of constraints on other
    unassigned variables.
    """
    smallest = 1000
    cur_v = None

    for v in csp.variables:
        if v.is_assigned(): # skip assigned vars
            continue
        if len(v.domain) < smallest: #if size of domain less than min, new min
            smallest = len(v.domain)
            cur_v = v # update v
        elif len(v.domain) == smallest: # if mrv ties, pick v with most c on unassigned
            temp_c = 0
            cur_c = 0
            for c in csp.constraints:
                if c.var1 == v or c.var2 == v:
                    temp_c = temp_c+1
                if c.var1 == cur_v or c.var2 == cur_v:
                    cur_c = cur_c+1
            if temp_c > cur_c: # if v has more constraints than current v
                cur_v = v # update v
    return cur_v if cur_v else None


def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    This method implements the least-constraining-value (LCV) heuristic; that is, the value
    that rules out the fewest choices for the neighboring variables in the constraint graph
    are placed before others.
    """
    q = PriorityQueue() # ordered domain

    for value in variable.domain: # get neighbors
        count = 0
        for c in csp.constraints[variable]:
            if c.var2.is_assigned() and c.is_satisfied(value, c.var2.value): # satisfied constraint
                    count+=1
            else:
                for val2 in c.var2.domain: # satisfied constraints
                    if c.is_satisfied(value, val2):
                        count+=1
        q.put((count,value))
    domain = []
    while not q.empty(): # convert to list
        count, value = q.get()
        domain.insert(0, value)
    return domain

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