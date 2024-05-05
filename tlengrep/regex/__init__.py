from abc import ABC, abstractmethod

from automata import AFND

__all__ = [
    "RegEx",
    "Empty",
    "Lambda",
    "Char",
    "Union",
    "Concat",
    "Star",
    "Plus"
]

cached_AFD   = AFND()
cached_REGEX = ""

class RegEx(ABC):
    """Clase abstracta para representar expresiones regulares."""

    @abstractmethod
    def naive_match(self, word: str) -> bool:
        """
        Indica si la expresión regular acepta la cadena dada.
        Implementación recursiva, poco eficiente.
        """
        pass

    def match(self, word: str) -> bool:
        """Indica si la expresión regular acepta la cadena dada."""

        ### Ésto corre por cada linea ###

        # Declaramos éstas variables como globales
        global cached_AFD   # Tenemos un AFD cacheado.
        global cached_REGEX # RegEX del AFD cacheado

        # ¿Armamos AFD?
        # Si el RegEx que quiero matchear no coincide con el del AFD cacheado, armo un nuevo AFD 
        if str(self) != cached_REGEX:
            cached_REGEX = str(self)
            cached_AFD   = self.to_afnd().determinize().minimize()

        return cached_AFD.accept_string(word)

    @abstractmethod
    def to_afnd(self) -> AFND:
        """Convierte la expresión regular a un AFND."""
        pass


    @abstractmethod
    def _atomic(self) -> bool:
        """
        (Interno) Indica si la expresión regular es atómica. Útil para
        implementar la función __str__.
        """
        pass


class Empty(RegEx):
    """Expresión regular que denota el lenguaje vacío (∅)."""

    def naive_match(self, word: str):
        return False

    def to_afnd(self) -> AFND:

        # Un AFND con un único estado que es inicial y no es final
        RES = AFND()
        RES.add_state("q0", False)
        RES.mark_initial_state("q0")
        return RES

    def _atomic(self):
        return True

    def __str__(self):
        return "∅"


class Lambda(RegEx):
    """Expresión regular que denota el lenguaje de la cadena vacía (Λ)."""

    def naive_match(self, word: str):
        return word == ""

    def to_afnd(self) -> AFND:

        # Un AFND con un único estado que es inicial y final
        RES = AFND()
        RES.add_state("q0", True)
        RES.mark_initial_state("q0")
        return RES

    def _atomic(self):
        return True

    def __str__(self):
        return "λ"


class Char(RegEx):
    """Expresión regular que denota el lenguaje de un determinado carácter."""

    def __init__(self, char: str):
        assert len(char) == 1
        self.char = char

    def naive_match(self, word: str):
        return word == self.char

    def to_afnd(self) -> AFND:

        RES = AFND()
        RES.add_state("q0", False)
        RES.add_state("q1", True)
        RES.mark_initial_state("q0")
        RES.add_transition("q0", "q1", self.char)
        return RES

    def _atomic(self):
        return True

    def __str__(self):
        return self.char


class Concat(RegEx):
    """Expresión regular que denota la concatenación de dos expresiones regulares."""

    def __init__(self, exp1: RegEx, exp2: RegEx):
        self.exp1 = exp1
        self.exp2 = exp2

    def naive_match(self, word: str):
        for i in range(len(word) + 1):
            if self.exp1.naive_match(word[:i]) and self.exp2.naive_match(word[i:]):
                return True
        return False

    def to_afnd(self) -> AFND:

        RES = AFND()               # Hago el AFND de retorno
        AFND1 = self.exp1.to_afnd() # Hago el AFND de la primer  expresión
        AFND2 = self.exp2.to_afnd() # Hago el AFND de la segunda expresión

        # Agregamos todos los estados de la primer expresión a RES.
        # No hace falta marcar los estados finales de AFND1 como finales de RES
        for q in AFND1.states: 
            RES.add_state(q, False)

        # Agregamos los estados de AFND2 a RES
        num  = 0
        name = str(num)
        
        # TODO: ¡Quitar este copy!
        for q in AFND2.states.copy(): #copy() porque sino daba "Set changed size during iteration"

            # Creo el nombre nuevo del estado
            AFND2._rename_state(q, name)

            if name in AFND2.final_states:
                RES.add_state(name, True)
            else:
                RES.add_state(name, False)
            
            num += 1
            name = str(num)


        # Agregamos las transiciones de AFND1
        for q in AFND1.states:
            RES.transitions[q] = AFND1.transitions[q]

        # Agregamos las transiciones de AFND2
        for q in AFND2.states:
            RES.transitions[q] = AFND2.transitions[q]

        # Mergeamos el alfabeto
        RES.alphabet = (AFND1.alphabet).union(AFND2.alphabet)

        # Conectamos los estados finales de AFND1 con el inicial de AFND2
        for q in AFND1.final_states:
            RES.add_transition(q, AFND2.initial_state, "λ")

        RES.mark_initial_state(AFND1.initial_state)

        # Normalizamos los estados
        RES.normalize_states()

        return RES


    def _atomic(self):
        return False

    def __str__(self):
        return f"{f'({self.exp1})' if not self.exp1._atomic() else self.exp1}" \
            f"{f'({self.exp2})' if not self.exp2._atomic() else self.exp2}"


