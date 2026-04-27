"""Responsabilidad única: Recibir una estrategia, datos y rangos de parámetros, probar todas las combinaciones posibles y devolver un ranking de resultados. 
No imprime nada directamente, no genera gráficos, solo calcula y guarda resultados en un CSV."""

import itertools
import csv
from src.backtester import Backtester
from src.metrics import Metrics
import config

class Optimizer:
    def __init__(self, estrategia_clase, datos, balance_inicial, parametros):
        self.estrategia_clase = estrategia_clase
        self.datos = datos
        self.balance_inicial = balance_inicial
        self.parametros = parametros
        
    def optimizar(self):
        # Usando itertools.product(*self.parametros.values()) para generar todas las combinaciones posibles de parámetros
        combinacion = itertools.product(*self.parametros.values())
        resultados = []
        
        for c in combinacion:   
            params = dict(zip(self.parametros.keys(), c))
            # Instanciando la estrategia
            estrategia = self.estrategia_clase(**params)
            
        # Creando un Backtester con la instancia y con self.balance_inicial
            backtester = Backtester( estrategia, config.BALANCE_INICIAL)
            backtester.ejecutar(self.datos)
        
            metrics = Metrics(backtester.historial)
            resultados.append({
                "params": params,
                "retorno_porcentual": metrics.retorno_porcentual(self.balance_inicial, backtester.balance),
                "win_rate": len([op for op in backtester.historial if op["resultado"] > 0]) / len(backtester.historial) if backtester.historial else 0
                })
            
        resultados = sorted(resultados, key=lambda x: x["retorno_porcentual"], reverse=True)   
        
        with open("Backtesting/output/optimization_results.csv", "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames= ["params", "retorno_porcentual", "win_rate"])
            writer.writeheader()
            writer.writerows(resultados)
        return resultados