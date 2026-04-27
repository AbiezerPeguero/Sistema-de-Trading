"""Responsabilidad única: Verificar que su módulo correspondiente funciona correctamente con datos controlados. 
Los tests no dependen del CSV ni de internet — crean sus propios datos dentro de cada función."""

from src.metrics import Metrics

def test_mejor_trade():
    historial = [
        {"resultado": 5.0},
        {"resultado": 10.0},
        {"resultado": -3.0},
    ]
    metrics = Metrics(historial)
    assert metrics.mejor_trade() == 10.0
    
def test_peor_trade():
    historial = [
        {"resultado": 5.0},
        {"resultado": 10.0},
        {"resultado": -3.0},
    ]
    metrics = Metrics(historial)
    assert metrics.peor_trade() == -3.0
    
def test_historial_vacio():
    historial = []
    metrics = Metrics(historial)
    assert metrics.mejor_trade() == None