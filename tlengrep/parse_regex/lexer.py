import ply.lex  as lex

tokens = (
   'RANGE',
   'OR',
   'STAR',
   'PLUS',
   'OPTIONAL',
   'POWER',
   'POWER_RANGE',   
   '_W',
   '_D',
   'CHAR',
   'NUMBER',
   'LPAREN',
   'RPAREN',
   'LCORCHETE',
   'RCORCHETE',
   'LLLAVE',
   'RLLAVE',
   'MINUS'
)

t_OR          = r'\|'
t_STAR        = r'\*'
t_PLUS        = r'\+'
t_OPTIONAL    = r'\?'
t_POWER       = r'{\d+ }'
t_POWER_RANGE = r'{\d+ , \d+}'
t__W          = r'\\w'
t__D          = r'\\d'
t_NUMBER      = r'\d+'
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_LCORCHETE   = r'\['
t_RCORCHETE   = r'\]'
t_LLLAVE      = r'\{'
t_RLLAVE      = r'\}'
t_MINUS       = r'-'

# Esta función hace lo mismo que:
# t_RANGO = r'\w-\w'
# Esta definida así para que tenga más prioridad que CHAR, NUMBER y MINUS.
def t_RANGE(t):
     r'\w-\w'
     return t

# [a-zA-Z] | _ | <espacio> | <los símbolos escopeados>
def t_CHAR(t):
     r' [a-zA-Z_ ] | \\\* | \\\+ | \\\| | \\\? | \\\( | \\\) | \\\\ | \\\[ | \\\] |  \\\{ | \\\}'
     if len(t.value)>1: # ¿Es un símbolo escopeado?
          t.value = t.value[-1] # Me quedo sólo con el último caracter
     return t

# Error handling rule
def t_error(t):
    raise SyntaxError

# # Build the lexer
lexer = lex.lex()