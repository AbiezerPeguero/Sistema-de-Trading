from abc import ABC, abstractmethod

# Clase base abstracta. Define el contrato que todas las estrategias deben cumplir.
# No se puede instanciar directamente, solo sirve como plantilla.
class Estrategia(ABC):
    @abstractmethod
    def generar_senal(self, dato):
        # Recibe un diccionario con los datos de un día.
        # Debe devolver "comprar", "vender" o None.
        # Cada estrategia hija implementa su propia lógica.
        pass
    
class EstrategiaMediaMovil(Estrategia):
    def __init__(self):
        # Guarda el precio del día anterior para poder compararlo con el día actual.
        # Empieza en None porque al inicio no hay día anterior.
        self.precio_anterior = None
        
    def generar_senal(self, dato):
        # Obtenemos el precio de cierre del día actual desde el diccionario.
        precio_hoy = dato["precio_cierre"]
        
        # Si es el primer día, no hay precio anterior para comparar.
        # Guardamos el precio de hoy y devolvemos None (no operamos).
        if self.precio_anterior is None:
            self.precio_anterior = precio_hoy
            return None
        
        # Si el precio subió respecto al día anterior, señal de compra.
        elif precio_hoy > self.precio_anterior:
            self.precio_anterior = precio_hoy
            return "comprar"
        
        # Si el precio bajó respecto al día anterior, señal de venta.
        elif precio_hoy < self.precio_anterior: 
            self.precio_anterior = precio_hoy
            return "vender"
        
        # Si el precio es igual al anterior, no hacemos nada.
        self.precio_anterior = precio_hoy
        return None

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
