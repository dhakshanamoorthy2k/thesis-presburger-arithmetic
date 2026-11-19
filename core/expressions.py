
from dataclasses import dataclass



# =================================
# BASE CLASSES
# =================================

class Term:
    """Base class for arithmetic expressions."""
    pass


class Formula:
    """Base class for logical formulas."""
    pass


# =================================
# ARITHMETIC TERMS
# =================================

@dataclass(frozen=True)
class Var(Term):
    name: str


@dataclass(frozen=True)
class IntConst(Term):
    value: int


@dataclass(frozen=True)
class Add(Term):
    left: Term
    right: Term

@dataclass(frozen=True)
class Sub(Term):
    left: Term
    right: Term


@dataclass(frozen=True)
class MulConst(Term):
    coefficient: int
    term: Term


# =================================
# ATOMIC FORMULAS
# =================================

@dataclass(frozen=True)
class Eq(Formula):
    left: Term
    right: Term


@dataclass(frozen=True)
class Lt(Formula):
    left: Term
    right: Term


@dataclass(frozen=True)
class Le(Formula):
    left: Term
    right: Term

@dataclass(frozen=True)
class Gt(Formula):
    left: Term
    right: Term


@dataclass(frozen=True)
class Ge(Formula):
    left: Term
    right: Term


@dataclass(frozen=True)
class Divides(Formula):
    divisor: int
    term: Term

    def __post_init__(self):
        if self.divisor <= 0:
            raise ValueError("Divisor must be positive") 

#################################
#logical operators
##############################
@dataclass(frozen=True)
class Not(Formula):
    formula: Formula

@dataclass(frozen=True)
class And(Formula):
    left: Formula
    right: Formula

@dataclass(frozen=True)
class Or(Formula):
    left: Formula
    right: Formula

#quantifiers
@dataclass(frozen=True)
class Exists(Formula):
    variable: str
    formula: Formula

@dataclass(frozen=True)
class ForAll(Formula):
    variable: str
    formula: Formula

    

