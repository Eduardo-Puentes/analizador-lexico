import ply.lex as lex

tokens = [
    'ID',
    'INT',
    'FLOAT',
    'STRING',
    'PLUS',
    'MINUS',
    'TIMES',
    'POW',
    'DIV',
    'LE',

    'IF',
    'ELSE',
    'WHILE',
    'RETURN'
]

t_LE = r"<="
t_POW = r"\*\*"
t_PLUS = r"\+"
t_TIMES = r"\*"
t_MINUS = r"-"
t_DIV = r"/"
literals = "(){};,=<"

def t_ID(t):
    r"[A-Za-z][0-9A-Za-z]*"
    if t.value in ['if', 'else', 'while', 'return']:
        t.type = t.value.upper()
    return t

def t_INT(t):
    r"\d+"
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character {t.value[0]!r} at index {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

lexer.input("""
int main() {
    int n = 5;
    int i, f;
    i = 1;
    f = 1;
    while (i <= n) {
        f = f * i;
        i = i + 1;
    }
    return f;
}
""")

for tok in lexer:
    print(tok)
