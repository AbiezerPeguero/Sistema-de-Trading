"""Heredar de Estrategia, recibir un dato a la vez, y devolver "comprar", "vender" o None. No ejecutan operaciones, no guardan historial, 
solo analizan precios y emiten señales."""

from src.strategies import Estrategia

class EstrategiaSmaCrossover(Estrategia):
    def __init__(self, periodo_corto, periodo_largo):
        self.periodo_corto = periodo_corto
        self.periodo_largo = periodo_largo
        self.precios = []
        
        # Agrega dato["precio_cierre"] a self.precios Si la cantidad de precios acumulados es menor que periodo_largo → devuelve None
    def generar_senal(self, dato):
        self.precios.append(dato["precio_cierre"])
        if len(self.precios) < self.periodo_largo:
            return None
        
        sma_corto = sum(self.precios[-self.periodo_corto:]) / self.periodo_corto
        sma_largo = sum(self.precios[-self.periodo_largo:]) / self.periodo_largo
        
        if sma_corto > sma_largo:
            return "comprar"
        elif sma_corto < sma_largo:
            return "vender"
        else:
            return None