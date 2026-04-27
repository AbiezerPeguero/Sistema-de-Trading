from src.strategies import Estrategia
import statistics

class EstrategiaBollinger(Estrategia):
    def __init__(self, periodo, desviaciones):
        self.periodo = periodo
        self.desviaciones = desviaciones
        self.precios = []
        
    def generar_senal(self, dato):
        self.precios.append(dato["precio_cierre"])
        if len(self.precios) < self.periodo:
            return None
        
        # Tomando los últimos periodo precios con slicing
        ultimo = self.precios[-(self.periodo + 1): - 1]
        
        # Calcula sma = suma de esos precios dividido entre periodo
        sma = sum(ultimo) / len(ultimo)
        
        # Calcula la desviación estándar con statistics.stdev() sobre esos mismos precios
        desviacion = statistics.stdev(ultimo) if len(ultimo) > 1 else 0
        banda_superior = sma + (self.desviaciones * desviacion)
        banda_inferior = sma - (self.desviaciones * desviacion)
        
        # Calculando estrategia Bollinger
        if dato["precio_cierre"] > banda_superior:
            return "comprar"
        elif dato["precio_cierre"] < banda_inferior:
            return "vender"
        else:
            return None
        