"""Responsabilidad única: Recibir datos y una estrategia, simular las operaciones y registrar cada resultado."""
from src import decoradores

class Backtester:
    def __init__(self, estrategia, balance):
        # Solo reciben como parámetros los valores que varían al crear el objeto.
        # El resto se inicializa internamente con valores fijos (no van en el paréntesis).
        self.estrategia = estrategia
        self.balance = balance
        self.posicion = False       # False = sin operación abierta, True = operación activa
        self.precio_compra = None   # Guarda el precio al que se compró para calcular ganancia/pérdida
        self.historial = []         # Registro de todas las operaciones cerradas

    @decoradores.medir_tiempo       # Mide cuánto tarda en ejecutarse el backtest completo
    def ejecutar(self, datos):
        # Recorre cada día del CSV uno por uno y consulta a la estrategia qué hacer.
        for dato in datos:
            senal = self.estrategia.generar_senal(dato)
            precio_hoy = dato["precio_cierre"]

            # Si la estrategia dice comprar y no hay operación abierta, abrimos posición.
            if senal == "comprar" and not self.posicion:
                self.posicion = True
                self.precio_compra = precio_hoy

            # Si la estrategia dice vender y hay operación abierta, cerramos y registramos.
            elif senal == "vender" and self.posicion:
                ganancia_perdida = precio_hoy - self.precio_compra
                self.balance += ganancia_perdida
                self.posicion = False
                # El append va antes de resetear precio_compra, si no guardaría None.
                self.historial.append({
                    "fecha": dato["fecha"],
                    "precio_compra": self.precio_compra,
                    "precio_venta": precio_hoy,
                    "resultado": round(ganancia_perdida, 1)
                })
                self.precio_compra = None

            # Si la señal es None, no hacemos nada y pasamos al siguiente día.
