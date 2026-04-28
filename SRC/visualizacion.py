import matplotlib.pyplot as plt

""" Recibir los datos del historial y los precios, y generar gráficos. No calcula métricas, no imprime texto, solo produce imágenes."""

class Visualizacion:
    def __init__(self, historial, datos, balance_inicial):
        self.historial = historial
        self.datos = datos
        self.balance_inicial = balance_inicial
        
    def _calcular_balance_curva(self):
        # Creando una lista llamada balance_curva
        balance_curva = [self.balance_inicial]
        
        # Recorre el historial y por cada operación suma el resultado al último valor de balance_curva y agregarlo a la lista
        for re in self.historial:
            balance_curva = balance_curva + [balance_curva[-1] + re["resultado"]]
        return balance_curva
    
    def grafico_curva_capital(self):
        balance_curva = self._calcular_balance_curva()
        # Crear figura con plt
        plt.figure(figsize=(10, 5))
        plt.plot(balance_curva)
        plt.xlabel("Tiempo")
        plt.ylabel("Capital")
        plt.title("Curva de Capital")
        plt.savefig("Backtesting/output/charts/curva_capital.png")
        plt.close()
        
    #  mostrar cuántas operaciones tuvieron cada resultado. Eje X son los resultados, eje Y es la frecuencia.
    def grafico_histograma(self):
        # Extrae todos los resultados del historial en una lista.
        resultados = [re["resultado"] for re in self.historial]
        
        # Crear figura con plt
        plt.figure(figsize=(10, 5))
        plt.hist(resultados, bins=10, edgecolor='red')
        plt.xlabel("Resultado")
        plt.ylabel("Frecuencia")
        plt.title("Histograma de Resultados")
        plt.savefig("Backtesting/output/charts/histograma_resultados.png")
        plt.close()
        
    # mostrar la línea de precios del CSV y marcar con puntos de color dónde ocurrió cada compra y cada venta.
    def grafico_precio_semanales(self):
        # Extrae los precios de cierre y de fecha de self.datos en una lista usando list comprehension con dato["precio_cierre"]
        cierre = [datos["precio_cierre"] for datos in self.datos]
        [datos["fecha"] for datos in self.datos]
        
        # Extraer dos listas separadas para las compras y ventas del historial
        compras = [datos["precio_compra"] for datos in self.historial]
        ventas = [datos["precio_venta"] for datos in self.historial]
        
        fecha_a_indice = {datos["fecha"]: i for i, datos in enumerate(self.datos)}
        indices_compras = [fecha_a_indice[op["fecha"]] for op in self.historial]
        indices_ventas = [fecha_a_indice[op["fecha"]] for op in self.historial]
        
        # Crear figura con plt
        plt.figure(figsize=(12, 5))
        plt.plot(cierre, label="Precios")
        plt.scatter(indices_compras, compras, color='green', label="Compras")
        plt.scatter(indices_ventas, ventas, color='red', label="Ventas")
        plt.xlabel("Tiempo")
        plt.ylabel("Precio")
        plt.title("Precios Semanales")
        plt.legend()
        plt.savefig("Backtesting/output/charts/precios_semanales.png")
        plt.close()
        
    # mostrar la caída del balance desde el punto más alto en cada momento a lo largo de las operaciones.
    def grafico_drawdown(self):
        balance_curva = self._calcular_balance_curva()
        
        # Crea una lista drawdown vacía, luego recorre balance_curva llevando un pico que empieza en balance_curva[0]. 
        drawdown = []
        pico = balance_curva[0]
        for ba in balance_curva:
            if ba > pico:
                pico = ba
            drawdown.append(pico - ba)
            
        # Crear figura con plt
        plt.figure(figsize=(12, 5))
        plt.fill_between(range(len(drawdown)), drawdown, color='red', alpha=0.4)
        plt.plot(drawdown)
        plt.xlabel("Tiempo")
        plt.ylabel("Drawdown")
        plt.title("Drawdown del Capital")
        plt.savefig("Backtesting/output/charts/drowdown.png")
        plt.close()
        
