import streamlit as st
import pandas as pd
from app.strategy_config import StrategyConfig
from src.optimizer import Optimizer
from src.data_fetcher import YahooFinanceFetcher
from src.strategies.media_movil import EstrategiaMediaMovil
from src.strategies.breakout import EstrategiaBreakout
from src.strategies.sma_crossover import EstrategiaSmaCrossover
from src.strategies.rsi import EstrategiaRsi
from src.strategies.bollinger import EstrategiaBollinger
from src.strategies.macd import EstrategiaMACD

strategy_config = StrategyConfig()

# --- SIDEBAR: zona de configuración ---
ticker = st.sidebar.text_input("Ticker", value="AAPL", help="Ejemplos: AAPL, MSFT, BTC-USD, ETH-USD, AMZN, TSLA")
periodo = st.sidebar.selectbox("Periodo", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"])
balance_inicial = st.sidebar.number_input("Balance Inicial", min_value=1000, value=10000)
estrategia_nombre = st.sidebar.selectbox("Estrategia", strategy_config.nombres_estrategias())

# A diferencia de 1_backtest.py donde el usuario elige un valor por parámetro,
# aquí define un rango — Optimizer prueba todas las combinaciones posibles (grid search)
parametros_optimizer = {}
for param in strategy_config.obtener_params(estrategia_nombre):
    with st.sidebar.expander(param["label"]):
        min_value = st.number_input("Minimo", value=param["min"], key=f"min_{param['nombre']}")
        max_value = st.number_input("Maximo", value=param["max"], key=f"max_{param['nombre']}")
        # El paso por defecto es 1 para enteros y 0.5 para floats
        paso_default = 1 if param["tipo"] == "int" else 0.5
        paso = st.number_input("Paso", value=paso_default, key=f"paso_{param['nombre']}")
        
        # range() solo acepta enteros — para floats construimos la lista manualmente
        if param["tipo"] == "int":
            valores = range(int(min_value), int(max_value), int(paso))
        else:
            valores = [round(min_value + paso * i, 2) for i in range(int((max_value - min_value) / paso))]

        parametros_optimizer[param["nombre"]] = valores

# --- EJECUCIÓN ---
ejecutar = st.sidebar.button("Ejecutar optimizacion")

if ejecutar:
    optimizar = None
    try:
        with st.spinner("Ejecutando optimización..."):
            fetcher = YahooFinanceFetcher(ticker, periodo)
            datos = fetcher.descargar()
            
            # Si no hay datos no tiene sentido continuar — st.stop() detiene
            # la ejecución de Streamlit en este punto sin lanzar excepción
            if not datos:
                st.error(f"No se pudieron obtener datos para {ticker}")
                st.stop()
            
            # Optimizer recibe la clase, no una instancia, porque necesita
            # crear una instancia nueva por cada combinación de parámetros
            _mapa_estrategia = {
                "MediaMovil": EstrategiaMediaMovil,
                "Breakout": EstrategiaBreakout,
                "SmaCrossover": EstrategiaSmaCrossover,
                "Rsi": EstrategiaRsi,
                "Bollinger": EstrategiaBollinger,
                "MACD": EstrategiaMACD
            }
            
            clase_estrategia = _mapa_estrategia[estrategia_nombre]
            optimizer = Optimizer(clase_estrategia, datos, balance_inicial, parametros_optimizer)
            optimizar = optimizer.optimizar()

    except ValueError as e:
        st.error(str(e))
    
    # --- RESULTADOS ---    
    if optimizar is not None:
        df_optimizar = pd.DataFrame(optimizar)
        st.subheader("Resultados de la optimización")
        if not df_optimizar.empty:
            st.dataframe(df_optimizar)
        else:
            st.warning("No se encontraron resultados para mostrar.")
