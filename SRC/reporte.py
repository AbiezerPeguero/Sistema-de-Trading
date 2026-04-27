"""Recibir el historial y el balance final, y mostrar los resultados. No calcula nada, solo presenta."""
from src import decoradores
from src.metrics import Metrics

class Reporte:
    def __init__(self, historial, balance_inicial, balance_final):
        # Recibe los datos ya procesados por el Backtester.
        # Esta clase no hace operaciones, solo presenta lo que recibe.
        self.historial = historial
        self.balance_inicial = balance_inicial
        self.balance_final = balance_final
        self.metrics = Metrics(self.historial)
        
    @decoradores.log_operacion # Imprime en consola cuando el reporte comienza y termina.
    def mostrar_resultados(self):
        # Muestra cada operación cerrada del historial. 
        print("Historial de operaciones")
        for operacion in self.historial:
            print(operacion)
        print(f"Balance inicial: {self.balance_inicial}")
        print(f"Balance final: {self.balance_final:.2f}")
        
        # La ganancia o pérdida total es simplemente la diferencia entre ambos balances.
        print(f"Ganancia/Perdida: {self.balance_final - self.balance_inicial:.2f}")
        
        # len() devuelve el número de elementos de la lista, cada elemento es una operación cerrada.
        print(f"Numero de operaciones realizadas: {len(self.historial)}")
        
        # Una operación es ganadora si su resultado es positivo.
        print(f"Numero de operaciones ganadas: {sum(1 for op in self.historial if op['resultado'] > 0)}")
        
        # Protección contra división entre cero si no hubo operaciones.
        # Win rate = operaciones ganadoras / total de operaciones * 100.
        if len(self.historial) > 0:
            print(f"Win rate: {sum(1 for op in self.historial if op['resultado'] > 0) / len(self.historial) * 100:.2f}%")
        else:
            print("Win rate: sin operaciones realizadas")
            
        # Seccion de metricas avanzadas mostrando cada clave del diccionario
        print("\n--- Metricas Avanzadas ---")
        metricas = self.metrics.resumen(self.balance_inicial, self.balance_final)
        for clave, valor in metricas.items():
            print(f"{clave}: {valor}")