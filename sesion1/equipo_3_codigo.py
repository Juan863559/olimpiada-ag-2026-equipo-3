"""
Sesión 1 - El Optimizador Perfecto
Algoritmos Genéticos: Transformaciones de Fitness + Elitismo
Función objetivo: Rastrigin 10D (minimización)
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

# ─────────────────────────────────────────────
# PARÁMETROS FIJOS
# ─────────────────────────────────────────────
POBLACION      = 50
GENERACIONES   = 100
LONGITUD       = 10          # dimensiones de Rastrigin
PROB_CRUZ      = 0.8
PROB_MUT       = 0.01
DOMINIO_MIN    = -5.12
DOMINIO_MAX    =  5.12
K_TORNEO       = 3


# ─────────────────────────────────────────────
# FUNCIÓN OBJETIVO
# ─────────────────────────────────────────────
def rastrigin(x):
    """
    Función Rastrigin para minimización.
    Óptimo global: f(0,...,0) = 0
    """
    A = 10
    n = len(x)
    return A * n + np.sum(x**2 - A * np.cos(2 * np.pi * x))


# ─────────────────────────────────────────────
# TRANSFORMACIONES DE FITNESS
# ─────────────────────────────────────────────
def fitness_inversion(valor_objetivo):
    """Transforma minimización en maximización usando inversión."""
    return 1.0 / (1.0 + valor_objetivo)


def fitness_negacion(valor_objetivo, c_max):
    """Negación con desplazamiento. c_max = max_poblacion * 1.1"""
    return max(0.0, c_max - valor_objetivo)


def fitness_ranking(poblacion_ordenada, sp=1.5):
    """
    Asigna fitness basado en ranking lineal.
    poblacion_ordenada: lista de valores objetivos ordenados de PEOR a MEJOR
                        (mayor a menor en Rastrigin porque minimizamos).
    Devuelve array con el fitness para cada índice del ranking.
    """
    N = len(poblacion_ordenada)
    fitness_arr = np.zeros(N)
    for rank in range(1, N + 1):          # rank 1 = peor, rank N = mejor
        fitness_arr[rank - 1] = 2 - sp + 2 * (sp - 1) * (rank - 1) / (N - 1)
    return fitness_arr                     # índice 0 = peor, N-1 = mejor


# ─────────────────────────────────────────────
# OPERADORES GENÉTICOS
# ─────────────────────────────────────────────
def inicializar_poblacion():
    """Genera una población de vectores reales en el dominio."""
    return np.random.uniform(DOMINIO_MIN, DOMINIO_MAX, (POBLACION, LONGITUD))


def evaluar_poblacion(poblacion):
    """Devuelve array con el valor Rastrigin de cada individuo."""
    return np.array([rastrigin(ind) for ind in poblacion])


def seleccion_torneo(poblacion, fitness_vals):
    """Selección por torneo con k=3 (mayor fitness = mejor)."""
    seleccionados = []
    for _ in range(len(poblacion)):
        candidatos = np.random.choice(len(poblacion), K_TORNEO, replace=False)
        mejor = candidatos[np.argmax(fitness_vals[candidatos])]
        seleccionados.append(poblacion[mejor].copy())
    return np.array(seleccionados)


def cruzamiento_un_punto(padre1, padre2):
    """Cruce de un punto para vectores reales."""
    if np.random.rand() < PROB_CRUZ:
        punto = np.random.randint(1, LONGITUD)
        hijo1 = np.concatenate([padre1[:punto], padre2[punto:]])
        hijo2 = np.concatenate([padre2[:punto], padre1[punto:]])
        return hijo1, hijo2
    return padre1.copy(), padre2.copy()


def mutacion_uniforme(individuo):
    """Mutación uniforme: reemplaza gen con valor aleatorio en el dominio."""
    mutado = individuo.copy()
    for i in range(LONGITUD):
        if np.random.rand() < PROB_MUT:
            mutado[i] = np.random.uniform(DOMINIO_MIN, DOMINIO_MAX)
    return mutado


def aplicar_elitismo(poblacion, obj_vals, nueva_poblacion, nueva_obj_vals, k):
    """
    Preserva los k mejores individuos (menor valor objetivo = mejor en Rastrigin).
    Los inserta reemplazando a los k peores de la nueva población.
    """
    if k == 0:
        return nueva_poblacion.copy(), nueva_obj_vals.copy()

    # índices ordenados: mejores primero (menor objetivo)
    idx_actuales = np.argsort(obj_vals)[:k]
    idx_peores   = np.argsort(nueva_obj_vals)[-k:]

    resultado     = nueva_poblacion.copy()
    resultado_obj = nueva_obj_vals.copy()

    for i, j in zip(idx_actuales, idx_peores):
        resultado[j]     = poblacion[i].copy()
        resultado_obj[j] = obj_vals[i]

    return resultado, resultado_obj


def calcular_diversidad(fitness_vals):
    """Diversidad = desviación estándar del fitness en la población."""
    return float(np.std(fitness_vals))


# ─────────────────────────────────────────────
# ALGORITMO GENÉTICO GENÉRICO
# ─────────────────────────────────────────────
def ejecutar_ag(tipo_fitness, k_elitismo, seed=42):
    """
    Ejecuta el AG con la transformación de fitness y elitismo dados.

    tipo_fitness : 'inversion' | 'negacion' | 'ranking'
    k_elitismo   : 0 | 2 | 5
    seed         : semilla aleatoria (default 42)

    Devuelve:
        mejor_obj_final   - valor Rastrigin del mejor individuo en gen 100
        historial_mejor   - lista de mejores por generación (valor objetivo)
        tiempo_seg        - tiempo de ejecución
        diversidad_final  - std del fitness en la última generación
    """
    np.random.seed(seed)
    t_inicio = time.time()

    poblacion = inicializar_poblacion()
    obj_vals  = evaluar_poblacion(poblacion)

    historial_mejor = []

    for gen in range(GENERACIONES):
        # ── Calcular fitness según transformación ──────────────────────────
        if tipo_fitness == 'inversion':
            fit_vals = np.array([fitness_inversion(v) for v in obj_vals])

        elif tipo_fitness == 'negacion':
            c_max    = float(np.max(obj_vals)) * 1.1
            fit_vals = np.array([fitness_negacion(v, c_max) for v in obj_vals])

        elif tipo_fitness == 'ranking':
            # ordenar población de peor (mayor obj) a mejor (menor obj)
            orden    = np.argsort(obj_vals)[::-1]   # mayor -> menor
            rank_fit = fitness_ranking(np.sort(obj_vals)[::-1])
            fit_vals = np.zeros(POBLACION)
            for posicion, idx in enumerate(orden):
                fit_vals[idx] = rank_fit[posicion]
        else:
            raise ValueError(f"tipo_fitness desconocido: {tipo_fitness}")

        # ── Registrar mejor objetivo ───────────────────────────────────────
        historial_mejor.append(float(np.min(obj_vals)))

        # ── Selección ─────────────────────────────────────────────────────
        seleccionados = seleccion_torneo(poblacion, fit_vals)

        # ── Cruzamiento y mutación ─────────────────────────────────────────
        nueva_pob = []
        for i in range(0, POBLACION, 2):
            h1, h2 = cruzamiento_un_punto(seleccionados[i],
                                          seleccionados[(i + 1) % POBLACION])
            nueva_pob.append(mutacion_uniforme(h1))
            nueva_pob.append(mutacion_uniforme(h2))
        nueva_pob = np.array(nueva_pob[:POBLACION])
        nueva_obj = evaluar_poblacion(nueva_pob)

        # ── Elitismo ──────────────────────────────────────────────────────
        poblacion, obj_vals = aplicar_elitismo(
            poblacion, obj_vals, nueva_pob, nueva_obj, k_elitismo
        )

    tiempo_seg       = time.time() - t_inicio
    diversidad_final = calcular_diversidad(
        np.array([fitness_inversion(v) for v in obj_vals])   # en escala fitness
    )

    return float(np.min(obj_vals)), historial_mejor, tiempo_seg, diversidad_final


# ─────────────────────────────────────────────
# EXPERIMENTOS: MATRIZ 3 × 3
# ─────────────────────────────────────────────
transformaciones = ['inversion', 'negacion', 'ranking']
elitismos        = [0, 2, 5]
nombres_tf       = {'inversion': 'Inversion', 'negacion': 'Negacion', 'ranking': 'Ranking'}

resultados     = []
historiales    = {}   # key: (tipo_fitness, k)

print("Ejecutando 9 configuraciones (esto puede tardar unos segundos)...\n")

for tf in transformaciones:
    for k in elitismos:
        label = f"{nombres_tf[tf]} k={k}"
        print(f"  -> {label} ...")
        mejor, hist, t, div = ejecutar_ag(tf, k, seed=42)
        resultados.append({
            'Transformacion':  nombres_tf[tf],
            'Elitismo':        k,
            'Mejor_Fitness':   round(mejor, 6),
            'Generaciones':    GENERACIONES,
            'Tiempo_seg':      round(t, 4),
            'Diversidad_Final': round(div, 6)
        })
        historiales[(tf, k)] = hist

print("\n[OK] Experimentos completados.\n")


# ─────────────────────────────────────────────
# GUARDAR CSV
# ─────────────────────────────────────────────
df = pd.DataFrame(resultados)
csv_path = 'equipo_X_resultados.csv'
df.to_csv(csv_path, index=False)
print(f"CSV guardado: {csv_path}")
print(df.to_string(index=False))


# ─────────────────────────────────────────────
# GRÁFICA DE CONVERGENCIA
# ─────────────────────────────────────────────
COLORES_BASE = {
    'inversion': '#1f77b4',   # azul
    'negacion' : '#ff7f0e',   # naranja
    'ranking'  : '#2ca02c',   # verde
}
ESTILOS = {0: 'solid', 2: 'dashed', 5: 'dotted'}
GROSOR  = {0: 2.0,     2: 1.8,      5: 1.6}

gens = np.arange(1, GENERACIONES + 1)

fig, ax = plt.subplots(figsize=(13, 8))

for tf in transformaciones:
    for k in elitismos:
        etiq = f"{nombres_tf[tf]}, k={k}"
        ax.plot(
            gens,
            historiales[(tf, k)],
            label=etiq,
            color=COLORES_BASE[tf],
            linestyle=ESTILOS[k],
            linewidth=GROSOR[k],
            alpha=0.85
        )

ax.set_xlabel('Generación', fontsize=13)
ax.set_ylabel('Mejor Fitness (valor Rastrigin)', fontsize=13)
ax.set_title(
    'Convergencia: Transformaciones de Fitness × Elitismo\n'
    'Función Rastrigin 10D — Semilla 42',
    fontsize=14, fontweight='bold'
)
ax.legend(loc='upper right', fontsize=9, framealpha=0.85)
ax.grid(True, alpha=0.3)
ax.set_yscale('log')     # escala logarítmica para apreciar diferencias
ax.set_xlim(1, GENERACIONES)

plt.tight_layout()
png_path = 'equipo_X_grafica.png'
plt.savefig(png_path, dpi=300, bbox_inches='tight')
plt.show()
print(f"Grafica guardada: {png_path}")
print("\n[DONE] Archivos generados:")
print(f"   - {csv_path}")
print(f"   - {png_path}")
