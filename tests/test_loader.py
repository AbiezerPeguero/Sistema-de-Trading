"""Responsabilidad única: Verificar que su módulo correspondiente funciona correctamente con datos controlados. 
Los tests no dependen del CSV ni de internet — crean sus propios datos dentro de cada función."""

import pytest
from src.data_loader import DataLoader
import tempfile
import os

def test_ruta_vacia_lanza_error():
    with pytest.raises(ValueError):
        DataLoader("")
        
def test_carga_correcta():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("fecha,precio_cierre,volumen\n")
        f.write("2024-01-01,150.00,1000000\n")
        f.write("2024-01-02,153.50,1200000\n")
        ruta = f.name
            
    datos = DataLoader(ruta).cargar()
    assert len(datos) == 2
    os.unlink(ruta)
        
def test_precio_es_float():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("fecha,precio_cierre,volumen\n")
        f.write("2024-01-01,150.00,1000000\n")
        f.write("2024-01-02,153.50,1200000\n")
        ruta = f.name
        
    datos = DataLoader(ruta).cargar()
    assert isinstance(datos[0]["precio_cierre"], float) 
    os.unlink(ruta)