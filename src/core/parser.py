from core.tokens import Token
from core.expressions import (
    Var, IntConst, Add, Sub, MulConst,
    Eq, Lt, Le, Gt, Ge, Divides,  And, Or, Not,
    Exists, ForAll
)

class Parser:
    #revcieves the tokens,store inside parser,start reading from position 0
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    #look at the current token without moving forward
    def peek(self):
        return self.tokens[self.position]

    #read the currrent token and move forward to the next token
    def advance(self):
        current = self.peek()
        self.position += 1
        return current

    #suppose the parser excepts EXISTS, but the iput contains FORALL
    #instead of crashing, we can raise a syntax error with a message that indicates what was expected and what was found
    def expect(self, token_type):

        current = self.peek()

        if current.type == token_type:
            return self.advance()

        raise SyntaxError(
            f"Expected {token_type}, "
            f"but found {current.type} "
            f"at position {current.position}"
        )

    #parse_atom is a method that parses 
    # an atomic formula, which can be either an 
    # integer constant or a variable. 
    # It checks the type of the current token 
    # and creates the corresponding AST node (IntConst or Var). 
    # If the token is neither an integer nor a variable, it raises a SyntaxError with a message indicating what was expected and what was found.
    def parse_atom(self):

        current = self.peek()

        if current.type == "INTEGER":
            token = self.advance()
            return IntConst(int(token.value))

        elif current.type == "VARIABLE":
            token = self.advance()
            return Var(token.value)
        
        elif current.type == "LPAREN":
            self.advance()  # consume '('
            expression = self.parse_expression()
            self.expect("RPAREN")  # expect ')'
            return expression

        else:
            raise SyntaxError(
            f"Expected an integer,variable, or parenthesized expression, "
            f"but found {current.type} "
            f"at position {current.position}"
        )

    def parse_product(self):

        current = self.peek()

        if current.type == "INTEGER":

            number = int(self.advance().value)

            if self.peek().type == "STAR":
                self.advance()

                term = self.parse_atom()
                return MulConst(number, term)

            elif self.peek().type == "VARIABLE":
                term = self.parse_atom()
                return MulConst(number, term)

            else:
                return IntConst(number)

        else:
            return self.parse_atom()
    
    
    #parse_expression:
    #Parse the first multiplication term.
    # Check whether the next token is PLUS or MINUS.
    # Parse the next multiplication term.
    # Construct an Add or Sub node.
    # Continue until there are no more addition or subtraction operators.
    def parse_expression(self):

        left = self.parse_product()

        while self.peek().type in ("PLUS", "MINUS"):
            operator = self.advance()
            right = self.parse_product()

            if operator.type == "PLUS":
                left = Add(left, right)
            elif operator.type == "MINUS":
                left = Sub(left, right)

        return left
    def parse_atomic_formula(self):

        left = self.parse_expression()

        operator = self.advance()

        right = self.parse_expression()

        if operator.type == "EQ":
            return Eq(left, right)

        elif operator.type == "LT":
            return Lt(left, right)

        elif operator.type == "LE":
            return Le(left, right)

        elif operator.type == "GT":
            return Gt(left, right)

        elif operator.type == "GE":
            return Ge(left, right)

        else:
            raise SyntaxError(
            f"Expected a comparison operator, "
            f"but found {operator.type}"
        )

    def parse_divisibility(self):
        divisor_token = self.expect("INTEGER")
        divisor = int(divisor_token.value)

        if self.peek().type == "DIVIDES":
            self.advance()  # consume the 'DIVIDES' token
            term = self.parse_expression()
            return Divides(divisor, term)
        elif self.peek().type == "NOT_DIVIDES":
            self.advance()  # consume the 'NOT_DIVIDES' token
            term = self.parse_expression()
            return Not(Divides(divisor, term))
        else:
            raise SyntaxError(
                f"Expected 'DIVIDES' or 'NOT_DIVIDES', "
            )

    #parse_logical formulas
    def parse_not(self):

        if self.peek().type == "NOT":
            self.advance()  # consume the 'NOT' token
            formula = self.parse_not()
            return Not(formula)

        elif self.peek().type == "LPAREN":
            self.advance()  # consume '('
            formula = self.parse_not()
            self.expect("RPAREN")  # expect ')'
            return formula

        elif self.peek().type in ("EXISTS", "FORALL"):
            return self.parse_quantified_formula()
        
        elif(
            self.peek().type == "INTEGER" and
            self.position + 1 < len(self.tokens) and
            self.tokens[self.position + 1].type in ("DIVIDES", "NOT_DIVIDES")
        ):
            return self.parse_divisibility()

        else:
            return self.parse_atomic_formula()

    def parse_and(self):
        left = self.parse_not()

        while self.peek().type == "AND":
            self.advance()  # consume 'AND'
            right = self.parse_not()
            left = And(left, right)

        return left

    def parse_or(self):
        left = self.parse_and()

        while self.peek().type == "OR":
            self.advance()  # consume 'OR'
            right = self.parse_and()
            left = Or(left, right)

        return left

    #parse_quantified_formula:This method handles existential and universal quantifiers.
    def parse_quantified_formula(self):
        if self.peek().type == "EXISTS":
            self.advance()  # consume 'EXISTS'
            variable_token = self.expect("VARIABLE")
            variable = variable_token.value
            self.expect("COLON")  # expect ':'
            formula = self.parse_or()
            return Exists(variable, formula)
        
        elif self.peek().type == "FORALL":
            self.advance()  # consume 'FORALL'
            variable_token = self.expect("VARIABLE")
            variable = variable_token.value
            self.expect("COLON")  # expect ':'
            formula = self.parse_or()
            return ForAll(variable, formula)

        else:
            raise SyntaxError(
                f"Expected 'EXISTS' or 'FORALL', "
               
            )

    def parse_formula(self):
        formula = self.parse_or()

        self.expect("EOF")  # Ensure that we have consumed all tokens
        return formula