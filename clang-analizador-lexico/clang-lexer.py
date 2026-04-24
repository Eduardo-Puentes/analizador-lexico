import sys

import ply.lex as lex


reserved = {
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "return": "RETURN",
    "int": "INT_TYPE",
    "float": "FLOAT_TYPE",
    "char": "CHAR_TYPE",
    "void": "VOID",
    "break": "BREAK",
    "continue": "CONTINUE",
}


tokens = [
    "ID",
    "INT_LITERAL",
    "FLOAT_LITERAL",
    "STRING_LITERAL",
    "CHAR_LITERAL",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MOD",
    "INCREMENT",
    "DECREMENT",
    "ASSIGN",
    "EQ",
    "NE",
    "LT",
    "LE",
    "GT",
    "GE",
    "AND",
    "OR",
    "NOT",
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    "LBRACKET",
    "RBRACKET",
    "COMMA",
    "SEMICOLON",
] + list(reserved.values())


states = (
    ("comment", "exclusive"),
    ("string", "exclusive"),
    ("char", "exclusive"),
)


class LexicalError(Exception):
    """Raised when the lexer finds an unrecoverable malformed token."""


def find_column(text: str, lexpos: int) -> int:
    line_start = text.rfind("\n", 0, lexpos) + 1
    return (lexpos - line_start) + 1


t_INCREMENT = r"\+\+"
t_DECREMENT = r"--"
t_LE = r"<="
t_GE = r">="
t_EQ = r"=="
t_NE = r"!="
t_AND = r"&&"
t_OR = r"\|\|"
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_MOD = r"%"
t_ASSIGN = r"="
t_LT = r"<"
t_GT = r">"
t_NOT = r"!"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_COMMA = r","
t_SEMICOLON = r";"

t_ignore = " \t\r\f\v"


def t_begin_comment(t):
    r"/\*"
    t.lexer.comment_start_line = t.lineno
    t.lexer.comment_start_lexpos = t.lexpos
    t.lexer.begin("comment")


def t_line_comment(t):
    r"//[^\n]*"
    pass


def t_FLOAT_LITERAL(t):
    r"((\d+\.\d*)|(\.\d+))([eE][+-]?\d+)?"
    return t


