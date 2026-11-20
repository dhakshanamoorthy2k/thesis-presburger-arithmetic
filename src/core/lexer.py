
from core.tokens import Token


KEYWORDS = {
    "EXISTS": "EXISTS",
    "FORALL": "FORALL",
    "AND": "AND",
    "OR": "OR",
    "NOT": "NOT"
}


SINGLE_CHAR_TOKENS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "=": "EQ",
    "<": "LT",
    ">": "GT",
    "|": "DIVIDES",
    "∣": "DIVIDES",
    "(": "LPAREN",
    ")": "RPAREN",
    ":": "COLON",
    "∃": "EXISTS",
    "∀": "FORALL",
    "∧": "AND",
    "∨": "OR",
    "¬": "NOT",
    "≤": "LE",
    "≥": "GE",
    "∤": "NOT_DIVIDES"
}


def tokenize(text):

    tokens = []
    position = 0

    while position < len(text):

        char = text[position]

        # 1. Ignore whitespace
        if char.isspace():
            position += 1
            continue

        # 2. Recognize integers
        if char.isdigit():

            start = position

            while position < len(text) and text[position].isdigit():
                position += 1

            value = text[start:position]

            tokens.append(Token("INTEGER", value, start))
            continue

        # 3. Recognize variables and keywords
        if char.isalpha() or char == "_":

            start = position

            while (
                position < len(text)
                and (text[position].isalnum() or text[position] == "_")
            ):
                position += 1

            value = text[start:position]
            token_type = KEYWORDS.get(value.upper(), "VARIABLE")

            tokens.append(Token(token_type, value, start))
            continue

        # 4. Recognize multi-character operators first
        if text[position:position + 2] == "<=":
            tokens.append(Token("LE", "<=", position))
            position += 2
            continue

        if text[position:position + 2] == ">=":
            tokens.append(Token("GE", ">=", position))
            position += 2
            continue

        # 5. Recognize single-character tokens
        if char in SINGLE_CHAR_TOKENS:

            token_type = SINGLE_CHAR_TOKENS[char]

            tokens.append(Token(token_type, char, position))
            position += 1
            continue

        # 6. Report unknown characters
        raise ValueError(
            f"Unexpected character {char!r} at position {position}"
        )

    # 7. End-of-input marker for the future parser
    tokens.append(Token("EOF", "", len(text)))

    return tokens
