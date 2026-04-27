class Metrics:
    def __init__(self, historial):
        self.historial = historial

# mejor_trade() → el resultado más alto del historial. Usa max() sobre los resultados. Si el historial está vacío devuelve None
    def mejor_trade(self):
        if not self.historial:
            return None
        return round(max(self.historial, key=lambda op: op["resultado"])["resultado"], 2)
    
# peor_trade() → el resultado más bajo. Usa min(). Si está vacío devuelve None
    def peor_trade(self):
        if not self.historial:
            return None
        return round(min(self.historial, key=lambda op: op["resultado"])["resultado"], 2)

# ganancia_promedio() → filtra solo las operaciones donde resultado > 0, saca el promedio. Si no hay ninguna devuelve 0
    def ganancia_promedio(self):
        ganancias = [x["resultado"] for x in self.historial if x["resultado"] > 0]
        if not ganancias:
            return 0
        return round(sum(ganancias) / len(ganancias), 2)

# Perdida promedio
    def perdida_promedio(self):
        perdidas = [x["resultado"] for x in self.historial if x["resultado"] < 0]
        if not perdidas:
            return 0
        return round(abs(sum(perdidas) / len(perdidas)), 2)
    
# Que porcentaje gano o perdio respecto al capital inicial
    def retorno_porcentual(self, balance_inicial, balance_final):
        if balance_inicial == 0:
            return 0
        return round((balance_final - balance_inicial) / balance_inicial * 100, 2)
    
# Ratio entre ganancias totales y perdidas totales
    def profit_factor(self):
        ganancias_totales = sum(x["resultado"] for x in self.historial if x ["resultado"] > 0)
        if ganancias_totales == 0:
            return None

        perdidas_totales = abs(sum(x["resultado"] for x in self.historial if x["resultado"] < 0))
        if not perdidas_totales:
            return None
        return round(ganancias_totales / perdidas_totales, 2)

# Mide la mayor caída consecutiva del balance desde un punto alto.
    def max_drawdown(self):
        if not self.historial:
            return None
        
        pico = 0
        max_dd = 0
        acumulado = 0
        
        for op in self.historial:
            acumulado += op["resultado"]
            if acumulado > pico:
                pico = acumulado
            elif acumulado < pico:
                dd = pico - acumulado
                if dd > max_dd:
                    max_dd = dd
        return round(max_dd, 2) 
    
# Cuánto se espera ganar o perder en promedio por operación donde el win_rate es el numero de operaciones ganadoras.
    def expectancy(self):
        if not self.historial:
            return 0
        total = len(self.historial)
        ganancias = sum(1 for op in self.historial if op["resultado"] > 0)
        win_rate =  round(ganancias / total, 2)
        return round((win_rate * self.ganancia_promedio() - (1 - win_rate) * self.perdida_promedio()), 2)
    
# Llama a todos los métodos anteriores y devuelve un diccionario con todos los resultados. 
    def resumen(self, balance_inicial, balance_final):
        return {
            "mejor_trade": self.mejor_trade(),
            "peor_trade": self.peor_trade(),
            "ganancia_promedio": self.ganancia_promedio(),
            "perdida_promedio": self.perdida_promedio(),
            "retorno_porcentual": self.retorno_porcentual(balance_inicial, balance_final),
            "profit_factor": self.profit_factor(),
            "max_drawdown": self.max_drawdown(),
            "expectancy": self.expectancy()

        }