from src.strategies import Estrategia

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