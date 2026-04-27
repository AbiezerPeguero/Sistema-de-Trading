from src.strategies import Estrategia

class EstrategiaMACD(Estrategia):
    def __init__(self, periodo_corto, periodo_largo, periodo_signal):
        self.periodo_corto = periodo_corto
        self.periodo_largo = periodo_largo
        self.periodo_signal = periodo_signal
        self.precios = []
        self.macd_historia = []
        
    def generar_senal(self, dato):
        self.precios.append(dato["precio_cierre"])
        if len(self.precios) < self.periodo_largo:
            return None
        
        #Calcula sma_corta con los últimos periodo_corto precios
        sma_corta = sum(self.precios[-self.periodo_corto:]) / self.periodo_corto
        
        # Calcula sma_larga con los últimos periodo_largo precios
        sma_larga = sum(self.precios[-self.periodo_largo:]) / self.periodo_largo
        
        macd = sma_corta - sma_larga
        self.macd_historia.append(macd)
        
        if len(self.macd_historia) < self.periodo_signal:
            return None
        
        # Calcula signal_line = promedio de los últimos periodo_signal valores de macd_historia
        signal = sum(self.macd_historia[-self.periodo_signal:]) / self.periodo_signal
        
        if macd > signal:
            return "comprar"
        elif macd < signal:
            return "vender"
        else: 
            return None