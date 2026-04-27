from src.strategies import Estrategia
import config

class EstrategiaRsi(Estrategia):
    def __init__(self, periodo):
        self.periodo = periodo
        self.precios = []
        
    def generar_senal(self, dato):
        self.precios.append(dato["precio_cierre"])
        if len(self.precios) <= self.periodo:
            return None
        
        # tomando los últimos periodo + 1 precios con slicing y calculando los cambios diarios con un for
        ultimo = self.precios[-(self.periodo + 1):]
        cambios = [ultimo[i] - ultimo[i-1] for i in range(1, len(ultimo))]
        
        # Calcula el RSI
        ganancias = [c for c in cambios if c > 0]
        perdidas = [c for c in cambios if c < 0]
        if not ganancias:
            return "comprar"
        elif not perdidas:
            return "vender"
        
        avg_ganancias = sum(ganancias) / len(ganancias)
        avg_perdidas = abs(sum(perdidas) / len(perdidas))
        rs = avg_ganancias / avg_perdidas if avg_perdidas != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        if rsi > config.RSI_SOBRECOMPRADO:
            return "vender"
        elif rsi < config.RSI_SOBREVENDIDO:
            return "comprar"
        else:
            return None