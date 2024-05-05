from typing import Hashable
from automata.af import AF

__all__ = ["AFD"]


class AFD(AF):
    """Autómata finito determinístico."""

    def accept_string(self, word: str):
        """ Verifica si la cadena Word es aceptada por el autómata """

        # q es el estado en el que estamos parades
        q = self.initial_state
        
        # Hacemos el match
        for a in word:
            if a in self.transitions[q]:
                q = self.transitions[q][a]
            else:
                return False

        # ¿Terminamos en un estado final?
        if q in self.final_states:
            return True
        else:
            return False

    def add_transition(self, state1: Hashable, state2: Hashable, char: str):
        """Agrega una transición al autómata."""
        if state1 not in self.states:
            raise ValueError(f"El estado {state1} no pertenece al autómata.")
        if state2 not in self.states:
            raise ValueError(f"El estado {state2} no pertenece al autómata.")
        self.transitions[state1][char] = state2
        self.alphabet.add(char)

    def estados_accesibles(self, Q: set, Qv: set) -> set:
        
        # Qv son los estados que ya visité        
        Qv = Qv | Q
        U = set()
                
        if len(Q) == 0:
            return U
        else:

            # Formo U como el conjunto de estados visitables desde Q con una transición
            for q in Q:
                for a in self.alphabet:
                    if a in self.transitions[q]:
                        U = U | {self.transitions[q][a]}
            
            # A U le quito aquellos estados que no quiero volver a visitar
            U = U - Qv
            return U | self.estados_accesibles(U, Qv)


    def minimize(self):

        """Minimiza el autómata."""

        # Como no se cómo quitar estados de una automata, prefiero crear uno nuevo
        afd = AFD()

        # Buscamos los estados accesibles desde el estado inicial
        # accesibles = self.estados_accesibles({self.initial_state}, set()) | {self.initial_state}
        
        accesibles = self.states

        """ Algoritmo de la tablita """

        # Diccionario con todas las clases de  equivalencia
        clases      = {} # clases[<número de iteración>][<estado>] = <clase de equivalencia>
        clases_en_i = {}

        # Clase de equivalencia de la iteración 0
        for q in accesibles:
            if q in self.final_states:
                clases_en_i[q] = 1
            else:
                clases_en_i[q] = 0
        clases[0] = clases_en_i

        alphabet = list(self.alphabet)
        alphabet.sort()

        i = 0
        seguimos_iterando = True

        # si hay la misma cantidad de clases en clases[i] que en clases[i-1], me estanqué
        # si hay menos cantidad de clases en clases[i] que en clases[i-1], sigo iterando
        while seguimos_iterando:
            
            i += 1

            # Clases de equivalencia de la iteración i
            clases_en_i = {}

            # Cada clase de equivalencia tiene un id que la identifica
            id  = 0
            # En ids guardamos qué id le corresponde a cada lista de ids
            ids = {}

            for q in self.states:

                clase_de_q = []
                clase_de_q.append(clases[i-1][q])

                for a in alphabet:
                    clase_de_q.append(clases[i-1][self.transitions[q][a]])

                # Le asignamos un id a clase_de_q
                if str(clase_de_q) not in ids.keys():
                    ids[str(clase_de_q)] = id
                    id += 10

                # Agrego la clase de q a las clases de la iteración i
                clases_en_i[q] = ids[str(clase_de_q)]

            # Agrego las clases de la iteración i a las clases de todas las iteraciones
            clases[i] = clases_en_i
            
            # Guardamos las clases de equivalencia de la iteración i en un set
            values_i = set()
            for v in clases[i].values():
                values_i.add(str(v))

            # Guardamos las clases de equivalencia de la iteración i-1 en un set
            values_i_1 = set()
            for v in clases[i-1].values():
                values_i_1.add(str(v))

            # Si tenemos la misma cantidad de clases de equivalencia que en la iteración
            # anterior, entonces nos estancamos. Terminamos de iterar.
            seguimos_iterando = len(values_i) > len(values_i_1)

        # Por cada clase de equivalencia que encontramos, agregamos un nuevo estado
        # en el AFD mínimo

        for q in self.states:
            clase = str(clases[i][q])
            if clase not in afd.states:
                if q in self.final_states:
                    afd.add_state(clase, True)  
                else:
                    afd.add_state(clase, False)

        clase = str(clases[i][self.initial_state])
        afd.mark_initial_state(clase)

        for q in self.states:
            for a in self.alphabet:
                if self.transitions[q][a] != set():

                    p = self.transitions[q][a]
                    
                    claseQ = str(clases[i][q])
                    claseP = str(clases[i][p])
                    
                    afd.add_transition(claseQ, claseP, a)

        afd.normalize_states()
        
        return afd

    def _rename_state_in_transitions(self, old_name: Hashable, new_name: Hashable):
        """Renombra un estado dentro de las transiciones del autómata."""
        self.transitions[new_name] = self.transitions[old_name]
        del self.transitions[old_name]
        for state in self.transitions:
            for char in self.transitions[state]:
                if self.transitions[state][char] == old_name:
                    self.transitions[state][char] = new_name

    def _get_extended_alphabet(self) -> list[str]:
        """Obtiene el alfabeto extendido del autómata (incluyendo símbolos especiales)."""
        return list(self.alphabet)

    def _transitions_to_str(self, state: Hashable) -> dict[Hashable, str]:
        """Devuelve las transiciones de un estado para cada símbolo como string."""
        transitions = {}
        for char in self._get_extended_alphabet():
            if char in self.transitions[state]:
                transitions[char] = self.transitions[state][char]
            else:
                transitions[char] = "-"
        return transitions
