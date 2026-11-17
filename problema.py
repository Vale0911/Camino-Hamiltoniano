"""
problema.py
-----------
Módulo del proyecto: representación lógica de un CICLO HAMILTONIANO.

Contiene la clase `CicloHamiltoniano`, con:
  * el descriptor único  Visita(c, t)  =  "la ciudad c se visita en la posición t",
  * las 5 reglas del problema (regla1() ... regla5()), escritas con Ytoria / Otoria.

Descriptor:
    c  ->  índice de ciudad       (0 .. n-1)
    t  ->  posición / turno        (0 .. n-1)

Los dibujos están en visualizador.py. Requiere logica.py en la misma carpeta.
"""

from types import MethodType
from logica import Descriptor, Ytoria, Otoria
import visualizador


def escribir_ciclo(self, literal):
    """Traduce una letra proposicional a lenguaje natural (para el método .ver)."""
    if '-' in literal:
        atomo, neg = literal[1:], ' no'
    else:
        atomo, neg = literal, ''
    c, t = self.unravel(atomo)
    return f"La ciudad {self._ciudades[c]}{neg} se visita en la posicion {t + 1}"


class CicloHamiltoniano:
    """
    Problema del ciclo hamiltoniano sobre un grafo no dirigido de ciudades.

    Parámetros
    ----------
    ciudades : list[str]       nombres de las ciudades.
    aristas  : list[set[int]]  carreteras, como conjuntos de índices de ciudad.
    coords   : dict[int,(x,y)] posición de cada ciudad para dibujar (opcional).
    """

    def __init__(self, ciudades, aristas, coords=None):
        self.ciudades = ciudades
        self.n = len(ciudades)                          # #ciudades = #posiciones
        self.E = set(frozenset(a) for a in aristas)     # aristas
        self.coords = coords
        # Descriptor único Visita(c, t)
        self.Visita = Descriptor([self.n, self.n])
        self.Visita._ciudades = ciudades
        self.Visita.escribir = MethodType(escribir_ciclo, self.Visita)
        # Implementamos las 5 reglas
        self.reglas = [self.regla1(), self.regla2(), self.regla3(),
                       self.regla4(), self.regla5()]

    def ady(self, u, v):
        """True si hay carretera (arista) entre las ciudades u y v."""
        return u != v and frozenset({u, v}) in self.E

    # ==========================================
    #  IMPLEMENTACIÓN DE LAS REGLAS DEL PROBLEMA
    # ===========================================

    def regla1(self):
        """Regla 1 — En cada posición hay al menos una ciudad.
        Y_t ( O_c Visita(c,t) )"""
        return Ytoria([Otoria([self.Visita.ravel([c, t]) for c in range(self.n)])
                       for t in range(self.n)])

    def regla2(self):
        """Regla 2 — Cada ciudad está en al menos una posición.
        Y_c ( O_t Visita(c,t) )"""
        return Ytoria([Otoria([self.Visita.ravel([c, t]) for t in range(self.n)])
                       for c in range(self.n)])

    def regla3(self):
        """Regla 3 — Cada ciudad está en a lo sumo una posición.
        Y_c Y_t ( Visita(c,t) -> -( O_{t'!=t} Visita(c,t') ) )"""
        L = []
        for c in range(self.n):
            for t in range(self.n):
                otras = [self.Visita.ravel([c, tp]) for tp in range(self.n) if tp != t]
                L.append('(' + self.Visita.ravel([c, t]) + '>-' + Otoria(otras) + ')')
        return Ytoria(L)

    def regla4(self):
        """Regla 4 — Transiciones válidas (adyacencia entre posiciones consecutivas).
        Y_{t=0..n-2} Y_u ( Visita(u,t) -> O_{v vecino de u} Visita(v,t+1) )"""
        L = []
        for t in range(self.n - 1):
            for u in range(self.n):
                vec = [self.Visita.ravel([v, t + 1]) for v in range(self.n) if self.ady(u, v)]
                L.append('(' + self.Visita.ravel([u, t]) + '>' + Otoria(vec) + ')')
        return Ytoria(L)

    def regla5(self):
        """Regla 5 — Cierre del ciclo (la última posición conecta con la primera).
        Y_u ( Visita(u,n-1) -> O_{v vecino de u} Visita(v,0) )"""
        L = []
        for u in range(self.n):
            vec = [self.Visita.ravel([v, 0]) for v in range(self.n) if self.ady(u, v)]
            L.append('(' + self.Visita.ravel([u, self.n - 1]) + '>' + Otoria(vec) + ')')
        return Ytoria(L)

    # =============================
    #  MODELO -> RECORRIDO
    # ==============================

    def _orden(self, I):
        """Del modelo I saca el recorrido: orden[t] = índice de la ciudad del turno t.
        Ignora las letras que no son Visita(c,t) (por ejemplo, las auxiliares de Tseitin)."""
        inicio, fin = self.Visita.rango
        orden = [None] * self.n
        for lit, val in I.items():
            if val and inicio <= ord(lit) < fin:
                c, t = self.Visita.unravel(lit)
                orden[t] = c
        return orden

    # Los dibujos viven en visualizador.py; se dejan como métodos por comodidad.
    def dibujar_grafo(self, ax=None):
        visualizador.dibujar_grafo(self, ax)

    def visualizar_regla(self, k, ejemplo=None):
        visualizador.visualizar_regla(self, k, ejemplo)

    def visualizar_por_turnos(self, I):
        visualizador.visualizar_por_turnos(self, I)

    def _xy(self):
        """Posiciones (x,y) de las ciudades (nombre usado en los notebooks anteriores)."""
        return visualizador.posiciones(self)
