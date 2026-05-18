"""Responsabilidad única: Recibir los datos del resultado del runner y devolver figuras de Plotly listas para que Streamlit las renderice con st.plotly_chart()."""

import plotly.graph_objects as go

class Charts:
    def __init__(self, resultado):
        # Extrae solo lo necesario del diccionario completo para no repetir
        # la extracción en cada método
        self.historial = resultado["historial"]
        self.datos = resultado["datos"]
        self.balance_inicial = resultado["balance_inicial"]
        
    def equity_curve(self):
        # Reconstruye el balance acumulado operación por operación
        # empezando desde el balance inicial
        balance_curva = [self.balance_inicial]
        for op in self.historial:
            balance_curva.append(balance_curva[-1] + op["resultado"])
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=balance_curva, mode="lines", name="Capital"))
        fig.update_layout(title="Curva de Capital", xaxis_title="Operaciones", yaxis_title="Balance")
        return fig
    
    def drawdown(self):
        # Reutiliza la misma lógica de equity_curve para obtener el balance acumulado
        balance_curva = [self.balance_inicial]
        for op in self.historial:
            balance_curva.append(balance_curva[-1] + op["resultado"])
            
        # El drawdown es la caída desde el pico más alto hasta el valor actual
        # El pico se actualiza cada vez que el balance supera el máximo anterior
        drawdown_curva = []
        pico = 0
        for balance in balance_curva:
            if balance > pico:
                pico = balance
            drawdown_curva.append(pico - balance)
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=drawdown_curva, mode="lines", name="Drawdown", fill='tozeroy', line=dict(color='red')))  
        fig.update_layout(title="Drawdown", xaxis_title="Operaciones", yaxis_title="Drawdown")
        return fig
    
    def histograma_resultados(self):
        # Muestra cuántas operaciones tuvieron cada resultado
        # útil para ver si la estrategia tiene sesgo hacia ganancias o pérdidas
        resultados = [op["resultado"] for op in self.historial]
        
        fig = go.Figure(data=[go.Histogram(x=resultados)])
        fig.update_layout(title="Distribución de resultados", xaxis_title="Resultados", yaxis_title="Frecuencia")
        return fig
    
    def precio_con_senales(self):
        cierre = [d["precio_cierre"] for d in self.datos]
        
        # fecha_a_indice mapea cada fecha a su posición en el eje X
        # para ubicar los puntos de compra y venta exactamente donde ocurrieron
        fecha_a_indice = {d["fecha"]: i for i, d in enumerate(self.datos)}
        indices_compras = [fecha_a_indice[op["fecha"]] for op in self.historial]
        precios_compra = [op["precio_compra"] for op in self.historial]
        indices_ventas = [fecha_a_indice[op["fecha"]] for op in self.historial]
        precios_venta = [op["precio_venta"] for op in self.historial]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(cierre))), y=cierre, mode="lines", name="Precio"))
        fig.add_trace(go.Scatter(x=indices_compras, y=precios_compra, mode="markers", name="Compra", marker=dict(color="green", size=10)))
        fig.add_trace(go.Scatter(x=indices_ventas, y=precios_venta, mode="markers", name="Venta", marker=dict(color="red", size=10)))
        fig.update_layout(title="Precio con señales", xaxis_title="Tiempo", yaxis_title="Precio")
        return fig