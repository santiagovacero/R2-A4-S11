# =========================
# CLASE NODO
# =========================

class Nodo:

    def __init__(self, dato):

        self.dato = dato
        self.siguiente = None


# =========================
# LISTA ENLAZADA
# =========================

class ListaEnlazada:

    def __init__(self):

        self.cabeza = None

    def agregar(self, dato):

        nuevo_nodo = Nodo(dato)

        if self.cabeza is None:

            self.cabeza = nuevo_nodo
            return

        actual = self.cabeza

        while actual.siguiente is not None:

            actual = actual.siguiente

        actual.siguiente = nuevo_nodo

    def mostrar(self):

        elementos = []

        actual = self.cabeza

        while actual is not None:

            elementos.append(actual.dato)

            actual = actual.siguiente

        return elementos


# =========================
# LISTA CIRCULAR
# =========================

class ListaCircular:

    def __init__(self):

        self.cabeza = None

    def agregar(self, dato):

        nuevo_nodo = Nodo(dato)

        if self.cabeza is None:

            self.cabeza = nuevo_nodo

            nuevo_nodo.siguiente = self.cabeza

            return

        actual = self.cabeza

        while actual.siguiente != self.cabeza:

            actual = actual.siguiente

        actual.siguiente = nuevo_nodo

        nuevo_nodo.siguiente = self.cabeza

    def mostrar(self):

        elementos = []

        if self.cabeza is None:

            return elementos

        actual = self.cabeza

        while True:

            elementos.append(actual.dato)

            actual = actual.siguiente

            if actual == self.cabeza:

                break

        return elementos