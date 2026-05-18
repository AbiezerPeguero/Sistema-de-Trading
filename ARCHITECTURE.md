# 🏗️ ARCHITECTURE.md — Trading Backtesting Engine v1

Documentación técnica interna del sistema. Este archivo explica cómo está diseñado el proyecto por dentro,
qué decisiones de arquitectura se tomaron, por qué se tomaron, y cómo extender el sistema correctamente.

---

## 📐 Principio de diseño central

Todo el sistema está construido bajo el **Principio de Responsabilidad Única (SRP)** de los principios SOLID.
Cada archivo, clase y módulo tiene una sola razón para existir y una sola razón para cambiar.

Esto significa que si necesitas cambiar cómo se cargan los datos, solo tocas `data_loader.py`.
Si necesitas cambiar cómo se presentan los resultados en consola, solo tocas `reporte.py`.
Si necesitas cambiar cómo se ven los gráficos en la interfaz web, solo tocas `charts.py`.
Ningún módulo depende de los detalles internos de otro — solo de su interfaz pública.

La segunda fase del proyecto agregó una **capa de presentación desacoplada** (`app/` y `pages/`)
sin modificar ningún archivo del núcleo original. El núcleo no sabe que Streamlit existe.

---

## 🗺️ Mapa de dependencias

### Modo consola

```
config.py
    ↓
main.py
    ├── DataLoader / YahooFinanceFetcher  →  datos (lista de diccionarios)
    ├── strategy_factory                  →  estrategia (instancia de Estrategia)
    ├── Backtester                        →  historial, balance
    ├── Visualizacion                     →  gráficos PNG
    ├── Reporte                           →  salida en consola
    │       └── Metrics                  →  cálculos de métricas
    └── Optimizer                         →  optimization_results.csv
            ├── Backtester
            └── Metrics
```

`main.py` es el orquestador — no contiene lógica de negocio, solo conecta los módulos en el orden correcto.
`config.py` es la única fuente de verdad para todos los valores configurables del sistema en modo consola.

### Modo Streamlit

```
streamlit_app.py  (punto de entrada)
    ↓
pages/
    ├── 1_backtest.py
    │       ├── StrategyConfig     →  parámetros configurables por estrategia
    │       ├── BacktestRunner     →  orquesta datos + estrategia + backtester + métricas
    │       │       ├── YahooFinanceFetcher  →  datos
    │       │       ├── Backtester           →  historial, balance
    │       │       └── Metrics              →  métricas de rendimiento
    │       └── Charts             →  figuras interactivas de Plotly
    │
    ├── 2_optimizacion.py
    │       ├── StrategyConfig     →  parámetros configurables por estrategia
    │       ├── YahooFinanceFetcher →  datos
    │       └── Optimizer          →  grid search completo
    │
    └── 3_historial.py
            └── st.session_state   →  resultado guardado por 1_backtest.py
```

`BacktestRunner` es el orquestador de la capa web — equivale a `main.py` pero para Streamlit.
Los parámetros vienen del usuario en tiempo real, no de `config.py`.

---

## 📁 Descripción detallada de cada módulo

### `config.py`

**Responsabilidad:** Centralizar toda la configuración del sistema en modo consola.

Ningún otro archivo del núcleo tiene valores hardcodeados. Si un valor puede cambiar entre ejecuciones,
vive en `config.py`. Esto incluye el balance inicial, la ruta del CSV, la estrategia activa,
y todos los parámetros de cada estrategia.

Para cambiar la estrategia activa se modifica únicamente:

```python
ESTRATEGIA = "SmaCrossover"  # o "Rsi", "Bollinger", "MACD", "MediaMovil", "Breakout"
```

En modo Streamlit los parámetros vienen del usuario a través de la UI — `config.py` no interviene.

---

### `src/data_loader.py` — Clase `DataLoader`

**Responsabilidad:** Cargar el CSV local y devolver una lista de diccionarios.

