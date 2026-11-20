
import pytest

from core.expressions import (
    Var, IntConst, Add, Sub, MulConst,
    Eq, Lt, Le, Gt, Ge, Divides,
    Not, And, Or, Exists, ForAll
)


def test_variable():
    x = Var("x")
    assert x.name == "x"


def test_integer_constant():
    number = IntConst(5)
    assert number.value == 5


def test_addition():
    expression = Add(Var("x"), IntConst(5))
    assert isinstance(expression, Add)


def test_subtraction():
    expression = Sub(Var("x"), IntConst(3))
    assert isinstance(expression, Sub)


def test_multiplication_by_constant():
    expression = MulConst(2, Var("x"))
    assert expression.coefficient == 2


@pytest.mark.parametrize(
    "formula_type",
    [Eq, Lt, Le, Gt, Ge]
)
def test_comparison_operators(formula_type):
    formula = formula_type(Var("x"), IntConst(5))
    assert isinstance(formula, formula_type)


def test_divisibility():
    formula = Divides(3, Var("x"))
    assert formula.divisor == 3


def test_invalid_divisor():
    with pytest.raises(ValueError):
        Divides(0, Var("x"))


def test_logical_operators():
    p = Lt(Var("x"), IntConst(5))
    q = Divides(3, Var("x"))

    assert isinstance(Not(p), Not)
    assert isinstance(And(p, q), And)
    assert isinstance(Or(p, q), Or)


def test_quantifiers():
    p = Lt(Var("x"), IntConst(5))

    assert isinstance(Exists("x", p), Exists)
    assert isinstance(ForAll("x", p), ForAll)


def test_complete_formula():
    x = Var("x")

    formula = Exists(
        "x",
        And(
            Lt(
                Add(
                    MulConst(2, x),
                    IntConst(1)
                ),
                IntConst(8)
            ),
            Divides(
                3,
                Add(x, IntConst(1))
            )
        )
    )

    assert isinstance(formula, Exists)
    assert isinstance(formula.formula, And)

