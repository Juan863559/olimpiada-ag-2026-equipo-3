# Decisiones Técnicas — Sesión 1: El Optimizador Perfecto

## Función Objetivo: Rastrigin 10D

Se optó por implementar la función de Rastrigin en 10 dimensiones tal como se especificó.
- **Dominio**: x ∈ [-5.12, 5.12]^10
- **Óptimo global**: f(0, 0, ..., 0) = 0
- Es una función multimodal con numerosos mínimos locales, lo que la hace un benchmark desafiante para algoritmos evolutivos.

---

## Parámetros del AG (fijos según el reto)

| Parámetro | Valor |
|---|---|
| Tamaño de población | 50 |
| Generaciones | 100 |
| Longitud del cromosoma | 10 |
| Probabilidad de cruzamiento | 0.8 |
| Probabilidad de mutación | 0.01 |
| Selección | Torneo (k=3) |
| Cruzamiento | Un punto |
| Mutación | Uniforme (valores reales) |
| Semilla aleatoria | 42 |

---

## Decisiones en las Transformaciones de Fitness

### Inversión Simple
- Fórmula: `f = 1 / (1 + objetivo)`
- Siempre produce valores positivos en (0, 1].
- Simple y eficiente; el valor de fitness 1.0 corresponde al óptimo global exacto.

### Negación con Desplazamiento
- Fórmula: `f = max(0, c_max - objetivo)`, donde `c_max = max(población) × 1.1`
- `c_max` se recalcula en cada generación para adaptarse a la evolución de la población.
- El factor 1.1 garantiza que ningún individuo tenga fitness cero (a excepción de posibles valores muy extremos).

### Ranking Lineal
- Asigna fitness basado en la posición en el ranking en lugar del valor absoluto.
- Presión selectiva `sp = 1.5` (valor recomendado entre 1 y 2).
- Reduce el efecto de individuos con valores extremos (muy buenos o muy malos), lo que puede mejorar la diversidad.

---

## Observación clave: equivalencia de transformaciones

Bajo la configuración experimental de este reto (misma semilla, mismo operador de selección por torneo), las **3 transformaciones producen resultados idénticos**. Esto ocurre porque el torneo de selección opera sobre el **orden relativo** de los individuos, no sobre sus valores absolutos de fitness. Las 3 transformaciones preservan ese orden relativo (son funciones monótonas crecientes del fitness original), por lo que el comportamiento del AG es el mismo.

---

## Decisiones en el Elitismo

- **k=0**: Sin elitismo. Toda la nueva generación proviene de los operadores genéticos. Mayor exploración, pero riesgo de perder buenas soluciones.
- **k=2**: Elitismo bajo. Se preservan los 2 mejores individuos. Balance entre exploración y explotación.
- **k=5**: Elitismo moderado (10% de la población). Mayor presión hacia convergencia. Puede reducir la diversidad, pero garantiza preservar buenas soluciones.

El elitismo se implementa **reemplazando los k peores** individuos de la nueva generación con los k mejores de la generación anterior, garantizando que el mejor fitness nunca empeore.

---

## Métrica de Diversidad

Se definió la diversidad como la **desviación estándar del fitness** (usando transformación inversión) en la generación final. Un valor cercano a 0 indica convergencia prematura (baja diversidad). Valores más altos indican mayor exploración activa.

---

## Herramientas utilizadas

- **Python 3.x**
- **numpy**: operaciones vectoriales y generación aleatoria
- **matplotlib**: gráficas de convergencia
- **pandas**: generación y exportación del CSV de resultados
