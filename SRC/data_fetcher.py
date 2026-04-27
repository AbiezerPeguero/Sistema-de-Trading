"""Responsabilidad única: Conectarse a Yahoo Finance, descargar datos históricos de cualquier activo y devolverlos en el mismo formato de lista 
de diccionarios que usa DataLoader, 
para que el resto del sistema funcione sin ningún cambio."""

class YahooFinanceFetcher:
    # ticker → símbolo del activo, ejemplo "AAPL" o "BTC-USD"
    # periodo → rango de tiempo a descargar, ejemplo "1mo", "3mo", "1y"
    def __init__(self, ticker, periodo):
        self.ticker = ticker
        self.periodo = periodo
        
    def descargar(self):
        import yfinance
        
        # Descargar datos
        data = yfinance.download(self.ticker, period=self.periodo)
        
        datos = []
        for fila, row in data.iterrows():
            datos.append({
                "fecha": str(fila),
                    "precio_cierre": round(float(row["Close"].iloc[0]), 2),
                    "volumen": float(row["Volume"].iloc[0]),
            })
            
        if not datos:
            print(f"No se pudieron descargar datos para {self.ticker}")
        else:
            return datos 
        

