# -*- coding: utf-8 -*-
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