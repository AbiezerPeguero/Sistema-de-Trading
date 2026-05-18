"""Responsabilidad única: Ser la página principal de la aplicación. Muestra el título, una descripción breve del sistema, y el menú de navegación. 
No ejecuta backtests aquí."""

import streamlit  as st

st.title("Backtesting de Estrategias")
st.markdown("Bienvenido al sistema de backtesting de estrategia de trading")
st.info("Seleccione una estrategia del menu para inciar el backtesting")