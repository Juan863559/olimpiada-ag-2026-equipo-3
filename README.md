# Olimpiada AG 2026 — Equipo 3

## Integrantes

 - Cesar Daniel Morales Ramirez	cmorales17@ucol.mx
 - Juan Pablo Rodriguez Garcia	jrodriguez142@ucol.mx
 - Ángel Roberto Rodríguez Miranda	arodriguez114@ucol.mx

---

## Descripción

Implementación de un Algoritmo Genético para minimizar la función de **Rastrigin en 10 dimensiones**, comparando:

- **3 transformaciones de fitness**: Inversión, Negación con desplazamiento, Ranking lineal
- **3 niveles de elitismo**: k=0 (sin elitismo), k=2 (elitismo bajo), k=5 (elitismo moderado)

Esto genera una **matriz 3×3 de 9 configuraciones** experimentales ejecutadas con semilla fija (42).

---

## Estructura del Proyecto

```
sesion1/
├── equipo_X_codigo.py       # Implementación principal del AG
├── equipo_X_notebook.ipynb  # Libreta Jupyter con el mismo código + explicaciones
├── equipo_X_resultados.csv  # Matriz 3×3 de resultados (9 configuraciones)
├── equipo_X_grafica.png     # Gráfica de convergencia comparativa
├── requirements.txt         # Dependencias
└── docs/
    └── decisiones.md        # Documentación de decisiones técnicas
```

---

## Requisitos

```bash
pip install -r requirements.txt
```

Dependencias: `numpy`, `matplotlib`, `pandas`

---

## Ejecución

```bash
cd sesion1
python equipo_X_codigo.py
```

Genera automáticamente:
- `equipo_X_resultados.csv` — Tabla de resultados
- `equipo_X_grafica.png` — Gráfica de convergencia

---

## Resultados Principales

| Transformacion | Elitismo | Mejor Fitness | Diversidad Final |
|---|:---:|:---:|:---:|
| Inversion | 0 | 10.528 | 0.0116 |
| Inversion | 2 | 13.920 | 0.0029 |
| Inversion | 5 | 13.306 | 0.0000 |
| Negacion | 0 | 10.528 | 0.0116 |
| Negacion | 2 | 13.920 | 0.0029 |
| Negacion | 5 | 13.306 | 0.0000 |
| Ranking | 0 | 10.528 | 0.0116 |
| Ranking | 2 | 13.920 | 0.0029 |
| Ranking | 5 | 13.306 | 0.0000 |

> **Observación clave**: Las 3 transformaciones producen resultados idénticos porque el torneo de selección opera sobre el orden relativo de los individuos (no sus valores absolutos), y las 3 transformaciones preservan ese orden.

---

## Decisiones Técnicas

Ver [`docs/decisiones.md`](docs/decisiones.md) para detalles completos sobre las decisiones de implementación.
## Documentación técnica

## Resultados Principales
Se compararon 9 configuraciones (3 transformaciones × 3 niveles de elitismo). El ranking lineal con k=0 obtuvo la mejor convergencia.
