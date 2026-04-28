# 📊 Trading Backtesting Engine v1

## 🧠 ¿Qué problema resuelve?

Antes de arriesgar capital real, un trader necesita saber si su estrategia funciona.
Este sistema permite simular cualquier estrategia de trading sobre datos históricos reales o locales,
medir su rendimiento con métricas profesionales, visualizar los resultados y optimizar los parámetros automáticamente,
todo sin exponer dinero real.

Está orientado a quienes quieren entender cómo se evalúa una estrategia de forma sistemática,
como primer paso hacia el trading algorítmico profesional.

---

## 🎯 Contexto

Este proyecto nació como ejercicio práctico de Programación Orientada a Objetos aplicado a un dominio real:
el análisis cuantitativo de estrategias de trading.

El objetivo no fue solo escribir código que funcione, sino diseñar un sistema con arquitectura limpia,
responsabilidades separadas y componentes reutilizables, simulando cómo se estructura software en un entorno profesional.

Cada módulo aplica principios SOLID, en especial el Principio de Responsabilidad Única:
ningún archivo hace más de una cosa.

---

## ⚙️ ¿Cómo funciona?

```
Datos históricos (CSV local o Yahoo Finance)
            ↓
    DataLoader / YahooFinanceFetcher → carga y estructura los datos
            ↓
    StrategyFactory → selecciona la estrategia configurada
            ↓
    Estrategia → analiza cada día y genera una señal (comprar / vender / None)
            ↓
    Backtester → simula las operaciones y lleva el balance
            ↓
    Metrics → calcula métricas de rendimiento
            ↓
    Visualizacion → genera 4 gráficos en output/charts/
            ↓
    Reporte → presenta los resultados en consola
            ↓
    Optimizer → prueba todas las combinaciones de parámetros y guarda el ranking
```

---

## 📈 Estrategias disponibles

| Estrategia         | Clave en config | Descripción                                                         |
| ------------------ | --------------- | ------------------------------------------------------------------- |
| Media Móvil Simple | `MediaMovil`    | Compra si el precio sube respecto al día anterior, vende si baja    |
| Breakout           | `Breakout`      | Compra si el precio supera un umbral fijo, vende si está por debajo |
| SMA Crossover      | `SmaCrossover`  | Compra cuando la SMA rápida cruza por encima de la SMA lenta        |
| RSI                | `Rsi`           | Compra en zona de sobrevendido (<30), vende en sobrecomprado (>70)  |
| Bollinger Breakout | `Bollinger`     | Opera cuando el precio rompe las bandas de Bollinger                |
| MACD Crossover     | `MACD`          | Compra cuando la MACD line cruza por encima de la signal line       |

Para cambiar de estrategia, modifica `ESTRATEGIA` en `config.py`:

```python
ESTRATEGIA = "SmaCrossover"  # Cambia por cualquier clave de la tabla
```

---

## 📊 Métricas calculadas

El sistema calcula automáticamente las siguientes métricas tras cada simulación:

| Métrica                     | Descripción                                                 |
| --------------------------- | ----------------------------------------------------------- |
| Win Rate                    | Porcentaje de operaciones ganadoras                         |
| Retorno porcentual          | Ganancia o pérdida total respecto al capital inicial        |
| Mejor / Peor trade          | Operación más rentable y más costosa                        |
| Ganancia / Pérdida promedio | Promedio de operaciones ganadoras y perdedoras por separado |
| Profit Factor               | Ratio entre ganancias totales y pérdidas totales            |
| Max Drawdown                | Mayor caída consecutiva del balance desde un punto alto     |
| Expectancy                  | Ganancia o pérdida esperada promedio por operación          |

---

## 📉 Visualizaciones

El sistema genera automáticamente 4 gráficos en `output/charts/`:

**Curva de Capital** — Evolución del balance a lo largo de las operaciones.
![Curva de Capital](output/charts/curva_capital.png)

**Histograma de Resultados** — Distribución de ganancias y pérdidas por operación.
![Histograma de Resultados](output/charts/histograma_resultados.png)

**Precios y Señales** — Línea de precios con puntos de compra y venta marcados.
![Precios y Señales](output/charts/precios_semanales.png)

**Drawdown** — Área de caída del balance desde el punto más alto.
![Drawdown](output/charts/drawdown.png)

---

## 🔧 Optimización de parámetros

El `Optimizer` prueba automáticamente todas las combinaciones posibles de parámetros (Grid Search)
y guarda el ranking en `output/optimization_results.csv`.

Ejemplo de uso en `main.py`:

```python
optimizer = Optimizer(
    estrategia_clase=EstrategiaSmaCrossover,
    datos=datos,
    balance_inicial=config.BALANCE_INICIAL,
    parametros={
        "periodo_corto": [2, 3, 5],
        "periodo_largo": [4, 5, 10]
    }
)
optimizer.optimizar()
```

Resultado en `optimization_results.csv`:

```
params,retorno_porcentual,win_rate
"{'periodo_corto': 2, 'periodo_largo': 5}",0.43,0.67
"{'periodo_corto': 2, 'periodo_largo': 4}",0.10,0.50
"{'periodo_corto': 3, 'periodo_largo': 10}",0.08,1.00
...
```

---

## 🧱 Arquitectura del sistema

El sistema aplica el **Principio de Responsabilidad Única** en cada módulo:

