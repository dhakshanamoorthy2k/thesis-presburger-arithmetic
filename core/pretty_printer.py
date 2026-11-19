
from core.expressions import (
    Var, IntConst, Add, Sub, MulConst,
    Eq, Lt, Le, Gt, Ge, Divides,  And, Or, Not,
    Exists, ForAll
)

#arithmetic terms
def pretty_print(term):
    if isinstance(term, Var):
        return term.name

    elif isinstance(term, IntConst):
        return str(term.value)

    elif isinstance(term, Add):
        return f"({pretty_print(term.left)} + {pretty_print(term.right)})"

    elif isinstance(term, Sub):
        return f"({pretty_print(term.left)} - {pretty_print(term.right)})"

    elif isinstance(term, MulConst):
        return f"({term.coefficient} * {pretty_print(term.term)})"

    else:
        raise ValueError(f"Unknown term type: {type(term)}")

#atomic formulas
def pretty_print_atomicformula(formula):
    if isinstance(formula, Eq):
        return f"({pretty_print(formula.left)} = {pretty_print(formula.right)})"

    elif isinstance(formula, Lt):
        return f"({pretty_print(formula.left)} < {pretty_print(formula.right)})"

    elif isinstance(formula, Le):
        return f"({pretty_print(formula.left)} <= {pretty_print(formula.right)})"

    elif isinstance(formula, Gt):
        return f"({pretty_print(formula.left)} > {pretty_print(formula.right)})"

    elif isinstance(formula, Ge):
        return f"({pretty_print(formula.left)} >= {pretty_print(formula.right)})"

    elif isinstance(formula, Divides):
        return f"({formula.divisor} | {pretty_print(formula.term)})"

    else:
        raise ValueError(f"Unknown formula type: {type(formula)}")

#logical formulas
def pretty_print_logical(formula):

    if isinstance(formula, Not):
        return f"(NOT {pretty_print_logical_or_atomic(formula.formula)})"

    elif isinstance(formula, And):
        left = pretty_print_logical_or_atomic(formula.left)
        right = pretty_print_logical_or_atomic(formula.right)
        return f"({left} AND {right})"

    elif isinstance(formula, Or):
        left = pretty_print_logical_or_atomic(formula.left)
        right = pretty_print_logical_or_atomic(formula.right)
        return f"({left} OR {right})"

    else:
        return pretty_print_atomicformula(formula)


def pretty_print_logical_or_atomic(formula):
    if isinstance(formula, (Not, And, Or)):
        return pretty_print_logical(formula)

    return pretty_print_atomicformula(formula)

#quantified formulas
def pretty_print_quantified(formula):
    if isinstance(formula, ForAll):
        return f"(FORALL {formula.variable}: {pretty_print_logical_or_atomic(formula.formula)})"

    elif isinstance(formula, Exists):
        return f"(EXISTS {formula.variable}: {pretty_print_logical_or_atomic(formula.formula)})"

    else:
        raise ValueError(f"Unknown quantified formula type: {type(formula)}")


#to read all types of formulas
def pretty_print_formula(formula):

    if isinstance(formula, Exists):
        return f"(EXISTS {formula.variable}: {pretty_print_formula(formula.formula)})"

    elif isinstance(formula, ForAll):
        return f"(FORALL {formula.variable}: {pretty_print_formula(formula.formula)})"

    elif isinstance(formula, Not):
        return f"(NOT {pretty_print_formula(formula.formula)})"

    elif isinstance(formula, And):
        left = pretty_print_formula(formula.left)
        right = pretty_print_formula(formula.right)
        return f"({left} AND {right})"

    elif isinstance(formula, Or):
        left = pretty_print_formula(formula.left)
        right = pretty_print_formula(formula.right)
        return f"({left} OR {right})"

    else:
        return pretty_print_atomicformula(formula)

