"""Responsabilidad única: Mostrar la tabla de operaciones del historial de forma navegable."""

import streamlit as st
import pandas as pd

# Verificando si "resultado" esta en el historial y convertir el historial en un DataFrame para mostrarla en Streamlit como tabla usando st.dataframe()
if "resultado" not in st.session_state:
    st.warning("Primero ejecuta un backtest en la página principal.")
else:
    # Mostrar tabla
    historial = st.session_state["resultado"]["historial"]
    st.title("Metricas resumen")
    col1, col2, col3, col4, = st.columns(4)
    col1.metric("Operaciones ganadora", sum(1 for op in historial if op['resultado'] > 0))
    col2.metric("Operaciones perdedoras", sum(1 for op in historial if op['resultado'] < 0))
    col3.metric("Total de operaciones", len(historial))
    col4.metric("Max Drawdown", st.session_state['resultado']["metricas"]['max_drawdown'])
    df = pd.DataFrame(historial)
    st.subheader("Historial de operaciones")
    st.dataframe(df)


