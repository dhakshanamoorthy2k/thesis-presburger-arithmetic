from core.expressions import (Var, IntConst, Add, MulConst,
Eq, Lt, Le, Gt, Ge, Divides, And, Or, Not, Exists, ForAll)
from core.pretty_printer import pretty_print
from core.pretty_printer import pretty_print_atomicformula, pretty_print_logical, pretty_print_quantified, pretty_print_logical_or_atomic, pretty_print_formula

from core.parser import Parser
from core.lexer import tokenize
from core.pretty_printer import pretty_print, pretty_print_atomicformula,pretty_print_formula

# formula =  "3 | (x + 2)"

# formula =  "((x < 10) AND (y > 5)) OR (3 | x)"
formula = "EXISTS x: FORALL y: EXISTS z: (((2*x + 3*y) < z) AND (5 | (x + y + z)))"
tokens = tokenize(formula)

parser = Parser(tokens)
result = parser.parse_formula()
# result = parser.parse_expression()
# result = parser.parse_product()
# result = parser.parse_expression()

# result = parser.parse_atom()

print("AST:", result)
print("Pretty printed:", pretty_print_formula(result))

# formula ="EXISTS x: 2*x + 15"
# tokens = tokenize(formula)
# parser = Parser(tokens)

# print("current tokken:", parser.peek())
# print("consumed token", parser.advance())
# print("next token:", parser.peek())
# print("Expected token:", parser.expect("VARIABLE"))


# tokens = Token("Integer","25",0)
# print(tokens)
# print(tokens.type)
# print(tokens.value)
# print(tokens.position)


# from core.lexer import tokenize
# formula = "13 ∤ (x + 5)"
# # formula = "13 | (x + 5)"
# # formula = "2x + 15"
# # formula = "EXISTS x: (2*x + 15 <= 100) AND (3 | (x + 1))"

# tokens = tokenize(formula)

# for token in tokens:
#     print(token)












# x = Var("x")
# y = Var("y")

# formula = Exists(
#     "x",
#     ForAll(
#         "y",
#         And(
#             Lt(
#                 Add(
#                     MulConst(2, x),
#                     MulConst(3, y)
#                 ),
#                 IntConst(10)
#             ),
#             Divides(
#                 3,
#                 Add(x, y)
#             )
#         )
#     )
# )

# print(pretty_print_formula(formula))

# # x = Var("x")

# # p = Lt(
# #     Add(
# #         MulConst(2, x),
# #         IntConst(1)
# #     ),
# #     IntConst(8)
# # )

# q = Divides(3, Add(x, IntConst(1)))

# combined = And(p, q)

# formula1 = Exists("x", combined)
# formula2 = ForAll("x", combined)

# print(pretty_print_quantified(formula1))
# print(pretty_print_quantified(formula2))
# x=Var("x")
# # Atomic formulas
# p = Lt(x, IntConst(5))
# q = Divides(3, x)
# r = Ge(x, IntConst(10))

# formula = Not(p)
# formula2 = And(q, r)
# formula3 = Or(formula, formula2)
# formula4 = Not(formula3)
# formula5 = And(formula4, p)
# formula6 = Or(formula5, q)
# formula7 = Not(formula6)
# formula8 = And(formula7, r)
# formula9 = Or(formula8, p)
# formula10 = Not(formula9)
# #display
# tests =[
#     formula,formula2,formula3,formula4,formula5,formula6,formula7,formula8,formula9,formula10
# ]

# for i, item in enumerate(tests, start=1):
#     print(f"Test {i}: {pretty_print_logical(item)}")

# Second condition: 3 | (x + 1)
# condition2 = Divides(
#     3,
#     Add(x, IntConst(1))
# )

# # Combine both conditions using AND
# combined = And(condition1, condition2)

# # Add existential quantifier
# formula = Exists("x", combined)

# print(formula)
