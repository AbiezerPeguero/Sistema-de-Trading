# 📊 Sistema de Backtesting Simplificado

## 🧠 ¿Qué problema resuelve?

Antes de arriesgar capital real, un trader necesita saber si su estrategia funciona.
Este sistema permite simular una estrategia de trading sobre datos históricos,
medir su rendimiento y obtener métricas clave, todo sin exponer dinero real.

Está orientado a quienes quieren entender cómo se evalúa una estrategia
de forma sistemática, como primer paso hacia el trading algorítmico.

---

## 🎯 Contexto

Este proyecto nació como ejercicio práctico de Programación Orientada a Objetos,
aplicado a un dominio real: el análisis de estrategias de trading.

El objetivo no fue solo escribir código que funcione, sino diseñar un sistema
con arquitectura limpia, responsabilidades separadas y componentes reutilizables,
simulando cómo se estructura software en un entorno profesional.

---

## ⚙️ ¿Cómo funciona?

Datos históricos (CSV)
↓
DataLoader → carga y estructura los datos
↓
Estrategia → analiza cada día y genera una señal
↓
Backtester → simula las operaciones y lleva el balance
↓
Reporte → presenta las métricas finales

**Estrategia implementada — Media Móvil Simple:**

- Si el precio de hoy es mayor al de ayer → señal de compra
- Si el precio de hoy es menor al de ayer → señal de venta
- Si es el primer dato → sin señal

**Estrategia implementada — Breakout:**

- Si el precio supera un umbral definido → señal de compra
- Si el precio está por debajo → señal de venta

---

## 🧱 Arquitectura del sistema

El sistema está diseñado bajo el **Principio de Responsabilidad Única**:
cada módulo tiene una función específica y no interfiere con los demás.

| Módulo           | Responsabilidad                                          |
| ---------------- | -------------------------------------------------------- |
| `data_loader.py` | Carga y valida los datos históricos del CSV              |
| `estrategia.py`  | Define el contrato de estrategia y sus implementaciones  |
| `backtester.py`  | Ejecuta la simulación y registra cada operación          |
| `reporte.py`     | Presenta las métricas finales de rendimiento             |
| `decoradores.py` | Herramientas transversales: logging y medición de tiempo |

---

## 🧠 Decisiones de diseño

**Clases abstractas en `Estrategia`**
Se usó `ABC` para definir un contrato obligatorio. Cualquier estrategia nueva
debe implementar `generar_senal()`, garantizando que el sistema funcione
sin importar qué estrategia se use.

**Inyección de dependencia en `Backtester`**
El `Backtester` no crea su estrategia, la recibe como parámetro.
Esto permite cambiar de estrategia sin tocar el motor de simulación.

**Decoradores como herramientas transversales**
En lugar de repetir lógica de logging y medición en cada función,
se encapsuló en decoradores reutilizables que se aplican con una sola línea.

---

## 🗂️ Estructura del proyecto

```
backtesting/
├── data/
│ └── precios.csv # Datos históricos de precios
├── src/
│ ├── data_loader.py # Carga y validación de datos
│ ├── estrategia.py # Clase abstracta y estrategias concretas
│ ├── backtester.py # Motor de simulación
│ ├── reporte.py # Generación de métricas
│ └── decoradores.py # Logging y medición de tiempo
└── main.py # Punto de entrada del sistema
```

---

## ▶️ Cómo ejecutarlo

```bash
git clone https://github.com/AbiezerPeguero/Sistema-de-Trading
cd backtesting
python main.py
```

No requiere librerías externas. Solo Python 3.

---

## 📊 Ejemplo de salida

La funcion tardó 0.0 segundos
La operacion comenzo
Historial de operaciones:
{'fecha': '2024-01-03', 'precio_compra': 153.5, 'precio_venta': 149.8, 'resultado': -3.70}
{'fecha': '2024-01-05', 'precio_compra': 155.0, 'precio_venta': 152.3, 'resultado': -2.70}
Balance inicial: 10000.00
Balance final: 9977.40
Ganancia/Perdida: -22.60
Operaciones realizadas: 9
Operaciones ganadoras: 0
Win rate: 0.00%
La operacion finalizo

---

## 🚀 Mejoras futuras

- Implementar estrategias avanzadas: RSI, Medias Móviles, Bandas de Bollinger
- Conectar con APIs de datos reales (Yahoo Finance, Binance)
- Visualización de la curva de capital con `matplotlib`
- Cálculo de métricas de riesgo: drawdown máximo, ratio de Sharpe
- Optimización automática de parámetros por estrategia

---

## 👤 Autor

**Abiezer Peguero**

Enfocado en el desarrollo de sistemas aplicados al trading algorítmico
y la ciencia de datos. Este proyecto es parte de un camino hacia
la construcción de herramientas que conecten ingeniería de software
con análisis financiero cuantitativo.
