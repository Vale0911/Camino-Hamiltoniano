# Ciclo Hamiltoniano — Representación lógica y SAT-solvers

Proyecto de **Lógica para Ciencias de la Computación** (Universidad del Rosario).

**De Ciudades a Recorridos: Representación Lógica de un Ciclo Hamiltoniano.**
Dado un grafo de ciudades conectadas por carreteras, buscamos un recorrido que visite **cada
ciudad exactamente una vez** y **regrese** a la ciudad de origen. Lo modelamos con lógica
proposicional y lo resolvemos con distintos SAT-solvers.

## El problema

- **Ciudades:** Baq, Buc, Bog, Med, Per, con 7 carreteras.
- **Descriptor único:** `Visita(c, t)` = "la ciudad `c` se visita en la posición (turno) `t`".
- **Dominios:** `c` ∈ 5 ciudades, `t` ∈ 5 posiciones → **25 letras proposicionales**.
- **Reglas (1–5):**
  1. En cada posición hay al menos una ciudad.
  2. Cada ciudad está en al menos una posición.
  3. Cada ciudad está en a lo sumo una posición.
  4. Transiciones válidas: posiciones consecutivas son ciudades conectadas por una carretera.
  5. Cierre del ciclo: la última posición conecta con la primera.

## Estructura del repositorio

```
Camino-Hamiltoniano/
├── README.md                # problema, estructura, cómo ejecutar, autores
├── requirements.txt         # numpy, matplotlib, pandas (+ python-sat si MiniSAT lo usa)
├── .gitignore               # .ipynb_checkpoints, __pycache__
│
├── logica.py                # librería ÚNICA: fórmulas, Descriptor, Ytoria/Otoria,
│                            #   tableaux (nodos), FNC, tseitin/a_clausal
├── problema.py              # CicloHamiltoniano: descriptor Visita(c,t) + reglas 1 a 5
├── visualizador.py          # grafo, una regla, y recorrido por turnos
│
├── 01_Visualizador.ipynb    # por regla: lenguaje natural, fórmula, visualización
├── 02_SAT-Tabla.ipynb
├── 03_SAT-Tableaux.ipynb    # anchura, profundidad y backtracking
├── 04_DPLL.ipynb            # Tseitin + DPLL
├── 05_WalkSAT.ipynb         # flip: voltear un literal; try: cambiar I
├── 06_MiniSAT.ipynb         # (pendiente)
├── 07_Comparacion.ipynb     # (pendiente) junta los CSV y compara solvers por regla
│
├── datos/                   # opcional: JSON del tablero
│   ├── reglas.json          #   las 5 reglas generadas (lo guarda 01)
│   └── tseitin.json         #   forma clausal de cada regla (lo calcula 04 una vez)
├── resultados/              # un CSV por solver (resultados_SATtabla.csv, ...)
│                            #   y los modelos encontrados (modelos_*.json)
└── docs/                    # paper IEEE (.tex) y diapositivas (.pdf)
```

## Requisitos

```bash
pip install -r requirements.txt
```

Python 3 con `numpy`, `matplotlib`, `pandas` y `jupyter`. El módulo `signal.alarm` que usa el
límite de tiempo de `03_SAT-Tableaux.ipynb` funciona en Mac y Linux (no en Windows).

## Cómo ejecutar

1. Abrir los notebooks desde la **raíz del repositorio** (para que `logica.py`, `problema.py` y
   `visualizador.py` queden en la misma carpeta que el notebook, y las carpetas `datos/` y
   `resultados/` se encuentren).
2. En cada notebook: **Kernel → Restart & Run All**.
3. Orden recomendado: `01` → `02`/`03` → `04` (genera `datos/tseitin.json`) → `05`. El `05` también
   calcula `datos/tseitin.json` si todavía no existe.

Todos los notebooks importan igual:

```python
from logica import *
from problema import CicloHamiltoniano
```

## Qué hace cada notebook

| Notebook | Qué hace | Salida |
|---|---|---|
| `01_Visualizador` | Cada regla en lenguaje natural, como fórmula y dibujada; modelo armado a mano dibujado turno por turno | `datos/reglas.json` |
| `02_SAT-Tabla` | Tabla de verdad (recorre las 2²⁵ interpretaciones) | `resultados/resultados_SATtabla.csv` |
| `03_SAT-Tableaux` | Tableaux por anchura, por profundidad y con backtracking, con límite de tiempo | `resultados/resultados_Tableaux.csv` |
| `04_DPLL` | Transformación de Tseitin a forma clausal y DPLL | `datos/tseitin.json`, `resultados/resultados_DPLL.csv` |
| `05_WalkSAT` | Búsqueda local aleatoria (WalkSAT incremental) sobre la forma clausal | `resultados/resultados_WalkSAT.csv` |

Todos los CSV tienen las columnas `Solver, Regla, Resultado, ¿Verifica?, Tiempo (s)` (algunos
añaden columnas propias, que se pueden ignorar al comparar). Los modelos encontrados quedan en
`resultados/modelos_<solver>.json`.

## Autores

- Moises Bulla Ospina
- Julian David Parra Granados
- Valentina Mesa Fajardo

Matemáticas Aplicadas y Ciencias de la Computación — Universidad del Rosario