class Union(RegEx):
    """Expresión regular que denota la unión de dos expresiones regulares."""

    def __init__(self, exp1: RegEx, exp2: RegEx):
        self.exp1 = exp1
        self.exp2 = exp2

    def naive_match(self, word: str):
        return self.exp1.naive_match(word) or self.exp2.naive_match(word)

    def to_afnd(self) -> AFND:
        
        RES = AFND()               # AFND de la unión
        AFND1 = self.exp1.to_afnd() # AFND de la primer  expresióin
        AFND2 = self.exp2.to_afnd() # AFND de la segunda expresión
        
        # Agrego a RES los estados de AFND1
        for q in AFND1.states: 
            if q in AFND1.final_states:
                RES.add_state(q, True)
            else:
                RES.add_state(q, False)

        # Agregamos los estados de AFND2 a RES
        # Tenemos que renombrar los estados para que no coindidan con los de AFND1

        num  = 0
        name = str(num)

        for q in AFND2.states.copy(): #copy() porque sino daba "Set changed size during iteration"

            AFND2._rename_state(q, name)

            if name in AFND2.final_states:
                RES.add_state(name, True)
            else:
                RES.add_state(name, False)
            
            num += 1
            name = str(num)


        # Agregamos las transiciones de AFND1
        for q in AFND1.states:
            RES.transitions[q] = AFND1.transitions[q]

        # Agregamos las transiciones de AFND2
        for q in AFND2.states:
            RES.transitions[q] = AFND2.transitions[q]

        # Mergeamos el alfabeto
        RES.alphabet = (AFND1.alphabet).union(AFND2.alphabet)

        # Agregamos un nuevo estado inicial, y lo conectamos con los iniciales de AFND1 y AFND2
        RES.add_state("qi", False)
        RES.mark_initial_state("qi")
        RES.add_transition("qi", AFND1.initial_state, "λ")
        RES.add_transition("qi", AFND2.initial_state, "λ")

        # Normalizamos los estados (por si tenemos nombres repetidos)
        RES.normalize_states()

        return RES


    def _atomic(self):
        return False

    def __str__(self):
        return f"{f'({self.exp1})' if not self.exp1._atomic() else self.exp1}" \
            f"|{f'({self.exp2})' if not self.exp2._atomic() else self.exp2}"


class Star(RegEx):
    """Expresión regular que denota la clausura de Kleene de otra expresión regular."""

    def __init__(self, exp: RegEx):
        self.exp = exp

    def naive_match(self, word: str):
        if word == "" or self.exp.naive_match(word):
            return True
        for i in range(1, len(word) + 1):
            if self.exp.naive_match(word[:i]) and self.naive_match(word[i:]):
                return True
        return False

    def to_afnd(self) -> AFND:
        
        afnd = self.exp.to_afnd()

        afnd.add_state("qi", False)
        afnd.add_state("qf", True)
        afnd.add_transition("qi", afnd.initial_state, "λ")
        afnd.mark_initial_state("qi")
        for q in afnd.final_states:
            afnd.add_transition(q, "qf", "λ")
            afnd.add_transition(q, "qi", "λ")
        afnd.add_transition("qi", "qf", "λ")
        afnd.normalize_states()
        return afnd

    def _atomic(self):
        return False

    def __str__(self):
        return f"({self.exp})*" if not self.exp._atomic() else f"{self.exp}*"


class Plus(RegEx):
    """Expresión regular que denota la clausura positiva de otra expresión regular."""

    def __init__(self, exp: RegEx):
        self.exp = exp

    def naive_match(self, word: str):
        if self.exp.naive_match(word):
            return True
        for i in range(1, len(word) + 1):
            if self.exp.naive_match(word[:i]) and self.naive_match(word[i:]):
                return True
        return False

    def to_afnd(self) -> AFND:
        RES = Concat(self.exp, Star(self.exp)).to_afnd()
        return RES

    def _atomic(self) -> bool:
        return False

    def __str__(self):
        return f"({self.exp})+" if not self.exp._atomic() else f"{self.exp}+"