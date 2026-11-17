"""
visualizador.py
---------------
Dibujos del proyecto del ciclo hamiltoniano. Todas las funciones reciben el problema `H`
(un objeto `CicloHamiltoniano` de problema.py) y no dependen de ningún SAT-solver.

  * dibujar_grafo(H)                 -> el grafo de ciudades y carreteras.
  * visualizar_regla(H, k)           -> UNA regla (1 a 5): qué letras Visita(c,t) relaciona.
  * visualizar_por_turnos(H, I)      -> el recorrido de un modelo `I`, una imagen por turno.
"""

import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch


def posiciones(H):
    """Posiciones (x,y) de las ciudades. Si H no trae coordenadas, las pone en un círculo."""
    if H.coords:
        return H.coords
    return {i: (math.cos(2 * math.pi * i / H.n), math.sin(2 * math.pi * i / H.n))
            for i in range(H.n)}


def dibujar_grafo(H, ax=None):
    """Dibuja el grafo: ciudades (nodos) y carreteras (aristas)."""
    P = posiciones(H)
    mostrar = ax is None
    if ax is None:
        fig, ax = plt.subplots(figsize=(4, 3.4))
    for a in H.E:
        u, v = tuple(a)
        ax.plot([P[u][0], P[v][0]], [P[u][1], P[v][1]], color='gray', lw=1.5, zorder=1)
    for i in range(H.n):
        ax.scatter(*P[i], s=650, color='#eef3fb', edgecolors='#2457d6', lw=2.2, zorder=3)
        ax.text(P[i][0], P[i][1], H.ciudades[i], ha='center', va='center',
                fontsize=8, fontweight='bold', color='#14181f', zorder=4)
    ax.margins(0.15)                     # margen para que no se corten los nodos de los bordes
    ax.set_aspect('equal')
    ax.axis('off')
    if mostrar:
        plt.show()


def visualizar_por_turnos(H, I):
    """Dibuja el recorrido TURNO POR TURNO: una imagen por cada posición.
    I es una interpretación (un modelo) del problema; las letras auxiliares de Tseitin
    se ignoran (solo cuentan las letras Visita(c,t))."""
    P = posiciones(H)
    orden = H._orden(I)
    if None in orden:
        raise ValueError('El modelo no asigna una ciudad a cada turno: ' + str(orden))
    fig, axes = plt.subplots(1, H.n, figsize=(2.6 * H.n, 3))
    if H.n == 1:
        axes = [axes]
    for k in range(H.n):                 # k = turno actual (mostramos el recorrido hasta aquí)
        ax = axes[k]
        # Todas las carreteras (gris)
        for a in H.E:
            u, v = tuple(a)
            ax.plot([P[u][0], P[v][0]], [P[u][1], P[v][1]], color='lightgray', lw=1.5, zorder=1)
        # Tramos ya recorridos (azul con flecha)
        for t in range(k):
            u, v = orden[t], orden[t + 1]
            ax.annotate('', xy=P[v], xytext=P[u],
                        arrowprops=dict(arrowstyle='-|>', color='#2457d6', lw=2.3), zorder=2)
        # En el último turno, el cierre del ciclo (naranja)
        if k == H.n - 1:
            u, v = orden[H.n - 1], orden[0]
            ax.annotate('', xy=P[v], xytext=P[u],
                        arrowprops=dict(arrowstyle='-|>', color='#e8820c', lw=2.3), zorder=2)
        # Nodos (ciudades)
        for i in range(H.n):
            ya = i in orden[:k + 1]
            borde = '#2457d6' if i == orden[k] else ('#9db4f0' if ya else '#d0d5de')
            ax.scatter(*P[i], s=650, color='#eef3fb', edgecolors=borde, lw=2.2, zorder=3)
            ax.text(P[i][0], P[i][1], H.ciudades[i], ha='center', va='center', fontsize=8,
                    fontweight='bold', color='#14181f' if ya else '#9aa3b2', zorder=4)
        ax.set_title(f"Turno {k + 1}: {H.ciudades[orden[k]]}", fontsize=9)
        ax.margins(0.15)
        ax.set_aspect('equal')
        ax.axis('off')
    fig.suptitle("Recorrido del ciclo hamiltoniano, turno por turno", fontsize=12, y=1.04)
    plt.tight_layout()
    plt.show()


# ----------------------------------------------------------------------------
#  UNA REGLA
# ----------------------------------------------------------------------------

_AZUL, _NARANJA, _GRIS = '#2457d6', '#e8820c', '#d0d5de'


def _ejemplo_por_defecto(H, k):
    """Un conjunto (sub-fórmula unida por Y) representativo de la regla k."""
    c = min(2, H.n - 1)       # Bog en el grafo del proyecto: la ciudad con más carreteras
    t = min(1, H.n - 2) if H.n > 1 else 0
    return {1: (0,), 2: (0,), 3: (c, t), 4: (c, t), 5: (c,)}[k]


