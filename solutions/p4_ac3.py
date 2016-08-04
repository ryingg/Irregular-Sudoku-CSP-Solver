# -*- coding: utf-8 -*-

from collections import deque

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