Recibe la ruta en `__init__` y lanza `ValueError` inmediatamente si está vacía.
El método `cargar()` usa `csv.DictReader` para leer cada fila como diccionario
y convierte `precio_cierre` y `volumen` a `float`.

**Formato de salida garantizado:**

```python
[
    {"fecha": "2024-01-01", "precio_cierre": 150.0, "volumen": 1000000.0},
    {"fecha": "2024-01-02", "precio_cierre": 153.5, "volumen": 1200000.0},
    ...
]
```

Este formato es el contrato que todos los demás módulos esperan. Si cambias la fuente de datos,
el formato de salida debe mantenerse idéntico.

---

### `src/data_fetcher.py` — Clase `YahooFinanceFetcher`

**Responsabilidad:** Descargar datos históricos reales desde Yahoo Finance y devolverlos en el mismo formato que `DataLoader`.

Recibe `ticker` (símbolo del activo) y `periodo` (rango de tiempo) en `__init__`.
El método `descargar()` importa `yfinance` internamente para que el sistema no falle
si la librería no está instalada.

Usa `.iterrows()` de pandas para convertir el DataFrame en la lista de diccionarios
con el mismo formato que `DataLoader`. Esto garantiza que el resto del sistema
funciona igual sin importar la fuente de datos.

Es usado tanto por `main.py` (modo consola con `--ticker`) como por `BacktestRunner` y `2_optimizacion.py` (modo Streamlit).

**Uso desde terminal:**

```bash
python Backtesting/main.py --ticker AAPL
python Backtesting/main.py --ticker BTC-USD
```

Sin `--ticker`, el sistema usa automáticamente el CSV local.

---

### `src/strategies/__init__.py` — Clase abstracta `Estrategia`

**Responsabilidad:** Definir el contrato obligatorio que todas las estrategias deben cumplir.

```python
from abc import ABC, abstractmethod

class Estrategia(ABC):
    @abstractmethod
    def generar_senal(self, dato):
        pass
```

Usar `ABC` garantiza que ninguna estrategia puede instanciarse sin implementar `generar_senal()`.
Si alguien intenta crear una estrategia sin ese método, Python lanza un `TypeError` en tiempo de ejecución.

**Contrato del método `generar_senal(self, dato)`:**

- Recibe un diccionario con al menos la clave `"precio_cierre"` (y opcionalmente `"fecha"`, `"volumen"`)
- Devuelve exactamente uno de estos tres valores: `"comprar"`, `"vender"`, o `None`
- No ejecuta operaciones, no modifica el balance, no guarda historial
- Puede guardar estado interno (precio anterior, lista de precios acumulados)

---

### `src/__init__.py`

**Responsabilidad:** Vacío intencionalmente. Su presencia convierte `src/` en un paquete Python
y habilita los imports con prefijo `src.` en todo el sistema, como `from src.backtester import Backtester`.
Sin este archivo, todos los imports del proyecto fallarían.

---

### `src/strategies/*.py` — Estrategias concretas

**Responsabilidad:** Analizar cada precio y emitir una señal. Nada más.

Cada estrategia vive en su propio archivo y hereda de `Estrategia`.
Todas implementan `generar_senal(self, dato)` con su propia lógica financiera.

| Archivo            | Clase                    | Lógica                                   |
| ------------------ | ------------------------ | ---------------------------------------- |
| `media_movil.py`   | `EstrategiaMediaMovil`   | Compara precio de hoy con precio de ayer |
| `breakout.py`      | `EstrategiaBreakout`     | Compara precio contra un umbral fijo     |
| `sma_crossover.py` | `EstrategiaSmaCrossover` | Cruza dos SMAs de períodos distintos     |
| `rsi.py`           | `EstrategiaRsi`          | Calcula el RSI y opera en zonas extremas |
| `bollinger.py`     | `EstrategiaBollinger`    | Opera cuando el precio rompe las bandas  |
| `macd.py`          | `EstrategiaMACD`         | Cruza la MACD line con la signal line    |

