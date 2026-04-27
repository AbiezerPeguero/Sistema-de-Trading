import config
from src.strategies.media_movil import EstrategiaMediaMovil
from src.strategies.breakout import EstrategiaBreakout
from src.strategies.sma_crossover import EstrategiaSmaCrossover
from src.strategies.rsi import EstrategiaRsi
from src.strategies.bollinger import EstrategiaBollinger
from src.strategies.macd import EstrategiaMACD

# Leer la configuración y devolver el objeto de estrategia correcto. Nadie más decide qué estrategia usar.
def crear_estrategia():
    estrategia = config.ESTRATEGIA
    if estrategia == "MediaMovil":
        return EstrategiaMediaMovil()
    elif estrategia == "Breakout":
        return EstrategiaBreakout(umbral=config.BREAKOUT_UMBRAL)
    elif estrategia == "SmaCrossover":
        return EstrategiaSmaCrossover(periodo_corto=config.SMA_PERIODO_CORTO, periodo_largo=config.SMA_PERIODO_LARGO)
    elif estrategia == "Rsi":
        return EstrategiaRsi(periodo=config.RSI_PERIODO)
    elif estrategia == "Bollinger":
        return EstrategiaBollinger(periodo=config.BOLLINGER_PERIODO, desviaciones=config.BOLLINGER_DESVIACIONES)
    elif estrategia == "MACD":
        return EstrategiaMACD(periodo_corto=config.MACD_PERIODO_CORTO, periodo_largo=config.MACD_PERIODO_LARGO, periodo_signal=config.MACD_PERIODO_SIGNAL)
    else:
        raise ValueError(f"Estrategia no reconocida: {estrategia}")
    