# -*- coding: utf-8 -*-



def is_consistent(csp, variable, value):
    """Returns True when the variable assignment to value is consistent, i.e. it does not violate any of the constraints
    associated with the given variable for the variables that have values assigned.

    For example, if the current variable is X and its neighbors are Y and Z (there are constraints (X,Y) and (X,Z)
    in csp.constraints), and the current assignment as Y=y, we want to check if the value x we want to assign to X
    violates the constraint c(x,y).  This method does not check c(x,Z), because Z is not yet assigned."""

    # The constraint is satisfied (is satisfied(val1, val2) == True) when the values of
    # var1 and var2 ( val1 and val2) satisfy the relationship specified by relation
    
    variable.assign(value)
    for c in csp.constraints[variable]:
        if c.var1.is_assigned and c.var2.is_assigned(): # check if both vars are assigned
            if not c.is_satisfied(c.var1.value,c.var2.value): # check if violated constraint
                return False
    return True