**Estado interno:** Las estrategias que necesitan memoria (SMA, RSI, Bollinger, MACD)
acumulan precios en `self.precios`. Este estado se reinicia cada vez que se crea una nueva instancia,
lo que es crítico en el `Optimizer` — cada combinación de parámetros usa una instancia nueva.

---

### `src/strategy_factory.py` — Función `crear_estrategia()`

**Responsabilidad:** Leer `config.ESTRATEGIA` y devolver la instancia correcta. Solo se usa en modo consola.

Es el único lugar del núcleo que decide qué estrategia instanciar para `main.py`.
En modo Streamlit esta responsabilidad la tiene `_mapa_estrategia` dentro de `BacktestRunner`
y `2_optimizacion.py`, porque los parámetros vienen del usuario y no de `config.py`.

Lanza `ValueError` si el valor de `config.ESTRATEGIA` no coincide con ningún caso conocido,
lo que da un mensaje de error claro en lugar de un fallo silencioso.

---

### `src/backtester.py` — Clase `Backtester`

**Responsabilidad:** Recibir datos y una estrategia, simular las operaciones y registrar cada resultado.

Recibe la estrategia por inyección de dependencia — no la crea internamente.
Esto permite que cualquier objeto que implemente `generar_senal()` funcione como estrategia,
incluyendo las estrategias falsas usadas en los tests.

**Estado interno:**

- `posicion` → `False` si no hay operación abierta, `True` si hay una activa
- `precio_compra` → precio al que se compró, `None` si no hay posición abierta
- `historial` → lista de operaciones cerradas
  **Ciclo de una operación:**

1. Estrategia devuelve `"comprar"` y `posicion == False` → abre posición, guarda `precio_compra`
2. Estrategia devuelve `"vender"` y `posicion == True` → cierra posición, calcula ganancia/pérdida, guarda en historial
   **Formato de cada entrada en el historial:**

```python
{
    "fecha": "2024-01-07",
    "precio_compra": 158.0,
    "precio_venta": 156.5,
    "resultado": -1.5
}
```

El método `ejecutar()` está decorado con `@decoradores.medir_tiempo`.

---

### `src/metrics.py` — Clase `Metrics`

**Responsabilidad:** Recibir el historial y calcular métricas de rendimiento. No imprime nada.

Todos los métodos son puros — reciben datos, calculan y devuelven un valor.
No tienen efectos secundarios.

| Método                                               | Descripción                                        |
| ---------------------------------------------------- | -------------------------------------------------- |
| `mejor_trade()`                                      | Resultado más alto del historial                   |
| `peor_trade()`                                       | Resultado más bajo del historial                   |
| `ganancia_promedio()`                                | Promedio de operaciones con resultado > 0          |
| `perdida_promedio()`                                 | Promedio absoluto de operaciones con resultado < 0 |
| `retorno_porcentual(balance_inicial, balance_final)` | Porcentaje de ganancia o pérdida total             |
| `profit_factor()`                                    | Ratio ganancias totales / pérdidas totales         |
| `max_drawdown()`                                     | Mayor caída consecutiva desde un punto alto        |
| `expectancy()`                                       | Ganancia o pérdida esperada promedio por operación |
| `resumen(balance_inicial, balance_final)`            | Diccionario con todas las métricas                 |

Todos los métodos devuelven `None` o `0` si el historial está vacío, nunca lanzan excepciones.
`profit_factor()` devuelve `None` cuando es matemáticamente indefinido — la UI de Streamlit
maneja este caso mostrando `"N/A"` en lugar del valor.

---

### `src/reporte.py` — Clase `Reporte`

**Responsabilidad:** Presentar los resultados en consola. No calcula nada. Solo se usa en modo consola.

Recibe `historial`, `balance_inicial` y `balance_final` ya procesados por el `Backtester`.
Crea internamente un objeto `Metrics` para acceder a las métricas avanzadas.

El método `mostrar_resultados()` está decorado con `@decoradores.log_operacion`.

---

