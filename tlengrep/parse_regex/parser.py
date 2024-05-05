import ply.yacc as yacc
from regex import RegEx, Empty, Lambda, Char, Union, Concat, Star, Plus
from parse_regex.lexer import tokens
from parse_regex.errors import *

# Todas las producciones producen RegEx
# Salvo por SYMB, que produce chr

# La gramática:
# P    -> S | lambda
# S    -> R OR S | R
# R    -> TR | T
# T    -> K* | K+ | K? | K POWER | K POWER_RANGE | K
# K    -> (P) | [F | SYMB | RANGE | _W | _D
# F    -> SYMBF | RANGEF | ]
# SYMB -> NUMBER | CHAR | MINUS | LLLAVE | RLLAVE

# (SYMB de "symbol")

#---(Funciones auxiliares)---

# Devuelve S{N}
def Power(S, N) -> RegEx:
    regex = Lambda()
    for i in range(0, N):
        regex = Concat(regex, S)
    return regex

# Devuelve la unión de [N-M]
def UnionRange(N,M) -> RegEx:
    regex = Empty()
    for c in range(ord(N), ord(M)+1):
        regex = Union(regex, Char(chr(c)))
    return regex


#---(Definición de las producciones)---

### Producciones de P
### P -> S | Lambda

def p_P_S(p) -> RegEx:
    'P : S'
    p[0] = p[1]

def p_LAMBDA(p) -> RegEx:
    'P :'
    p[0] = Lambda()


### Producciones de S
### S -> R OR S | R

def p_union(p) -> RegEx:
    'S : R OR S'
    p[0] = Union(p[1], p[3])

def p_S_R(p) -> RegEx:
    'S : R'
    p[0] = p[1]


### Producciones de R
###  R -> TR | T

def p_concat(p) -> RegEx:
    'R : T R'
    p[0] = Concat(p[1], p[2])

def p_R_T(p) -> RegEx:
    'R : T'
    p[0] = p[1]


### Producciones de T
### T -> K* | K+ | K? | K POWER | K POWER_RANGE | K

# K*
def p_STAR(p) -> RegEx:
    'T : K STAR'
    p[0] = Star(p[1])

# K+
def p_PLUS(p) -> RegEx:
    'T : K PLUS'
    p[0] = Plus(p[1])

# K?
def p_OPTIONAL(p) -> RegEx:
    'T : K OPTIONAL'
    p[0] = Union(p[1], Lambda())

# K{N}
def p_POWER(p) -> RegEx:
    'T : K POWER'
    # POWER es un string: {n}, dónde n es un número
    n = int(p[2][1:-1])
    p[0] = Power(p[1], n)

# K{N,M}
def p_POWER_RANGE(p) -> RegEx:
    'T : K POWER_RANGE'

    T = p[1]

    # p[2] es un string: {n, m}, dónde n y m son números
    power_range  = p[2][1:-1].split(",")
    N = int(power_range[0])
    M = int(power_range[1])

    if M < N: # ¿El rango es inválido?
        raise SyntaxError

    regex = Empty()
    for i in range (N, M+1):
        regex = Union(regex, Power(T, i))
    p[0] = regex

# K
def p_K(p) -> RegEx:
    'T : K'
    p[0] = p[1]


### Producciones de K
### K -> (P) | [F | SYMB | RANGE | _W | _D

# (P)
def p_braces(p) -> RegEx:
    'K : LPAREN P RPAREN'
    p[0] = p[2]

# [F
def p_CHAR_RANGE(p) -> RegEx:
    'K : LCORCHETE F'
    p[0] = p[2]

# SYMB
def p_SYMB(p) -> RegEx:
    'K : SYMB'
    p[0] = Char(p[1]) # Obs: p[1] es un chr.

# _W
def p_W(p) -> RegEx:
    'K : _W'
    regex = Char('_')
    regex = Union(regex, UnionRange('a', 'z'))
    regex = Union(regex, UnionRange('A', 'Z'))
    regex = Union(regex, UnionRange('0', '9'))
    p[0] = regex

# _D
def p_D(p) -> RegEx:
    'K : _D'
    p[0] = UnionRange('0', '9')

# RANGE
# Este es un caso especial. El token RANGE puede aparecer fuera de corchetes,
# en cuyo caso hay que interpretarlo como una concatenación.
def p_RANGE(p) -> RegEx:
    'K : RANGE'

    # p[1] es un string: n-m, dondé a y b son chr
    rango = p[1].split('-')
    N = Char(rango[0])
    M = Char(rango[1])
    p[0] = Concat(Concat(N, Char('-')), M)


### Producciones de F
### F    -> SYMBF | RANGEF | ]

# SYMB F
def p_SYMBF(p) -> RegEx:
    'F : SYMB F'
    # F puede ser la unión de otro rango de caracteres o puede ser Empty
    p[0] = Union(Char(p[1]), p[2])

# RANGE F
def p_RANGEF(p) -> RegEx:
    'F : RANGE F'

    F = p[2] # Puede ser la unión de otro rango de caracteres o puede ser Empty

    # p[1] es un string: n-m, dondé n y m son chr
    rango  = p[1].split("-")
    N = rango[0]
    M = rango[1]

    if ord(M) < ord(N): # ¿Es un rango inválido?
        raise SyntaxError

    p[0] = Union(UnionRange(N,M), F)

# ]
def p_RCORCHETE(p) -> RegEx:
    'F : RCORCHETE'
    p[0] = Empty()


# Producciones de SYMB
# SYMB -> NUMBER | CHAR | MINUS | LLLAVE | RLLAVE

def p_CHAR(p) -> chr:
    'SYMB : CHAR'
    p[0] = p[1]

def p_NUMBER(p) -> chr:
    'SYMB : NUMBER'
    p[0] = p[1]

def p_MINUS(p) -> chr:
    'SYMB : MINUS'
    p[0] = '-'

def p_LLLAVE(p) -> chr:
    'SYMB : LLLAVE'
    p[0] = '{'

def p_RLLAVE(p) -> chr:
    'SYMB : RLLAVE'
    p[0] = '}'




def p_error(p):
    raise SyntaxError

parser = yacc.yacc(debug=True)