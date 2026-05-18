"""Responsabilidad única: Recibir los parámetros que el usuario configuró en la UI, orquestar la ejecución completa del backtest usando el núcleo existente, 
y devolver un diccionario de resultados que Streamlit puede consumir directamente."""
from src.data_fetcher import YahooFinanceFetcher
from src.strategies.media_movil import EstrategiaMediaMovil
from src.strategies.breakout import EstrategiaBreakout
from src.strategies.sma_crossover import EstrategiaSmaCrossover
from src.strategies.rsi import EstrategiaRsi
from src.strategies.bollinger import EstrategiaBollinger
from src.strategies.macd import EstrategiaMACD
from src.backtester import Backtester
from src.metrics import Metrics


class BacktestRunner:
    def __init__(self, ticker, estrategia_nombre, params_estrategia, balance_inicial, periodo):
        self.ticker = ticker
        self.estrategia_nombre = estrategia_nombre
        self.params_estrategia = params_estrategia
        self.balance_inicial = balance_inicial
        self.periodo = periodo
        # Los resultados no se calculan al crear el objeto, sino cuando se llama ejecutar()
        self.resultado = None
    
    def _obtener_datos(self):
        # Descarga los datos históricos del ticker desde Yahoo Finance
        fetcher = YahooFinanceFetcher(self.ticker, self.periodo) # Instanciando
        datos = fetcher.descargar()
        
        # Si yfinance no devuelve nada, no tiene sentido continuar
        if not datos:
            raise ValueError(f"No se encontraron datos para el ticker {self.ticker}.")
        return datos
        
    def _crear_estrategia(self):
        # El mapa vive aquí y no en strategy_factory.py porque esta capa es independiente
        # del sistema de consola — los parámetros vienen del usuario, no de config.py
        _mapa_estrategia = {
            "MediaMovil": EstrategiaMediaMovil,
            "Breakout": EstrategiaBreakout,
            "SmaCrossover": EstrategiaSmaCrossover,
            "Rsi": EstrategiaRsi,
            "Bollinger": EstrategiaBollinger,
            "MACD": EstrategiaMACD
            
        }
        
        if self.estrategia_nombre not in _mapa_estrategia:
            raise ValueError(f"Estrategia {self.estrategia_nombre} no es válida/reconocida.")
        # ** desempaqueta el diccionario como kwargs — equivale a EstrategiaRsi(periodo=14)
        return _mapa_estrategia[self.estrategia_nombre](**self.params_estrategia)
        
    def ejecutar(self):
        datos = self._obtener_datos()
        estrategia = self._crear_estrategia()
        
        backtester = Backtester(estrategia, self.balance_inicial) # Instanciando
        backtester.ejecutar(datos)
        metricas = Metrics(backtester.historial).resumen(self.balance_inicial, backtester.balance)
        # win_rate no está en Metrics.resumen() así que lo calculamos manualmente aquí
        win_rate = sum(1 for trade in backtester.historial if trade["resultado"] > 0) / len(backtester.historial) if backtester.historial else 0
        
        # Diccionario único de resultados que todas las páginas de Streamlit pueden consumir
        self.resultado ={
            "historial": backtester.historial,
            "datos": datos,
            "balance_inicial": self.balance_inicial,
            "balance_final": backtester.balance,
            "metricas": metricas,         # el dict que devuelve resumen()
            "win_rate": win_rate,
            "n_operaciones": len(backtester.historial)
        }
        
        return self.resultado