### `src/visualizacion.py` — Clase `Visualizacion`

**Responsabilidad:** Generar los 4 gráficos PNG. No calcula métricas, no imprime texto. Solo se usa en modo consola.

Usa `matplotlib.pyplot` para generar y guardar los gráficos en `output/charts/`.
El método privado `_calcular_balance_curva()` es reutilizado por `grafico_curva_capital()`
y `grafico_drawdown()` para no repetir la misma lógica.

Para posicionar correctamente los puntos de compra y venta en `grafico_precio_semanales()`,
construye un diccionario `fecha_a_indice` que mapea cada fecha a su posición en el eje X:

```python
fecha_a_indice = {datos["fecha"]: i for i, datos in enumerate(self.datos)}
```

En modo Streamlit esta responsabilidad la tiene `Charts` en `app/charts.py`,
que produce figuras interactivas de Plotly en lugar de imágenes PNG estáticas.

---

### `src/optimizer.py` — Clase `Optimizer`

**Responsabilidad:** Probar todas las combinaciones de parámetros y guardar el ranking en CSV.

Recibe la **clase** de la estrategia (no una instancia) para poder crear instancias nuevas
por cada combinación. Usa `itertools.product` para generar el producto cartesiano
de todos los rangos de parámetros (Grid Search).

Por cada combinación:

1. Instancia la estrategia con esos parámetros
2. Crea un `Backtester` nuevo (es crítico que sea nuevo para resetear el estado)
3. Ejecuta el backtest
4. Calcula métricas
5. Guarda el resultado en la lista
   Ordena los resultados por `retorno_porcentual` de mayor a menor y los guarda en
   `output/optimization_results.csv`.

**Nota importante:** Cada combinación debe usar una instancia nueva de `Backtester`
y una instancia nueva de la estrategia. Reutilizar instancias contaminaría el estado interno
(especialmente `self.precios` en las estrategias que acumulan datos).

---

### `src/decoradores.py`

**Responsabilidad:** Herramientas transversales de logging y medición. No pertenecen a ningún módulo específico.

| Decorador       | Función                                                |
| --------------- | ------------------------------------------------------ |
| `medir_tiempo`  | Cronometra la ejecución de cualquier función           |
| `log_operacion` | Imprime cuando una operación comienza y termina        |
| `validar_lista` | Verifica que una lista no esté vacía antes de ejecutar |

Todos usan `*args, **kwargs` para ser compatibles con cualquier función del sistema.
En modo Streamlit el output de `medir_tiempo` aparece en la terminal del servidor, no en la UI.

---

### `app/strategy_config.py` — Clase `StrategyConfig`

**Responsabilidad:** Ser el catálogo de parámetros configurables de cada estrategia para la UI.

Define un diccionario interno `_config` donde cada clave es el nombre de la estrategia
y el valor es una lista de diccionarios — uno por parámetro. Cada parámetro tiene:

```python
{
    "nombre": "periodo",    # nombre exacto del kwarg que recibe la estrategia
    "tipo": "int",          # "int" o "float" — determina el widget y el rango
    "min": 5,
    "max": 30,
    "default": 14,
    "label": "Período RSI"  # texto que ve el usuario en la UI
}
```

`MediaMovil` tiene lista vacía `[]` porque no recibe parámetros.
`tipo` determina si se usa `range()` o una lista de floats en la página de optimización.

**Métodos:**

- `obtener_params(nombre_estrategia)` → devuelve la lista de parámetros de esa estrategia
- `nombres_estrategias()` → devuelve la lista de nombres para poblar el `selectbox` de la UI

---

### `app/runner.py` — Clase `BacktestRunner`

**Responsabilidad:** Recibir los parámetros de la UI, orquestar la ejecución completa del backtest
usando el núcleo existente, y devolver un diccionario de resultados que Streamlit puede consumir.

Es el equivalente a `main.py` para el modo Streamlit — no contiene lógica de negocio,
solo conecta los módulos del núcleo en el orden correcto.

**Métodos privados:**