| Módulo                   | Responsabilidad                                                             |
| ------------------------ | --------------------------------------------------------------------------- |
| `config.py`              | Centraliza toda la configuración. Ningún archivo tiene valores hardcodeados |
| `data_loader.py`         | Carga y valida el CSV local. Devuelve lista de diccionarios                 |
| `data_fetcher.py`        | Descarga datos reales desde Yahoo Finance con el mismo formato              |
| `strategies/__init__.py` | Define la clase abstracta `Estrategia` con el contrato obligatorio          |
| `strategies/*.py`        | Cada estrategia en su propio archivo. Solo analiza precios y emite señales  |
| `strategy_factory.py`    | Decide qué estrategia instanciar según la configuración                     |
| `backtester.py`          | Simula las operaciones y registra el historial                              |
| `metrics.py`             | Calcula todas las métricas de rendimiento. No imprime nada                  |
| `reporte.py`             | Presenta los resultados en consola. No calcula nada                         |
| `visualizacion.py`       | Genera los 4 gráficos. No calcula métricas ni imprime texto                 |
| `optimizer.py`           | Prueba combinaciones de parámetros y guarda el ranking en CSV               |
| `decoradores.py`         | Herramientas transversales: logging y medición de tiempo                    |

### Decisiones de diseño

**Clases abstractas en `Estrategia`**
Se usó `ABC` para definir un contrato obligatorio. Cualquier estrategia nueva debe implementar `generar_senal()`,
garantizando que el sistema funcione sin importar qué estrategia se use.

**Inyección de dependencia en `Backtester`**
El `Backtester` no crea su estrategia, la recibe como parámetro.
Esto permite cambiar de estrategia sin tocar el motor de simulación.

**Decoradores como herramientas transversales**
En lugar de repetir lógica de logging y medición en cada función,
se encapsuló en decoradores reutilizables que se aplican con una sola línea.

**Factory Pattern en `strategy_factory.py`**
Ningún otro archivo decide qué estrategia usar. Toda esa lógica vive en un solo lugar.

---

## 🗂️ Estructura del proyecto

```
Backtesting/
├── data/
│   └── precios.csv
├── src/
│   ├── strategies/
│   │   ├── __init__.py          ← clase abstracta Estrategia
│   │   ├── media_movil.py
│   │   ├── breakout.py
│   │   ├── sma_crossover.py
│   │   ├── rsi.py
│   │   ├── bollinger.py
│   │   └── macd.py
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_fetcher.py
│   ├── backtester.py
│   ├── reporte.py
│   ├── decoradores.py
│   ├── strategy_factory.py
│   ├── metrics.py
│   ├── visualizacion.py
│   └── optimizer.py
├── tests/
│   ├── test_loader.py
│   ├── test_backtester.py
│   └── test_metrics.py
├── output/
│   └── charts/
│       ├── curva_capital.png
│       ├── histograma_resultados.png
│       ├── precios_semanales.png
│       └── drowdown.png
├── conftest.py
├── config.py
├── main.py
└── README.md
```

---

## 🛠️ Tecnologías utilizadas

| Tecnología                                               | Uso                                 |
| -------------------------------------------------------- | ----------------------------------- |
| Python 3.14                                              | Lenguaje principal                  |
| `matplotlib`                                             | Generación de gráficos              |
| `yfinance`                                               | Descarga de datos históricos reales |
| `pytest`                                                 | Testing unitario                    |
| `csv`, `itertools`, `statistics`, `argparse`, `tempfile` | Librería estándar de Python         |

---

## ▶️ Cómo ejecutarlo

**Con datos locales (CSV):**

```bash
python Backtesting/main.py
```

**Con datos reales de Yahoo Finance:**

```bash
python Backtesting/main.py --ticker AAPL
python Backtesting/main.py --ticker BTC-USD
python Backtesting/main.py --ticker MSFT
```

El ticker puede ser cualquier símbolo válido de Yahoo Finance — acciones, ETFs, criptomonedas, índices.

**Ejecutar los tests:**

```bash
pytest Backtesting/tests/ -v
```

**Instalar dependencias:**

```bash
pip install matplotlib yfinance pytest
```

---

## 📦 Ejemplo de salida

```
La funcion tardó 0.0001 segundos
La operacion comenzo
Historial de operaciones
{'fecha': '2026-02-05', 'precio_compra': 269.76, 'precio_venta': 275.65, 'resultado': 5.9}
{'fecha': '2026-02-20', 'precio_compra': 264.35, 'precio_venta': 264.58, 'resultado': 0.2}
...
Balance inicial: 10000
Balance final: 10001.11
Ganancia/Perdida: 1.11
Numero de operaciones realizadas: 10
Numero de operaciones ganadas: 6
Win rate: 60.00%
--- Metricas Avanzadas ---
mejor_trade: 6.6
peor_trade: -6.2
ganancia_promedio: 3.02
perdida_promedio: 4.27
retorno_porcentual: 0.01
profit_factor: 1.06
max_drawdown: 15.4
expectancy: 0.1
La operacion finalizo
```

---

## 🚀 Próximos pasos

- Conectar con APIs adicionales: Binance, Alpha Vantage
- Implementar EMA real en lugar de SMA aproximada para MACD
- Agregar ratio de Sharpe como métrica de riesgo ajustado
- Interfaz web con Flask o Streamlit para visualizar resultados en el navegador
- Backtesting con múltiples activos simultáneos
- Exportar reporte completo a PDF

---

## 👤 Autor

**Abiezer Peguero**

Enfocado en el desarrollo de sistemas aplicados al trading algorítmico y la ciencia de datos.
Este proyecto es parte de un camino hacia la construcción de herramientas que conecten
ingeniería de software con análisis financiero cuantitativo.

Para documentación técnica interna ver [ARCHITECTURE.md](ARCHITECTURE.md)

[![GitHub](https://img.shields.io/badge/GitHub-AbiezerPeguero-181717?style=flat&logo=github)](https://github.com/AbiezerPeguero/Sistema-de-Trading)