def _celdas_regla(H, k, ej):
    """Devuelve (antecedente, consecuente, texto): celdas (c, t) de cada papel y una frase."""
    n = H.n
    if k == 1:
        (t,) = ej
        return [], [(c, t) for c in range(n)], \
            f"Regla 1 · posición {t + 1}: al menos UNA de estas ciudades (O) va en la posición {t + 1}"
    if k == 2:
        (c,) = ej
        return [], [(c, t) for t in range(n)], \
            f"Regla 2 · {H.ciudades[c]}: aparece en al menos UNA de estas posiciones (O)"
    if k == 3:
        c, t = ej
        return [(c, t)], [(c, tp) for tp in range(n) if tp != t], \
            f"Regla 3 · si {H.ciudades[c]} va en la posición {t + 1}, NO va en ninguna de las otras (→ ¬O)"
    if k == 4:
        u, t = ej
        return [(u, t)], [(v, t + 1) for v in range(n) if H.ady(u, v)], \
            f"Regla 4 · si {H.ciudades[u]} va en la posición {t + 1}, en la {t + 2} va una ciudad vecina (→ O)"
    u, = ej
    return [(u, n - 1)], [(v, 0) for v in range(n) if H.ady(u, v)], \
        f"Regla 5 · si {H.ciudades[u]} va en la última posición, en la primera va una ciudad vecina (→ O)"


def visualizar_regla(H, k, ejemplo=None):
    """Dibuja UNA regla (k = 1..5) sobre la cuadrícula de letras Visita(c,t).

    Filas = ciudades, columnas = posiciones: cada casilla es una letra proposicional.
    Como cada regla es una Y-toria de conjuntos parecidos, se dibuja un conjunto de
    ejemplo (`ejemplo`: (t,) en la regla 1, (c,) en la 2 y la 5, (c,t) en la 3 y la 4):
      azul    = el antecedente (la letra que se supone verdadera),
      naranja = las letras que se juntan con O (en la regla 3, con ¬O).
    En las reglas 4 y 5 se dibuja también el grafo, con la ciudad y sus vecinas."""
    assert k in (1, 2, 3, 4, 5), "k debe estar entre 1 y 5"
    ej = ejemplo if ejemplo is not None else _ejemplo_por_defecto(H, k)
    ant, cons, frase = _celdas_regla(H, k, ej)
    n = H.n
    con_grafo = k in (4, 5)
    fig, axes = plt.subplots(1, 2 if con_grafo else 1, figsize=(9.4 if con_grafo else 5.2, 3.9),
                             gridspec_kw={'width_ratios': [1.25, 1]} if con_grafo else None)
    ax = axes[0] if con_grafo else axes
    for c in range(n):
        for t in range(n):
            if (c, t) in ant:
                fondo, borde, color = '#cfdcfb', _AZUL, '#14181f'
            elif (c, t) in cons:
                fondo, borde, color = '#fde4c8', _NARANJA, '#14181f'
            else:
                fondo, borde, color = '#f6f7fa', _GRIS, '#9aa3b2'
            ax.add_patch(Rectangle((t, n - 1 - c), 0.94, 0.94, facecolor=fondo, edgecolor=borde, lw=1.8))
            ax.text(t + 0.47, n - 1 - c + 0.47, f"Visita\n({H.ciudades[c]}, {t + 1})", ha='center',
                    va='center', fontsize=6.5, color=color)
    for c in range(n):
        ax.text(-0.15, n - 1 - c + 0.47, H.ciudades[c], ha='right', va='center', fontsize=8, fontweight='bold')
    for t in range(n):
        ax.text(t + 0.47, n + 0.05, f"Pos. {t + 1}", ha='center', va='bottom', fontsize=8, fontweight='bold')
    ax.set_xlim(-0.9, n); ax.set_ylim(-0.1, n + 0.55)
    ax.set_aspect('equal'); ax.axis('off')
    if con_grafo:
        ax2 = axes[1]
        P = posiciones(H)
        origen = ant[0][0]
        vecinas = {c for c, _ in cons}
        for a in H.E:
            u, v = tuple(a)
            resaltada = origen in a and (u if v == origen else v) in vecinas
            ax2.plot([P[u][0], P[v][0]], [P[u][1], P[v][1]], color=_NARANJA if resaltada else 'lightgray',
                     lw=2.6 if resaltada else 1.4, zorder=1)
        for i in range(n):
            borde = _AZUL if i == origen else (_NARANJA if i in vecinas else _GRIS)
            ax2.scatter(*P[i], s=650, color='#eef3fb', edgecolors=borde, lw=2.4, zorder=3)
            ax2.text(P[i][0], P[i][1], H.ciudades[i], ha='center', va='center', fontsize=8,
                     fontweight='bold', zorder=4)
        ax2.margins(0.15); ax2.set_aspect('equal'); ax2.axis('off')
        ax2.set_title('Carreteras desde ' + H.ciudades[origen], fontsize=9)
    leyenda = []
    if ant:
        leyenda.append(Patch(facecolor='#cfdcfb', edgecolor=_AZUL, label='antecedente'))
    leyenda.append(Patch(facecolor='#fde4c8', edgecolor=_NARANJA,
                         label={1: 'se juntan con O', 2: 'se juntan con O',
                                3: 'se juntan con O, y se niega la O', 4: 'consecuente: O de las vecinas',
                                5: 'consecuente: O de las vecinas'}[k]))
    fig.legend(handles=leyenda, loc='lower center', ncol=len(leyenda), fontsize=8, frameon=False)
    fig.suptitle(frase, fontsize=10, y=0.99)
    plt.tight_layout(rect=(0, 0.07, 1, 0.95))
    plt.show()
