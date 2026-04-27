"""Responsabilidad única: Centralizar toda la configuración del sistema en un solo lugar. Ningún otro archivo debe tener valores hardcodeados."""

BALANCE_INICIAL = 10000

CSV_PATH = "Backtesting/data/precios.csv"

ESTRATEGIA = "MACD"

BREAKOUT_UMBRAL = 160.00

COMISION = 0

SMA_PERIODO_CORTO = 2
SMA_PERIODO_LARGO = 4

RSI_PERIODO = 5
RSI_SOBRECOMPRADO = 70
RSI_SOBREVENDIDO = 30

BOLLINGER_PERIODO = 5
BOLLINGER_DESVIACIONES = 2

MACD_PERIODO_CORTO = 3
MACD_PERIODO_LARGO = 5
MACD_PERIODO_SIGNAL = 2