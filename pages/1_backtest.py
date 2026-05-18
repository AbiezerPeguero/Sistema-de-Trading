import streamlit  as st
from app.strategy_config import StrategyConfig
from app.runner import BacktestRunner
from app.charts import Charts

# StrategyConfig se instancia una sola vez fuera del botón para que
# el sidebar esté siempre disponible sin importar si se ejecutó o no el backtest
strategy_config = StrategyConfig()

# --- SIDEBAR: zona de configuración ---
ticker = st.sidebar.text_input("Ticker", value="AAPL", help="Ejemplos: AAPL, MSFT, BTC-USD, ETH-USD, AMZN, TSLA")
periodo = st.sidebar.selectbox("Periodo", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"])  
balance_inicial = st.sidebar.number_input("Balance Inicial", min_value=1000, value=10000)
estrategia_nombre = st.sidebar.selectbox("Estrategia", strategy_config.nombres_estrategias())

# Cada estrategia tiene parámetros distintos — el loop los genera dinámicamente
# usando la metadata definida en StrategyConfig
params_usuario = {}
for param in strategy_config.obtener_params(estrategia_nombre):
    params_usuario[param["nombre"]] = st.sidebar.slider(
        param["label"], 
        min_value=param["min"], 
        max_value=param["max"], 
        value=param["default"]
    )

# --- EJECUCIÓN ---
# El botón devuelve True solo cuando el usuario lo presiona
ejecutar = st.sidebar.button("Ejecutar Backtest")

if ejecutar:
    resultado = None
    try:
        with st.spinner("Ejecutando backtest..."):
            runner = BacktestRunner(ticker, estrategia_nombre, params_usuario, balance_inicial, periodo)
            resultado = runner.ejecutar()
    except ValueError as e:
        st.error(str(e))
    
    # --- RESULTADOS ---
    if resultado:
        if resultado["n_operaciones"] == 0:
            st.warning("No se generaron operaciones con esta configuración.")
        else:
            # Métricas clave en columnas para vista rápida
            st.subheader("Métricas clave")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Retorno %", f"{resultado['metricas']['retorno_porcentual']}%")
            col2.metric("Win Rate", f"{round(resultado['win_rate'] * 100, 2)}%")
            col3.metric("Max Drawdown", resultado['metricas']['max_drawdown'])
            # profit_factor puede ser None cuando no hay pérdidas — se muestra N/A
            col4.metric("Profit Factor", resultado['metricas']['profit_factor'] if resultado['metricas']['profit_factor'] is not None else "N/A")

            # Gráficos interactivos de Plotly
            charts = Charts(resultado)
            st.plotly_chart(charts.equity_curve(), use_container_width=True)
            st.plotly_chart(charts.drawdown(), use_container_width=True)
            st.plotly_chart(charts.histograma_resultados(), use_container_width=True)
            st.plotly_chart(charts.precio_con_senales(), use_container_width=True)
            
            # Guardamos en session_state para que 3_historial.py pueda acceder
            # sin necesidad de volver a ejecutar el backtest
            st.session_state["resultado"] = resultado