- `_obtener_datos()` → instancia `YahooFinanceFetcher` y valida que los datos no sean `None`
- `_crear_estrategia()` → usa un mapa interno para instanciar la estrategia con `**params_estrategia`
  El mapa interno existe aquí y no en `strategy_factory.py` porque los parámetros vienen
  del usuario en tiempo real — no de `config.py`.

**Diccionario de resultados que devuelve `ejecutar()`:**

```python
{
    "historial": [...],        # lista de operaciones cerradas
    "datos": [...],            # datos históricos descargados
    "balance_inicial": 10000,
    "balance_final": 10523.4,
    "metricas": {...},         # diccionario de Metrics.resumen()
    "win_rate": 0.6,
    "n_operaciones": 15
}
```

Este diccionario es el contrato entre `runner.py` y las páginas de Streamlit.
`Charts` lo recibe completo, `3_historial.py` lo lee desde `session_state`.

---

### `app/charts.py` — Clase `Charts`

**Responsabilidad:** Recibir el diccionario de resultados del runner y devolver figuras de Plotly
listas para renderizar con `st.plotly_chart()`. No calcula métricas, no imprime texto.

Es el equivalente a `Visualizacion` para el modo Streamlit — produce gráficos interactivos
con zoom, hover y tooltips en lugar de imágenes PNG estáticas.

| Método                    | Descripción                                                           |
| ------------------------- | --------------------------------------------------------------------- |
| `equity_curve()`          | Curva de capital acumulado operación por operación                    |
| `drawdown()`              | Área de caída del balance desde el pico más alto, rellena en rojo     |
| `histograma_resultados()` | Distribución de ganancias y pérdidas por operación                    |
| `precio_con_senales()`    | Línea de precios con puntos de compra (verde) y venta (rojo) marcados |

`precio_con_senales()` usa el mismo truco de `fecha_a_indice` que `Visualizacion`:

```python
fecha_a_indice = {d["fecha"]: i for i, d in enumerate(self.datos)}
```

Esto ubica los puntos de compra y venta exactamente donde ocurrieron en la línea de tiempo.

---

### `streamlit_app.py`

**Responsabilidad:** Ser el punto de entrada de la aplicación Streamlit. Solo contiene la portada.

Streamlit detecta automáticamente la carpeta `pages/` y construye el menú de navegación lateral.
No ejecuta backtests ni importa módulos del núcleo.

---

### `pages/1_backtest.py`

**Responsabilidad:** Configuración interactiva, ejecución del backtest y visualización de resultados.

El sidebar contiene todos los controles de configuración. El loop de parámetros genera
un `slider` por cada parámetro de la estrategia seleccionada usando `StrategyConfig`.

Al ejecutar, guarda el resultado en `st.session_state["resultado"]` para que
`3_historial.py` pueda acceder sin volver a ejecutar el backtest.

---

### `pages/2_optimizacion.py`

**Responsabilidad:** Grid search interactivo con ranking de combinaciones de parámetros.

A diferencia de `1_backtest.py` donde el usuario elige un valor por parámetro,
aquí define mínimo, máximo y paso — el sistema prueba todas las combinaciones posibles.

Para parámetros `int` usa `range()`. Para parámetros `float` construye la lista manualmente:

```python
valores = [round(min_value + paso * i, 2) for i in range(int((max_value - min_value) / paso))]
```

Esto es necesario porque `range()` no acepta flotantes.

---

### `pages/3_historial.py`

**Responsabilidad:** Mostrar la tabla completa del historial de operaciones de forma navegable.

Lee el resultado desde `st.session_state["resultado"]` que guardó `1_backtest.py`.
Si no existe, muestra un aviso indicando que primero se debe ejecutar un backtest.

Convierte el historial a DataFrame de pandas para mostrarlo con `st.dataframe()`,
que permite ordenar y filtrar columnas directamente en la UI.

---

### `tests/`

**Responsabilidad:** Verificar que cada módulo funciona correctamente con datos controlados.