def t_INT_LITERAL(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_ID(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    t.type = reserved.get(t.value, "ID")
    return t


def t_BEGIN_STRING(t):
    r"\""
    t.lexer.string_start_line = t.lineno
    t.lexer.string_start_lexpos = t.lexpos
    t.lexer.string_buffer = ['"']
    t.lexer.begin("string")


def t_BEGIN_CHAR(t):
    r"'"
    t.lexer.char_start_line = t.lineno
    t.lexer.char_start_lexpos = t.lexpos
    t.lexer.char_buffer = ["'"]
    t.lexer.begin("char")


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    column = find_column(t.lexer.lexdata, t.lexpos)
    print(
        f"Lexical error: illegal character {t.value[0]!r} at line {t.lineno}, column {column}",
        file=sys.stderr,
    )
    t.lexer.skip(1)


t_comment_ignore = ""


def t_comment_end(t):
    r"\*/"
    t.lexer.begin("INITIAL")


def t_comment_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_comment_text(t):
    r"[^*\n]+|\*+[^/\n]"
    pass


def t_comment_error(t):
    t.lexer.skip(1)


t_string_ignore = ""


def t_string_escape(t):
    r'\\([\\\'"?abfnrtv]|x[0-9A-Fa-f]+|[0-7]{1,3})'
    t.lexer.string_buffer.append(t.value)


def t_string_text(t):
    r'[^\\\"\n]+'
    t.lexer.string_buffer.append(t.value)


def t_string_end(t):
    r"\""
    t.lexer.string_buffer.append('"')
    t.value = "".join(t.lexer.string_buffer)
    t.type = "STRING_LITERAL"
    t.lineno = t.lexer.string_start_line
    t.lexpos = t.lexer.string_start_lexpos
    t.lexer.begin("INITIAL")
    return t


def t_string_newline(t):
    r"\n"
    column = find_column(t.lexer.lexdata, t.lexer.string_start_lexpos)
    print(
        f"Lexical error: unterminated string literal starting at line "
        f"{t.lexer.string_start_line}, column {column}",
        file=sys.stderr,
    )
    t.lexer.lineno += 1
    t.lexer.begin("INITIAL")


def t_string_error(t):
    column = find_column(t.lexer.lexdata, t.lexpos)
    print(
        f"Lexical error: invalid character {t.value[0]!r} inside string "
        f"at line {t.lineno}, column {column}",
        file=sys.stderr,
    )
    t.lexer.skip(1)


t_char_ignore = ""


def t_char_escape(t):
    r"\\([\\\'\"?abfnrtv]|x[0-9A-Fa-f]+|[0-7]{1,3})"
    t.lexer.char_buffer.append(t.value)


def t_char_text(t):
    r"[^\\'\n]"
    t.lexer.char_buffer.append(t.value)


def t_char_end(t):
    r"'"
    t.lexer.char_buffer.append("'")
    lexeme = "".join(t.lexer.char_buffer)
    contents = lexeme[1:-1]
    if len(contents) == 0:
        column = find_column(t.lexer.lexdata, t.lexer.char_start_lexpos)
        print(
            f"Lexical error: empty character literal at line "
            f"{t.lexer.char_start_line}, column {column}",
            file=sys.stderr,
        )
        t.lexer.begin("INITIAL")
        return None

    is_single_character = len(contents) == 1
    is_escape_sequence = contents.startswith("\\")
    if not is_single_character and not is_escape_sequence:
        column = find_column(t.lexer.lexdata, t.lexer.char_start_lexpos)
        print(
            f"Lexical error: invalid character literal {lexeme!r} at line "
            f"{t.lexer.char_start_line}, column {column}",
            file=sys.stderr,
        )
        t.lexer.begin("INITIAL")
        return None

    t.value = lexeme
    t.type = "CHAR_LITERAL"
    t.lineno = t.lexer.char_start_line
    t.lexpos = t.lexer.char_start_lexpos
    t.lexer.begin("INITIAL")
    return t


def t_char_newline(t):
    r"\n"
    column = find_column(t.lexer.lexdata, t.lexer.char_start_lexpos)
    print(
        f"Lexical error: unterminated character literal starting at line "
        f"{t.lexer.char_start_line}, column {column}",
        file=sys.stderr,
    )
    t.lexer.lineno += 1
    t.lexer.begin("INITIAL")


def t_char_error(t):
    column = find_column(t.lexer.lexdata, t.lexpos)
    print(
        f"Lexical error: invalid character {t.value[0]!r} inside character literal "
        f"at line {t.lineno}, column {column}",
        file=sys.stderr,
    )
    t.lexer.skip(1)


def build_lexer():
    return lex.lex(module=sys.modules[__name__])


def tokenize(source: str):
    lexer = build_lexer()
    lexer.input(source)

    collected = []
    while True:
        token = lexer.token()
        if not token:
            break
        token.column = find_column(source, token.lexpos)
        collected.append(token)

    if lexer.current_state() == "comment":
        column = find_column(source, lexer.comment_start_lexpos)
        print(
            f"Lexical error: unterminated block comment starting at line "
            f"{lexer.comment_start_line}, column {column}",
            file=sys.stderr,
        )
    elif lexer.current_state() == "string":
        column = find_column(source, lexer.string_start_lexpos)
        print(
            f"Lexical error: unterminated string literal starting at line "
            f"{lexer.string_start_line}, column {column}",
            file=sys.stderr,
        )
    elif lexer.current_state() == "char":
        column = find_column(source, lexer.char_start_lexpos)
        print(
            f"Lexical error: unterminated character literal starting at line "
            f"{lexer.char_start_line}, column {column}",
            file=sys.stderr,
        )

    return collected


def format_token(token) -> str:
    return (
        f"{token.type:<16} value={token.value!r:<20} "
        f"line={token.lineno:<3} column={token.column}"
    )


def read_source_from_argv() -> str:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as source_file:
            return source_file.read()

    return """
int main() {
    int n = 5;
    int i = 0;
    float avg = 3.14;
    char initial = 'A';
    // factorial loop
    while (i <= n) {
        printf("step %d\\n ", i);
        i++;
    }
    return 0;
}
"""


if __name__ == "__main__":
    source = read_source_from_argv()
    for token in tokenize(source):
        print(format_token(token))
