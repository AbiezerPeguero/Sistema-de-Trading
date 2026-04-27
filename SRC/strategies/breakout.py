from src.strategies import Estrategia

# Estrategia basada en un precio umbral fijo.
# Si el precio supera el umbral compramos, si está por debajo vendemos.
class EstrategiaBreakout(Estrategia):
    def __init__(self, umbral):
        # El umbral se recibe al crear el objeto y permanece fijo durante toda la ejecución.
        # Ejemplo de uso: EstrategiaBreakout(umbral=160.00)
        self.umbral = umbral
        
    def generar_senal(self, dato):
        precio_hoy = dato["precio_cierre"]
        
        # Comparamos el precio de hoy contra el umbral fijo. 
        if precio_hoy > self.umbral:
            return "comprar"
        else:
            return "vender"