Los tests no dependen del CSV ni de internet. Crean sus propios datos dentro de cada función
para que sean completamente reproducibles e independientes del entorno.

| Archivo              | Qué verifica                                                                  |
| -------------------- | ----------------------------------------------------------------------------- |
| `test_loader.py`     | Que `DataLoader` carga correctamente y lanza errores apropiados               |
| `test_backtester.py` | Que el `Backtester` registra operaciones y actualiza el balance correctamente |
| `test_metrics.py`    | Que cada métrica devuelve el valor correcto con datos conocidos               |

`test_backtester.py` usa una clase auxiliar `EstrategiaFalsa` que recibe una lista de señales
predefinidas y las devuelve una por una. Esto permite controlar exactamente qué hace
el backtester sin depender de ninguna estrategia real.

Para ejecutar todos los tests:

```bash
pytest Backtesting/tests/ -v
```

El archivo `conftest.py` en la raíz de `Backtesting/` agrega esa carpeta al path de Python
para que los imports funcionen correctamente desde cualquier directorio.

---

## 🔌 Cómo agregar una nueva estrategia

Sigue estos 6 pasos en orden — los primeros 4 son para el modo consola, los últimos 2 para Streamlit:

**Paso 1 — Crear el archivo de la estrategia**

Crea `src/strategies/nombre_estrategia.py` con esta estructura:

```python
from src.strategies import Estrategia

class EstrategiaNombre(Estrategia):
    def __init__(self, parametro1, parametro2):
        self.parametro1 = parametro1
        self.parametro2 = parametro2
        self.precios = []  # si necesita acumular precios

    def generar_senal(self, dato):
        # Tu lógica aquí
        # Devuelve "comprar", "vender" o None
        pass
```

**Paso 2 — Agregar parámetros en `config.py`**

```python
NOMBRE_PARAMETRO1 = valor1
NOMBRE_PARAMETRO2 = valor2
```

**Paso 3 — Registrar en `strategy_factory.py`**

```python
from src.strategies.nombre_estrategia import EstrategiaNombre

elif estrategia == "Nombre":
    return EstrategiaNombre(
        parametro1=config.NOMBRE_PARAMETRO1,
        parametro2=config.NOMBRE_PARAMETRO2
    )
```

**Paso 4 — Activar en `config.py`**

```python
ESTRATEGIA = "Nombre"
```

**Paso 5 — Registrar en `app/strategy_config.py`**

Agrega la estrategia al diccionario `_config` con sus parámetros:

```python
"Nombre": [
    {"nombre": "parametro1", "tipo": "int", "min": 2, "max": 50, "default": 10, "label": "Parámetro 1"},
    {"nombre": "parametro2", "tipo": "float", "min": 0.5, "max": 3.0, "default": 1.5, "label": "Parámetro 2"}
]
```

**Paso 6 — Registrar en `_mapa_estrategia` de `runner.py` y `2_optimizacion.py`**

```python
from src.strategies.nombre_estrategia import EstrategiaNombre

_mapa_estrategia = {
    ...
    "Nombre": EstrategiaNombre
}
```

---

## 🔌 Cómo agregar una nueva fuente de datos

Crea una clase en `src/` que siga el mismo contrato que `DataLoader`:

- Método `descargar()` o `cargar()` sin parámetros
- Devuelve una lista de diccionarios con las claves `"fecha"`, `"precio_cierre"`, `"volumen"`
  Luego agrégala como opción en el bloque `if args.ticker` de `main.py` para modo consola,
  y en `_obtener_datos()` de `runner.py` para modo Streamlit si aplica.

---

## ⚠️ Decisiones técnicas y sus razones

**¿Por qué `profit_factor()` devuelve `None` en lugar de `0` cuando no hay ganancias?**

Porque `0` implicaría que el ratio es cero, lo cual es matemáticamente incorrecto.
Si no hay ganancias, el ratio es indefinido — no existe. `None` comunica eso con precisión.
La UI de Streamlit maneja este caso con el operador ternario mostrando `"N/A"`.

