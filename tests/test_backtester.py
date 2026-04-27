"""Responsabilidad única: Verificar que su módulo correspondiente funciona correctamente con datos controlados. 
Los tests no dependen del CSV ni de internet — crean sus propios datos dentro de cada función."""

from src.backtester import Backtester
from src.strategies import Estrategia

class EstrategiaFalsa(Estrategia):
    def __init__(self, senales):
        self.senales = senales
        self.indice = 0
        
    def generar_senal(self, dato):
        senal = self.senales[self.indice]
        self.indice += 1
        return senal
    
def test_operacion_registrada():
    datos = [
        {"fecha": "2024-01-01", "precio_cierre": 100},
        {"fecha": "2024-01-02", "precio_cierre": 110},
        
    ]
    estrategia = EstrategiaFalsa(["comprar", "vender"])
    backtester = Backtester(estrategia, 10000)
    backtester.ejecutar(datos)
    assert len(backtester.historial) == 1
        
def test_balance_actualizado():
    datos = [
        {"fecha": "2024-01-01", "precio_cierre": 100},
        {"fecha": "2024-01-02", "precio_cierre": 110},
    ]
    estrategia = EstrategiaFalsa(["comprar", "vender"])
    backtester = Backtester(estrategia, 10000)
    backtester.ejecutar(datos)
    assert backtester.balance == 10010.0  
        
def test_sin_operaciones():
    datos = [
        {"fecha": "2024-01-01", "precio_cierre": 100},
        {"fecha": "2024-01-02", "precio_cierre": 110},
    ]
    estrategia = EstrategiaFalsa([None, None])
    backtester = Backtester(estrategia, 10000)
    backtester.ejecutar(datos)
    assert backtester.historial == []