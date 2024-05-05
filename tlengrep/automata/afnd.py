from enum import Enum
from typing import Hashable, Union

from automata.af import AF
from automata.afd import AFD


__all__ = ["AFND"]


class SpecialSymbol(Enum):
    Lambda = "λ"


class AFND(AF):
    """Autómata finito no determinístico (con transiciones lambda)."""

    def add_transition(self, state1: Hashable, state2: Hashable, char: Union[str, SpecialSymbol]):
        """Agrega una transición al autómata."""
        if state1 not in self.states:
            raise ValueError(f"El estado {state1} no pertenece al autómata.")
        if state2 not in self.states:
            raise ValueError(f"El estado {state2} no pertenece al autómata.")
        if char not in self.transitions[state1]:
            self.transitions[state1][char] = set()
        self.transitions[state1][char].add(state2)
        if char is not SpecialSymbol.Lambda:
            self.alphabet.add(char)

    # Obs: Quizás se está formando un ciclo de λ
    def clausura_lambda(self, Q: set, Qv: set) -> set:

        # Q es el conjunto de estados al que le aplicamos la Clausura λ
        # Qv son los estados ya visitados, no los quiero volver a visitar en futuras recursiones
        # (Para evitar entrar en un ciclo de transiciones λ)

        Qv = Qv | Q
        U = set()
                
        if len(Q) == 0:
            return U
        else:
            # Formo U como el conjunto de estados visitables desde Q con una transición λ
            for q in Q:
                if "λ" in self.transitions[q]:
                    U = U | self.transitions[q]["λ"]
            # A U le quito aquellos estados que no quiero volver a visitar
            U = U - Qv
            return U | self.clausura_lambda(U, Qv)

    def determinize(self) -> AFD:
        """Determiniza el autómata."""

        # Creamos el autómata
        afd = AFD()
        
        # Estado inicial
        qi = self.clausura_lambda({self.initial_state}, set())
        qi.add(self.initial_state)
        qi = frozenset(qi)

        Estados = [qi]      # Estados del afd (visitados y sin visitar)
        Visitados = set()   # Estados del afd (visitados)

        # Esta es la mejor forma que encontramos de hacer un dict adentro de otro dict
        # (que vergüenzaaa!!!)
        delta      = {}  # Función de transición delta
        mini_delta = {}  # Variable auxiliar para delta

        for Q in Estados:

            if Q not in Visitados:
                
                Visitados.add(Q)

                for a in self.alphabet - set("λ"): # Por cada símbolo del alfabeto

                    # Formo U como el conjunto de estados visitables desde Q consumiendo 'a'
                    U = set()
                    for q in Q:
                        if a in self.transitions[q]:
                            U = U | self.transitions[q][a]

                    U = U | self.clausura_lambda(U, set())

                    # Formo delta[Q]
                    # Las siguientes lineas son para hacer: 
                    # delta[Q][a] = frozenset(U)
                    
                    # aaaa que espanto que vergüenzaaa
                    if Q not in delta.keys():
                        mini_delta = {}
                    else:
                        mini_delta = delta[Q]
                    
                    mini_delta[a] = frozenset(U)
                    delta[Q] = mini_delta

                    if U not in Estados:
                        Estados.append(frozenset(U))

        # Agregamos los estados
        for Q in Estados:
            if len(Q & self.final_states) > 0:
                afd.add_state(Q, True)
            else:
                afd.add_state(Q, False)

        afd.mark_initial_state(qi)

        # Agregamos las transiciones
        for Q in Estados:
            for a in self.alphabet:
                if delta != {} and a in delta[Q]:
                    afd.add_transition(Q, delta[Q][a], a)

        afd.normalize_states()
        return afd
            
     

    def _rename_state_in_transitions(self, old_name: Hashable, new_name: Hashable):
        """Renombra un estado dentro de las transiciones del autómata."""
        self.transitions[new_name] = self.transitions[old_name]
        del self.transitions[old_name]
        for state in self.transitions:
            for char in self.transitions[state]:
                if old_name in self.transitions[state][char]:
                    self.transitions[state][char].remove(old_name)
                    self.transitions[state][char].add(new_name)

    def _get_extended_alphabet(self) -> list[str]:
        """Obtiene el alfabeto extendido del autómata (incluyendo símbolos especiales)."""
        return list(self.alphabet) + [SpecialSymbol.Lambda]

    def _transitions_to_str(self, state: Hashable) -> dict[Hashable, str]:
        """Devuelve las transiciones de un estado para cada símbolo como string."""
        transitions = {}
        for char in self._get_extended_alphabet():
            if char in self.transitions[state]:
                transitions[char] = ",".join(self.transitions[state][char])
            else:
                transitions[char] = "-"
        return transitions