**¿Por qué `yfinance` se importa dentro del método y no en la cabecera del archivo?**

Para que el sistema no falle al importar `data_fetcher.py` si `yfinance` no está instalado.
Si el usuario usa solo el CSV local, nunca necesita `yfinance` y no debería recibir un error por eso.

**¿Por qué el `Optimizer` recibe la clase de la estrategia y no una instancia?**

Porque necesita crear una instancia nueva por cada combinación de parámetros.
Si recibiera una instancia, no podría cambiar sus parámetros entre combinaciones.

**¿Por qué los decoradores usan `\*args, **kwargs`?\*\*

Para ser compatibles con cualquier función del sistema, independientemente de sus parámetros.
Sin `*args, **kwargs`, cada decorador solo funcionaría con funciones de una firma específica.

**¿Por qué cada estrategia vive en su propio archivo?**

Para cumplir el Principio de Responsabilidad Única y el Principio Abierto/Cerrado (OCP).
Agregar una estrategia nueva no requiere modificar ningún archivo existente de estrategias —
solo crear uno nuevo. Esto evita romper código que ya funciona.

**¿Por qué `BacktestRunner` tiene su propio `_mapa_estrategia` en lugar de usar `strategy_factory.py`?**

Porque `strategy_factory.py` lee los parámetros de `config.py` — valores fijos hardcodeados.
`BacktestRunner` necesita crear estrategias con los parámetros que el usuario configuró en tiempo real.
Son dos responsabilidades distintas que no deben mezclarse.

**¿Por qué `Charts` usa Plotly y no Matplotlib como `Visualizacion`?**

Porque Plotly produce gráficos interactivos que Streamlit renderiza nativamente con zoom, hover y tooltips.
Matplotlib produce imágenes PNG estáticas — útiles para guardar archivos pero no para una UI web.
Ambas clases coexisten porque cada una sirve a su propio contexto de uso.

**¿Por qué el resultado del backtest se guarda en `session_state`?**

Porque Streamlit re-ejecuta el script completo de arriba a abajo cada vez que el usuario
interactúa con la UI. Sin `session_state`, el resultado se perdería al navegar entre páginas.
Guardarlo permite que `3_historial.py` acceda al resultado sin volver a ejecutar el backtest.

---

## 📦 Dependencias externas

| Librería     | Versión mínima | Uso                                       |
| ------------ | -------------- | ----------------------------------------- |
| `streamlit`  | 1.57.0         | Interfaz web interactiva                  |
| `plotly`     | cualquiera     | Gráficos interactivos en la interfaz web  |
| `pandas`     | cualquiera     | Conversión de historial a tabla navegable |
| `matplotlib` | cualquiera     | Generación de gráficos PNG (modo consola) |
| `yfinance`   | 1.3.0          | Descarga de datos históricos reales       |
| `pytest`     | cualquiera     | Testing unitario                          |

Todo lo demás usa la **librería estándar de Python**: `csv`, `itertools`, `statistics`, `argparse`, `tempfile`, `time`, `abc`.

Instalación:

```bash
pip install matplotlib yfinance pytest streamlit plotly pandas
```

---

## 🧪 Convenciones del proyecto

- Nombres de clases en `PascalCase`: `EstrategiaRsi`, `YahooFinanceFetcher`, `BacktestRunner`
- Nombres de funciones y métodos en `snake_case`: `generar_senal`, `mostrar_resultados`, `equity_curve`
- Métodos privados con guión bajo: `_calcular_balance_curva`, `_obtener_datos`, `_crear_estrategia`
- Cada archivo empieza con un docstring que describe su responsabilidad única
- Los comentarios explican el **por qué**, no el **qué** — el código ya dice qué hace
- Todos los valores numéricos configurables del modo consola viven en `config.py`, nunca hardcodeados
- Los parámetros del modo Streamlit vienen del usuario a través de `StrategyConfig`, nunca de `config.py`
