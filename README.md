Sistema de Backtesting Simplificado

¿Qué es este proyecto?
Un sistema que simula estrategias de trading con datos históricos. A partir de precios de cierre diarios, el sistema determina automáticamente cuándo comprar y cuándo vender, calcula las ganancias o pérdidas de cada operación y genera un reporte final con los resultados.

¿Cómo funciona?
El sistema compara el precio de cierre de cada día con el del día anterior. Si el precio subió, genera una señal de compra. Si bajó, genera una señal de venta. Al final muestra el balance, el número de operaciones realizadas y el win rate.

Tecnologías y conceptos aplicados.
Python
Programación Orientada a Objetos (POO)
Clases abstractas para definir contratos obligatorios entre clases
Principio de Responsabilidad Única (SRP): cada clase hace una sola cosa
Decoradores para medir tiempo de ejecución y loguear operaciones
Módulo csv para lectura de datos históricos

Estructura del proyecto.

```
backtesting/
├── data/
│ └── precios.csv
├── SRC/
│ ├── data_loader.py
│ ├── estrategia.py
│ ├── backtester.py
│ ├── reporte.py
│ └── decoradores.py
└── main.py
```

Cómo ejecutarlo.
Clona el repositorio
Asegúrate de tener Python instalado
Ejecuta desde la raíz del proyecto:
python main.py

Ejemplo de salida
La funcion tardó 0.0 segundos
La operacion comenzo
Historial de operaciones
{'fecha': '2024-01-03', 'precio_compra': 153.5, 'precio_venta': 149.8, 'resultado': -3.70}
Balance inicial: 10000
Balance final: 9977.40
Ganancia/Perdida: -22.60
Numero de operaciones realizadas: 9
Numero de operaciones ganadas: 0
Win rate: 0.00%
La operacion finalizo

Autor
Abiezer

Proyecto desarrollado como parte de mi formación en Python y POO,
aplicando principios de diseño de software en un contexto real de trading.
